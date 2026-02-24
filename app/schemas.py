from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CardCreate(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    order: Optional[int] = None


class CardRead(CardCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
