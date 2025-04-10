from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import RedirectResponse
import hashlib

from contextlib import asynccontextmanager

from database import create_tables, new_session, UrlTable


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("Database is ready")
    yield
    print("Turning off")


app = FastAPI(lifespan=lifespan)


# Определение модели для получения URL
class UrlRequest(BaseModel):
    url: str


@app.post("/", status_code=201)
async def shorten_url(url_request: UrlRequest):
    original_url = url_request.url
    # Генерация уникального идентификатора
    shorten_url_id = hashlib.md5(original_url.encode()).hexdigest()[:6]

    async with new_session() as session:
        new_url = UrlTable(full_url=original_url, shorten_url=shorten_url_id)
        session.add(new_url)

        await session.flush()
        await session.commit()
        print(new_url.id)
    return {"shortened_url": f"http://127.0.0.1:8080/{shorten_url_id}"}


@app.get("/{shorten_url_id}/")
async def get_original_url(shorten_url_id: str):
    async with new_session() as session:
        result = await session.get(UrlTable, shorten_url_id)

        if result:
            return {"full_url": result.full_url}
        raise HTTPException(status_code=404, detail="URL not found")
