from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_async_session
from backend.schemas.tweets import TweetCreate
from backend.services.tweets import create_tweet as create_tweet_services
from backend.services.users import get_user_by_api_key

router = APIRouter(prefix="/api/tweets", tags=["Tweets"])


@router.post("")
async def create_tweet(
    payload: TweetCreate,
    api_key: str = Header(...),
    session: AsyncSession = Depends(get_async_session),
):
    # получаем пользователя по api-key
    user = await get_user_by_api_key(api_key, session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid api-key")

    tweet = await create_tweet_services(
        author_id=user.id,
        text=payload.tweet_data,
        media_ids=payload.tweet_media_ids,
        session=session,
    )

    return {"result": True, "tweet_id": tweet.id}
