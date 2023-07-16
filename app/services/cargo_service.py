from fastapi import HTTPException, status

from app.models import Cargo


class CargoService:
    """Сервис для работы с Грузами."""

    @staticmethod
    async def get_cargo_by_params(**kwargs) -> Cargo:
        """Получить Груз по параметрам."""
        cargo_db = await Cargo.filter(**kwargs).first()
        if not cargo_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Груз не найден")
        return cargo_db

    @staticmethod
    async def get_or_create_cargo(name: str) -> Cargo:
        """Получить или создать Груз."""
        cargo_db, _ = await Cargo.get_or_create(name=name)
        return cargo_db

    @staticmethod
    async def get_all_cargos() -> list[Cargo]:
        """Получить все Грузы."""
        return await Cargo.all()

    async def set_cargo_value(self, cargo_id: int, value: float) -> dict:
        """Установить объявленную стоимость Груза."""
        cargo_db = await self.get_cargo_by_params(id=cargo_id)
        cargo_db.value = value
        await cargo_db.save()
        return {"info": f"Объявленная стоимость Груза {cargo_db.name} изменена на {value}"}
