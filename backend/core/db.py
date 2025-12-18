from config import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase


#  Базовый класс моделей
class Base(DeclarativeBase):
    pass


#  Строка подключения к БД
DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}"
    f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)


#  Создаем async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)


#  Фабрика async sessionmaker
async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# Dependency для FastAPI
async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
