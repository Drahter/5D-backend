from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

"""Database on sqlite with async driver"""
engine = create_async_engine(
    "sqlite+aiosqlite:///urls.db"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)


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
