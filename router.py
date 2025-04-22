from fastapi import APIRouter

from fastapi import HTTPException
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from repository import UrlRepository

router = APIRouter()


class UrlRequest(BaseModel):
    url: str


@router.post("/", status_code=201)
async def shorten_url(url_request: UrlRequest):
    """Gets full URL, creates short version, made object in database"""
    original_url = url_request.url

    short_url = original_url.split("//")[-1].replace("/", "_")[:10]

    data = {
        "full_url": original_url,
        "shorten_url": short_url
    }

    new_url_id = await UrlRepository.add_url(data)
    return {
        "url_id": new_url_id
    }


@router.get("/{url_id}")
async def get_original_url(url_id: int):
    """Gets ID of URL in database, returns original URL and redirects"""
    result = await UrlRepository.find_url(url_id)
    if result:
        return RedirectResponse(url=result.full_url, status_code=307)
    raise HTTPException(status_code=404, detail="URL not found")
