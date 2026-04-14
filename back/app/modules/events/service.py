from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.events.model import Event
from app.modules.events.schema import EventCreate, EventUpdate


def create_user_event(db: Session, user_id: int, payload: EventCreate) -> Event:
    new_event = Event(**payload.model_dump(), user_id=user_id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


def list_user_events(db: Session, user_id: int) -> list[Event]:
    return db.query(Event).filter(Event.user_id == user_id).order_by(Event.id.desc()).all()


def get_user_event_or_404(db: Session, user_id: int, event_id: int) -> Event:
    event = db.query(Event).filter(Event.id == event_id, Event.user_id == user_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Evento nao encontrado")
    return event


def update_user_event(db: Session, user_id: int, event_id: int, payload: EventUpdate) -> Event:
    event = get_user_event_or_404(db, user_id, event_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(event, field, value)

    db.commit()
    db.refresh(event)
    return event


def delete_user_event(db: Session, user_id: int, event_id: int) -> None:
    event = get_user_event_or_404(db, user_id, event_id)
    db.delete(event)
    db.commit()
