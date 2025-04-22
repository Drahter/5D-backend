from fastapi import FastAPI

from contextlib import asynccontextmanager

from router import router as urls_router
from schemas import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Creating database when app is up"""
    await create_tables()
    print("Database is ready")
    yield
    print("Turning off")


app = FastAPI(lifespan=lifespan)
app.include_router(urls_router)
