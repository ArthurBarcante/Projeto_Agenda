from datetime import datetime, timezone

from app.modules.events.model import Event


def utc_datetime(year, month, day, hour, minute=0, second=0):
    return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)


def test_create_event_creates_event_for_authenticated_user(client, db_session, auth_headers):
    headers, user = auth_headers()

    response = client.post(
        "/events",
        json={
            "title": "Reuniao de kickoff",
            "description": "Alinhar escopo do projeto",
            "start_at": "2026-04-16T13:00:00Z",
            "end_at": "2026-04-16T14:00:00Z",
            "location": "Sala virtual",
        },
        headers=headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Reuniao de kickoff"
    assert body["location"] == "Sala virtual"
    assert body["user_id"] == user.id
    assert body["start_at"].startswith("2026-04-16T13:00:00")
    assert body["end_at"].startswith("2026-04-16T14:00:00")

    created_event = db_session.query(Event).filter(Event.id == body["id"]).first()
    assert created_event is not None
    assert created_event.user_id == user.id


def test_list_events_returns_only_authenticated_user_events(client, db_session, auth_headers, create_user):
    headers, user = auth_headers()
    other_user, _ = create_user()

    db_session.add_all(
        [
            Event(title="Evento visivel", start_at=utc_datetime(2026, 4, 18, 9), user_id=user.id),
            Event(title="Evento oculto", start_at=utc_datetime(2026, 4, 18, 10), user_id=other_user.id),
        ]
    )
    db_session.commit()

    response = client.get("/events", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Evento visivel"
    assert body[0]["user_id"] == user.id


def test_get_event_returns_event_owned_by_authenticated_user(client, db_session, auth_headers):
    headers, user = auth_headers()
    event = Event(title="Workshop", start_at=utc_datetime(2026, 4, 19, 15), user_id=user.id)
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)

    response = client.get(f"/events/{event.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == event.id
    assert response.json()["title"] == "Workshop"


def test_get_event_returns_404_for_event_from_other_user(client, db_session, auth_headers, create_user):
    headers, _ = auth_headers()
    other_user, _ = create_user()
    event = Event(title="Privado", start_at=utc_datetime(2026, 4, 20, 8), user_id=other_user.id)
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)

    response = client.get(f"/events/{event.id}", headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Evento nao encontrado"}


def test_update_event_updates_only_owned_event(client, db_session, auth_headers):
    headers, user = auth_headers()
    event = Event(
        title="Original",
        description="Descricao antiga",
        start_at=utc_datetime(2026, 4, 21, 12),
        location="Sala 1",
        user_id=user.id,
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)

    response = client.put(
        f"/events/{event.id}",
        json={"title": "Atualizado", "location": "Sala 2"},
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Atualizado"
    assert body["location"] == "Sala 2"
    assert body["description"] == "Descricao antiga"


def test_delete_event_removes_owned_event(client, db_session, auth_headers):
    headers, user = auth_headers()
    event = Event(title="Excluir", start_at=utc_datetime(2026, 4, 22, 17), user_id=user.id)
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)

    response = client.delete(f"/events/{event.id}", headers=headers)

    assert response.status_code == 204
    deleted_event = db_session.query(Event).filter(Event.id == event.id).first()
    assert deleted_event is None


def test_events_require_authentication(client):
    response = client.get("/events")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}