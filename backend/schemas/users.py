from pydantic import BaseModel


class UserShort(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserProfileResponse(BaseModel):
    id: int
    name: str
    followers: list[UserShort]
    following: list[UserShort]

    class Config:
        orm_mode = True
