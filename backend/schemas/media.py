from pydantic import BaseModel


class MediaResponse(BaseModel):
    id: int
    file_path: str

    class Config:
        orm_mode = True
