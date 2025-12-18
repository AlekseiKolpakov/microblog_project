from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_async_session
from backend.services.media import create_media
from backend.services.users import get_user_by_api_key

router = APIRouter(prefix="/api/medias", tags=["Media"])


@router.post("")
async def upload_media(
    api_key: str = Header(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
):
    user = await get_user_by_api_key(api_key, session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid api-key")

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    media = await create_media(
        file_path=file_path,
        owner_id=user.id,
        session=session
    )

    return {"result": True, "media_id": media.id}
