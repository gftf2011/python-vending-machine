from typing import Optional

from src.infra.database.postgres.psycopg2_transaction import QueryInput

from src.domain.repositories.machine import IMachineRepository
from src.domain.value_objects.uuid import UUIDValueObject
from src.domain.entities.machine import MachineEntity, MachineState
from src.domain.entities.owner import OwnerEntity
from src.domain.entities.product import ProductEntity

from src.services.contracts.database.base import IDatabaseQuery


class Psycopg2MachineRepository(IMachineRepository):
    def __init__(self, query_runner: IDatabaseQuery):
        self._query_runner: IDatabaseQuery = query_runner

    async def find_by_id(self, id: UUIDValueObject) -> Optional[MachineEntity]:
        machine_query_input: QueryInput = {
            "text": "SELECT * FROM machines_schema.machines WHERE id = %s LIMIT 1",
            "values": (id.value,),
        }
        await self._query_runner.query(machine_query_input)
        machine_rows = await self._query_runner.fetchall()

        if len(machine_rows) == 0:
            return None

        owner_query_input: QueryInput = {
            "text": "SELECT * FROM machines_schema.owners WHERE id = %s LIMIT 1",
            "values": (machine_rows[0]["owner_id"],),
        }
        await self._query_runner.query(owner_query_input)
        owner_rows = await self._query_runner.fetchall()

        if len(owner_rows) == 0:
            return None

        machine_products_query_input: QueryInput = {
            "text": """
                SELECT products.id AS product_id,
                       products.name AS name,
                       products.unit_price AS unit_price,
                       products_stock.code AS code,
                       products_stock.product_qty AS qty,
                       products_stock.machine_id AS machine_id
                FROM machines_schema.machine_products products_stock
                INNER JOIN products_schema.products products ON products_stock.product_id = products.id
                WHERE products_stock.machine_id = %s
            """,
            "values": (machine_rows[0]["id"],),
        }
        await self._query_runner.query(machine_products_query_input)
        machine_products_rows = await self._query_runner.fetchall()

        products_list: list[ProductEntity] = []

        for product in machine_products_rows:
            products_list.append(
                ProductEntity.create(
                    id=product["product_id"],
                    name=product["name"],
                    qty=int(product["qty"]),
                    code=product["code"],
                    unit_price=int(product["unit_price"]),
                )
            )

        machine = MachineEntity.create(
            id=machine_rows[0]["id"],
            owner=OwnerEntity.create(
                id=owner_rows[0]["id"],
                full_name=owner_rows[0]["full_name"],
                email=owner_rows[0]["email"],
            ),
            state=MachineState[machine_rows[0]["state"]],
            coin_01_qty=machine_rows[0]["coin_01_qty"],
            coin_05_qty=machine_rows[0]["coin_05_qty"],
            coin_10_qty=machine_rows[0]["coin_10_qty"],
            coin_25_qty=machine_rows[0]["coin_25_qty"],
            coin_50_qty=machine_rows[0]["coin_50_qty"],
            coin_100_qty=machine_rows[0]["coin_100_qty"],
            products=products_list,
        )

        return machine

    async def save(self, entity: MachineEntity) -> None:
        owner_query_input: QueryInput = {
            "text": "INSERT INTO machines_schema.owners (id, full_name, email) VALUES (%s, %s, %s)",
            "values": (
                entity.owner.id.value,
                entity.owner.full_name,
                entity.owner.email.value,
            ),
        }
        machine_query_input: QueryInput = {
            "text": """
                INSERT INTO machines_schema.machines (
                    id, owner_id, state, coin_01_qty, coin_05_qty, coin_10_qty, coin_25_qty, coin_50_qty, coin_100_qty
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            "values": (
                entity.id.value,
                entity.owner.id.value,
                entity.state.value,
                entity.coin_01.qty,
                entity.coin_05.qty,
                entity.coin_10.qty,
                entity.coin_25.qty,
                entity.coin_50.qty,
                entity.coin_100.qty,
            ),
        }
        machine_products_query_input_list: list[QueryInput] = []
        for product in entity.products:
            machine_products_query_input_list.append(
                {
                    "text": """INSERT INTO machines_schema.machine_products (
                            machine_id,
                            product_id,
                            product_qty,
                            code
                        ) VALUES (%s, %s, %s, %s);""",
                    "values": (
                        entity.id.value,
                        product.id.value,
                        product.qty,
                        product.code,
                    ),
                }
            )
        await self._query_runner.query(owner_query_input)
        await self._query_runner.query(machine_query_input)
        for machine_products_query_input in machine_products_query_input_list:
            await self._query_runner.query(machine_products_query_input)

    async def update(self, entity: MachineEntity):
        owner_query_input: QueryInput = {
            "text": "UPDATE machines_schema.owners SET id = %s, full_name = %s, email = %s WHERE id = %s",
            "values": (
                entity.owner.id.value,
                entity.owner.full_name,
                entity.owner.email.value,
                entity.owner.id.value,
            ),
        }
        machine_query_input: QueryInput = {
            "text": """
                UPDATE machines_schema.machines 
                SET id = %s,
                    owner_id = %s,
                    state = %s,
                    coin_01_qty = %s,
                    coin_05_qty = %s,
                    coin_10_qty = %s,
                    coin_25_qty = %s,
                    coin_50_qty = %s,
                    coin_100_qty = %s
                WHERE id = %s
            """,
            "values": (
                entity.id.value,
                entity.owner.id.value,
                entity.state.value,
                entity.coin_01.qty,
                entity.coin_05.qty,
                entity.coin_10.qty,
                entity.coin_25.qty,
                entity.coin_50.qty,
                entity.coin_100.qty,
                entity.id.value,
            ),
        }
        products_stock_query_input_list: list[QueryInput] = []
        for product in entity.products:
            products_stock_query_input_list.append(
                {
                    "text": """
                        UPDATE machines_schema.machine_products
                        SET product_qty = %s
                        WHERE machine_id = %s AND product_id = %s
                    """,
                    "values": (product.qty, entity.id.value, product.id.value),
                }
            )
        await self._query_runner.query(owner_query_input)
        await self._query_runner.query(machine_query_input)
        for products_stock_query_input in products_stock_query_input_list:
            await self._query_runner.query(products_stock_query_input)
