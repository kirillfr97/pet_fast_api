from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import create_tables, delete_tables
from router import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("DB cleared")
    await create_tables()
    print("DB created")
    yield
    print("Turning off DB")


# Приложение
app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
