# === FILE HEADER ===
# Title: Pytest Conftest
# Path: tests/conftest.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Isolate webhook state paths; silence reaction sleeps.
# === END FILE HEADER ===

"""Shared fixtures for mocked Discord / isolated local state."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from common import cia_common as c


@pytest.fixture
def webhook_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point webhook message ID persistence at an isolated temp file."""
    state_path = tmp_path / ".webhook_messages.json"
    lock_path = tmp_path / ".webhook_messages.lock"
    monkeypatch.setattr(c, "WEBHOOK_MESSAGES_PATH", state_path)
    monkeypatch.setattr(c, "WEBHOOK_MESSAGES_LOCK_PATH", lock_path)
    return state_path


@pytest.fixture
def no_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    """Avoid real sleeps in retry / rate-limit paths (keeps CI non-flaky)."""
    monkeypatch.setattr(c.time, "sleep", lambda *_a, **_k: None)


@pytest.fixture
def empty_bot_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(c, "_bot_token", lambda: "")


@pytest.fixture
def fake_webhook_session(monkeypatch: pytest.MonkeyPatch) -> Any:
    session = pytest.importorskip("unittest.mock").MagicMock()
    monkeypatch.setattr(c, "_session_with_timeout", lambda: session)
    return session


# === FILE FOOTER ===
# End of file: tests/conftest.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
