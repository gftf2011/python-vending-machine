from src.domain.repositories.product import IProductRepository

class DummyProductRepository(IProductRepository):
    async def find_by_code(self, code, machine_id):
        pass

    async def update(self, entity):
        pass
