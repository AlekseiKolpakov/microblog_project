from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.follow import Follow


async def follow_user(
    current_user_id: int, target_user_id: int, session: AsyncSession
) -> bool:
    follow = Follow(
        Follow.follower_id == current_user_id,
        Follow.followed_id == target_user_id
    )

    session.add(follow)
    await session.commit()
    return True


async def unfollow_user(
    current_user_id: int, target_user_id: int, session: AsyncSession
) -> bool:
    stmt = select(Follow).where(
        Follow.follower_id == current_user_id,
        Follow.followed_id == target_user_id
    )
    result = await session.execute(stmt)
    follow_record = result.scalar_one_or_none()

    if follow_record:
        await session.delete(follow_record)
        await session.commit()

    return True
