import pytest
import pytest_asyncio

from fastapi.testclient import TestClient

from src.services.contracts.database.base import IDatabaseTransaction

from src.infra.database.postgres.psycopg2_transaction import Psycopg2Transaction
from src.infra.database.postgres.connection.psycopg2_connection import Psycopg2PoolConnection

from src.main.bootstrap.bootstrap import load
from src.main.configs.app import application
from src.main.loaders.loaders import loader


def make_transaction() -> IDatabaseTransaction:
    query_runner = Psycopg2Transaction(Psycopg2PoolConnection.get_instance())

    return query_runner


class Test_E2E_Choose_Product:
    @pytest_asyncio.fixture(scope="class", autouse=True)
    async def bootstrap_and_load(self):
        load()
        await loader()
        yield

    @pytest_asyncio.fixture(scope="function", autouse=True)
    async def manage_data(self):
        transaction = make_transaction()

        await transaction.create_client()
        await transaction.open_transaction()

        await transaction.query(
            {
                "text": """INSERT INTO products_schema.products (id, name, unit_price) VALUES ('223e4567-e89b-12d3-a456-426614174003', 'Pepsi', 150);""",
                "values": [],
            }
        )
        await transaction.query(
            {
                "text": """INSERT INTO products_schema.products (id, name, unit_price) VALUES ('223e4567-e89b-12d3-a456-426614174004', 'Butterfinger', 50);""",
                "values": [],
            }
        )
        await transaction.query(
            {
                "text": """INSERT INTO products_schema.products (id, name, unit_price) VALUES ('223e4567-e89b-12d3-a456-426614174005', 'Hershey''s', 75);""",
                "values": [],
            }
        )
        await transaction.query(
            {
                "text": """INSERT INTO products_schema.products (id, name, unit_price) VALUES ('223e4567-e89b-12d3-a456-426614174006', 'Twix Candy Bars', 95);""",
                "values": [],
            }
        )

        await transaction.commit()
        await transaction.release()

        yield

        await transaction.create_client()
        await transaction.open_transaction()

        await transaction.query(
            {
                "text": """DELETE FROM products_schema.products;""",
                "values": [],
            }
        )
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
    async def test_should_status_code_be_404_when_choose_product_is_called(self):
        client = TestClient(application())

        response = client.get("/v1/machine/a8351752-ec32-4578-bdb6-883d703cbee7/choose_product/01")

        assert response.status_code == 404
        assert response.json() == {
            "detail": {
                "error": {
                    "message": 'machine - "a8351752-ec32-4578-bdb6-883d703cbee7" - is not registered in the system'
                }
            }
        }

    @pytest.mark.asyncio
    async def test_should_status_code_be_404_when_choose_product_is_called_and_product_does_not_exists(self):
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
        await transaction.release()

        client = TestClient(application())

        response = client.get("/v1/machine/a8351752-ec32-4578-bdb6-883d703cbee7/choose_product/03")

        assert response.status_code == 404
        assert response.json() == {"detail": {"error": {"message": "product does not exists"}}}

    @pytest.mark.asyncio
    async def test_should_status_code_be_200_when_choose_product_is_called(self):
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
        await transaction.release()

        client = TestClient(application())

        response = client.get("/v1/machine/a8351752-ec32-4578-bdb6-883d703cbee7/choose_product/01")

        assert response.status_code == 200
        assert response.json() == {
            "product_id": "223e4567-e89b-12d3-a456-426614174003",
            "product_name": "Pepsi",
            "product_price": 150,
        }
