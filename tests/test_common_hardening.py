# === FILE HEADER ===
# Title: Test Common Hardening
# Path: tests/test_common_hardening.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Unit tests for masking, logos, mentions, purge order, limits.
#   - 2026-07-17 | docshamxo | Reuse shared webhook_state fixture (avoid flaky repo state).
#   - 2026-07-17 | docshamxo | Expand logo-path and mentions regression coverage.
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


def test_console_print_falls_back_on_unicode_encode_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    writes: list[str] = []
    state = {"n": 0}

    def fake_print(message: str = "", *_a: object, **_k: object) -> None:
        state["n"] += 1
        if state["n"] == 1:
            raise UnicodeEncodeError("cp1252", str(message), 0, 1, "narrow")
        writes.append(str(message))

    class FakeStdout:
        encoding = "cp1252"

    monkeypatch.setattr(c.sys, "stdout", FakeStdout())
    monkeypatch.setattr("builtins.print", fake_print)
    c.console_print("skipped ✅ reactions")
    assert writes
    assert "\u2705" not in writes[0]  # replaced for cp1252


def test_mask_webhook_url_redacts_token() -> None:
    masked = c.mask_webhook_url("https://discord.com/api/webhooks/1234567890/super-secret-token")
    assert "1234567890" in masked
    assert "super-secret-token" not in masked
    assert masked.endswith("/***")


@pytest.mark.parametrize(
    "bad",
    [
        "../README.md",
        "..\\README.md",
        "/etc/passwd",
        "C:\\Windows\\System32\\cmd.exe",
        "subdir/DS.png",
        "subdir\\DS.png",
        "~/.ssh/id_rsa",
        ".",
        "..",
        "",
        "DS.png/../../../etc/passwd",
    ],
)
def test_confined_logo_path_rejects_traversal(bad: str) -> None:
    with pytest.raises(ValueError):
        c.confined_logo_path(bad)


def test_confined_logo_path_accepts_bare_filename() -> None:
    path = c.confined_logo_path("DS.png")
    assert path.name == "DS.png"
    assert path.parent.resolve() == c.LOGOS_DIR.resolve()


def test_logo_file_rejects_escape_via_path_object() -> None:
    with pytest.raises(ValueError):
        c.logo_file(Path("../README.md"))


def test_validate_embed_limits_detects_oversize_field() -> None:
    embed = discord.Embed(title="ok", description="ok", color=1)
    embed.add_field(name="n", value="x" * (c.EMBED_FIELD_VALUE_LIMIT + 1), inline=False)
    with pytest.raises(ValueError, match="field"):
        c.validate_embed_limits([embed])


def test_is_staff_placeholder() -> None:
    assert c.is_staff_placeholder("https://example.invalid/STAFF_LOCAL_REQUIRED")
    assert not c.is_staff_placeholder("https://docs.google.com/document/d/abc")


def test_send_webhook_sets_allowed_mentions_none_and_posts_before_delete(
    webhook_state: Path,
    empty_bot_token: None,
    fake_webhook_session: Any,
) -> None:
    webhook_state.write_text(json.dumps({"WEBHOOK_TEST": [111, 222]}), encoding="utf-8")

    events: list[str] = []
    posted = MagicMock()
    posted.id = 999
    posted.channel_id = 42

    class FakeWebhook:
        def send(self, **kwargs: Any) -> Any:
            events.append("send")
            assert kwargs.get("allowed_mentions") is not None
            mentions = kwargs["allowed_mentions"]
            assert isinstance(mentions, discord.AllowedMentions)
            assert mentions.everyone is False
            assert mentions.users is False
            assert mentions.roles is False
            assert kwargs.get("wait") is True
            return posted

        def delete_message(self, message_id: int) -> None:
            events.append(f"delete:{message_id}")

    with patch("discord.SyncWebhook.from_url") as from_url:
        from_url.return_value = FakeWebhook()
        ids = c.send_webhook(
            "https://discord.com/api/webhooks/1234567890/token",
            [discord.Embed(title="t", description="d", color=1)],
            username="Test Bot",
            state_key="WEBHOOK_TEST",
        )
        # Secret split: reaction bot token must not ride the webhook client.
        kwargs = from_url.call_args.kwargs
        assert not kwargs.get("bot_token")
        assert "bot_token" not in kwargs

    assert ids == [999]
    assert events[0] == "send"
    assert "delete:111" in events
    assert "delete:222" in events
    assert events.index("send") < min(events.index("delete:111"), events.index("delete:222"))

    saved = json.loads(webhook_state.read_text(encoding="utf-8"))
    assert saved["WEBHOOK_TEST"] == [999]


def test_send_webhook_file_factory_called(
    webhook_state: Path,
    empty_bot_token: None,
    fake_webhook_session: Any,
) -> None:
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

    with patch("discord.SyncWebhook.from_url", return_value=FakeWebhook()):
        factory_calls = {"n": 0}

        def factory() -> list[discord.File]:
            factory_calls["n"] += 1
            return [c.logo_file(c.LOGOS["ds"])]

        c.send_webhook(
            "https://discord.com/api/webhooks/1234567890/token",
            [discord.Embed(title="t", description="d", color=1)],
            username="Test Bot",
            files=factory,
        )
    assert factory_calls["n"] == 1


# === FILE FOOTER ===
# End of file: tests/test_common_hardening.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
