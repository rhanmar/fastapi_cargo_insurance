from datetime import date
from fastapi import Body, Depends

from app.models import Cargo
from app.schemas import CargoSchema, RateCreateSchema, RateSchema
from fastapi import APIRouter

from app.services import CargoService, RateService
from app.services.cargo_rate_service import CargoRateService

router = APIRouter(
    prefix="/api",
)


def get_cargo_service() -> CargoService:
    """Получить сервис для Грузов."""
    return CargoService()


def get_rate_service() -> RateService:
    """Получить сервис для Тарифов."""
    return RateService()


def get_cargo_rate_service() -> CargoRateService:
    """Получить сервис для Грузов и Тарифов."""
    return CargoRateService()


@router.post("/rates/")
async def import_rates(
    rates: dict[date, RateCreateSchema], service: CargoRateService = Depends(get_cargo_rate_service)
) -> dict:
    """Импорт Тарифов.

    Пример тела запроса:
    {
        "2022-12-02": {
            "cargo_type": "Glass",
            "rate": "1.1"
        },
        "2023-12-02": {
            "cargo_type": "Other",
            "rate": "2.2"
        }
    }
    """
    return await service.import_rates(rates)


@router.get("/rates/")
async def get_rates(service: RateService = Depends(get_rate_service)) -> list[RateSchema]:
    """Получить все Тарифы."""
    return await service.get_all_rates()


@router.patch("/cargos/{cargo_id}/")
async def set_cargo_value(
    cargo_id: int,
    value: float = Body(embed=True),
    service: CargoService = Depends(get_cargo_service),
) -> dict:
    """Изменить Объявленную стоимость у Груза."""
    return await service.set_cargo_value(cargo_id, value)


@router.get("/cargos/{cargo_id}/", response_model=CargoSchema)
async def get_cargo_by_id(
    cargo_id: int, service: CargoService = Depends(get_cargo_service)
) -> Cargo:
    """Получить Груз по ID."""
    return await service.get_cargo_by_params(id=cargo_id)


@router.get("/cargos/", response_model=list[CargoSchema])
async def get_cargos(service: CargoService = Depends(get_cargo_service)) -> list[Cargo]:
    """Получить все Грузы."""
    return await service.get_all_cargos()


@router.post("/cargo_insurance/")
async def calc_cargo_insurance(
    chosen_date: date = Body(embed=True),
    cargo_type: str = Body(embed=True),
    service: CargoRateService = Depends(get_cargo_rate_service),
) -> dict:
    """Посчитать стоимость страхования для выбранного типа груза и даты."""
    return await service.calc_cargo_insurance(chosen_date=chosen_date, cargo_type=cargo_type)
