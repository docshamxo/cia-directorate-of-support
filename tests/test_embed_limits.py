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

from datetime import date

import discord
import pytest

from common import cia_common as c
from common.announcer import subunit_coc_embeds
from common.manifest import ANNOUNCERS
from units.esd import information as esd_info
from units.esd import staff_documents as esd_staff
from units.grs import information as grs_info
from units.grs import staff_documents as grs_staff
from units.osec import information as osec_info
from units.osec import staff_documents as osec_staff
from units.ote import public_information as ote_info
from units.ote import staff_documents as ote_staff


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
    assert embeds[0].title == "DIRECTORATE OF SUPPORT"
    blob = "\n".join(e.description or "" for e in embeds)
    assert "Office of Security" in blob
    assert "Community Server Regulations" in blob
    assert "Unofficial Roblox Roleplay Community" in blob
    assert "Office of Training & Education" not in blob
    # Mid-sentence soft wraps must not appear as Discord hard breaks.
    assert "based on race,\n" not in blob
    assert "without Office of Security leadership\n" not in blob
    policy = next(e for e in embeds if e.title == "Governing Policies")
    field_names = [f.name for f in policy.fields]
    assert "Discord Terms of Service" in field_names
    assert "Roblox Terms of Use" in field_names
    assert "Code of Agency Conduct" in field_names
    assert "discord.com/terms" in (policy.fields[0].value or "")
    assert "roblox.com/info/terms" in "\n".join(f.value for f in policy.fields)


def test_ote_server_regulations_embeds_use_ote_office() -> None:
    embeds = c.server_regulations_embeds(
        office="Office of Training & Education",
        motto=c.OTE_MOTTO,
        logo=c.LOGOS["ote"],
        color=c.COLOR_OTE,
    )
    c.validate_embed_limits(embeds)
    assert embeds[0].title == "DIRECTORATE OF SUPPORT"
    blob = "\n".join(e.description or "" for e in embeds)
    assert "Office of Training & Education" in blob
    assert "Community Server Regulations" in blob
    assert "Office of Security" not in blob
    assert c.OTE_MOTTO in blob
    assert "based on race,\n" not in blob
    assert "without Office of Training & Education leadership\n" not in blob
    assert blob.lower().count("unofficial") == 1
    assert "Unofficial Roblox Roleplay Community" in blob


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
    titles = [e.title for e in embeds]
    assert titles[0] == "CHAIN OF COMMAND"
    assert "Agency Executive Leadership" not in titles
    assert "Directorate of Support" not in titles
    assert "Global Response Staff" in titles
    assert "Reporting Line" not in titles
    assert any(f.name == "Command Team" for e in embeds for f in e.fields)
    assert all(f.name != "Executive Leadership" for e in embeds for f in e.fields)
    assert all(f.name != "Leadership" for e in embeds for f in e.fields)
    thumbs = [e.thumbnail.url for e in embeds if e.thumbnail and e.thumbnail.url]
    assert len(thumbs) == 1
    assert thumbs[0].startswith("attachment://")


def test_apply_effective_date_footer_stamps_last() -> None:
    embeds = [
        discord.Embed(title="a", description="d", color=1),
        discord.Embed(title="b", description="d", color=1),
    ]
    c.apply_effective_date_footer(embeds)
    assert embeds[0].footer.text is None or embeds[0].footer.text == ""
    assert embeds[-1].footer and "Effective" in (embeds[-1].footer.text or "")
    assert "(community)" not in (embeds[-1].footer.text or "")
    assert "Inter Studios" in (embeds[-1].footer.text or "")
    assert "roleplay" not in (embeds[-1].footer.text or "").lower()


def test_disclaimer_does_not_duplicate_property_notice() -> None:
    text = c.disclaimer_embed(color=c.COLOR_DS).description or ""
    assert "not affiliated" in text.lower()
    assert "Inter Studios" not in text
    assert "Property of the Central Intelligence Agency" not in text


def test_format_display_date_uses_ordinal() -> None:
    assert c.format_display_date(date(2026, 8, 30)) == "August 30th, 2026"
    assert c.format_display_date(date(2026, 6, 1)) == "June 1st, 2026"
    assert c.format_display_date(date(2026, 6, 2)) == "June 2nd, 2026"
    assert c.format_display_date(date(2026, 6, 3)) == "June 3rd, 2026"
    assert c.format_display_date(date(2026, 6, 11)) == "June 11th, 2026"
    assert c.format_display_date(date(2026, 6, 21)) == "June 21st, 2026"


def test_last_updated_line_is_italic() -> None:
    line = c.last_updated_line(date(2026, 8, 30))
    assert line == "*Last updated: August 30th, 2026*"


def test_announcer_catalog_nonempty() -> None:
    assert len(ANNOUNCERS) >= 18
    keys = [item[2] for item in ANNOUNCERS]
    assert len(keys) == len(set(keys))


@pytest.mark.parametrize(
    ("builder", "abbrev", "unit_full"),
    [
        (osec_staff._build_embeds, "OSEC", "Office of Security"),
        (ote_staff._build_embeds, "OTE", "Office of Training & Education"),
        (grs_staff._build_embeds, "GRS", "Global Response Staff"),
        (esd_staff._build_embeds, "ESD", "Executive Security Detail"),
    ],
)
def test_staff_documents_share_standard_frame(builder, abbrev: str, unit_full: str) -> None:
    embeds = builder()
    c.validate_embed_limits(embeds)
    assert embeds[0].title == "STAFF DOCUMENTS"
    assert (
        f"Authorized {abbrev} staff documentation index. Need-to-know access only."
        in (embeds[0].description or "")
    )
    assert embeds[1].title == "Central Repository"
    assert embeds[-1].title == "Classification & Handling Notice"
    assert unit_full in (embeds[-1].description or "")
    assert f"CIA {unit_full}" in (embeds[-1].description or "")
    blob = "\n".join(
        [
            *(e.description or "" for e in embeds),
            *(f.value for e in embeds for f in e.fields),
        ]
    )
    assert "CIA OTE |" not in blob
    assert "CIA DS |" in blob


def test_information_channels_share_standard_frame() -> None:
    osec = osec_info._build_embeds()
    ote = ote_info._build_embeds()
    grs = grs_info._build_embeds()
    esd = esd_info._build_embeds()
    for embeds in (osec, ote, grs, esd):
        c.validate_embed_limits(embeds)

    assert osec[0].title == "INFORMATION"
    assert "Reference hub for OSEC records" in (osec[0].description or "")
    assert osec[1].title == "About the Office"
    assert osec[2].title == "Reference Documents"

    for embeds, abbrev in ((ote, "OTE"), (grs, "GRS"), (esd, "ESD")):
        assert embeds[0].title == "PUBLIC INFORMATION"
        assert (
            f"Public overview of {abbrev}, its mission, and official community resources."
            in (embeds[0].description or "")
        )
        assert embeds[-1].title == "Community Links"

    assert grs[1].title == "About GRS"
    assert esd[1].title == "About ESD"
    assert ote[1].title == "About the Office"
    assert grs[2].title == "Tryout Requirements"
    assert esd[2].title == "Tryout Requirements"


# === FILE FOOTER ===
# End of file: tests/test_embed_limits.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
