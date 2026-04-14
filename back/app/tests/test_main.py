import importlib
import os
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app

ROOT_DIR = Path(__file__).resolve().parents[3]


client = TestClient(create_app(init_database_on_startup=False))


def test_root_returns_backend_running_message():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Backend funcionando!"}


def test_render_entrypoint_module_can_be_imported():
    module = importlib.import_module("main")

    assert hasattr(module, "app")


def test_render_entrypoint_module_can_be_imported_from_back_directory():
    result = subprocess.run(
        [sys.executable, "-c", "import main; assert hasattr(main, 'app')"],
        cwd=ROOT_DIR / "back",
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr


def test_render_startup_works_without_env_variables():
    env = os.environ.copy()
    env.pop("DATABASE_URL", None)
    env.pop("SECRET_KEY", None)
    env["APP_INIT_DB_ON_STARTUP"] = "0"

    script = """
from unittest.mock import patch

with patch('dotenv.load_dotenv', lambda *args, **kwargs: False):
    import app.core.config as config
    assert config.DATABASE_URL
    assert config.SECRET_KEY
"""

    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=ROOT_DIR / "back",
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
