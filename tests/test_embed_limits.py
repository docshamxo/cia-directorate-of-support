# === FILE HEADER ===
# Title: Test Embed Limits
# Path: tests/test_embed_limits.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Cover Discord embed preflight limits end-to-end.
# === END FILE HEADER ===

"""Regression tests for Discord embed preflight validation."""

from __future__ import annotations

import discord
import pytest

from common import cia_common as c
from common.announcer import subunit_coc_embeds
from common.manifest import ANNOUNCERS


def test_validate_embed_limits_accepts_valid() -> None:
    embeds = [
        discord.Embed(title="ok", description="short", color=1),
        discord.Embed(title="ok2", description="also short", color=1),
    ]
    embeds[0].add_field(name="n", value="v", inline=False)
    c.validate_embed_limits(embeds)


def test_validate_embed_limits_too_many_embeds() -> None:
    embeds = [
        discord.Embed(title=f"t{i}", description="d", color=1)
        for i in range(c.EMBEDS_PER_MESSAGE_LIMIT + 1)
    ]
    with pytest.raises(ValueError, match="at most"):
        c.validate_embed_limits(embeds)


def test_validate_embed_limits_title() -> None:
    embed = discord.Embed(title="x" * (c.EMBED_TITLE_LIMIT + 1), description="d", color=1)
    with pytest.raises(ValueError, match="title"):
        c.validate_embed_limits([embed])


def test_validate_embed_limits_description() -> None:
    embed = discord.Embed(title="t", description="x" * (c.EMBED_DESCRIPTION_LIMIT + 1), color=1)
    with pytest.raises(ValueError, match="description"):
        c.validate_embed_limits([embed])


def test_validate_embed_limits_footer() -> None:
    embed = discord.Embed(title="t", description="d", color=1)
    embed.set_footer(text="x" * (c.EMBED_FOOTER_LIMIT + 1))
    with pytest.raises(ValueError, match="footer"):
        c.validate_embed_limits([embed])


def test_validate_embed_limits_field_name() -> None:
    embed = discord.Embed(title="t", description="d", color=1)
    embed.add_field(
        name="x" * (c.EMBED_FIELD_NAME_LIMIT + 1),
        value="v",
        inline=False,
    )
    with pytest.raises(ValueError, match="field .* name"):
        c.validate_embed_limits([embed])


def test_validate_embed_limits_field_value() -> None:
    embed = discord.Embed(title="t", description="d", color=1)
    embed.add_field(
        name="n",
        value="x" * (c.EMBED_FIELD_VALUE_LIMIT + 1),
        inline=False,
    )
    with pytest.raises(ValueError, match="field .* value"):
        c.validate_embed_limits([embed])


def test_server_regulations_embeds_within_limits() -> None:
    embeds = c.server_regulations_embeds()
    c.validate_embed_limits(embeds)
    assert len(embeds) <= c.EMBEDS_PER_MESSAGE_LIMIT


def test_subunit_coc_embeds_within_limits() -> None:
    embeds = subunit_coc_embeds(
        unit_full="Global Response Staff",
        unit_abbrev="GRS",
        color=c.COLOR_GRS,
        about=c.GRS_ABOUT,
        command_roles=c.GRS_COMMAND,
        logo=c.LOGOS["grs"],
    )
    c.validate_embed_limits(embeds)


def test_apply_effective_date_footer_stamps_last() -> None:
    embeds = [
        discord.Embed(title="a", description="d", color=1),
        discord.Embed(title="b", description="d", color=1),
    ]
    c.apply_effective_date_footer(embeds)
    assert embeds[0].footer.text is None or embeds[0].footer.text == ""
    assert embeds[-1].footer and "Effective" in (embeds[-1].footer.text or "")
    assert "community roleplay" in (embeds[-1].footer.text or "")


def test_announcer_catalog_nonempty() -> None:
    assert len(ANNOUNCERS) >= 18
    keys = [item[2] for item in ANNOUNCERS]
    assert len(keys) == len(set(keys))


# === FILE FOOTER ===
# End of file: tests/test_embed_limits.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
