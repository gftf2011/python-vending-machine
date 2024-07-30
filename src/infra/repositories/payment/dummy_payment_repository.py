from src.domain.repositories.payment import IPaymentRepository


class DummyPaymentRepository(IPaymentRepository):
    async def save(self, entity):
        pass
