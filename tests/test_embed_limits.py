# === FILE HEADER ===
# Title: Test Embed Limits
# Path: tests/test_embed_limits.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Cover Discord embed preflight limits end-to-end.
#   - 2026-09-28 | docshamxo | Cover GRS/ESD MIDCOM open-positions embeds.
#   - 2026-09-28 | docshamxo | Load open_positions via importlib (units are scripts).
#   - 2026-10-03 | docshamxo | Expect VACANT for vacated GRS CM/DCM in open-positions embeds.
#   - 2026-10-03 | docshamxo | Expect VACANT for vacated OSEC ADS / ESD CM in open-positions embeds.
#   - 2026-10-05 | docshamxo | Expect DCDSD/DS/DDS rotation (Andy gone; DDS vacant).
# === END FILE HEADER ===

"""Regression tests for Discord embed preflight validation."""

from __future__ import annotations

import importlib.util
from datetime import date
from pathlib import Path

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

_ROOT = Path(__file__).resolve().parents[1]


def _load_unit_module(relative_path: str, module_name: str):
    """Load a units/*.py announcer by path (units/ is not a Python package)."""
    path = _ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    assert "bound by the policies linked below" in (policy.description or "")
    assert embeds[-1].title == "Classification"
    assert "LEVEL 1" in (embeds[-1].description or "")
    view = c.rules_policy_view()
    labels = [child.label for child in view.children]
    assert any("Discord Terms" in (label or "") for label in labels)
    assert any("Roblox Terms" in (label or "") for label in labels)
    assert any("Code of Agency Conduct" in (label or "") for label in labels)


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
    # Property notice is docs/config only (OIG-aligned), not Discord footers.
    assert "Invictus Studios" not in (embeds[-1].footer.text or "")
    assert "Inter Studios" not in (embeds[-1].footer.text or "")
    assert "roleplay" not in (embeds[-1].footer.text or "").lower()


def test_disclaimer_does_not_duplicate_property_notice() -> None:
    text = c.disclaimer_embed(color=c.COLOR_DS).description or ""
    assert "not affiliated" in text.lower()
    assert "Invictus Studios" not in text
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
    assert len(ANNOUNCERS) >= 20
    keys = [item[2] for item in ANNOUNCERS]
    assert len(keys) == len(set(keys))
    assert "WEBHOOK_GRS_OPEN_POSITIONS" in keys
    assert "WEBHOOK_ESD_OPEN_POSITIONS" in keys


def test_ds_coc_reflects_dcdsd_and_osec_hc_rotation() -> None:
    ds_coc = _load_unit_module("units/ds/chain_of_command.py", "ds_chain_of_command")
    embeds = ds_coc._build_embeds()
    c.validate_embed_limits(embeds)
    blob = "\n".join(
        [(e.description or "") + "\n".join(f.value for f in e.fields) for e in embeds]
    )
    assert "AndyShotSecond" not in blob
    assert "rattler_29" in blob
    assert "Shaikhuu" in blob
    assert "VACANT" in blob
    # rattler is DCDSD only; DS slot is Shaikhuu.
    assert blob.count("rattler_29") == 1
    assert blob.count("Shaikhuu") == 1


def test_grs_esd_open_positions_embeds_within_limits(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "GRS_MIDCOM_APPLICATION_URL",
        "https://example.invalid/grs-midcom-app",
    )
    monkeypatch.setenv(
        "ESD_MIDCOM_APPLICATION_URL",
        "https://example.invalid/esd-midcom-app",
    )
    grs_open = _load_unit_module("units/grs/open_positions.py", "grs_open_positions")
    esd_open = _load_unit_module("units/esd/open_positions.py", "esd_open_positions")

    grs = grs_open._build_embeds()
    esd = esd_open._build_embeds()
    c.validate_embed_limits(grs)
    c.validate_embed_limits(esd)
    grs_blob = "\n".join(
        [(e.description or "") + "\n".join(f.value for f in e.fields) for e in grs]
    )
    esd_blob = "\n".join(
        [(e.description or "") + "\n".join(f.value for f in e.fields) for e in esd]
    )
    assert "MIDCOM" in grs_blob
    assert "example.invalid/grs-midcom-app" in grs_blob
    assert "VACANT" in grs_blob
    assert "qv4_pendragon" not in grs_blob
    assert "idk_manti" not in grs_blob
    assert "MIDCOM" in esd_blob
    assert "example.invalid/esd-midcom-app" in esd_blob
    assert "VACANT" in esd_blob
    assert "xBlq_h" not in esd_blob
    assert "jayheart592010" in esd_blob
    assert "SSA+" in esd_blob
    assert "2 weeks" in esd_blob
    assert "exempted for 1 week" in grs_blob
    assert "instant denial" in grs_blob
    assert "instant denial" in esd_blob
    assert "@" not in grs_blob  # no inventing Discord pings
    assert "<@" not in grs_blob


