from pydantic import BaseModel
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import Rate, Cargo

Tortoise.init_models(["app.models"], "models")

# Схема Тарифа
RateSchema = pydantic_model_creator(
    Rate, name="RateSchema", include=("id", "rate", "date", "cargo_id")
)

# Схема Груза
CargoSchema = pydantic_model_creator(Cargo, name="CargoListSchema", include=("id", "name", "value"))


class RateCreateSchema(BaseModel):
    """Схема создания Тарифа."""

    cargo_type: str
    rate: float
