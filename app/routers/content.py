from typing import List

from fastapi import APIRouter, HTTPException

from ..crud import create_card, delete_card, get_card, list_cards, update_card
from ..schemas import CardCreate, CardRead

router = APIRouter()


@router.post("/", response_model=CardRead)
def create(card: CardCreate):
    return create_card(card)


@router.get("/", response_model=List[CardRead])
def read_all():
    return list_cards()


@router.get("/{card_id}", response_model=CardRead)
def read(card_id: int):
    card = get_card(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.put("/{card_id}", response_model=CardRead)
def update(card_id: int, card: CardCreate):
    updated = update_card(card_id, card)
    if not updated:
        raise HTTPException(status_code=404, detail="Card not found")
    return updated


@router.delete("/{card_id}")
def remove(card_id: int):
    ok = delete_card(card_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"ok": True}
