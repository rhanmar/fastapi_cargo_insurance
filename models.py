from tortoise.models import Model
from tortoise import fields


class Cargo(Model):
    """Груз."""

    name = fields.CharField(max_length=64, unique=True)
    value = fields.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.name} | {self.value}"


class Rate(Model):
    """Тариф."""

    cargo = fields.ForeignKeyField("models.Cargo", related_name="rates")
    rate = fields.FloatField()
    date = fields.DateField()

    def __str__(self) -> str:
        return f"{self.date} | {self.cargo} | {self.rate}"
