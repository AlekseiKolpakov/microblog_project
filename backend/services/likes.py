from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.like import Like


async def like_tweet(
        user_id: int,
        tweet_id: int,
        session: AsyncSession
) -> bool:
    """
    Ставит лайк на твит.
    Если лайк уже существует — ничего не делает.
    """

    # Проверяем, существует ли уже лайк
    stmt = select(Like).where(
        Like.user_id == user_id,
        Like.tweet_id == tweet_id
    )
    result = await session.execute(stmt)
    existing_like = result.scalar_one_or_none()

    if existing_like:
        return True

    like = Like(user_id=user_id, tweet_id=tweet_id)

    session.add(like)
    await session.commit()

    return True


async def unlike_tweet(
        user_id: int,
        tweet_id: int,
        session: AsyncSession
) -> bool:
    """
    Удаляет лайк с твита.
    Если лайка нет — просто возвращает True.
    """

    stmt = select(Like).where(
        Like.user_id == user_id,
        Like.tweet_id == tweet_id
    )
    result = await session.execute(stmt)
    like = result.scalar_one_or_none()

    if like:
        await session.delete(like)
        await session.commit()

    return True
