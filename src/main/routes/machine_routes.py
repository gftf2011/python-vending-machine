from typing import Literal, Annotated
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query, Body, Path
from pydantic import BaseModel, Field

from src.main.factories.controllers.machine_factory import make_machine_controller
from src.main.factories.infra.database_conn import make_conn

from src.domain.entities.payment import PaymentType

from src.services.contracts.controllers.machine import ChooseProductInputControllerDTO, PayForProductInputControllerDTO

router = APIRouter()


@router.get("/v1/machine/{machine_id}/choose_product/{product_code}", status_code=status.HTTP_200_OK)
async def get_machine_choose_product(
    machine_id: Annotated[str, Path(title="The ID from the machine")],
    product_code: Annotated[str, Path(title="The CODE from the product")],
):
    controller = make_machine_controller(make_conn())
    result = await controller.choose_product(ChooseProductInputControllerDTO(product_code, machine_id))
    if result[1] == 200:
        return result[0]
    raise HTTPException(status_code=result[1], detail=result[0])


class PayForProductRequestBody(BaseModel):
    coin_01_qty: int = Field(default=0, title="Quantity of 1 cent coins inserted in the machine")
    coin_05_qty: int = Field(default=0, title="Quantity of 5 cent coins inserted in the machine")
    coin_10_qty: int = Field(default=0, title="Quantity of 10 cent coins inserted in the machine")
    coin_25_qty: int = Field(default=0, title="Quantity of 25 cent coins inserted in the machine")
    coin_50_qty: int = Field(default=0, title="Quantity of 50 cent coins inserted in the machine")
    coin_100_qty: int = Field(default=0, title="Quantity of 1 dollar coins inserted in the machine")


class PayForProductQueryParameters(BaseModel):
    model_config = {"extra": "forbid"}

    product_qty: int = Field(0, ge=0, lt=100)
    payment_type: Literal["CASH"] = Field("CASH")


@router.post("/v1/machine/{machine_id}/pay_for_product/{product_id}", status_code=status.HTTP_201_CREATED)
async def post_machine_pay_for_product(
    machine_id: Annotated[str, Path(title="The ID from the machine")],
    product_id: Annotated[str, Path(title="The ID from the product")],
    body: Annotated[PayForProductRequestBody, Body()],
    query: Annotated[PayForProductQueryParameters, Query()],
):
    controller = make_machine_controller(make_conn())
    result = await controller.pay_for_product(
        PayForProductInputControllerDTO(
            machine_id,
            product_id,
            int(query.product_qty),
            PaymentType[query.payment_type],
            body.coin_01_qty,
            body.coin_05_qty,
            body.coin_10_qty,
            body.coin_25_qty,
            body.coin_50_qty,
            body.coin_100_qty,
            datetime.now().isoformat(timespec="seconds"),
        )
    )
    if result[1] == 201:
        return result[0]
    raise HTTPException(status_code=result[1], detail=result[0])
