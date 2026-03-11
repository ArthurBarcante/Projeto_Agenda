import importlib
import sys

import pytest


MODULE_PATH = "app.core.settings.settings"
PACKAGE_PATH = "app.core.settings"


def _reload_settings_module(monkeypatch: pytest.MonkeyPatch, environment: str, secret_key: str) -> None:
    monkeypatch.setenv("ENVIRONMENT", environment)
    monkeypatch.setenv("SECRET_KEY", secret_key)

    # Force module re-import so startup validation runs with fresh env values.
    sys.modules.pop(MODULE_PATH, None)
    sys.modules.pop(PACKAGE_PATH, None)
    importlib.import_module(MODULE_PATH)


def test_allows_dev_secret_key_in_development(monkeypatch: pytest.MonkeyPatch) -> None:
    _reload_settings_module(monkeypatch, environment="development", secret_key="dev-secret-key")


def test_rejects_default_secret_key_outside_development(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with pytest.raises(RuntimeError, match="Insecure SECRET_KEY configuration detected"):
        _reload_settings_module(monkeypatch, environment="production", secret_key="dev-secret-key")


def test_rejects_blank_secret_key_outside_development(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with pytest.raises(RuntimeError, match="Insecure SECRET_KEY configuration detected"):
        _reload_settings_module(monkeypatch, environment="staging", secret_key="   ")


def test_allows_custom_secret_key_outside_development(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _reload_settings_module(
        monkeypatch,
        environment="production",
        secret_key="a-strong-secret-key-value",
    )
