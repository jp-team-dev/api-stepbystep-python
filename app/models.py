from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Card(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    order: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
