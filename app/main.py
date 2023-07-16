from fastapi import FastAPI
from .routers import router
from app.config.database import init_db

app = FastAPI()
app.include_router(router)


@app.get("/")
def root() -> dict:
    return {"FastAPI": "Cargo Insurance"}


init_db(app)
