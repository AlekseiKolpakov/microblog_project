from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.follow import Follow
from backend.models.like import Like
from backend.models.media import Media
from backend.models.tweet import Tweet


# Создать твит
async def create_tweet(
    author_id: int,
        text: str,
        media_ids: Optional[List[int]],
        session: AsyncSession
) -> Tweet:

    new_tweet = Tweet(author_id=author_id, text=text, media_ids=media_ids)

    session.add(new_tweet)
    await session.commit()
    await session.refresh(new_tweet)

    return new_tweet


# Получить твит по ID
async def get_tweet_by_id(
        tweet_id: int,
        session: AsyncSession
) -> Optional[Tweet]:
    stmt = select(Tweet).where(Tweet.id == tweet_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


# Проверка: твит принадлежит пользователю?
async def is_tweet_owner(
        tweet_id: int,
        user_id: int,
        session: AsyncSession
) -> bool:
    stmt = select(Tweet).where(
        Tweet.id == tweet_id,
        Tweet.author_id == user_id
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is not None


# Удалить твит
async def delete_tweet(tweet: Tweet, session: AsyncSession) -> bool:
    await session.delete(tweet)
    await session.commit()
    return True


# Получить ленту твитов
# По ТЗ: твиты пользователей,
# на которых подписан текущий пользователь,
# отсортированные по популярности (кол-во лайков)
async def get_feed_for_user(user_id: int, session: AsyncSession):
    """
    Возвращаем список твитов пользователей, на которых подписан user_id,
    отсортированных по популярности (=количеству лайков).
    """

    # Ищем тех, на кого подписан пользователь
    follows_stmt = select(Follow.followed_id).where(
        Follow.follower_id == user_id
    )
    result = await session.execute(follows_stmt)
    followed_users = result.scalars().all()

    if not followed_users:
        return []  # ни на кого не подписан

    # Получаем твиты и сортируем по количеству лайков DESC
    stmt = (
        select(Tweet, func.count(Like.id).label("likes_count"))
        .outerjoin(Like, Like.tweet_id == Tweet.id)
        .where(Tweet.author_id.in_(followed_users))
        .group_by(Tweet.id)
        .order_by(func.count(Like.id).desc())
    )

    result = await session.execute(stmt)
    rows = result.all()  # вернёт tuples: (Tweet, likes_count)

    return rows


# Получить медиа твита (если понадобится)
async def get_media_for_tweet(
    media_ids: List[int], session: AsyncSession
) -> List[Media]:
    if not media_ids:
        return []

    stmt = select(Media).where(Media.id.in_(media_ids))
    result = await session.execute(stmt)
    return result.scalars().all()
