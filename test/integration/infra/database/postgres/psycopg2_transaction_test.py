import pytest
import pytest_asyncio

from src.services.contracts.database.base import IDatabaseTransaction

from src.infra.database.postgres.psycopg2_transaction import Psycopg2Transaction
from src.infra.database.postgres.connection.psycopg2_connection import Psycopg2PoolConnection

from src.main.bootstrap.bootstrap import load
from src.main.loaders.loaders import loader


def make_transaction() -> IDatabaseTransaction:
    query_runner = Psycopg2Transaction(Psycopg2PoolConnection.get_instance())

    return query_runner


class Test_Psycopg2_Transaction:
    @pytest_asyncio.fixture(scope="class", autouse=True)
    async def bootstrap_and_load(self):
        load()
        await loader()
        yield
        await Psycopg2PoolConnection.get_instance().disconnect()

    @pytest_asyncio.fixture(scope="function", autouse=True)
    async def delete_data(self):
        yield

        transaction = make_transaction()

        await transaction.create_client()
        await transaction.open_transaction()

        await transaction.query(
            {
                "text": """DELETE FROM payments_schema.cash_payments;""",
                "values": [],
            }
        )
        await transaction.query(
            {
                "text": """DELETE FROM payments_schema.payments;""",
                "values": [],
            }
        )
        await transaction.query(
            {
                "text": """DELETE FROM orders_schema.order_items;""",
                "values": [],
            }
        )
        await transaction.query(
            {
                "text": """DELETE FROM orders_schema.orders;""",
                "values": [],
            }
        )
        await transaction.query(
            {
                "text": """DELETE FROM machines_schema.machine_products;""",
                "values": [],
            }
        )
        await transaction.query(
            {
                "text": """DELETE FROM machines_schema.machines;""",
                "values": [],
            }
        )
        await transaction.query(
            {
                "text": """DELETE FROM machines_schema.owners;""",
                "values": [],
            }
        )

        await transaction.commit()
        await transaction.release()

    @pytest.mark.asyncio
    async def test_should_commit_transaction(self):
        transaction = make_transaction()

        await transaction.create_client()
        await transaction.open_transaction()

        await transaction.query(
            {
                "text": """
                    SELECT fn_create_machine_partition(
                        ROW(
                            'a8351752-ec32-4578-bdb6-883d703cbee7'::UUID,
                            'READY'::machine_state,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0
                        )::machine_type,
                        ROW(
                            '223e4567-e89b-12d3-a456-426614174001'::UUID,
                            'Jane Doe',
                            'jane.doe@example.com'
                        )::owner_type,
                        ARRAY[
                            ROW(
                                '223e4567-e89b-12d3-a456-426614174003'::UUID,
                                'Pepsi',
                                150,
                                10
                            )::product_type,
                            ROW(
                                '223e4567-e89b-12d3-a456-426614174004'::UUID,
                                'Butterfinger',
                                50,
                                2
                            )::product_type
                        ]::product_type[]
                    );
                """,
                "values": [],
            }
        )

        await transaction.commit()

        await transaction.query(
            {
                "text": "SELECT * FROM machines_schema.machines WHERE id = %s LIMIT 1",
                "values": ("a8351752-ec32-4578-bdb6-883d703cbee7",),
            }
        )

        rows = await transaction.fetchall()

        await transaction.release()

        assert rows[0]["id"] == "a8351752-ec32-4578-bdb6-883d703cbee7"

    @pytest.mark.asyncio
    async def test_should_rollback_transaction(self):
        transaction = make_transaction()

        await transaction.create_client()
        await transaction.open_transaction()

        await transaction.query(
            {
                "text": """
                    SELECT fn_create_machine_partition(
                        ROW(
                            'a8351752-ec32-4578-bdb6-883d703cbee7'::UUID,
                            'READY'::machine_state,
                            0,
                            0,
                            0,
                            0,
                            0,
                            0
                        )::machine_type,
                        ROW(
                            '223e4567-e89b-12d3-a456-426614174001'::UUID,
                            'Jane Doe',
                            'jane.doe@example.com'
                        )::owner_type,
                        ARRAY[
                            ROW(
                                '223e4567-e89b-12d3-a456-426614174003'::UUID,
                                'Pepsi',
                                150,
                                10
                            )::product_type,
                            ROW(
                                '223e4567-e89b-12d3-a456-426614174004'::UUID,
                                'Butterfinger',
                                50,
                                2
                            )::product_type
                        ]::product_type[]
                    );
                """,
                "values": [],
            }
        )

        await transaction.rollback()

        await transaction.query(
            {
                "text": "SELECT * FROM machines_schema.machines WHERE id = %s LIMIT 1",
                "values": ("a8351752-ec32-4578-bdb6-883d703cbee7",),
            }
        )

        rows = await transaction.fetchall()

        await transaction.release()

        assert len(rows) == 0
