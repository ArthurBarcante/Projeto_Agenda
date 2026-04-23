from datetime import datetime, timedelta, timezone

from app.modules.badges.model import Badge
from app.modules.progress.model import Progress
from app.modules.progress.service import calculate_progress, check_badges, update_progress
from app.modules.tasks.model import Task


def utc_datetime(days_ago: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days_ago)


def test_get_progress_returns_metrics_from_user_tasks(client, db_session, auth_headers):
    headers, user = auth_headers()
    db_session.add_all(
        [
            Task(title="Concluida hoje", completed=True, completed_at=utc_datetime(0), user_id=user.id),
            Task(title="Concluida ontem", completed=True, completed_at=utc_datetime(1), user_id=user.id),
            Task(title="Pendente", completed=False, user_id=user.id),
        ]
    )
    db_session.commit()

    response = client.get("/progress", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == user.id
    assert body["completed_tasks"] == 2
    assert body["total_tasks"] == 3
    assert body["daily_completed_tasks"] == 1
    assert body["streak_days"] >= 2
    assert body["best_streak"] >= 2
    assert body["completion_rate"] == 66.67
    assert body["level"] in {"bronze", "prata", "ouro"}


def test_get_progress_by_user_id_returns_badges_and_progress(client, db_session, auth_headers):
    headers, user = auth_headers()
    db_session.add_all(
        [
            Task(title="Concluida hoje", completed=True, completed_at=utc_datetime(0), user_id=user.id),
            Task(title="Concluida ontem", completed=True, completed_at=utc_datetime(1), user_id=user.id),
            Task(title="Pendente", completed=False, user_id=user.id),
            Badge(name="Iniciante", description="Primeira tarefa concluida", required_tasks=1, required_streak=0),
            Badge(name="Consistente", description="Dois dias seguidos", required_tasks=0, required_streak=2),
        ]
    )
    db_session.commit()

    client.get("/progress", headers=headers)
    response = client.get(f"/progress/{user.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["progress"] == 66.67
    assert body["completed_tasks"] == 2
    assert body["total_tasks"] == 3
    assert body["streak"] >= 2
    assert body["best_streak"] >= 2
    assert body["account_level"] >= 1
    assert body["current_xp"] >= 0
    assert body["xp_to_next_level"] == 100
    assert body["badges"] == [
        {"name": "Iniciante", "description": "Primeira tarefa concluida"},
        {"name": "Consistente", "description": "Dois dias seguidos"},
    ]


def test_get_progress_by_user_id_returns_empty_payload_when_missing(client):
    response = client.get("/progress/999999")

    assert response.status_code == 200
    assert response.json() == {
        "progress": 0.0,
        "completed_tasks": 0,
        "total_tasks": 0,
        "streak": 0,
        "best_streak": 0,
        "account_level": 1,
        "current_xp": 0,
        "xp_to_next_level": 100,
        "badges": [],
    }


def test_update_progress_goal_persists_daily_goal(client, db_session, auth_headers):
    headers, user = auth_headers()

    response = client.put("/progress", json={"daily_goal": 5}, headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["daily_goal"] == 5

    progress = db_session.query(Progress).filter(Progress.user_id == user.id).first()
    assert progress is not None
    assert progress.daily_goal == 5


def test_progress_requires_authentication(client):
    response = client.get("/progress")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_calculate_progress_returns_percentage():
    progress = Progress(completed_tasks=3, total_tasks=4)

    assert calculate_progress(progress) == 75.0


def test_check_badges_returns_matching_badges(db_session):
    db_session.add_all(
        [
            Badge(name="Iniciante", description="Primeira tarefa concluida", required_tasks=1, required_streak=0),
            Badge(name="Consistente", description="Sete dias de streak", required_tasks=0, required_streak=7),
            Badge(name="Veterano", description="Cinquenta tarefas concluidas", required_tasks=50, required_streak=0),
        ]
    )
    db_session.commit()

    progress = Progress(completed_tasks=5, total_tasks=8, streak_days=7, best_streak=7, daily_goal=3, daily_completed_tasks=1, updated_at=utc_datetime(0))

    unlocked_badges = check_badges(db_session, progress)

    assert [badge.name for badge in unlocked_badges] == ["Iniciante", "Consistente"]


def test_update_progress_never_goes_below_zero(db_session, create_user):
    user, _ = create_user()

    progress = update_progress(
        db_session,
        user.id,
        completed_increment=-5,
        total_increment=-3,
    )

    assert progress.completed_tasks == 0
    assert progress.total_tasks == 0


def test_update_progress_uses_last_completed_at_for_streak(db_session, create_user):
    user, _ = create_user()

    # Primeira conclusão para criar o registro de progresso.
    initial_progress = update_progress(db_session, user.id, completed_increment=1, total_increment=1)
    initial_progress.streak_days = 3
    initial_progress.best_streak = 3
    initial_progress.last_completed_at = utc_datetime(2)
    db_session.add(initial_progress)
    db_session.commit()

    # Decremento não deve alterar a referência de última conclusão.
    after_decrement = update_progress(db_session, user.id, completed_increment=-1, total_increment=0)
    assert after_decrement.last_completed_at is not None
    assert normalize_datetime(after_decrement.last_completed_at).date() == normalize_datetime(
        utc_datetime(2)
    ).date()

    # Como a última conclusão foi há 2 dias, nova conclusão precisa resetar streak para 1.
    after_new_completion = update_progress(db_session, user.id, completed_increment=1, total_increment=0)
    assert after_new_completion.streak_days == 1


def normalize_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)