import datetime
from typing import Optional, List, Any

import pydantic
from fastapi import File, UploadFile
from pydantic import Field


class AchievementFoldersDTO(pydantic.BaseModel):
    id: Optional[int] = None
    name: str
    created_at: Optional[datetime.datetime] = Field(None, alias="createdAt")

    class Config:
        orm_mode = True
        populate_by_name = True


class AchievementDTO(pydantic.BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    files: list[str]
    date: str
    created_at: Optional[datetime.datetime] = Field(None, alias="createdAt")

    class Config:
        orm_mode = True
        populate_by_name = True



