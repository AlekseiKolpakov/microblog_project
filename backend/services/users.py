from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.user import User


async def get_user_by_id(
        user_id: int,
        session: AsyncSession
) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_api_key(
        api_key: str,
        session: AsyncSession
) -> User | None:
    """Возвращает пользователя по api-key, или None если не найден."""
    query = select(User).where(User.api_key == api_key)
    result = await session.execute(query)
    return result.scalar_one_or_none()
