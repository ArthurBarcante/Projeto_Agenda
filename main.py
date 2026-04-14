from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
BACK_DIR = BASE_DIR / "back"

if str(BACK_DIR) not in sys.path:
    sys.path.insert(0, str(BACK_DIR))

from app.main import app  # noqa: E402
