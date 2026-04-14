from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database.deps import get_db
from app.modules.events.schema import EventCreate, EventResponse, EventUpdate
from app.modules.events.service import (
	create_user_event,
	delete_user_event,
	get_user_event_or_404,
	list_user_events,
	update_user_event,
)
from app.modules.users.model import User

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
	event_data: EventCreate,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	return create_user_event(db, current_user.id, event_data)


@router.get("", response_model=list[EventResponse])
def list_events(
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	return list_user_events(db, current_user.id)


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
	event_id: int,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	return get_user_event_or_404(db, current_user.id, event_id)


@router.put("/{event_id}", response_model=EventResponse)
def update_event(
	event_id: int,
	event_data: EventUpdate,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	return update_user_event(db, current_user.id, event_id, event_data)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
	event_id: int,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	delete_user_event(db, current_user.id, event_id)
