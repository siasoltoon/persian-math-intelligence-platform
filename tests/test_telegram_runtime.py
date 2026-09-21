import pytest

from persian_math.runtime_config import load_runtime_config


def test_runtime_config_requires_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="TELEGRAM_BOT_TOKEN"):
        load_runtime_config()


def test_runtime_config_loads_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    config = load_runtime_config()
    assert config.telegram_bot_token == "test-token"
