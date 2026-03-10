import os
from pathlib import Path
import sys

pytest_plugins = ["tests.fixtures"]

if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
