# === FILE HEADER ===
# Title: Test Accessibility
# Path: tests/test_accessibility.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Unit tests for marking notes, command bands, emoji-only guard.
# === END FILE HEADER ===

"""Accessibility helpers for Discord embeds."""

from __future__ import annotations

import discord
import pytest

from common import cia_common as c


def test_command_band_label_expands_known_bands() -> None:
    assert c.command_band_label("lowcom") == "Lower Command (LOWCOM)"
    assert c.command_band_label("MIDCOM") == "Middle Command (MIDCOM)"
    assert c.command_band_label("HIGHCOM") == "High Command (HIGHCOM)"


def test_marking_note_is_text_not_color() -> None:
    assert c.marking_note("public") == "Marking: PUBLIC."
    assert "STAFF" in c.marking_note("STAFF", "Authorized OSEC staff only.")
    assert "Authorized OSEC staff only." in c.marking_note("STAFF", "Authorized OSEC staff only.")


def test_has_text_signal_rejects_emoji_only() -> None:
    assert c.has_text_signal("Lower Command (LOWCOM)")
    assert c.has_text_signal("✅ Approved")
    assert not c.has_text_signal("✅")
    assert not c.has_text_signal("⚠️🚨")


def test_validate_embed_accessibility_rejects_emoji_only_field_name() -> None:
    embed = discord.Embed(title="Open Positions", description="Apply below.", color=1)
    embed.add_field(name="✅", value="Ready", inline=False)
    with pytest.raises(ValueError, match="emoji/symbol-only"):
        c.validate_embed_accessibility([embed])


def test_validate_embed_limits_includes_accessibility() -> None:
    embed = discord.Embed(title="⚠️", description="x", color=1)
    with pytest.raises(ValueError, match="accessibility"):
        c.validate_embed_limits([embed])


# === FILE FOOTER ===
# End of file: tests/test_accessibility.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
