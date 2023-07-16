from fastapi import HTTPException, status

from app.models import Rate


class RateService:
    """Сервис для работы с Тарифами."""

    @staticmethod
    async def get_rate_by_params(**kwargs) -> Rate:
        """Получить Тариф по параметрам."""
        rate_db = await Rate.filter(**kwargs).first()
        if not rate_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тариф не найден")
        return rate_db

    @staticmethod
    async def get_all_rates() -> list[Rate]:
        """Получить все Тарифы."""
        return await Rate.all()

    @staticmethod
    async def create_rate(**kwargs) -> Rate:
        """Создать Тариф."""
        return await Rate.create(**kwargs)
