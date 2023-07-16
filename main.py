from datetime import date

from fastapi import Body, FastAPI, HTTPException, status
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise

from models import Cargo, Rate

app = FastAPI()


class RateCreateSchema(BaseModel):
    """Схема создания Тарифа."""

    cargo_type: str
    rate: float


@app.get("/")
def root() -> dict:
    return {"FastAPI": "Cargo Insurance"}


@app.post("/rates/")
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


@app.get("/rates/")
async def get_rates():
    """Получить все Тарифы."""
    return await Rate.all()


@app.patch("/cargos/{cargo_id}/")
async def set_cargo_value(cargo_id: int, value: float = Body(embed=True)) -> dict:
    """Изменить Объявленную стоимость у Груза."""
    cargo_db = await Cargo.filter(id=cargo_id).first()
    if not cargo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Груз не найден")
    cargo_db.value = value
    await cargo_db.save()
    return {"info": f"Объявленная стоимость Груза {cargo_db.name} изменена на {value}"}


@app.get("/cargos/")
async def get_cargos() -> list:
    """Получить все Грузы."""
    return await Cargo.all()


@app.post("/cargo_insurance/")
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


register_tortoise(
    app,
    db_url="sqlite://sql_app.db",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
