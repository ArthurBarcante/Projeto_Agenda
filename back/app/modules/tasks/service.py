from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.progress.service import get_utc_now, update_progress
from app.modules.tasks.model import Task
from app.modules.tasks.schema import TaskCreate, TaskUpdate


def create_user_task(db: Session, user_id: int, payload: TaskCreate) -> Task:
    task_payload = payload.model_dump()
    completed_increment = 0

    if task_payload.get("completed"):
        task_payload["completed_at"] = get_utc_now()
        completed_increment = 1

    new_task = Task(**task_payload, user_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    update_progress(db, user_id, completed_increment=completed_increment, total_increment=1)
    return new_task


def list_user_tasks(db: Session, user_id: int) -> list[Task]:
    return db.query(Task).filter(Task.user_id == user_id).order_by(Task.id.desc()).all()


def get_user_task_or_404(db: Session, user_id: int, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa nao encontrada")
    return task


def update_user_task(db: Session, user_id: int, task_id: int, payload: TaskUpdate) -> Task:
    task = get_user_task_or_404(db, user_id, task_id)
    update_data = payload.model_dump(exclude_unset=True)
    completed_increment = 0

    if "completed" in update_data:
        if update_data["completed"] is True and not task.completed:
            update_data["completed_at"] = get_utc_now()
            completed_increment = 1
        elif update_data["completed"] is False:
            update_data["completed_at"] = None
            if task.completed:
                completed_increment = -1

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    if completed_increment != 0:
        update_progress(db, user_id, completed_increment=completed_increment)

    return task


def delete_user_task(db: Session, user_id: int, task_id: int) -> None:
    task = get_user_task_or_404(db, user_id, task_id)
    completed_increment = -1 if task.completed else 0

    db.delete(task)
    db.commit()
    update_progress(db, user_id, completed_increment=completed_increment, total_increment=-1)
