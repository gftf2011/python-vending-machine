from typing import Optional, Tuple
from datetime import datetime, timedelta

from src.domain.value_objects.uuid import UUIDValueObject
from src.domain.entities.product import ProductEntity
from src.domain.entities.order import OrderEntity, OrderStatus
from src.domain.entities.order_item import OrderItemEntity
from src.domain.repositories.order import IOrderRepository

from src.services.contracts.database.base import IDatabaseQuery

from src.infra.database.postgres.psycopg2_transaction import QueryInput


class Psycopg2OrderRepository(IOrderRepository):
    def __init__(self, query_runner: IDatabaseQuery):
        self._query_runner: IDatabaseQuery = query_runner

    def _get_month_range(self, timestamp: datetime) -> Tuple[str, str]:
        # First day of the month
        first_day: str = timestamp.replace(day=1).isoformat(timespec="seconds")

        # Calculate the last day of the month by going to the next month and subtracting one day
        if timestamp.month == 12:
            next_month = timestamp.replace(year=timestamp.year + 1, month=1, day=1)
        else:
            next_month = timestamp.replace(month=timestamp.month + 1, day=1)
        last_day: str = (next_month - timedelta(days=1)).isoformat(timespec="seconds")

        return (first_day, last_day)

    async def find_by_id_and_machine_id(
        self, id: UUIDValueObject, machine_id: UUIDValueObject, created_at: datetime
    ) -> Optional[OrderEntity]:
        timerange_month_tuple = self._get_month_range(created_at)
        order_query_input: QueryInput = {
            "text": "SELECT * FROM orders_schema.orders WHERE id = %s AND machine_id = %s AND created_at BETWEEN %s AND %s LIMIT 1",
            "values": (
                id.value,
                machine_id.value,
                timerange_month_tuple[0],
                timerange_month_tuple[1],
            ),
        }

        await self._query_runner.query(order_query_input)
        order_rows = await self._query_runner.fetchall()

        if len(order_rows) == 0:
            return None

        order_items_query_input: QueryInput = {
            "text": """
                SELECT order_items.id AS order_item_id,
                       order_items.order_id AS order_id,
                       order_items.created_at AS order_created_at,
                       order_items.qty AS order_qty,
                       machine_products2.product_id AS product_id,
                       machine_products2.unit_price AS product_unit_price,
                       machine_products2.product_qty AS product_total_qty,
                       machine_products2.name AS product_name,
                       machine_products2.code AS product_code
                FROM (
                    SELECT *
                    FROM orders_schema.order_items
                    WHERE order_id = %s AND created_at BETWEEN %s AND %s
                ) AS order_items
                INNER JOIN (
                    SELECT machine_products1.machine_id AS machine_id,
                           machine_products1.product_id AS product_id,
                           machine_products1.product_qty AS product_qty,
                           machine_products1.code AS code,
                           products1.unit_price AS unit_price,
                           products1.name AS name
                    FROM machines_schema.machine_products machine_products1
                    INNER JOIN products_schema.products products1 ON machine_products1.product_id = products1.id
                    WHERE machine_id = %s
                ) AS machine_products2
                ON machine_products2.product_id = order_items.product_id;""",
            "values": (
                id.value,
                timerange_month_tuple[0],
                timerange_month_tuple[1],
                machine_id.value,
            ),
        }

        await self._query_runner.query(order_items_query_input)
        order_items_rows = await self._query_runner.fetchall()

        if len(order_items_rows) == 0:
            return None

        order_item_list: list[OrderItemEntity] = []

        order_total_amount: int = 0

        for order_item in order_items_rows:
            order_total_amount += int(order_item["product_unit_price"])
            order_item_list.append(
                OrderItemEntity.create(
                    id=order_item["order_item_id"],
                    qty=int(order_item["order_qty"]),
                    created_at=order_item["order_created_at"],
                    product=ProductEntity.create(
                        id=order_item["product_id"],
                        unit_price=int(order_item["product_unit_price"]),
                        code=order_item["product_code"],
                        name=order_item["product_name"],
                        qty=int(order_item["product_total_qty"]),
                    ),
                )
            )

        order_query_input: QueryInput = {
            "text": """
                SELECT *
                FROM orders_schema.orders
                WHERE machine_id = %s
                AND id = %s
                AND created_at BETWEEN %s AND %s
                """,
            "values": (
                machine_id.value,
                order_items_rows[0]["order_id"],
                timerange_month_tuple[0],
                timerange_month_tuple[1],
            ),
        }

        await self._query_runner.query(order_query_input)
        order_rows = await self._query_runner.fetchall()

        if len(order_rows) == 0:
            return None

        order: OrderEntity = OrderEntity.create(
            id=order_rows[0]["id"],
            machine_id=order_rows[0]["machine_id"],
            created_at=order_rows[0]["created_at"],
            updated_at=order_rows[0]["updated_at"],
            order_status=OrderStatus[order_rows[0]["status"]],
            order_items=order_item_list,
        )

        return order

    async def save(self, entity: OrderEntity) -> None:
        print(entity.order_items[0].product.qty)
        order_query_input: QueryInput = {
            "text": """INSERT INTO orders_schema.orders (
                id,
                machine_id,
                status,
                total_amount,
                created_at,
                updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s);""",
            "values": (
                entity.id.value,
                entity.machine_id.value,
                entity.order_status.value,
                entity.total_amount,
                entity.created_at.isoformat(timespec="seconds"),
                entity.updated_at.isoformat(timespec="seconds"),
            ),
        }

        await self._query_runner.query(order_query_input)

        for order_item in entity.order_items:
            print(order_item.qty)
            print(order_item.product.qty)
            counter = 0
            while counter < order_item.qty:
                order_item.product.reduce_qty()
                counter += 1
            order_item_query_input: QueryInput = {
                "text": """INSERT INTO orders_schema.order_items (
                    id,
                    order_id,
                    product_id,
                    price,
                    qty,
                    created_at
                ) VALUES (%s, %s, %s, %s, %s, %s);""",
                "values": (
                    order_item.id.value,
                    entity.id.value,
                    order_item.product.id.value,
                    order_item.product.unit_price,
                    order_item.qty,
                    entity.created_at.isoformat(timespec="seconds"),
                ),
            }
            machine_products_query_input: QueryInput = {
                "text": """
                    UPDATE machines_schema.machine_products
                    SET product_qty = %s
                    WHERE machine_id = %s
                    AND product_id = %s;""",
                "values": (
                    order_item.product.qty,
                    entity.machine_id.value,
                    order_item.product.id.value,
                ),
            }
            await self._query_runner.query(order_item_query_input)
            await self._query_runner.query(machine_products_query_input)

    async def update(self, entity: OrderEntity) -> None:
        timerange_month_tuple = self._get_month_range(entity.created_at)
        order_query_input: QueryInput = {
            "text": """
                UPDATE orders_schema.orders
                SET status = %s, updated_at = %s
                WHERE machine_id = %s
                AND id = %s
                AND created_at BETWEEN %s AND %s;""",
            "values": (
                entity.order_status.value,
                entity.updated_at.isoformat(timespec="seconds"),
                entity.machine_id.value,
                entity.id.value,
                timerange_month_tuple[0],
                timerange_month_tuple[1],
            ),
        }

        await self._query_runner.query(order_query_input)

        if entity.order_status == OrderStatus.CANCELED:
            for order_item in entity.order_items:
                counter = 0
                while counter < order_item.qty:
                    order_item.product.increase_qty()
                    counter += 1
                machine_products_query_input: QueryInput = {
                    "text": """
                        UPDATE machines_schema.machine_products
                        SET product_qty = %s
                        WHERE machine_id = %s
                        AND product_id = %s;""",
                    "values": (
                        order_item.product.qty,
                        entity.machine_id.value,
                        order_item.product.id.value,
                    ),
                }
                await self._query_runner.query(machine_products_query_input)
