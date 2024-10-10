from src.domain.repositories.order import IOrderRepository


class DummyOrderRepository(IOrderRepository):
    async def find_by_id_and_machine_id(self, id, machine_id, created_at):
        pass

    async def save(self, entity):
        pass

    async def update(self, entity):
        pass
