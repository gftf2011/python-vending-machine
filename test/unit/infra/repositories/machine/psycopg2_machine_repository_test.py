import pytest
import pytest_asyncio

from testcontainers.postgres import PostgresContainer

from src.domain.value_objects.uuid import UUIDValueObject
from src.domain.entities.owner import OwnerEntity
from src.domain.entities.product import ProductEntity
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

from src.infra.repositories.machine.psycopg2_machine_repository import Psycopg2MachineRepository


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
                "text": """
                    CREATE TABLE IF NOT EXISTS machines_schema.machine_products(
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
    async def test_should_return_none_if_machine_does_not_exists(self, transaction):
        await self.open_transaction(transaction)
        await self.create_db(transaction)

        repo = Psycopg2MachineRepository(transaction)
        result = await repo.find_by_id(UUIDValueObject.create_new())

        await self.commit_transaction(transaction)

        assert result is None

    @pytest.mark.asyncio
    async def test_should_return_machine_if_exists(self, transaction):
        await self.open_transaction(transaction)
        await self.create_db(transaction)

        owner_id: str = "b9651752-6c44-4578-bdb6-883d703cbff5"
        machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"

        products = [ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", 0)]
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

        await self.create_machine(transaction, machine)
        await self.create_product(transaction, products[0])
        await self.link_product_to_machine(transaction, products[0], machine_id)

        repo = Psycopg2MachineRepository(transaction)
        result = await repo.find_by_id(machine.id)

        await self.commit_transaction(transaction)

        assert result.id.value == machine_id
        assert result.coin_01.qty == 0
        assert result.coin_05.qty == 0
        assert result.coin_10.qty == 0
        assert result.coin_25.qty == 0
        assert result.coin_50.qty == 0
        assert result.coin_100.qty == 0
        assert result.state == MachineState.READY
        assert result.owner.email.value == "test@mail.com"
        assert result.owner.full_name == "Sebastião Maia"
        assert result.owner.id.value == owner_id
        assert len(result.products) == 1

    @pytest.mark.asyncio
    async def test_should_save_new_machine(self, transaction):
        await self.open_transaction(transaction)
        await self.create_db(transaction)

        owner_id: str = "b9651752-6c44-4578-bdb6-883d703cbff5"
        machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"

        products = [ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", 0)]
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

        await self.create_product(transaction, products[0])

        repo = Psycopg2MachineRepository(transaction)
        await repo.save(machine)
        result = await repo.find_by_id(machine.id)

        await self.commit_transaction(transaction)

        assert result.id.value == machine_id
        assert result.coin_01.qty == 0
        assert result.coin_05.qty == 0
        assert result.coin_10.qty == 0
        assert result.coin_25.qty == 0
        assert result.coin_50.qty == 0
        assert result.coin_100.qty == 0
        assert result.state == MachineState.READY
        assert result.owner.email.value == "test@mail.com"
        assert result.owner.full_name == "Sebastião Maia"
        assert result.owner.id.value == owner_id
        assert len(result.products) == 1

    @pytest.mark.asyncio
    async def test_should_update_existing_machine(self, transaction):
        await self.open_transaction(transaction)
        await self.create_db(transaction)

        owner_id: str = "b9651752-6c44-4578-bdb6-883d703cbff5"
        machine_id: str = "a8351752-ec32-4578-bdb6-883d703cbee7"

        products = [ProductEntity.create("b9651752-6c44-4578-bdb6-883d703cbff5", "Hersheys", 0, "00", 0)]
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

        await self.create_product(transaction, products[0])

        repo = Psycopg2MachineRepository(transaction)
        await repo.save(machine)

        machine.add_coins(1, 0, 0, 0, 0, 0)
        await repo.update(machine)
        result = await repo.find_by_id(machine.id)

        await self.commit_transaction(transaction)

        assert result.id.value == machine_id
        assert result.coin_01.qty == 1
        assert result.coin_05.qty == 0
        assert result.coin_10.qty == 0
        assert result.coin_25.qty == 0
        assert result.coin_50.qty == 0
        assert result.coin_100.qty == 0
        assert result.state == MachineState.READY
        assert result.owner.email.value == "test@mail.com"
        assert result.owner.full_name == "Sebastião Maia"
        assert result.owner.id.value == owner_id
        assert len(result.products) == 1
