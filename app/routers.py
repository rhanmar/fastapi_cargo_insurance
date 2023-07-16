from datetime import date

from fastapi import Body, HTTPException, status

from app.models import Cargo, Rate
from app.schemas import CargoListSchema, RateCreateSchema, RateListSchema
from fastapi import APIRouter


router = APIRouter(
    prefix="/api",
)


@router.post("/rates/")
async def import_rates(rates: dict[date, RateCreateSchema]) -> dict:
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
    count = 0
    for dtime in rates:
        cargo_db, _ = await Cargo.get_or_create(name=rates[dtime].cargo_type)
        await Rate.create(date=dtime, cargo=cargo_db, rate=rates[dtime].rate)
        count += 1
    return {"info": f"Обработано тарифов: {count}"}


@router.get("/rates/")
async def get_rates() -> list[RateListSchema]:
    """Получить все Тарифы."""
    return await Rate.all()


@router.patch("/cargos/{cargo_id}/")
async def set_cargo_value(cargo_id: int, value: float = Body(embed=True)) -> dict:
    """Изменить Объявленную стоимость у Груза."""
    cargo_db = await Cargo.filter(id=cargo_id).first()
    if not cargo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Груз не найден")
    cargo_db.value = value
    await cargo_db.save()
    return {"info": f"Объявленная стоимость Груза {cargo_db.name} изменена на {value}"}


@router.get("/cargos/{cargo_id}/")
async def get_cargo_by_id(cargo_id: int):
    """Получить Груз по ID."""
    cargo_db = await Cargo.filter(id=cargo_id).first()
    if not cargo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Груз не найден")
    return cargo_db


@router.get("/cargos/")
async def get_cargos() -> list[CargoListSchema]:
    """Получить все Грузы."""
    return await Cargo.all()


@router.post("/cargo_insurance/")
async def calc_cargo_insurance(
    chosen_date: date = Body(embed=True), cargo_type: str = Body(embed=True)
) -> dict:
    """Посчитать стоимость страхования для выбранного типа груза и даты."""
    cargo_db = await Cargo.filter(name=cargo_type).first()
    if not cargo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Груз не найден")
    rate = await Rate.filter(cargo_id=cargo_db.id, date=chosen_date).first()
    if not rate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тариф не найден")
    return {
        "date": chosen_date,
        "cargo_type": cargo_type,
        "rate": rate.rate,
        "value": cargo_db.value,
        "cargo_insurance": cargo_db.value * rate.rate,
    }
