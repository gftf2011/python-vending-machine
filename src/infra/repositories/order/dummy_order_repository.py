from src.domain.repositories.order import IOrderRepository

class DummyOrderRepository(IOrderRepository):
    async def find_by_id(self, id):
        pass

    async def save(self, entity):
        pass

    async def update(self, entity):
        pass
