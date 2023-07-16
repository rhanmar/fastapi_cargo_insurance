from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from .routers import router

app = FastAPI()
app.include_router(router)


@app.get("/")
def root() -> dict:
    return {"FastAPI": "Cargo Insurance"}


register_tortoise(
    app,
    db_url="sqlite://sql_app.db",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
