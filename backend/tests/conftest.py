import os
from pathlib import Path
import sys

if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
