from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database.deps import get_db
from app.models.events import Event
from app.models.user import User
from app.schemas.agenda.events import EventCreate, EventResponse, EventUpdate

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
	event_data: EventCreate,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	new_event = Event(**event_data.model_dump(), user_id=current_user.id)

	db.add(new_event)
	db.commit()
	db.refresh(new_event)

	return new_event


@router.get("", response_model=list[EventResponse])
def list_events(
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	return (
		db.query(Event)
		.filter(Event.user_id == current_user.id)
		.order_by(Event.id.desc())
		.all()
	)


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
	event_id: int,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	event = (
		db.query(Event)
		.filter(Event.id == event_id, Event.user_id == current_user.id)
		.first()
	)

	if event is None:
		raise HTTPException(status_code=404, detail="Evento nao encontrado")

	return event


@router.put("/{event_id}", response_model=EventResponse)
def update_event(
	event_id: int,
	event_data: EventUpdate,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	event = (
		db.query(Event)
		.filter(Event.id == event_id, Event.user_id == current_user.id)
		.first()
	)

	if event is None:
		raise HTTPException(status_code=404, detail="Evento nao encontrado")

	for field, value in event_data.model_dump(exclude_unset=True).items():
		setattr(event, field, value)

	db.commit()
	db.refresh(event)

	return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
	event_id: int,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	event = (
		db.query(Event)
		.filter(Event.id == event_id, Event.user_id == current_user.id)
		.first()
	)

	if event is None:
		raise HTTPException(status_code=404, detail="Evento nao encontrado")

	db.delete(event)
	db.commit()
