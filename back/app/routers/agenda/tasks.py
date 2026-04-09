from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database.deps import get_db
from app.models.tasks import Task
from app.models.user import User
from app.schemas.agenda.tasks import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
	task_data: TaskCreate,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	new_task = Task(**task_data.model_dump(), user_id=current_user.id)

	db.add(new_task)
	db.commit()
	db.refresh(new_task)

	return new_task


@router.get("", response_model=list[TaskResponse])
def list_tasks(
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	return (
		db.query(Task)
		.filter(Task.user_id == current_user.id)
		.order_by(Task.id.desc())
		.all()
	)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
	task_id: int,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	task = (
		db.query(Task)
		.filter(Task.id == task_id, Task.user_id == current_user.id)
		.first()
	)

	if task is None:
		raise HTTPException(status_code=404, detail="Tarefa nao encontrada")

	return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
	task_id: int,
	task_data: TaskUpdate,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	task = (
		db.query(Task)
		.filter(Task.id == task_id, Task.user_id == current_user.id)
		.first()
	)

	if task is None:
		raise HTTPException(status_code=404, detail="Tarefa nao encontrada")

	for field, value in task_data.model_dump(exclude_unset=True).items():
		setattr(task, field, value)

	db.commit()
	db.refresh(task)

	return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
	task_id: int,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
):
	task = (
		db.query(Task)
		.filter(Task.id == task_id, Task.user_id == current_user.id)
		.first()
	)

	if task is None:
		raise HTTPException(status_code=404, detail="Tarefa nao encontrada")

	db.delete(task)
	db.commit()
