from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from contextlib import asynccontextmanager

from database import create_tables, new_session, UrlTable


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Creating database when app is up"""
    await create_tables()
    print("Database is ready")
    yield
    print("Turning off")


app = FastAPI(lifespan=lifespan)


class UrlRequest(BaseModel):
    url: str


@app.post("/", status_code=201)
async def shorten_url(url_request: UrlRequest):
    """Gets full URL, creates short version, made object in database"""
    original_url = url_request.url

    short_url = original_url.split("//")[-1].replace("/", "_")[:10]

    async with new_session() as session:
        new_url = UrlTable(full_url=original_url, shorten_url=short_url)
        session.add(new_url)

        await session.flush()
        await session.commit()

    return {
        "shorten_url": new_url.shorten_url,
        "redirect": f"http://127.0.0.1:8000/{new_url.id}"
    }


@app.get("/{url_id}")
async def get_original_url(url_id: int):
    """Gets ID of URL in database, returns original URL and redirects"""
    async with new_session() as session:
        async with session.begin():
            result = await session.get(UrlTable, url_id)

            if result:
                return RedirectResponse(url=result.full_url, status_code=307)
            raise HTTPException(status_code=404, detail="URL not found")
