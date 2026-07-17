# === FILE HEADER ===
# Title: Test Webhook Reactions
# Path: tests/test_webhook_reactions.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Regression: ✅ via bot token; require_reaction fail-closed.
# === END FILE HEADER ===

"""Regression tests for checkmark reactions (bot HTTP path, not webhook auth)."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch
from urllib.parse import quote

import discord
import pytest
import requests

from common import cia_common as c

WEBHOOK = "https://discord.com/api/webhooks/1234567890/react-token"


def _posted(message_id: int = 77, channel_id: int = 88) -> SimpleNamespace:
    return SimpleNamespace(id=message_id, channel_id=channel_id)


class SilentWebhook:
    def send(self, **kwargs: Any) -> Any:
        return _posted()

    def delete_message(self, message_id: int) -> None:
        return None


def test_checkmark_reaction_constant() -> None:
    assert c.CHECKMARK_REACTION == "\u2705"


def test_message_channel_id_prefers_channel_id() -> None:
    assert c._message_channel_id(_posted(1, 99)) == 99


def test_message_channel_id_from_channel_object() -> None:
    msg = SimpleNamespace(id=1, channel=SimpleNamespace(id=4242))
    assert c._message_channel_id(msg) == 4242


def test_message_channel_id_missing_returns_none() -> None:
    assert c._message_channel_id(SimpleNamespace(id=1)) is None


def test_add_checkmark_reaction_puts_encoded_emoji(no_sleep: None) -> None:
    session = MagicMock()
    response = MagicMock()
    response.status_code = 204
    session.put.return_value = response

    c._add_checkmark_reaction(session, bot_token="bot-secret", channel_id=10, message_id=20)

    url = session.put.call_args.args[0]
    headers = session.put.call_args.kwargs["headers"]
    assert quote(c.CHECKMARK_REACTION, safe="") in url
    assert "/channels/10/messages/20/reactions/" in url
    assert headers["Authorization"] == "Bot bot-secret"


def test_add_checkmark_reaction_retries_429_then_ok(no_sleep: None) -> None:
    session = MagicMock()
    limited = MagicMock()
    limited.status_code = 429
    limited.json.return_value = {"retry_after": 0.01}
    ok = MagicMock()
    ok.status_code = 204
    session.put.side_effect = [limited, ok]

    c._add_checkmark_reaction(session, bot_token="tok", channel_id=1, message_id=2)
    assert session.put.call_count == 2


def test_react_skips_without_token(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(c, "_bot_token", lambda: "")
    session = MagicMock()
    c._react_to_messages(session, [_posted()], require_reaction=False)
    session.put.assert_not_called()
    assert "DISCORD_BOT_TOKEN" in capsys.readouterr().out


def test_react_require_reaction_without_token_raises(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(c, "_bot_token", lambda: "")
    with pytest.raises(RuntimeError, match=c.BOT_TOKEN_ENV):
        c._react_to_messages(MagicMock(), [_posted()], require_reaction=True)


def test_send_webhook_never_passes_bot_token_to_sync_webhook(
    webhook_state: Any,
    fake_webhook_session: Any,
    no_sleep: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(c.BOT_TOKEN_ENV, "live-bot-token")
    put_ok = MagicMock()
    put_ok.status_code = 204
    fake_webhook_session.put.return_value = put_ok

    with patch("discord.SyncWebhook.from_url") as from_url:
        from_url.return_value = SilentWebhook()
        c.send_webhook(
            WEBHOOK,
            [discord.Embed(title="t", description="d", color=1)],
            username="Test Bot",
            state_key="WEBHOOK_REACT",
            require_reaction=True,
        )
        kwargs = from_url.call_args.kwargs
        assert not kwargs.get("bot_token")

    assert fake_webhook_session.put.called
    auth = fake_webhook_session.put.call_args.kwargs["headers"]["Authorization"]
    assert auth == "Bot live-bot-token"


def test_send_webhook_require_reaction_fails_closed_without_token(
    webhook_state: Any,
    empty_bot_token: None,
    fake_webhook_session: Any,
) -> None:
    with patch("discord.SyncWebhook.from_url", return_value=SilentWebhook()):
        with pytest.raises(RuntimeError, match=c.BOT_TOKEN_ENV):
            c.send_webhook(
                WEBHOOK,
                [discord.Embed(title="t", description="d", color=1)],
                username="Test Bot",
                state_key="WEBHOOK_REACT",
                require_reaction=True,
            )


def test_react_require_reaction_missing_channel_id_raises(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(c, "_bot_token", lambda: "tok")
    with pytest.raises(RuntimeError, match="Required"):
        c._react_to_messages(
            MagicMock(),
            [SimpleNamespace(id=5)],
            require_reaction=True,
        )


def test_add_checkmark_network_error_retries(no_sleep: None) -> None:
    session = MagicMock()
    session.put.side_effect = [
        requests.ConnectionError("boom"),
        MagicMock(status_code=204),
    ]
    c._add_checkmark_reaction(session, bot_token="t", channel_id=1, message_id=2)
    assert session.put.call_count == 2


# === FILE FOOTER ===
# End of file: tests/test_webhook_reactions.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
