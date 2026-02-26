from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field as PydanticField, field_validator


class CardBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    order: Optional[int] = None
    sensory_cue: Optional[str] = None


class CardCreate(CardBase):
    lesson_id: Optional[int] = None

    @field_validator("order")
    def ensure_positive_order(cls, v):
        if v is not None and v < 1:
            raise ValueError("order must be greater than zero")
        return v

    @field_validator("lesson_id")
    def ensure_lesson_id_positive(cls, value):
        if value is not None and value < 1:
            raise ValueError("lesson_id must be positive")
        return value


class CardRead(CardBase):
    id: int
    lesson_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    order: Optional[int] = None
    lesson_id: Optional[int] = None
    sensory_cue: Optional[str] = None

    @field_validator("order")
    def ensure_positive_order(cls, v):
        if v is not None and v < 1:
            raise ValueError("order must be greater than zero")
        return v

    @field_validator("lesson_id")
    def ensure_lesson_id_positive(cls, value):
        if value is not None and value < 1:
            raise ValueError("lesson_id must be positive")
        return value


class LessonBase(BaseModel):
    title: str
    description: Optional[str] = None
    level: Optional[str] = None
    order: Optional[int] = None


class LessonCreate(LessonBase):
    module_id: Optional[int] = None

    @field_validator("order")
    def ensure_positive_order(cls, v):
        if v is not None and v < 1:
            raise ValueError("order must be greater than zero")
        return v

    @field_validator("module_id")
    def ensure_module_id_positive(cls, value):
        if value is not None and value < 1:
            raise ValueError("module_id must be positive")
        return value


class LessonRead(LessonBase):
    id: int
    module_id: Optional[int] = None
    created_at: datetime
    cards: List[CardRead] = []

    model_config = ConfigDict(from_attributes=True)


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    level: Optional[str] = None
    order: Optional[int] = None
    module_id: Optional[int] = None

    @field_validator("order")
    def ensure_positive_order(cls, v):
        if v is not None and v < 1:
            raise ValueError("order must be greater than zero")
        return v

    @field_validator("module_id")
    def ensure_module_id_positive(cls, value):
        if value is not None and value < 1:
            raise ValueError("module_id must be positive")
        return value


class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None
    sensory_focus: List[str] = PydanticField(default_factory=list)
    order: Optional[int] = None


class ModuleCreate(ModuleBase):
    @field_validator("order")
    def ensure_positive_order(cls, v):
        if v is not None and v < 1:
            raise ValueError("order must be greater than zero")
        return v


class ModuleRead(ModuleBase):
    id: int
    created_at: datetime
    lessons: List[LessonRead] = []

    model_config = ConfigDict(from_attributes=True)


class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    sensory_focus: Optional[List[str]] = None
    order: Optional[int] = None

    @field_validator("order")
    def ensure_positive_order(cls, v):
        if v is not None and v < 1:
            raise ValueError("order must be greater than zero")
        return v
