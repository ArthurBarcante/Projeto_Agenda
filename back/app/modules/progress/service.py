from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.modules.badges.model import Badge
from app.modules.progress.model import Progress
from app.modules.tasks.model import Task


DEFAULT_DAILY_GOAL = 3
XP_PER_COMPLETED_TASK = 10
XP_PER_STREAK_DAY = 5
XP_PER_BADGE = 40
XP_PER_LEVEL = 100


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_datetime(value: datetime | None) -> datetime | None:
    if value is None:
        return None

    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc)


def calculate_streak(completed_dates: set[date], today: date | None = None) -> tuple[int, int]:
    if not completed_dates:
        return 0, 0

    current_day = today or get_utc_now().date()
    ordered_dates = sorted(completed_dates)
    best_streak = 1
    running_streak = 1

    for previous_day, next_day in zip(ordered_dates, ordered_dates[1:]):
        if next_day == previous_day + timedelta(days=1):
            running_streak += 1
            best_streak = max(best_streak, running_streak)
        else:
            running_streak = 1

    if current_day in completed_dates:
        streak_anchor = current_day
    elif current_day - timedelta(days=1) in completed_dates:
        streak_anchor = current_day - timedelta(days=1)
    else:
        return 0, best_streak

    current_streak = 0
    while streak_anchor in completed_dates:
        current_streak += 1
        streak_anchor -= timedelta(days=1)

    return current_streak, best_streak


def calculate_progress(progress: Progress) -> float:
    if progress.total_tasks <= 0:
        return 0.0

    return round((progress.completed_tasks / progress.total_tasks) * 100, 2)


def get_or_create_progress(db: Session, user_id: int) -> Progress:
    progress = db.query(Progress).filter(Progress.user_id == user_id).first()

    if progress is None:
        progress = Progress(
            user_id=user_id,
            completed_tasks=0,
            total_tasks=0,
            daily_goal=DEFAULT_DAILY_GOAL,
            streak_days=0,
            best_streak=0,
            daily_completed_tasks=0,
            updated_at=get_utc_now(),
        )
        db.add(progress)
        db.flush()

    return progress


def update_progress(
    db: Session,
    user_id: int,
    completed_increment: int = 0,
    total_increment: int = 0,
) -> Progress:
    progress = get_or_create_progress(db, user_id)
    previous_update = normalize_datetime(progress.updated_at)
    today = get_utc_now().date()

    progress.completed_tasks = max(progress.completed_tasks + completed_increment, 0)
    progress.total_tasks = max(progress.total_tasks + total_increment, 0)

    if completed_increment > 0:
        if previous_update is None:
            progress.streak_days = 1
        else:
            delta_days = (today - previous_update.date()).days
            if delta_days == 0:
                progress.streak_days = max(progress.streak_days, 1)
            elif delta_days == 1:
                progress.streak_days += 1
            else:
                progress.streak_days = 1

        progress.best_streak = max(progress.best_streak, progress.streak_days)
        if previous_update is None or previous_update.date() != today:
            progress.daily_completed_tasks = max(completed_increment, 0)
        else:
            progress.daily_completed_tasks = max(progress.daily_completed_tasks + completed_increment, 0)

    progress.updated_at = get_utc_now()

    if progress.daily_goal < 1:
        progress.daily_goal = DEFAULT_DAILY_GOAL

    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


def check_badges(db: Session, progress: Progress) -> list[Badge]:
    badges = db.query(Badge).order_by(Badge.id.asc()).all()
    unlocked_badges: list[Badge] = []
    streak_value = max(progress.streak_days, progress.best_streak)

    for badge in badges:
        required_tasks = badge.required_tasks or 0
        required_streak = badge.required_streak or 0

        if progress.completed_tasks >= required_tasks and streak_value >= required_streak:
            unlocked_badges.append(badge)

    return unlocked_badges


