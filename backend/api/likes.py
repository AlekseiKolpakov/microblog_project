from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_async_session
from backend.services.likes import like_tweet, unlike_tweet
from backend.services.users import get_user_by_api_key

router = APIRouter(prefix="/api/tweets", tags=["Likes"])


# Endpoint: поставить лайк
@router.post("/{tweet_id}/likes")
async def like(
    tweet_id: int,
    api_key: str = Header(...),
    session: AsyncSession = Depends(get_async_session),
):
    user = await get_user_by_api_key(api_key, session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid api-key")

    await like_tweet(user.id, tweet_id, session)
    return {"result": True}


# Endpoint: удалить лайк
@router.delete("/{tweet_id}/likes")
async def unlike(
    tweet_id: int,
    api_key: str = Header(...),
    session: AsyncSession = Depends(get_async_session),
):
    user = await get_user_by_api_key(api_key, session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid api-key")

    await unlike_tweet(user.id, tweet_id, session)
    return {"result": True}
