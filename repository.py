from sqlalchemy import select

from database import new_session
from schemas import UrlTable


class UrlRepository:
    @classmethod
    async def add_url(cls, data: dict):
        """Creates new URL entry in table"""
        async with new_session() as session:
            new_url = UrlTable(**data)
            session.add(new_url)
            await session.flush()
            await session.commit()
            return new_url.id

    @classmethod
    async def find_url(cls, url_id: int):
        """Gets URL data by ID"""
        async with new_session() as session:
            query = select(UrlTable).where(UrlTable.id == url_id)
            result = await session.execute(query)
            url_model = result.scalars().first()

            return url_model
