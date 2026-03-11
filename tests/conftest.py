import os

pytest_plugins = ["tests.fixtures"]

if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
