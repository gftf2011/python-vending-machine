import pytest

from testcontainers.postgres import PostgresContainer

from src.infra.database.postgres.connection.psycopg2_connection import (
    Psycopg2PoolConnection,
    Config,
)


@pytest.fixture(scope="class")
def container():
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


class Test_Psycopg2_Pool_Connection:
    @pytest.fixture(autouse=True)
    def reset_instances(self):
        Psycopg2PoolConnection.reset_instance()

    @pytest.mark.asyncio
    async def test_should_connect_to_database_and_disconnect(
        self, container: PostgresContainer
    ):
        sut = Psycopg2PoolConnection.get_instance()

        await sut.connect(
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

        pool = await sut.get_pool()
        pool_client = pool.getconn()
        pool.putconn(pool_client)
        await sut.disconnect()

        assert pool.closed is True
