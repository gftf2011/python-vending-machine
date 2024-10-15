import json

from typing import Any, TypedDict
from psycopg2 import pool as psycopg2_pool
from psycopg2.extras import RealDictCursor

from src.services.contracts.database.base import (
    IDatabaseTransaction,
    IDatabasePoolConnection,
)


class QueryInput(TypedDict):
    text: str
    values: Any


class Psycopg2Transaction(IDatabaseTransaction):
    def __init__(self, db_pool_conn: IDatabasePoolConnection):
        self._db_pool_conn = db_pool_conn
        self._pool: psycopg2_pool.ThreadedConnectionPool = None
        self._conn = None
        self._cursor = None

    async def create_client(self) -> None:
        self._pool: psycopg2_pool.ThreadedConnectionPool = await self._db_pool_conn.get_pool()
        self._conn = self._pool.getconn()
        self._cursor = self._conn.cursor(cursor_factory=RealDictCursor)

    async def open_transaction(self) -> None:
        self._cursor.execute("BEGIN")

    async def commit(self) -> None:
        self._cursor.execute("COMMIT")

    async def query(self, input_data: QueryInput) -> None:
        self._cursor.execute(input_data["text"], input_data["values"])

    async def fetchall(self) -> Any:
        return self._cursor.fetchall()

    async def rollback(self) -> None:
        self._cursor.execute("ROLLBACK")

    async def release(self) -> None:
        self._cursor.close()
        self._pool.putconn(self._conn)

    async def close(self) -> None:
        await self._db_pool_conn.disconnect()
