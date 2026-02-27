from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from .database import engine
from .models import Card, Lesson, Module
from .schemas import (
    CardCreate,
    CardUpdate,
    LessonCreate,
    LessonUpdate,
    ModuleCreate,
    ModuleUpdate,
)


class ResourceNotFoundError(Exception):
    """Raised when a related resource (module/lesson) is missing."""


def create_module(module_in: ModuleCreate) -> Module:
    with Session(engine) as session:
        module = Module(**module_in.model_dump())
        session.add(module)
        session.commit()
        module_id = module.id
    return get_module(module_id)

def list_modules():
    with Session(engine) as session:
        statement = (
            select(Module)
            .options(
                selectinload(Module.lessons).selectinload(Lesson.cards),
            )
            .order_by(Module.order)
        )
        return session.exec(statement).all()


def get_module(module_id: int):
    with Session(engine) as session:
        statement = (
            select(Module)
            .where(Module.id == module_id)
            .options(
                selectinload(Module.lessons).selectinload(Lesson.cards),
            )
        )
        return session.exec(statement).one_or_none()


def update_module(module_id: int, module_in: ModuleUpdate):
    with Session(engine) as session:
        module = session.get(Module, module_id)
        if not module:
            return None
        for key, value in module_in.model_dump(exclude_unset=True).items():
            setattr(module, key, value)
        session.add(module)
        session.commit()
    return get_module(module_id)


def delete_module(module_id: int):
    with Session(engine) as session:
        module = session.get(Module, module_id)
        if not module:
            return False
        session.delete(module)
        session.commit()
        return True


def create_lesson(lesson_in: LessonCreate) -> Lesson:
    with Session(engine) as session:
        module_id = lesson_in.module_id
        if module_id is not None:
            module = session.get(Module, module_id)
            if not module:
                raise ResourceNotFoundError(f"module {module_id} not found")

        lesson = Lesson(**lesson_in.model_dump())
        session.add(lesson)
        session.commit()
        lesson_id = lesson.id
    return get_lesson(lesson_id)


def list_lessons(module_id: Optional[int] = None):
    with Session(engine) as session:
        statement = select(Lesson).options(selectinload(Lesson.cards)).order_by(Lesson.order)
        if module_id is not None:
            statement = statement.where(Lesson.module_id == module_id)
        return session.exec(statement).all()


def get_lesson(lesson_id: int):
    with Session(engine) as session:
        return (
            session.exec(
                select(Lesson)
                .where(Lesson.id == lesson_id)
                .options(selectinload(Lesson.cards))
            )
            .one_or_none()
        )


def update_lesson(lesson_id: int, lesson_in: LessonUpdate):
    with Session(engine) as session:
        lesson = session.get(Lesson, lesson_id)
        if not lesson:
            return None
        module_id = lesson_in.module_id
        if module_id is not None:
            module = session.get(Module, module_id)
            if not module:
                raise ResourceNotFoundError(f"module {module_id} not found")
        for key, value in lesson_in.model_dump(exclude_unset=True).items():
            setattr(lesson, key, value)
        session.add(lesson)
        session.commit()
    return get_lesson(lesson_id)


def delete_lesson(lesson_id: int):
    with Session(engine) as session:
        lesson = session.get(Lesson, lesson_id)
        if not lesson:
            return False
        session.delete(lesson)
        session.commit()
        return True


def create_card(card_in: CardCreate) -> Card:
    with Session(engine) as session:
        lesson_id = card_in.lesson_id
        if lesson_id is not None:
            lesson = session.get(Lesson, lesson_id)
            if not lesson:
                raise ResourceNotFoundError(f"lesson {lesson_id} not found")

        card = Card(**card_in.model_dump())
        session.add(card)
        session.commit()
        session.refresh(card)
        return card


def get_card(card_id: int):
    with Session(engine) as session:
        return session.get(Card, card_id)


def list_cards(lesson_id: Optional[int] = None):
    with Session(engine) as session:
        statement = select(Card).order_by(Card.order)
        if lesson_id is not None:
            statement = statement.where(Card.lesson_id == lesson_id)
        return session.exec(statement).all()


def update_card(card_id: int, card_in: CardUpdate):
    with Session(engine) as session:
        card = session.get(Card, card_id)
        if not card:
            return None
        lesson_id = card_in.lesson_id
        if lesson_id is not None:
            lesson = session.get(Lesson, lesson_id)
            if not lesson:
                raise ResourceNotFoundError(f"lesson {lesson_id} not found")
        for k, v in card_in.dict(exclude_unset=True).items():
            setattr(card, k, v)
        session.add(card)
        session.commit()
        session.refresh(card)
        return card


def delete_card(card_id: int):
    with Session(engine) as session:
        card = session.get(Card, card_id)
        if not card:
            return False
        session.delete(card)
        session.commit()
        return True
