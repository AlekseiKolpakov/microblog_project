from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.media import Media


async def create_media(
        file_path: str,
        owner_id: int,
        session: AsyncSession
) -> Media:
    media = Media(file_path=file_path, owner_id=owner_id)

    session.add(media)
    await session.commit()
    await session.refresh(media)

    return media


async def get_media_by_id(
        media_id: int,
        session: AsyncSession
) -> Media | None:
    return await session.get(Media, media_id)
