from fastapi import APIRouter, HTTPException, status

from src.main.factories.controllers.machine_factory import make_machine_controller
from src.main.factories.infra.database_conn import make_conn

from src.services.contracts.controllers.machine import ChooseProductInputControllerDTO

router = APIRouter()


@router.get("/v1/machine/{machine_id}/choose_product/{product_code}", status_code=status.HTTP_200_OK)
async def get_machine_choose_product(machine_id: str, product_code: str):
    controller = make_machine_controller(make_conn())
    result = await controller.choose_product(ChooseProductInputControllerDTO(product_code, machine_id))
    if result[1] == 200:
        return result[0]
    raise HTTPException(status_code=result[1], detail=result[0])
