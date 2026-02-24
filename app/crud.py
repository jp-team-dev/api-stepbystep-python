from sqlmodel import Session, select

from .database import engine
from .models import Card
from .schemas import CardCreate


def create_card(card_in: CardCreate) -> Card:
    with Session(engine) as session:
        card = Card.from_orm(card_in)
        session.add(card)
        session.commit()
        session.refresh(card)
        return card


def get_card(card_id: int):
    with Session(engine) as session:
        return session.get(Card, card_id)


def list_cards():
    with Session(engine) as session:
        return session.exec(select(Card).order_by(Card.order)).all()


def update_card(card_id: int, card_in: CardCreate):
    with Session(engine) as session:
        card = session.get(Card, card_id)
        if not card:
            return None
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
