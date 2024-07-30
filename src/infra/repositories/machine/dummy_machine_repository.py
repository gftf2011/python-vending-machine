from src.domain.repositories.machine import IMachineRepository


class DummyMachineRepository(IMachineRepository):
    async def find_by_id(self, id):
        pass

    async def update(self, entity):
        pass
