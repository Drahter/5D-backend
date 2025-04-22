from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

"""Database on sqlite with async driver"""
engine = create_async_engine(
    "sqlite+aiosqlite:///urls.db"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)
