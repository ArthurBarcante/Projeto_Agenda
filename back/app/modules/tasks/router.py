from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database.deps import get_db
from app.modules.tasks.schema import TaskCreate, TaskResponse, TaskUpdate
from app.modules.tasks.service import (
	create_user_task,
	delete_user_task,
	get_user_task_or_404,
	list_user_tasks,
	update_user_task,
)
from app.modules.users.model import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
	task_data: TaskCreate,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	return create_user_task(db, current_user.id, task_data)


@router.get("", response_model=list[TaskResponse])
def list_tasks(
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	return list_user_tasks(db, current_user.id)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
	task_id: int,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	return get_user_task_or_404(db, current_user.id, task_id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
	task_id: int,
	task_data: TaskUpdate,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	return update_user_task(db, current_user.id, task_id, task_data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
	task_id: int,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	delete_user_task(db, current_user.id, task_id)
