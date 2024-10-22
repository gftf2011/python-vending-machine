from typing import Any
from abc import ABC, abstractmethod

from src.services.contracts.database.base import IDatabaseTransaction


class IQueryResponseObject(ABC):
    @abstractmethod
    def execute(self, input_data: Any):
        pass


class QueryResponseWithSuccessObject(IQueryResponseObject):
    def __init__(self, response):
        self.__response = response

    def execute(self, input_data: Any):
        return self.__response


class QueryResponseWithFailureObject(IQueryResponseObject):
    def __init__(self, exception: Exception):
        self.__response = exception

    def execute(self, input_data: Any):
        raise self.__response


class IFetchallResponseObject(ABC):
    @abstractmethod
    def execute(self):
        pass


class FetchallResponseWithSuccessObject(IFetchallResponseObject):
    def __init__(self, response):
        self.__response = response

    def execute(self):
        return self.__response


class FetchallResponseWithFailureObject(IFetchallResponseObject):
    def __init__(self, exception: Exception):
        self.__response = exception

    def execute(self):
        raise self.__response


class IOpenTransactionResponseObject(ABC):
    @abstractmethod
    def execute(self):
        pass


class OpenTransactionResponseWithSuccessObject(IOpenTransactionResponseObject):
    def __init__(self, response):
        self.__response = response

    def execute(self):
        return self.__response


class OpenTransactionResponseWithFailureObject(IOpenTransactionResponseObject):
    def __init__(self, exception: Exception):
        self.__response = exception

    def execute(self):
        raise self.__response


class IReleaseResponseObject(ABC):
    @abstractmethod
    def execute(self):
        pass


class ReleaseResponseWithSuccessObject(IReleaseResponseObject):
    def __init__(self, response):
        self.__response = response

    def execute(self):
        return self.__response


class ReleaseResponseWithFailureObject(IReleaseResponseObject):
    def __init__(self, exception: Exception):
        self.__response = exception

    def execute(self):
        raise self.__response


class ICreateClientResponseObject(ABC):
    @abstractmethod
    def execute(self):
        pass


class CreateClientResponseWithSuccessObject(ICreateClientResponseObject):
    def __init__(self, response):
        self.__response = response

    def execute(self):
        return self.__response


class CreateClientResponseWithFailureObject(ICreateClientResponseObject):
    def __init__(self, exception: Exception):
        self.__response = exception

    def execute(self):
        raise self.__response


class ICommitResponseObject(ABC):
    @abstractmethod
    def execute(self):
        pass


class CommitResponseWithSuccessObject(ICommitResponseObject):
    def __init__(self, response):
        self.__response = response

    def execute(self):
        return self.__response


class CommitResponseWithFailureObject(ICommitResponseObject):
    def __init__(self, exception: Exception):
        self.__response = exception

    def execute(self):
        raise self.__response


class IRollbackResponseObject(ABC):
    @abstractmethod
    def execute(self):
        pass


class RollbackResponseWithSuccessObject(IRollbackResponseObject):
    def __init__(self, response):
        self.__response = response

    def execute(self):
        return self.__response


class RollbackResponseWithFailureObject(IRollbackResponseObject):
    def __init__(self, exception: Exception):
        self.__response = exception

    def execute(self):
        raise self.__response


class ICloseResponseObject(ABC):
    @abstractmethod
    def execute(self):
        pass


class CloseResponseWithSuccessObject(ICloseResponseObject):
    def __init__(self, response):
        self.__response = response

    def execute(self):
        return self.__response


class CloseResponseWithFailureObject(ICloseResponseObject):
    def __init__(self, exception: Exception):
        self.__response = exception

    def execute(self):
        raise self.__response


class SpyTransaction(IDatabaseTransaction):
    def __init__(
        self,
        query_response_list: list[IQueryResponseObject],
        fetchall_response_list: list[IFetchallResponseObject],
        open_transaction_response_list: list[IOpenTransactionResponseObject],
        release_response_list: list[IReleaseResponseObject],
        create_client_response_list: list[ICreateClientResponseObject],
        commit_response_list: list[ICommitResponseObject],
        rollback_response_list: list[IRollbackResponseObject],
        close_response_list: list[ICloseResponseObject],
    ):
        self._query_response_list = query_response_list
        self._fetchall_response_list = fetchall_response_list
        self._open_transaction_response_list = open_transaction_response_list
        self._release_response_list = release_response_list
        self._create_client_response_list = create_client_response_list
        self._commit_response_list = commit_response_list
        self._rollback_response_list = rollback_response_list
        self._close_response_list = close_response_list
        self.query_counter = 0
        self.fetchall_counter = 0
        self.open_transaction_counter = 0
        self.release_counter = 0
        self.create_client_counter = 0
        self.commit_counter = 0
        self.rollback_counter = 0
        self.close_counter = 0

    async def query(self, input_data: Any) -> None:
        aux_counter = self.query_counter
        self.query_counter += 1
        response = self._query_response_list[aux_counter].execute(input_data)
        return response

    async def fetchall(self) -> Any:
        aux_counter = self.fetchall_counter
        self.fetchall_counter += 1
        response = self._fetchall_response_list[aux_counter].execute()
        return response

    async def open_transaction(self) -> None:
        aux_counter = self.open_transaction_counter
        self.open_transaction_counter += 1
        response = self._open_transaction_response_list[aux_counter].execute()
        return response

    async def release(self) -> None:
        aux_counter = self.release_counter
        self.release_counter += 1
        response = self._release_response_list[aux_counter].execute()
        return response

    async def create_client(self) -> None:
        aux_counter = self.create_client_counter
        self.create_client_counter += 1
        response = self._create_client_response_list[aux_counter].execute()
        return response

    async def commit(self) -> None:
        aux_counter = self.commit_counter
        self.commit_counter += 1
        response = self._commit_response_list[aux_counter].execute()
        return response

    async def rollback(self) -> None:
        aux_counter = self.rollback_counter
        self.rollback_counter += 1
        response = self._rollback_response_list[aux_counter].execute()
        return response

    async def close(self) -> None:
        aux_counter = self.close_counter
        self.close_counter += 1
        response = self._close_response_list[aux_counter].execute()
        return response
