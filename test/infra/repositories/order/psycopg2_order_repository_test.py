import pytest
import pytest_asyncio

from datetime import datetime
from testcontainers.postgres import PostgresContainer

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.entities.owner import OwnerEntity
from src.domain.entities.product import ProductEntity
from src.domain.entities.order import OrderEntity, OrderStatus
from src.domain.entities.order_item import OrderItemEntity
from src.domain.entities.machine import MachineEntity, MachineState

from src.services.contracts.database.base import (
    IDatabaseTransaction,
    IDatabasePoolConnection,
)

from src.infra.database.postgres.connection.psycopg2_connection import (
    Psycopg2PoolConnection,
    Config,
)
from src.infra.database.postgres.psycopg2_transaction import (
    Psycopg2Transaction,
)

from src.infra.repositories.order.psycopg2_order_repository import Psycopg2OrderRepository


class Test_Psycopg2_Machine_Repository:
    @pytest.fixture
    def postgres_container(self) -> PostgresContainer:
        postgres = (
            PostgresContainer(
                image="postgres:16-alpine",
                dbname="postgres",
                username="root",
                password="root",
                port=5432,
            )
            .with_bind_ports(5432, 5432)
            .with_exposed_ports(5432)
            .with_env("POSTGRES_MAX_CONNECTIONS", "1")
        )
        postgres.start()

        yield postgres

        postgres.stop(force=True, delete_volume=True)

    @pytest_asyncio.fixture
    async def pool(self, postgres_container: PostgresContainer) -> IDatabasePoolConnection:
        container = postgres_container
        conn_pool = Psycopg2PoolConnection.get_instance()

        await conn_pool.connect(
            Config(
                db=container.dbname,
                user=container.username,
                password=container.password,
                port=container.get_exposed_port(5432),
                host=container.get_container_host_ip(),
                min=1,
                max=1,
            )
        )

        yield conn_pool

        await conn_pool.disconnect()

        Psycopg2PoolConnection.reset_instance()

    @pytest.fixture
    def transaction(self, pool) -> IDatabaseTransaction:
        return Psycopg2Transaction(pool)

    async def create_db(self, t: IDatabaseTransaction) -> None:
        await t.query(
            {
                "text": """CREATE TYPE machine_state AS ENUM ('READY', 'DISPENSING');""",
                "values": [],
            }
        )

        await t.query(
            {
                "text": """CREATE TYPE order_status AS ENUM ('PENDING', 'DELIVERED', 'CANCELED');""",
                "values": [],
            }
        )

        await t.query(
            {
                "text": """CREATE SCHEMA IF NOT EXISTS orders_schema;""",
                "values": [],
            }
        )

        await t.query(
            {
                "text": """CREATE SCHEMA IF NOT EXISTS machines_schema;""",
                "values": [],
            }
        )

        await t.query(
            {
                "text": """CREATE SCHEMA IF NOT EXISTS products_schema;""",
                "values": [],
            }
        )

        await t.query(
            {
                "text": """CREATE TABLE IF NOT EXISTS products_schema.products(
                    id UUID UNIQUE NOT NULL,
                    name VARCHAR(320) NOT NULL,
                    unit_price INT NOT NULL,
                    CONSTRAINT pk_products_id PRIMARY KEY (id)
                );""",
                "values": [],
            }
        )

        await t.query(
            {
                "text": """CREATE TABLE IF NOT EXISTS machines_schema.owners(
                    id UUID UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    email VARCHAR(320) UNIQUE NOT NULL,
                    CONSTRAINT pk_owner_id PRIMARY KEY (id)
                );""",
                "values": [],
            }
        )

        await t.query(
            {
                "text": """CREATE TABLE IF NOT EXISTS machines_schema.machines(
                    id UUID NOT NULL,
                    owner_id UUID NOT NULL,
                    state machine_state NOT NULL,
                    coin_01_qty SMALLINT NOT NULL,
                    coin_05_qty SMALLINT NOT NULL,
                    coin_10_qty SMALLINT NOT NULL,
                    coin_25_qty SMALLINT NOT NULL,
                    coin_50_qty SMALLINT NOT NULL,
                    coin_100_qty SMALLINT NOT NULL,
                    CONSTRAINT pk_machine_id PRIMARY KEY (id)
                );""",
                "values": [],
            }
        )

        await t.query(
            {
                "text": """CREATE TABLE IF NOT EXISTS machines_schema.machine_products(
                    machine_id UUID NOT NULL,
                    product_id UUID NOT NULL,
                    product_qty INT NOT NULL,
                    code VARCHAR(2) NOT NULL,
                    CONSTRAINT fk_product_id FOREIGN KEY(product_id) REFERENCES products_schema.products(id) ON UPDATE CASCADE ON DELETE CASCADE,
                    CONSTRAINT fk_machine_id FOREIGN KEY(machine_id) REFERENCES machines_schema.machines(id) ON UPDATE CASCADE ON DELETE CASCADE
                );""",
                "values": [],
            }
        )

        await t.query(
            {
                "text": """CREATE TABLE IF NOT EXISTS orders_schema.orders(
                    id UUID NOT NULL,
                    machine_id UUID NOT NULL,
                    status order_status NOT NULL,
                    total_amount INT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    CONSTRAINT pk_order_id PRIMARY KEY (id, created_at)
                );""",
                "values": [],
            }
        )

        await t.query(
            {
                "text": """CREATE TABLE IF NOT EXISTS orders_schema.order_items(
                    id UUID NOT NULL,
                    order_id UUID NOT NULL,
                    product_id UUID NOT NULL,
                    price INT NOT NULL,
                    qty INT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    CONSTRAINT pk_order_item_id_created_at PRIMARY KEY (id, created_at),
                    CONSTRAINT fk_product_id FOREIGN KEY(product_id) REFERENCES products_schema.products(id) ON UPDATE CASCADE ON DELETE CASCADE
                );""",
                "values": [],
            }
        )

    async def create_product(self, t: IDatabaseTransaction, product: ProductEntity) -> None:
        await t.query(
            {
                "text": "INSERT INTO products_schema.products (id, name, unit_price) VALUES (%s, %s, %s);",
                "values": (
                    product.id.value,
                    product.name,
                    product.unit_price,
                ),
            }
        )

    async def create_order(self, t: IDatabaseTransaction, order: OrderEntity) -> None:
        await t.query(
            {
                "text": """INSERT INTO orders_schema.orders (
                    id,
                    machine_id,
                    status,
                    total_amount,
                    created_at,
                    updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s);""",
                "values": (
                    order.id.value,
                    order.machine_id.value,
                    order.order_status.value,
                    order.total_amount,
                    order.created_at.isoformat(timespec="seconds"),
                    order.updated_at.isoformat(timespec="seconds"),
                ),
            }
        )

        for order_item in order.order_items:
            await t.query(
                {
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
                        order.id.value,
                        order_item.product.id.value,
                        order_item.product.unit_price,
                        order_item.qty,
                        order.created_at.isoformat(timespec="seconds"),
                    ),
                }
            )

    async def link_product_to_machine(self, t: IDatabaseTransaction, product: ProductEntity, machine_id: str) -> None:
        await t.query(
            {
                "text": """INSERT INTO machines_schema.machine_products (
                    machine_id,
                    product_id,
                    product_qty,
                    code
                ) VALUES (%s, %s, %s, %s);""",
                "values": (
                    machine_id,
                    product.id.value,
                    product.qty,
                    product.code,
                ),
            }
        )

    async def create_machine(self, t: IDatabaseTransaction, machine: MachineEntity) -> None:
        await t.query(
            {
                "text": "INSERT INTO machines_schema.owners (id, full_name, email) VALUES (%s, %s, %s)",
                "values": (
                    machine.owner.id.value,
                    machine.owner.full_name,
                    machine.owner.email.value,
                ),
            }
        )

        await t.query(
            {
                "text": """
                    INSERT INTO machines_schema.machines (
                        id,
                        owner_id,
                        state,
                        coin_01_qty,
                        coin_05_qty,
                        coin_10_qty,
                        coin_25_qty,
                        coin_50_qty,
                        coin_100_qty
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                "values": (
                    machine.id.value,
                    machine.owner.id.value,
                    machine.state.value,
                    machine.coin_01.qty,
                    machine.coin_05.qty,
                    machine.coin_10.qty,
                    machine.coin_25.qty,
                    machine.coin_50.qty,
                    machine.coin_100.qty,
                ),
            }
        )

    async def open_transaction(self, t: IDatabaseTransaction) -> None:
        await t.create_client()
        await t.open_transaction()

    async def commit_transaction(self, t: IDatabaseTransaction) -> None:
        await t.commit()
        await t.release()

    async def rollback_transaction(self, t: IDatabaseTransaction) -> None:
        await t.rollback()
        await t.release()

    @pytest.mark.asyncio
    async def test_should_return_none_if_order_does_not_exists(self, transaction):
        await self.open_transaction(transaction)
        await self.create_db(transaction)

        repo = Psycopg2OrderRepository(transaction)
        result = await repo.find_by_id_and_machine_id(
            UUIDValueObject.create_new(), UUIDValueObject.create_new(), datetime(1970, 1, 1)
        )

        await self.commit_transaction(transaction)

        assert result is None

    @pytest.mark.asyncio
    async def test_should_return_none_if_order_items_do_not_exists(self, transaction):
        await self.open_transaction(transaction)
        await self.create_db(transaction)

        owner_id: str = "b9651752-6c44-4578-bdb6-883d703cbff5"
        machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"
        order_created_at: datetime = datetime(1970, 1, 1)

        products = [
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "01", 0),
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff6", "Twix", 1, "01", 0),
        ]
        owner = OwnerEntity.create(owner_id, "Sebastião Maia", "test@mail.com")
        machine = MachineEntity.create(
            machine_id,
            owner,
            MachineState.READY,
            0,
            0,
            0,
            0,
            0,
            0,
            products,
        )
        order_items = []
        order = OrderEntity.create(
            "f3331752-6c11-4578-adb7-331d703cb446",
            machine_id,
            order_items,
            OrderStatus.PENDING,
            order_created_at,
            order_created_at,
        )

        await self.create_machine(transaction, machine)
        await self.create_product(transaction, products[0])
        await self.create_product(transaction, products[1])
        await self.link_product_to_machine(transaction, products[0], machine_id)
        await self.link_product_to_machine(transaction, products[1], machine_id)
        await self.create_order(transaction, order)

        repo = Psycopg2OrderRepository(transaction)
        result = await repo.find_by_id_and_machine_id(order.id, machine.id, order_created_at)

        await self.commit_transaction(transaction)

        assert result is None

    @pytest.mark.asyncio
    async def test_should_return_order_if_exists(self, transaction):
        await self.open_transaction(transaction)
        await self.create_db(transaction)

        owner_id: str = "b9651752-6c44-4578-bdb6-883d703cbff5"
        machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"
        order_created_at: datetime = datetime(1970, 1, 1)

        products = [
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "01", 0),
            ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff6", "Twix", 1, "01", 0),
        ]
        owner = OwnerEntity.create(owner_id, "Sebastião Maia", "test@mail.com")
        machine = MachineEntity.create(
            machine_id,
            owner,
            MachineState.READY,
            0,
            0,
            0,
            0,
            0,
            0,
            products,
        )

        order_items = [OrderItemEntity.create("f3331752-6c11-4578-adb7-331d703cb445", 1, products[0], order_created_at)]
        order = OrderEntity.create(
            "f3331752-6c11-4578-adb7-331d703cb446",
            machine_id,
            order_items,
            OrderStatus.PENDING,
            order_created_at,
            order_created_at,
        )

        await self.create_machine(transaction, machine)
        await self.create_product(transaction, products[0])
        await self.create_product(transaction, products[1])
        await self.link_product_to_machine(transaction, products[0], machine_id)
        await self.link_product_to_machine(transaction, products[1], machine_id)
        await self.create_order(transaction, order)

        repo = Psycopg2OrderRepository(transaction)
        result = await repo.find_by_id_and_machine_id(order.id, machine.id, order_created_at)

        await self.commit_transaction(transaction)

        assert result.id.value == "f3331752-6c11-4578-adb7-331d703cb446"
        assert result.machine_id.value == machine_id
        assert result.order_status == OrderStatus.PENDING
        assert result.created_at.isoformat() == order_created_at.isoformat()
        assert result.updated_at.isoformat() == order_created_at.isoformat()
        assert result.total_amount == order.total_amount

        assert len(result.order_items) == 1

        assert result.order_items[0].id.value == order.order_items[0].id.value
        assert result.order_items[0].created_at.isoformat() == order.order_items[0].created_at.isoformat()
        assert result.order_items[0].qty == order.order_items[0].qty
        assert result.order_items[0].price == order.order_items[0].price

        assert result.order_items[0].product.id.value == order.order_items[0].product.id.value
        assert result.order_items[0].product.code == order.order_items[0].product.code
        assert result.order_items[0].product.name == order.order_items[0].product.name
        assert result.order_items[0].product.qty == order.order_items[0].product.qty
        assert result.order_items[0].product.unit_price == order.order_items[0].product.unit_price

    # @pytest.mark.asyncio
    # async def test_should_save_new_order(self, transaction):
    #     await self.open_transaction(transaction)
    #     await self.create_db(transaction)

    #     owner_id: str = "b9651752-6c44-4578-bdb6-883d703cbff5"
    #     machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"
    #     order_created_at: datetime = datetime(1970, 1, 1)

    #     products = [
    #         ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 1, "01", 0),
    #         ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff6", "Twix", 1, "01", 0),
    #     ]
    #     owner = OwnerEntity.create(owner_id, "Sebastião Maia", "test@mail.com")
    #     machine = MachineEntity.create(
    #         machine_id,
    #         owner,
    #         MachineState.READY,
    #         0,
    #         0,
    #         0,
    #         0,
    #         0,
    #         0,
    #         products,
    #     )

    #     order_items = [OrderItemEntity.create("f3331752-6c11-4578-adb7-331d703cb445", products[0], order_created_at)]
    #     order = OrderEntity.create(
    #         "f3331752-6c11-4578-adb7-331d703cb446",
    #         machine_id,
    #         order_items,
    #         OrderStatus.PENDING,
    #         order_created_at,
    #         order_created_at,
    #     )

    #     await self.create_machine(transaction, machine)
    #     await self.create_product(transaction, products[0])
    #     await self.create_product(transaction, products[1])
    #     await self.link_product_to_machine(transaction, products[0], machine_id)
    #     await self.link_product_to_machine(transaction, products[1], machine_id)

    #     repo = Psycopg2OrderRepository(transaction)
    #     await repo.save(order)
    #     result = await repo.find_by_id_and_machine_id(order.id, machine.id, order_created_at)

    #     await self.commit_transaction(transaction)

    #     assert result.id.value == "f3331752-6c11-4578-adb7-331d703cb446"
    #     assert result.machine_id.value == machine_id
    #     assert result.order_status == OrderStatus.PENDING
    #     assert result.created_at.isoformat() == order_created_at.isoformat()
    #     assert result.updated_at.isoformat() == order_created_at.isoformat()
    #     assert result.total_amount == order.total_amount

    #     assert len(result.order_items) == 1

    #     assert result.order_items[0].id.value == order.order_items[0].id.value
    #     assert result.order_items[0].created_at.isoformat() == order.order_items[0].created_at.isoformat()
    #     assert result.order_items[0].qty == order.order_items[0].qty
    #     assert result.order_items[0].price == order.order_items[0].price

    #     assert result.order_items[0].product.id.value == order.order_items[0].product.id.value
    #     assert result.order_items[0].product.code == order.order_items[0].product.code
    #     assert result.order_items[0].product.name == order.order_items[0].product.name
    #     assert result.order_items[0].product.qty == 0
    #     assert result.order_items[0].product.unit_price == order.order_items[0].product.unit_price
