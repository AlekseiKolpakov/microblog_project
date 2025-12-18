from typing import List

from pydantic import BaseModel

from backend.schemas.users import UserShort


#  Входящие данные
class TweetCreate(BaseModel):
    tweet_data: str
    tweet_media_ids: list[int] | None = None


#  Исходящие данные
class TweetResponse(BaseModel):
    id: int
    content: str
    attachments: List[str]
    author: UserShort
    likes: List[UserShort]

    class Config:
        orm_mode = True