def calculate_account_level_payload(progress: Progress | None, badges: list[Badge] | None = None) -> dict:
    if progress is None:
        return {
            "account_level": 1,
            "current_xp": 0,
            "xp_to_next_level": XP_PER_LEVEL,
        }

    unlocked_badges = badges or []
    total_xp = (
        (progress.completed_tasks * XP_PER_COMPLETED_TASK)
        + (progress.best_streak * XP_PER_STREAK_DAY)
        + (len(unlocked_badges) * XP_PER_BADGE)
    )
    account_level = (total_xp // XP_PER_LEVEL) + 1
    current_xp = total_xp % XP_PER_LEVEL

    return {
        "account_level": account_level,
        "current_xp": current_xp,
        "xp_to_next_level": XP_PER_LEVEL,
    }


def build_progress_detail_payload(progress: Progress | None, badges: list[Badge] | None = None) -> dict:
    if progress is None:
        return {
            "progress": 0.0,
            "completed_tasks": 0,
            "total_tasks": 0,
            "streak": 0,
            "best_streak": 0,
            "account_level": 1,
            "current_xp": 0,
            "xp_to_next_level": XP_PER_LEVEL,
            "badges": [],
        }

    unlocked_badges = badges or []
    account_level_payload = calculate_account_level_payload(progress, unlocked_badges)
    return {
        "progress": calculate_progress(progress),
        "completed_tasks": progress.completed_tasks,
        "total_tasks": progress.total_tasks,
        "streak": progress.streak_days,
        "best_streak": progress.best_streak,
        "account_level": account_level_payload["account_level"],
        "current_xp": account_level_payload["current_xp"],
        "xp_to_next_level": account_level_payload["xp_to_next_level"],
        "badges": [
            {
                "name": badge.name,
                "description": badge.description,
            }
            for badge in unlocked_badges
        ],
    }


def sync_progress(db: Session, user_id: int, *, commit: bool = False) -> Progress:
    progress = get_or_create_progress(db, user_id)
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    today = get_utc_now().date()

    completed_dates = {
        normalized_completed_at.date()
        for task in tasks
        for normalized_completed_at in [normalize_datetime(task.completed_at)]
        if task.completed and normalized_completed_at is not None
    }

    progress.total_tasks = len(tasks)
    progress.completed_tasks = sum(1 for task in tasks if task.completed)
    progress.daily_completed_tasks = sum(
        1
        for task in tasks
        for normalized_completed_at in [normalize_datetime(task.completed_at)]
        if task.completed and normalized_completed_at is not None and normalized_completed_at.date() == today
    )
    progress.streak_days, progress.best_streak = calculate_streak(completed_dates, today=today)
    progress.updated_at = get_utc_now()

    if progress.daily_goal < 1:
        progress.daily_goal = DEFAULT_DAILY_GOAL

    if commit:
        db.add(progress)
        db.commit()
        db.refresh(progress)
    else:
        db.flush()

    return progress


def build_progress_payload(progress: Progress) -> dict:
    completion_rate = calculate_progress(progress)

    goal_completed = progress.daily_completed_tasks >= progress.daily_goal

    if progress.best_streak >= 14 or completion_rate >= 85:
        level = "ouro"
        next_level = None
    elif progress.best_streak >= 7 or completion_rate >= 60:
        level = "prata"
        next_level = "ouro"
    else:
        level = "bronze"
        next_level = "prata"

    return {
        "user_id": progress.user_id,
        "completed_tasks": progress.completed_tasks,
        "total_tasks": progress.total_tasks,
        "completion_rate": completion_rate,
        "streak_days": progress.streak_days,
        "best_streak": progress.best_streak,
        "daily_goal": progress.daily_goal,
        "daily_completed_tasks": progress.daily_completed_tasks,
        "goal_completed": goal_completed,
        "level": level,
        "next_level": next_level,
        "updated_at": progress.updated_at,
    }


def get_user_progress_payload(db: Session, user_id: int) -> dict:
    progress = sync_progress(db, user_id, commit=True)
    check_badges(db, progress)
    return build_progress_payload(progress)


def get_progress_detail_payload(db: Session, user_id: int) -> dict:
    progress = db.query(Progress).filter(Progress.user_id == user_id).first()

    if progress is None:
        return build_progress_detail_payload(None)

    badges = check_badges(db, progress)
    return build_progress_detail_payload(progress, badges)


def update_user_daily_goal(db: Session, user_id: int, daily_goal: int) -> dict:
    progress = sync_progress(db, user_id, commit=False)
    progress.daily_goal = daily_goal
    db.add(progress)
    db.commit()
    db.refresh(progress)
    progress = sync_progress(db, user_id, commit=True)
    return build_progress_payload(progress)
