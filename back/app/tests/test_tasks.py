from app.modules.tasks.model import Task


def test_create_task_creates_task_for_authenticated_user(client, db_session, auth_headers):
    headers, user = auth_headers()

    response = client.post(
        "/tasks",
        json={
            "title": "Preparar sprint",
            "description": "Organizar backlog da semana",
            "completed": False,
            "due_date": "2026-04-15T14:00:00Z",
        },
        headers=headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Preparar sprint"
    assert body["description"] == "Organizar backlog da semana"
    assert body["completed"] is False
    assert body["user_id"] == user.id
    assert body["due_date"].startswith("2026-04-15T14:00:00")

    created_task = db_session.query(Task).filter(Task.id == body["id"]).first()
    assert created_task is not None
    assert created_task.user_id == user.id


def test_list_tasks_returns_only_authenticated_user_tasks(client, db_session, auth_headers, create_user):
    headers, user = auth_headers()
    other_user, _ = create_user()

    db_session.add_all(
        [
            Task(title="Tarefa visivel", completed=False, user_id=user.id),
            Task(title="Tarefa oculta", completed=False, user_id=other_user.id),
        ]
    )
    db_session.commit()

    response = client.get("/tasks", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Tarefa visivel"
    assert body[0]["user_id"] == user.id


def test_get_task_returns_task_owned_by_authenticated_user(client, db_session, auth_headers):
    headers, user = auth_headers()
    task = Task(title="Detalhar entrega", completed=False, user_id=user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    response = client.get(f"/tasks/{task.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == task.id
    assert response.json()["title"] == "Detalhar entrega"


def test_get_task_returns_404_for_task_from_other_user(client, db_session, auth_headers, create_user):
    headers, _ = auth_headers()
    other_user, _ = create_user()
    task = Task(title="Privada", completed=False, user_id=other_user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    response = client.get(f"/tasks/{task.id}", headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Tarefa nao encontrada"}


def test_update_task_updates_only_owned_task(client, db_session, auth_headers):
    headers, user = auth_headers()
    task = Task(title="Original", description="Antiga", completed=False, user_id=user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    response = client.put(
        f"/tasks/{task.id}",
        json={"title": "Atualizada", "completed": True},
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Atualizada"
    assert body["completed"] is True
    assert body["description"] == "Antiga"


def test_delete_task_removes_owned_task(client, db_session, auth_headers):
    headers, user = auth_headers()
    task = Task(title="Excluir", completed=False, user_id=user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    response = client.delete(f"/tasks/{task.id}", headers=headers)

    assert response.status_code == 204
    deleted_task = db_session.query(Task).filter(Task.id == task.id).first()
    assert deleted_task is None


def test_tasks_require_authentication(client):
    response = client.get("/tasks")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_create_task_increments_total_tasks_in_progress(client, auth_headers):
    headers, _ = auth_headers()

    create_response = client.post(
        "/tasks",
        json={
            "title": "Nova tarefa",
            "description": "Sem concluir",
            "completed": False,
        },
        headers=headers,
    )
    assert create_response.status_code == 201

    progress_response = client.get("/progress", headers=headers)
    assert progress_response.status_code == 200
    body = progress_response.json()
    assert body["total_tasks"] == 1
    assert body["completed_tasks"] == 0


def test_concluding_task_increments_completed_tasks_only_once(client, auth_headers):
    headers, _ = auth_headers()

    create_response = client.post(
        "/tasks",
        json={
            "title": "Concluir depois",
            "completed": False,
        },
        headers=headers,
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    first_update = client.put(
        f"/tasks/{task_id}",
        json={"completed": True},
        headers=headers,
    )
    assert first_update.status_code == 200

    progress_after_first = client.get("/progress", headers=headers)
    assert progress_after_first.status_code == 200
    body_after_first = progress_after_first.json()
    assert body_after_first["total_tasks"] == 1
    assert body_after_first["completed_tasks"] == 1

    second_update = client.put(
        f"/tasks/{task_id}",
        json={"completed": True},
        headers=headers,
    )
    assert second_update.status_code == 200

    progress_after_second = client.get("/progress", headers=headers)
    assert progress_after_second.status_code == 200
    body_after_second = progress_after_second.json()
    assert body_after_second["total_tasks"] == 1
    assert body_after_second["completed_tasks"] == 1