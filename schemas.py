from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database import engine


class Model(DeclarativeBase):
    pass


class UrlTable(Model):
    """Table in database with original URLs, shorten versions and unique IDs"""
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_url: Mapped[str]
    shorten_url: Mapped[str]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
