from fastapi.testclient import TestClient

from app.main import create_app


client = TestClient(create_app(init_database_on_startup=False))


def test_root_returns_backend_running_message():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Backend funcionando!"}
