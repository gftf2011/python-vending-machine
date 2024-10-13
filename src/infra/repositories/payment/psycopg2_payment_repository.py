from src.domain.entities.payment import PaymentEntity, CashPaymentEntity, PaymentType

from src.domain.repositories.payment import IPaymentRepository

from src.services.contracts.database.base import IDatabaseQuery

from src.infra.database.postgres.psycopg2_transaction import QueryInput


class Psycopg2PaymentRepository(IPaymentRepository):
    def __init__(self, query_runner: IDatabaseQuery):
        self._query_runner: IDatabaseQuery = query_runner

    async def save(self, entity: PaymentEntity) -> None:
        payment_query_input: QueryInput = {
            "text": """INSERT INTO payments_schema.payments (
                id,
                order_id,
                amount,
                payment_type,
                payment_date
            ) VALUES (%s, %s, %s, %s, %s);""",
            "values": (
                entity.id.value,
                entity.order_id.value,
                entity.amount,
                entity.type.value,
                entity.payment_date.isoformat(timespec="seconds"),
            ),
        }

        await self._query_runner.query(payment_query_input)

        if entity.type == PaymentType.CASH:
            cash_payment_entity: CashPaymentEntity = entity

            cash_payment_query_input: QueryInput = {
                "text": """INSERT INTO payments_schema.cash_payments (
                    id,
                    payment_id,
                    cash_tendered,
                    change,
                    payment_date
                ) VALUES (%s, %s, %s, %s, %s);""",
                "values": (
                    cash_payment_entity.id.value,
                    entity.id.value,
                    cash_payment_entity.cash_tendered,
                    cash_payment_entity.change,
                    cash_payment_entity.payment_date.isoformat(timespec="seconds"),
                ),
            }

            await self._query_runner.query(cash_payment_query_input)
