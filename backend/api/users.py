from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_async_session
from backend.schemas.users import UserProfileResponse
from backend.services.users import get_user_by_api_key, get_user_by_id

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(
    api_key: str = Header(...),
    session: AsyncSession = Depends(get_async_session),
):
    user = await get_user_by_api_key(api_key, session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid api-key")

    return {"result": True, "user": user}


@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(
    user_id: int,
    api_key: str = Header(...),
    session: AsyncSession = Depends(get_async_session),
):
    current_user = await get_user_by_api_key(api_key, session)
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid api-key")

    user = await get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {"result": True, "user": user}
