from pydantic import BaseModel

from fastapi import FastAPI, Body
from datetime import date


app = FastAPI()


class RateCreateSchema(BaseModel):
    """Схема создания Тарифа."""

    cargo_type: str
    rate: float


class DeclaredValueCreateSchema(BaseModel):
    """Схема создания Объявленной стоимости."""

    value: float
    cargo_type: str


@app.get("/")
def root() -> dict:
    return {"FastAPI": "Cargo Insurance"}


@app.post("/rate/")
def import_rates(rates: dict[date, RateCreateSchema]) -> list[list]:
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
    result = list()
    for d in rates:
        result.append([
            d,
            rates[d].cargo_type,
            rates[d].rate,
        ])
    return result


@app.post("/declared_value/")
def create_declared_value(declared_value: DeclaredValueCreateSchema) -> str:
    """Добавление Объявленной стоимости."""
    return f"{declared_value.cargo_type}: {declared_value.value}"


@app.post("/cargo_insurance/")
def calc_cargo_insurance(
        chosen_date: date = Body(embed=True, alias="date"),
        cargo_type: str = Body(embed=True)
) -> str:
    """Посчитать стоимость страхования для выбранного типа груза и даты."""
    return str(chosen_date) + " " + cargo_type
