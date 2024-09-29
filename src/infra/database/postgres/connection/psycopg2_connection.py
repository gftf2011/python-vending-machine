from typing import Self, Any

from psycopg2 import pool

from src.services.contracts.database.base import IDatabasePoolConnection


class Config:
    def __init__(
        self,
        user: str,
        password: str,
        db: str,
        host: str,
        port: int,
        min: int,
        max: int,
    ):
        self.user = user
        self.password = password
        self.db = db
        self.host = host
        self.port = port
        self.min = min
        self.max = max


class Psycopg2PoolConnection(IDatabasePoolConnection):
    _pool: pool.ThreadedConnectionPool = None
    _instance: Self = None

    def __new__(cls, *args, **kwargs):
        raise Exception("Use the 'get_instance' method to create an instance of this class.")

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        cls._instance = None

    async def connect(self, config: Config) -> Any:
        if Psycopg2PoolConnection._pool is None:
            Psycopg2PoolConnection._pool = pool.ThreadedConnectionPool(
                minconn=config.min,
                maxconn=config.max,
                user=config.user,
                password=config.password,
                host=config.host,
                port=config.port,
                database=config.db,
            )

            pool_client: Any = None

            while pool_client is None:
                try:
                    pool_client = Psycopg2PoolConnection._pool.getconn()
                except Exception:
                    pool_client = None

            Psycopg2PoolConnection._pool.putconn(pool_client)

    async def disconnect(self) -> None:
        Psycopg2PoolConnection._pool.closeall()
        Psycopg2PoolConnection._pool = None

    async def get_pool(self) -> pool.ThreadedConnectionPool:
        return Psycopg2PoolConnection._pool
