import pytest

from testcontainers.postgres import PostgresContainer

from src.infra.database.postgres.connection.psycopg2_connection import (
    Psycopg2PoolConnection,
    Config,
)

from src.infra.database.postgres.psycopg2_transaction import (
    Psycopg2Transaction,
)


class Test_Psycopg2_Pool_Transaction:
    @pytest.fixture(scope="function")
    def container(self):
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

    @pytest.fixture(scope="function")
    def pool(self):
        conn_pool = Psycopg2PoolConnection.get_instance()

        yield conn_pool

        Psycopg2PoolConnection.reset_instance()

    @pytest.mark.asyncio
    async def test_should_commit(self, pool, container):
        await pool.connect(
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

        sut = Psycopg2Transaction(pool)

        await sut.create_client()
        await sut.open_transaction()
        await sut.query(
            {
                "text": "CREATE TABLE test (id TEXT PRIMARY KEY, value TEXT NOT NULL)",
                "values": [],
            }
        )
        await sut.query(
            {
                "text": "INSERT INTO test (id, value) VALUES (%s, %s)",
                "values": ("1", "anything"),
            }
        )
        await sut.query(
            {
                "text": "SELECT * FROM test WHERE id = %s LIMIT 1",
                "values": ("1"),
            }
        )
        result = await sut.fetchall()

        await sut.commit()
        await sut.release()

        await pool.disconnect()

        assert result[0]["id"] == "1"
        assert result[0]["value"] == "anything"

    @pytest.mark.asyncio
    async def test_should_rollback(self, pool, container):
        await pool.connect(
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

        sut = Psycopg2Transaction(pool)

        await sut.create_client()
        await sut.open_transaction()
        await sut.query(
            {
                "text": "CREATE TABLE test (id TEXT PRIMARY KEY, value TEXT NOT NULL)",
                "values": [],
            }
        )
        await sut.commit()
        await sut.release()

        await sut.create_client()
        await sut.open_transaction()
        await sut.query(
            {
                "text": "INSERT INTO test (id, value) VALUES (%s, %s)",
                "values": ("1", "anything"),
            }
        )
        await sut.rollback()
        await sut.query(
            {
                "text": "SELECT * FROM test WHERE id = %s LIMIT 1",
                "values": ("1"),
            }
        )
        result = await sut.fetchall()
        await sut.release()

        await pool.disconnect()

        assert result == []
