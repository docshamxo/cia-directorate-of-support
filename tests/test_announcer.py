# === FILE HEADER ===
# Title: Test Announcer
# Path: tests/test_announcer.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Dry-run, staff fail-closed, CoC username wrap.
#   - 2026-07-17 | docshamxo | Expect alerting SystemExit codes from run_announcer.
#   - 2026-09-28 | docshamxo | Cover optional discord_id profile links in Role.format.
#   - 2026-09-28 | docshamxo | Cover MESSAGE_ID edit-in-place path.
# === END FILE HEADER ===

"""Regression tests for shared announcer entry helpers."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import discord
import pytest

from common import announcer as a
from common import cia_common as c
from common.exit_codes import ANNOUNCER_CONFIG, ANNOUNCER_SKIPPED


def test_role_format_puts_holder_on_own_line() -> None:
    role = c.Role(abbrev="DDTE", title="Deputy Director of Training and Education", holder="Andy")
    text = role.format()
    assert "\n→ Andy" in text
    assert " - Andy" not in text


def test_role_format_links_holder_when_discord_id_set() -> None:
    role = c.Role(
        abbrev="S",
        title="Superintendent",
        holder="crazybijij2",
        discord_id="123456789012345678",
    )
    text = role.format()
    assert "[crazybijij2](https://discord.com/users/123456789012345678)" in text
    assert "VACANT" not in text


def test_role_format_skips_link_for_vacant() -> None:
    role = c.Role(abbrev="CM", title="Chief Marshal", holder="VACANT", discord_id="999")
    assert role.format().endswith("→ VACANT")


def test_roles_text_joins_with_newlines() -> None:
    roles = (
        c.Role("A", "Alpha", "one"),
        c.Role("B", "Beta", "two"),
    )
    text = c.roles_text(*roles)
    assert text.count("\n→ ") == 2


def test_is_dry_run_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CIA_DRY_RUN", raising=False)
    assert a.is_dry_run() is False
    monkeypatch.setenv("CIA_DRY_RUN", "1")
    assert a.is_dry_run() is True
    assert a.is_dry_run(dry_run=False) is True  # env wins


def test_run_announcer_dry_run_does_not_send(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CIA_DRY_RUN", "1")
    sent = {"n": 0}

    def boom(*_a: Any, **_k: Any) -> list[int]:
        sent["n"] += 1
        raise AssertionError("send_webhook must not run in dry-run")

    monkeypatch.setattr(c, "send_webhook", boom)
    a.run_announcer(
        webhook_key="WEBHOOK_DS_PUBLIC_INFORMATION",
        username="Test",
        build_embeds=lambda: [discord.Embed(title="t", description="d", color=1)],
        dry_run=True,
    )
    assert sent["n"] == 0


def test_staff_placeholders_fail_closed_on_live_send(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CIA_DRY_RUN", raising=False)
    monkeypatch.setenv(
        "WEBHOOK_OSEC_STAFF_DOCUMENTS",
        "https://discord.com/api/webhooks/1/tok",
    )
    monkeypatch.setattr(c, "validate_webhook_url", lambda _u: None)

    def build() -> list[discord.Embed]:
        return [
            discord.Embed(
                title="Staff",
                description="See https://example.invalid/STAFF_LOCAL_REQUIRED",
                color=1,
            )
        ]

    with pytest.raises(SystemExit) as excinfo:
        a.run_announcer(
            webhook_key="WEBHOOK_OSEC_STAFF_DOCUMENTS",
            username="OSEC",
            build_embeds=build,
            dry_run=False,
        )
    assert excinfo.value.code == ANNOUNCER_CONFIG


def test_staff_placeholders_warn_on_dry_run(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("CIA_DRY_RUN", "1")

    def build() -> list[discord.Embed]:
        return [
            discord.Embed(
                title="Staff",
                description=f"link {c.STAFF_PLACEHOLDER_MARKER}",
                color=1,
            )
        ]

    a.run_announcer(
        webhook_key="WEBHOOK_OSEC_STAFF_DOCUMENTS",
        username="OSEC",
        build_embeds=build,
        dry_run=True,
    )
    out = capsys.readouterr().out
    assert "Warning" in out or "placeholder" in out.lower()


def test_skip_empty_webhook(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CIA_DRY_RUN", raising=False)
    monkeypatch.delenv("WEBHOOK_DS_PUBLIC_INFORMATION", raising=False)
    monkeypatch.setenv("CIA_SKIP_EMPTY_WEBHOOKS", "1")
    called = MagicMock()
    monkeypatch.setattr(c, "send_webhook", called)
    with pytest.raises(SystemExit) as excinfo:
        a.run_announcer(
            webhook_key="WEBHOOK_DS_PUBLIC_INFORMATION",
            username="DS",
            build_embeds=lambda: [discord.Embed(title="t", description="d", color=1)],
            dry_run=False,
        )
    assert excinfo.value.code == ANNOUNCER_SKIPPED
    called.assert_not_called()


def test_resolve_edit_message_id(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("WEBHOOK_OSEC_OPEN_POSITIONS_MESSAGE_ID", raising=False)
    assert a.resolve_edit_message_id("WEBHOOK_OSEC_OPEN_POSITIONS") is None
    monkeypatch.setenv("WEBHOOK_OSEC_OPEN_POSITIONS_MESSAGE_ID", "1554285150685233232")
    assert a.resolve_edit_message_id("WEBHOOK_OSEC_OPEN_POSITIONS") == 1554285150685233232
    monkeypatch.setenv("WEBHOOK_OSEC_OPEN_POSITIONS_MESSAGE_ID", "not-a-snowflake")
    with pytest.raises(SystemExit) as excinfo:
        a.resolve_edit_message_id("WEBHOOK_OSEC_OPEN_POSITIONS")
    assert excinfo.value.code == ANNOUNCER_CONFIG


def test_edit_in_place_uses_message_id(monkeypatch: pytest.MonkeyPatch, capsys: Any) -> None:
    monkeypatch.delenv("CIA_DRY_RUN", raising=False)
    monkeypatch.setenv("WEBHOOK_OSEC_OPEN_POSITIONS", "https://discord.com/api/webhooks/1/token")
    monkeypatch.setenv("WEBHOOK_OSEC_OPEN_POSITIONS_MESSAGE_ID", "1554285150685233232")
    monkeypatch.setenv("CIA_ALLOW_SKIP_REACTION", "1")
    edited = MagicMock()
    send = MagicMock()
    monkeypatch.setattr(c, "edit_webhook_message", edited)
    monkeypatch.setattr(c, "send_webhook", send)
    a.run_announcer(
        webhook_key="WEBHOOK_OSEC_OPEN_POSITIONS",
        username="OSEC",
        build_embeds=lambda: [discord.Embed(title="t", description="d", color=1)],
        dry_run=False,
    )
    edited.assert_called_once()
    assert edited.call_args.kwargs["message_id"] == 1554285150685233232
    send.assert_not_called()
    assert "1554285150685233232" in capsys.readouterr().out


def test_missing_webhook_raises_without_skip(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CIA_DRY_RUN", raising=False)
    monkeypatch.delenv("WEBHOOK_DS_PUBLIC_INFORMATION", raising=False)
    monkeypatch.delenv("CIA_SKIP_EMPTY_WEBHOOKS", raising=False)
    with pytest.raises(SystemExit) as excinfo:
        a.run_announcer(
            webhook_key="WEBHOOK_DS_PUBLIC_INFORMATION",
            username="DS",
            build_embeds=lambda: [discord.Embed(title="t", description="d", color=1)],
            dry_run=False,
        )
    assert excinfo.value.code == ANNOUNCER_CONFIG


def test_run_announcer_passes_state_key_and_file_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CIA_DRY_RUN", raising=False)
    monkeypatch.setenv(
        "WEBHOOK_DS_PUBLIC_INFORMATION",
        "https://discord.com/api/webhooks/1/tok",
    )
    monkeypatch.setattr(c, "validate_webhook_url", lambda _u: None)
    captured: dict[str, Any] = {}

    def fake_send(url: str, embeds: list[discord.Embed], **kwargs: Any) -> list[int]:
        captured["url"] = url
        captured["kwargs"] = kwargs
        if callable(kwargs.get("files")):
            captured["files"] = kwargs["files"]()
        return [1]

    monkeypatch.setattr(c, "send_webhook", fake_send)
    a.run_announcer(
        webhook_key="WEBHOOK_DS_PUBLIC_INFORMATION",
        username="DS",
        build_embeds=lambda: [discord.Embed(title="t", description="d", color=1)],
        files=lambda: [],
        dry_run=False,
    )
    assert captured["kwargs"]["state_key"] == "WEBHOOK_DS_PUBLIC_INFORMATION"
    assert captured["files"] == []


# === FILE FOOTER ===
# End of file: tests/test_announcer.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
