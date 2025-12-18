from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_async_session
from backend.services.follows import follow_user, unfollow_user
from backend.services.users import get_user_by_api_key

router = APIRouter(prefix="/api/users", tags=["Follows"])


# Endpoint: подписаться на пользователя
@router.post("{user_id}/follow")
async def follow(
    user_id: int,
    api_key: str = Header(...),
    session: AsyncSession = Depends(get_async_session),
):
    current_user = await get_user_by_api_key(api_key, session)
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid api-key")

    if current_user.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot follow yourself")

    await follow_user(
        current_user_id=current_user.id,
        target_user_id=user_id,
        session=session
    )

    return {"result": True}


# Endpoint: отписаться от пользователя
@router.delete("{user_id}/follow")
async def unfollow(
    user_id: int,
    api_key: str = Header(...),
    session: AsyncSession = Depends(get_async_session),
):
    current_user = await get_user_by_api_key(api_key, session)
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid api-key")

    if current_user.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot unfollow yourself")

    await unfollow_user(
        current_user_id=current_user.id,
        target_user_id=user_id,
        session=session
    )

    return {"return": True}
