# === FILE HEADER ===
# Title: Test Webhook Purge
# Path: tests/test_webhook_purge.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Regression: post-before-purge, retain IDs, 404/429.
#   - 2026-07-17 | docshamxo | Pass require_reaction=False when testing purge without bot token.
# === END FILE HEADER ===

"""Regression tests for safer webhook purge (post first, then delete priors)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import discord
import pytest
from discord.errors import HTTPException

from common import cia_common as c

WEBHOOK = "https://discord.com/api/webhooks/1234567890/purge-token"


def _http_exc(status: int) -> HTTPException:
    response = MagicMock()
    response.status = status
    response.headers = {}
    return HTTPException(response, {"message": f"status {status}"})


def _posted(message_id: int = 9001, channel_id: int = 42) -> MagicMock:
    msg = MagicMock()
    msg.id = message_id
    msg.channel_id = channel_id
    return msg


class RecordingWebhook:
    def __init__(
        self, *, send_result: Any = None, delete_errors: dict[int, Exception] | None = None
    ):
        self.events: list[str] = []
        self._send_result = send_result if send_result is not None else _posted()
        self._delete_errors = delete_errors or {}
        self.delete_calls: list[int] = []

    def send(self, **kwargs: Any) -> Any:
        self.events.append("send")
        assert kwargs.get("wait") is True
        if isinstance(self._send_result, Exception):
            raise self._send_result
        return self._send_result

    def delete_message(self, message_id: int) -> None:
        self.events.append(f"delete:{message_id}")
        self.delete_calls.append(message_id)
        err = self._delete_errors.get(message_id)
        if err is not None:
            raise err


def test_unique_message_ids_preserves_order() -> None:
    assert c._unique_message_ids([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_load_webhook_state_coerces_scalar_and_skips_junk(
    webhook_state: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    webhook_state.write_text(
        json.dumps({"A": 11, "B": ["22", 33, "nope"], "C": {"x": 1}, 9: [1]}),
        encoding="utf-8",
    )
    state = c._load_webhook_message_state()
    assert state["A"] == [11]
    assert state["B"] == [22, 33]
    assert "C" not in state


def test_load_webhook_state_corrupt_json_returns_empty(webhook_state: Path) -> None:
    webhook_state.write_text("{not-json", encoding="utf-8")
    assert c._load_webhook_message_state() == {}


def test_save_webhook_message_state_atomic_and_drops_empty(webhook_state: Path) -> None:
    c._save_webhook_message_state({"KEEP": [1, 2], "DROP": []})
    saved = json.loads(webhook_state.read_text(encoding="utf-8"))
    assert saved == {"KEEP": [1, 2]}
    assert not webhook_state.with_suffix(".json.tmp").exists()


def test_delete_404_counts_as_cleared(no_sleep: None) -> None:
    webhook = RecordingWebhook(delete_errors={111: _http_exc(404)})
    remaining = c._delete_webhook_messages(
        webhook, state_key="WEBHOOK_TEST", message_ids=[111, 111]
    )
    assert remaining == []
    assert webhook.delete_calls == [111]


def test_delete_non_404_keeps_remaining(no_sleep: None) -> None:
    webhook = RecordingWebhook(delete_errors={222: _http_exc(403)})
    remaining = c._delete_webhook_messages(
        webhook, state_key="WEBHOOK_TEST", message_ids=[111, 222]
    )
    assert remaining == [222]
    assert webhook.delete_calls == [111, 222]


def test_delete_429_retries_once(no_sleep: None) -> None:
    calls = {"n": 0}

    class FlakyWebhook:
        def delete_message(self, message_id: int) -> None:
            calls["n"] += 1
            if calls["n"] == 1:
                raise _http_exc(429)

    remaining = c._delete_webhook_messages(
        FlakyWebhook(), state_key="WEBHOOK_TEST", message_ids=[55]
    )
    assert remaining == []
    assert calls["n"] == 2


def test_failed_send_does_not_purge_or_rewrite_state(
    webhook_state: Path,
    empty_bot_token: None,
    fake_webhook_session: Any,
    no_sleep: None,
) -> None:
    webhook_state.write_text(json.dumps({"WEBHOOK_TEST": [111, 222]}), encoding="utf-8")
    fake = RecordingWebhook(send_result=_http_exc(400))

    with patch("discord.SyncWebhook.from_url", return_value=fake):
        with pytest.raises(RuntimeError, match="webhook send failed"):
            c.send_webhook(
                WEBHOOK,
                [discord.Embed(title="t", description="d", color=1)],
                username="Test Bot",
                state_key="WEBHOOK_TEST",
                require_reaction=False,
            )

    assert fake.events == ["send"]
    assert "delete:111" not in fake.events
    assert json.loads(webhook_state.read_text(encoding="utf-8"))["WEBHOOK_TEST"] == [111, 222]


def test_partial_purge_retains_remaining_plus_new_ids(
    webhook_state: Path,
    empty_bot_token: None,
    fake_webhook_session: Any,
    no_sleep: None,
) -> None:
    webhook_state.write_text(json.dumps({"WEBHOOK_TEST": [111, 222]}), encoding="utf-8")
    fake = RecordingWebhook(
        send_result=_posted(999),
        delete_errors={222: _http_exc(403)},
    )

    with patch("discord.SyncWebhook.from_url", return_value=fake):
        ids = c.send_webhook(
            WEBHOOK,
            [discord.Embed(title="t", description="d", color=1)],
            username="Test Bot",
            state_key="WEBHOOK_TEST",
            require_reaction=False,
        )

    assert ids == [999]
    assert fake.events[0] == "send"
    assert fake.events.index("send") < fake.events.index("delete:111")
    saved = json.loads(webhook_state.read_text(encoding="utf-8"))
    assert saved["WEBHOOK_TEST"] == [222, 999]


def test_send_without_state_key_skips_purge(
    webhook_state: Path,
    empty_bot_token: None,
    fake_webhook_session: Any,
) -> None:
    webhook_state.write_text(json.dumps({"OTHER": [1]}), encoding="utf-8")
    fake = RecordingWebhook(send_result=_posted(50))

    with patch("discord.SyncWebhook.from_url", return_value=fake):
        c.send_webhook(
            WEBHOOK,
            [discord.Embed(title="t", description="d", color=1)],
            username="Test Bot",
            require_reaction=False,
        )

    assert fake.events == ["send"]
    assert json.loads(webhook_state.read_text(encoding="utf-8")) == {"OTHER": [1]}


# === FILE FOOTER ===
# End of file: tests/test_webhook_purge.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
