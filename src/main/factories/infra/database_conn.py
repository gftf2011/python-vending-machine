from src.infra.database.postgres.connection.psycopg2_connection import Psycopg2PoolConnection


def make_conn():
    return Psycopg2PoolConnection.get_instance()
