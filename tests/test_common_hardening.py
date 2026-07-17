# === FILE HEADER ===
# Title: Test Common Hardening
# Path: tests/test_common_hardening.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Unit tests for masking, logos, mentions, purge order, limits.
#   - 2026-07-17 | docshamxo | Sibling purge and require_reaction missing-token tests.
# === END FILE HEADER ===

"""Unit tests for webhook helpers (mocked; no live Discord)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import discord
import pytest

from common import cia_common as c

WEBHOOK_URL = "https://discord.com/api/webhooks/1234567890/token"


def test_mask_webhook_url_redacts_token() -> None:
    masked = c.mask_webhook_url("https://discord.com/api/webhooks/1234567890/super-secret-token")
    assert "1234567890" in masked
    assert "super-secret-token" not in masked
    assert masked.endswith("/***")


def test_confined_logo_path_rejects_traversal() -> None:
    with pytest.raises(ValueError):
        c.confined_logo_path("../README.md")
    with pytest.raises(ValueError):
        c.confined_logo_path("/etc/passwd")
    path = c.confined_logo_path("DS.png")
    assert path.name == "DS.png"
    assert (
        c.LOGOS_DIR.resolve() in path.resolve().parents
        or path.parent.resolve() == c.LOGOS_DIR.resolve()
    )


def test_validate_embed_limits_detects_oversize_field() -> None:
    embed = discord.Embed(title="ok", description="ok", color=1)
    embed.add_field(name="n", value="x" * (c.EMBED_FIELD_VALUE_LIMIT + 1), inline=False)
    with pytest.raises(ValueError, match="field"):
        c.validate_embed_limits([embed])


def test_is_staff_placeholder() -> None:
    assert c.is_staff_placeholder("https://example.invalid/STAFF_LOCAL_REQUIRED")
    assert not c.is_staff_placeholder("https://docs.google.com/document/d/abc")


def test_send_webhook_sets_allowed_mentions_none_and_posts_before_delete(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state_path = tmp_path / ".webhook_messages.json"
    lock_path = tmp_path / ".webhook_messages.lock"
    monkeypatch.setattr(c, "WEBHOOK_MESSAGES_PATH", state_path)
    monkeypatch.setattr(c, "WEBHOOK_MESSAGES_LOCK_PATH", lock_path)

    state_path.write_text(json.dumps({"WEBHOOK_TEST": [111, 222]}), encoding="utf-8")

    events: list[str] = []
    posted = MagicMock()
    posted.id = 999
    posted.channel_id = 42

    class FakeWebhook:
        def send(self, **kwargs: Any) -> Any:
            events.append("send")
            assert kwargs.get("allowed_mentions") is not None
            mentions = kwargs["allowed_mentions"]
            assert mentions.everyone is False
            assert mentions.users is False
            assert mentions.roles is False
            assert kwargs.get("wait") is True
            return posted

        def delete_message(self, message_id: int) -> None:
            events.append(f"delete:{message_id}")

    fake_session = MagicMock()
    monkeypatch.setattr(c, "_session_with_timeout", lambda: fake_session)
    monkeypatch.setattr(c, "_bot_token", lambda: "")

    with patch("discord.SyncWebhook.from_url") as from_url:
        from_url.return_value = FakeWebhook()
        ids = c.send_webhook(
            WEBHOOK_URL,
            [discord.Embed(title="t", description="d", color=1)],
            username="Test Bot",
            state_key="WEBHOOK_TEST",
            require_reaction=False,
        )
        kwargs = from_url.call_args.kwargs
        assert kwargs.get("bot_token") in (None, "")
        assert "bot_token" not in kwargs or kwargs["bot_token"] in (None, "")

    assert ids == [999]
    assert events[0] == "send"
    assert "delete:111" in events
    assert "delete:222" in events
    assert events.index("send") < min(events.index("delete:111"), events.index("delete:222"))

    saved = json.loads(state_path.read_text(encoding="utf-8"))
    assert saved["WEBHOOK_TEST"] == [999]


def test_send_webhook_purges_sibling_state_keys(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state_path = tmp_path / ".webhook_messages.json"
    lock_path = tmp_path / ".webhook_messages.lock"
    monkeypatch.setattr(c, "WEBHOOK_MESSAGES_PATH", state_path)
    monkeypatch.setattr(c, "WEBHOOK_MESSAGES_LOCK_PATH", lock_path)

    state_path.write_text(
        json.dumps(
            {
                "WEBHOOK_PRIMARY": [101],
                "WEBHOOK_SIBLING": [202, 303],
            }
        ),
        encoding="utf-8",
    )

    deleted: list[int] = []
    posted = MagicMock()
    posted.id = 404
    posted.channel_id = 7

    class FakeWebhook:
        def send(self, **kwargs: Any) -> Any:
            return posted

        def delete_message(self, message_id: int) -> None:
            deleted.append(message_id)

    monkeypatch.setattr(c, "_session_with_timeout", MagicMock)
    monkeypatch.setattr(c, "_bot_token", lambda: "")
    monkeypatch.setenv("WEBHOOK_PRIMARY", WEBHOOK_URL)
    monkeypatch.setenv("WEBHOOK_SIBLING", WEBHOOK_URL)
    monkeypatch.setattr("discord.SyncWebhook.from_url", lambda *a, **k: FakeWebhook())

    c.send_webhook(
        WEBHOOK_URL,
        [discord.Embed(title="t", description="d", color=1)],
        username="Test Bot",
        state_key="WEBHOOK_PRIMARY",
        require_reaction=False,
    )

    assert sorted(deleted) == [101, 202, 303]
    saved = json.loads(state_path.read_text(encoding="utf-8"))
    assert saved == {"WEBHOOK_PRIMARY": [404]}
    assert "WEBHOOK_SIBLING" not in saved


def test_send_webhook_requires_bot_token_when_reaction_required(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(c, "WEBHOOK_MESSAGES_PATH", tmp_path / ".webhook_messages.json")
    monkeypatch.setattr(c, "WEBHOOK_MESSAGES_LOCK_PATH", tmp_path / ".webhook_messages.lock")

    posted = MagicMock()
    posted.id = 1
    posted.channel_id = 2

    class FakeWebhook:
        def send(self, **kwargs: Any) -> Any:
            return posted

        def delete_message(self, message_id: int) -> None:
            return None

    monkeypatch.setattr(c, "_session_with_timeout", MagicMock)
    monkeypatch.setattr(c, "_bot_token", lambda: "")
    monkeypatch.setattr("discord.SyncWebhook.from_url", lambda *a, **k: FakeWebhook())

    with pytest.raises(RuntimeError, match=c.BOT_TOKEN_ENV):
        c.send_webhook(
            WEBHOOK_URL,
            [discord.Embed(title="t", description="d", color=1)],
            username="Test Bot",
            require_reaction=True,
        )


def test_send_webhook_file_factory_called(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(c, "WEBHOOK_MESSAGES_PATH", tmp_path / ".webhook_messages.json")
    monkeypatch.setattr(c, "WEBHOOK_MESSAGES_LOCK_PATH", tmp_path / ".webhook_messages.lock")

    class FakeWebhook:
        def send(self, **kwargs: Any) -> Any:
            files = kwargs.get("files") or []
            assert len(files) == 1
            msg = MagicMock()
            msg.id = 1
            msg.channel_id = 2
            return msg

        def delete_message(self, message_id: int) -> None:
            return None

    monkeypatch.setattr(c, "_session_with_timeout", MagicMock)
    monkeypatch.setattr(c, "_bot_token", lambda: "")
    monkeypatch.setattr("discord.SyncWebhook.from_url", lambda *a, **k: FakeWebhook())

    factory_calls = {"n": 0}

    def factory() -> list[discord.File]:
        factory_calls["n"] += 1
        return [c.logo_file(c.LOGOS["ds"])]

    c.send_webhook(
        WEBHOOK_URL,
        [discord.Embed(title="t", description="d", color=1)],
        username="Test Bot",
        files=factory,
        require_reaction=False,
    )
    assert factory_calls["n"] == 1


# === FILE FOOTER ===
# End of file: tests/test_common_hardening.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
