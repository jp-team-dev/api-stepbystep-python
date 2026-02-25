from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, String, text
from sqlalchemy.dialects import postgresql
from sqlmodel import Field, Relationship, SQLModel


class Module(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    sensory_focus: List[str] = Field(
        default_factory=list,
        sa_column=Column(
            postgresql.ARRAY(String(length=255)),
            nullable=False,
            server_default=text("ARRAY[]::varchar[]"),
        ),
    )
    order: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    lessons: List["Lesson"] = Relationship(back_populates="module")


class Lesson(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    module_id: Optional[int] = Field(default=None, foreign_key="module.id")
    title: str
    description: Optional[str] = None
    level: Optional[str] = None
    order: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    module: Optional[Module] = Relationship(back_populates="lessons")
    cards: List["Card"] = Relationship(back_populates="lesson")


class Card(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lesson_id: Optional[int] = Field(default=None, foreign_key="lesson.id")
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    order: Optional[int] = None
    sensory_cue: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    lesson: Optional[Lesson] = Relationship(back_populates="cards")