def test_osec_open_positions_includes_grs_esd_midcom(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "OSEC_LOWCOM_APPLICATION_URL",
        "https://example.invalid/osec-lowcom-app",
    )
    monkeypatch.setenv(
        "OSEC_MIDCOM_APPLICATION_URL",
        "https://example.invalid/osec-midcom-app",
    )
    monkeypatch.setenv(
        "GRS_MIDCOM_APPLICATION_URL",
        "https://example.invalid/grs-midcom-app",
    )
    monkeypatch.setenv(
        "ESD_MIDCOM_APPLICATION_URL",
        "https://example.invalid/esd-midcom-app",
    )
    monkeypatch.setenv(
        "DISCORD_OSEC_APPLICATION_RESULTS_URL",
        "https://example.invalid/osec-results",
    )
    osec_open = _load_unit_module("units/osec/open_positions.py", "osec_open_positions")
    embeds = osec_open._build_embeds()
    c.validate_embed_limits(embeds)
    blob = "\n".join([(e.description or "") + "\n".join(f.value for f in e.fields) for e in embeds])
    titles = [e.title or "" for e in embeds]
    assert "GRS MIDCOM (OPEN)" in titles
    assert "ESD MIDCOM (OPEN)" in titles
    assert "example.invalid/osec-lowcom-app" in blob
    assert "example.invalid/osec-midcom-app" in blob
    assert "example.invalid/grs-midcom-app" in blob
    assert "example.invalid/esd-midcom-app" in blob
    assert "VACANT" in blob
    assert "qv4_pendragon" not in blob
    assert "idk_manti" not in blob
    assert "crazybijij2" not in blob
    assert "xBlq_h" not in blob
    assert "AndyShotSecond" not in blob
    assert "Shaikhuu" in blob
    assert "rattler_29" not in blob
    assert "Astroshard21" in blob
    assert "exempted for 1 week" in blob
    assert "SSA+" in blob
    assert "instant denial" in blob
    assert "<@" not in blob
    assert "@everyone" not in blob
    assert "@here" not in blob


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
    assert f"Authorized {abbrev} staff documentation index. Need-to-know access only." in (
        embeds[0].description or ""
    )
    assert embeds[1].title == "Central Repository"
    assert embeds[-1].title == "Classification"
    assert "LEVEL 2" in (embeds[-1].description or "")
    blob = "\n".join(
        [
            *(e.description or "" for e in embeds),
            *(f.value for e in embeds for f in e.fields),
        ]
    )
    assert "CIA OTE |" not in blob
    assert "CIA DS |" in blob or "buttons below" in blob.lower()
    _ = unit_full  # retained for parametrize readability


def test_information_channels_share_standard_frame() -> None:
    osec = osec_info._build_embeds()
    ote = ote_info._build_embeds()
    grs = grs_info._build_embeds()
    esd = esd_info._build_embeds()
    for embeds in (osec, ote, grs, esd):
        c.validate_embed_limits(embeds)
        assert embeds[-1].title == "Classification"

    assert osec[0].title == "INFORMATION"
    assert "Reference hub for OSEC records" in (osec[0].description or "")
    assert osec[1].title == "About the Office"
    assert osec[2].title == "Reference Documents"
    assert "LEVEL 2" in (osec[-1].description or "")

    for embeds, abbrev in ((ote, "OTE"), (grs, "GRS"), (esd, "ESD")):
        assert embeds[0].title == "PUBLIC INFORMATION"
        assert abbrev in (embeds[0].description or "")
        assert "LEVEL 1" in (embeds[-1].description or "")
        assert any((e.title or "") == "Community Links" for e in embeds)

    assert grs[1].title == "About GRS"
    assert esd[1].title == "About ESD"
    assert ote[1].title == "About the Office"
    assert grs[2].title == "Tryout Requirements"
    assert esd[2].title == "Tryout Requirements"
    assert "open" in (grs[2].description or "").lower()
    assert "open" in (esd[2].description or "").lower()
    assert "not yet open" not in (grs[2].description or "").lower()


# === FILE FOOTER ===
# End of file: tests/test_embed_limits.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
