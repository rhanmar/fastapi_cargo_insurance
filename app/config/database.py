from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

SQLITE_URL: str = "sqlite://sql_app.db"
POSTGRESQL_URL: str = "postgres://postgres:postgres@db:5432/"


def init_db(app: FastAPI):
    register_tortoise(
        app,
        db_url=POSTGRESQL_URL,
        modules={"models": ["app.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
