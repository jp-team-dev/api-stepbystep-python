from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field as PydanticField


class CardBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    order: Optional[int] = None
    sensory_cue: Optional[str] = None


class CardCreate(CardBase):
    lesson_id: Optional[int] = None


class CardRead(CardBase):
    id: int
    lesson_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True


class CardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    order: Optional[int] = None
    lesson_id: Optional[int] = None
    sensory_cue: Optional[str] = None


class LessonBase(BaseModel):
    title: str
    description: Optional[str] = None
    level: Optional[str] = None
    order: Optional[int] = None


class LessonCreate(LessonBase):
    module_id: Optional[int] = None


class LessonRead(LessonBase):
    id: int
    module_id: Optional[int] = None
    created_at: datetime
    cards: List[CardRead] = []

    class Config:
        orm_mode = True


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    level: Optional[str] = None
    order: Optional[int] = None
    module_id: Optional[int] = None


class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None
    sensory_focus: List[str] = PydanticField(default_factory=list)
    order: Optional[int] = None


class ModuleCreate(ModuleBase):
    pass


class ModuleRead(ModuleBase):
    id: int
    created_at: datetime
    lessons: List[LessonRead] = []

    class Config:
        orm_mode = True


class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    sensory_focus: Optional[List[str]] = None
    order: Optional[int] = None
