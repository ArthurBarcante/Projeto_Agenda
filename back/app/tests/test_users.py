def test_users_me_returns_authenticated_user(client, auth_headers):
    headers, user = auth_headers()

    response = client.get("/users/me", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == user.id
    assert body["email"] == user.email
    assert body["name"] == user.name


def test_users_me_requires_authentication(client):
    response = client.get("/users/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_users_me_put_updates_mutable_fields(client, auth_headers, db_session):
    headers, _ = auth_headers()

    response = client.put(
        "/users/me",
        json={"name": "Novo Nome", "email": "novo.email@example.com", "phone": "11998887777"},
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Novo Nome"
    assert body["email"] == "novo.email@example.com"
    assert body["phone"] == "11998887777"

    refreshed_response = client.get("/users/me", headers=headers)
    assert refreshed_response.status_code == 200
    assert refreshed_response.json()["email"] == "novo.email@example.com"


def test_users_me_put_rejects_duplicate_email(client, auth_headers, create_user):
    headers, _ = auth_headers()
    existing_user, _ = create_user()

    response = client.put(
        "/users/me",
        json={"email": existing_user.email},
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Email já cadastrado"}
