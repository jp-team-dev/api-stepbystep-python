from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from ..crud import (
    ResourceNotFoundError,
    create_card as crud_create_card,
    delete_card as crud_delete_card,
    get_card as crud_get_card,
    list_cards as crud_list_cards,
    update_card as crud_update_card,
    create_lesson as crud_create_lesson,
    delete_lesson as crud_delete_lesson,
    get_lesson as crud_get_lesson,
    list_lessons as crud_list_lessons,
    update_lesson as crud_update_lesson,
    create_module as crud_create_module,
    delete_module as crud_delete_module,
    get_module as crud_get_module,
    list_modules as crud_list_modules,
    update_module as crud_update_module,
)
from ..schemas import (
    CardCreate,
    CardRead,
    CardUpdate,
    LessonCreate,
    LessonRead,
    LessonUpdate,
    ModuleCreate,
    ModuleRead,
    ModuleUpdate,
)

router = APIRouter()


@router.post("/modules", response_model=ModuleRead)
def create_module(module: ModuleCreate):
    return crud_create_module(module)


@router.get("/modules", response_model=List[ModuleRead])
def read_modules():
    return crud_list_modules()


@router.get("/modules/{module_id}", response_model=ModuleRead)
def read_module(module_id: int):
    module = crud_get_module(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


@router.put("/modules/{module_id}", response_model=ModuleRead)
def update_module(module_id: int, module: ModuleUpdate):
    updated = crud_update_module(module_id, module)
    if not updated:
        raise HTTPException(status_code=404, detail="Module not found")
    return updated


@router.delete("/modules/{module_id}")
def delete_module(module_id: int):
    ok = crud_delete_module(module_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Module not found")
    return {"ok": True}


@router.post("/lessons", response_model=LessonRead)
def create_lesson(lesson: LessonCreate):
    try:
        return crud_create_lesson(lesson)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/lessons", response_model=List[LessonRead])
def read_lessons(module_id: Optional[int] = Query(None)):
    return crud_list_lessons(module_id)


@router.get("/lessons/{lesson_id}", response_model=LessonRead)
def read_lesson(lesson_id: int):
    lesson = crud_get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.put("/lessons/{lesson_id}", response_model=LessonRead)
def update_lesson(lesson_id: int, lesson: LessonUpdate):
    try:
        updated = crud_update_lesson(lesson_id, lesson)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    if not updated:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return updated


@router.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: int):
    ok = crud_delete_lesson(lesson_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {"ok": True}


@router.post("/cards", response_model=CardRead)
def create_card(card: CardCreate):
    try:
        return crud_create_card(card)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/cards", response_model=List[CardRead])
def read_cards(lesson_id: Optional[int] = Query(None)):
    return crud_list_cards(lesson_id)


@router.get("/cards/{card_id}", response_model=CardRead)
def read_card(card_id: int):
    card = crud_get_card(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.put("/cards/{card_id}", response_model=CardRead)
def update_card(card_id: int, card: CardUpdate):
    try:
        updated = crud_update_card(card_id, card)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    if not updated:
        raise HTTPException(status_code=404, detail="Card not found")
    return updated


@router.delete("/cards/{card_id}")
def remove_card(card_id: int):
    ok = crud_delete_card(card_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"ok": True}
