from datetime import date

from app.schemas import RateCreateSchema
from app.services import CargoService, RateService


class CargoRateService(CargoService, RateService):
    """Сервис для Грузов и Тарифов."""

    async def import_rates(self, rates: dict[date, RateCreateSchema]) -> dict:
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
        count: int = 0
        for dtime in rates:
            cargo_db = await self.get_or_create_cargo(name=rates[dtime].cargo_type)
            await self.create_rate(date=dtime, cargo=cargo_db, rate=rates[dtime].rate)
            count += 1
        return {"info": f"Обработано тарифов: {count}"}

    async def calc_cargo_insurance(self, chosen_date: date, cargo_type: str) -> dict:
        """Посчитать стоимость страхования для выбранного типа груза и даты."""
        cargo_db = await self.get_cargo_by_params(name=cargo_type)
        rate_db = await self.get_rate_by_params(cargo_id=cargo_db.id, date=chosen_date)
        return {
            "date": chosen_date,
            "cargo_type": cargo_type,
            "rate": rate_db.rate,
            "value": cargo_db.value,
            "cargo_insurance": round(cargo_db.value * rate_db.rate, 2),
        }
