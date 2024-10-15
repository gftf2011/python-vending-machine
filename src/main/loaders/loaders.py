import os

from src.infra.database.postgres.connection.psycopg2_connection import Psycopg2PoolConnection, Config


async def loader():
    await Psycopg2PoolConnection.get_instance().connect(
        Config(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            db=os.getenv("POSTGRES_DB"),
            host=os.getenv("POSTGRES_HOST"),
            port=int(os.getenv("POSTGRES_PORT")),
            min=int(os.getenv("POSTGRES_MIN")),
            max=int(os.getenv("POSTGRES_MAX")),
        )
    )
