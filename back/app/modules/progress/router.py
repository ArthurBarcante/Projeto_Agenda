from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database.deps import get_db
from app.modules.progress.schema import ProgressDetailResponse, ProgressGoalUpdate, ProgressResponse
from app.modules.progress.service import (
    get_progress_detail_payload,
    get_user_progress_payload,
    update_user_daily_goal,
)
from app.modules.users.model import User

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.get("/{user_id}", response_model=ProgressDetailResponse)
def get_progress_by_user_id(user_id: int, db: Session = Depends(get_db)):
    return get_progress_detail_payload(db, user_id)


@router.get("", response_model=ProgressResponse)
def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_user_progress_payload(db, current_user.id)


@router.put("", response_model=ProgressResponse)
def update_progress_goal(
    progress_data: ProgressGoalUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_user_daily_goal(db, current_user.id, progress_data.daily_goal)