from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProgressGoalUpdate(BaseModel):
    daily_goal: int = Field(ge=1, le=50)


class ProgressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    completed_tasks: int
    total_tasks: int
    completion_rate: float
    streak_days: int
    best_streak: int
    daily_goal: int
    daily_completed_tasks: int
    goal_completed: bool
    level: str
    next_level: str | None = None
    updated_at: datetime


class BadgeUnlockedResponse(BaseModel):
    name: str
    description: str | None = None


class ProgressDetailResponse(BaseModel):
    progress: float
    completed_tasks: int
    total_tasks: int
    streak: int
    best_streak: int
    account_level: int
    current_xp: int
    xp_to_next_level: int
    badges: list[BadgeUnlockedResponse]