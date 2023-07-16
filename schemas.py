from pydantic import BaseModel
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from models import Rate, Cargo

Tortoise.init_models(["models"], "models")

# Схема списка Тарифов
RateListSchema = pydantic_model_creator(Rate, name="RateListSchema", include=("id", "rate", "date", "cargo_id"))

# Схема списка Грузов
CargoListSchema = pydantic_model_creator(Cargo, name="CargoListSchema", include=("id", "name", "value"))


class RateCreateSchema(BaseModel):
    """Схема создания Тарифа."""

    cargo_type: str
    rate: float
