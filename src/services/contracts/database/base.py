from typing import Any
from abc import ABC, abstractmethod


class IDatabasePoolConnection(ABC):
    @abstractmethod
    async def connect(self, config: Any) -> Any:
        """Function used to connect to database"""
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self) -> None:
        """Function used to disconnect from database"""
        raise NotImplementedError

    @abstractmethod
    async def get_pool(self) -> Any:
        """Function used to get the client pool from the database connection pool"""
        raise NotImplementedError


class IDatabaseQuery(ABC):
    @abstractmethod
    async def query(self, input_data: Any) -> Any:
        """Function used to query data from database"""
        raise NotImplementedError


class IDatabaseTransaction(IDatabaseQuery):
    @abstractmethod
    async def open_transaction(self) -> None:
        """Function used to open a transaction to database after getting a connection client"""
        raise NotImplementedError

    @abstractmethod
    async def close_trnsaction(self) -> None:
        """Function used to close the transaction to database"""
        raise NotImplementedError

    @abstractmethod
    async def create_client(self) -> None:
        """Function used to get a connection client from client pool"""
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        """Function used to commit changes into database log"""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """Function used to rollback all changes made in the transaction"""
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """Function used to close transaction and make connection available for other calls"""
        raise NotImplementedError
