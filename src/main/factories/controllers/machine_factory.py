from src.presentation.controllers.machine import MachineController
from src.presentation.controllers.decorators.machine_transaction_decorator import MachineTransactionDecorator
from src.presentation.presenters.json_presenter import JSONPresenter

from src.services.machine import MachineService
from src.services.order import OrderService
from src.services.payment import PaymentService

from src.services.contracts.database.base import IDatabasePoolConnection

from src.infra.repositories.machine.psycopg2_machine_repository import Psycopg2MachineRepository
from src.infra.repositories.order.psycopg2_order_repository import Psycopg2OrderRepository
from src.infra.repositories.payment.psycopg2_payment_repository import Psycopg2PaymentRepository

from src.infra.database.postgres.psycopg2_transaction import Psycopg2Transaction


def make_machine_controller(db_pool_conn: IDatabasePoolConnection) -> MachineController:
    query_runner = Psycopg2Transaction(db_pool_conn)

    machine_repo = Psycopg2MachineRepository(query_runner)
    order_repo = Psycopg2OrderRepository(query_runner)
    payment_repo = Psycopg2PaymentRepository(query_runner)

    machine_service = MachineService(machine_repo)
    order_service = OrderService(machine_repo, order_repo)
    payment_service = PaymentService(order_repo, payment_repo)

    json_presenter = JSONPresenter()
    controller = MachineController(json_presenter, machine_service, order_service, payment_service)
    decorator = MachineTransactionDecorator(controller, query_runner)

    return decorator
