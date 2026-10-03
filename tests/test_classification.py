# === FILE HEADER ===
# Title: Test Classification
# Path: tests/test_classification.py
# Created: 2026-10-03
# Created by: docshamxo
# Modified:
#   - 2026-10-03 | docshamxo | OIG Levels + link_view regressions.
# === END FILE HEADER ===

"""OIG-aligned classification Levels and link-button helpers."""

from __future__ import annotations

from common import cia_common as c
from common.announcer import subunit_coc_embeds


def test_classification_label_and_block() -> None:
    assert "LEVEL 1" in c.classification_label("level_1")
    assert "LEVEL 2" in c.classification_label("level_2")
    embeds = c.append_classification_block([], c.classification_label("level_1"))
    assert len(embeds) == 1
    assert embeds[0].title == "Classification"
    assert "LEVEL 1" in (embeds[0].description or "")


def test_legacy_marking_aliases_map_to_levels() -> None:
    assert c.resolve_level_short("PUBLIC") == "LEVEL 1"
    assert c.resolve_level_short("STAFF") == "LEVEL 2"
    assert c.resolve_level_short("CANDIDATE") == "LEVEL 1"
    assert c.resolve_level_short("OSEC PERSONNEL") == "LEVEL 2"


def test_motto_line_omits_inline_classification() -> None:
    assert c.motto_line("WE GO AS ONE", classification="LEVEL 1") == "*WE GO AS ONE*"


def test_grs_coc_open_and_level_1() -> None:
    embeds = subunit_coc_embeds(
        unit_full="Global Response Staff",
        unit_abbrev="GRS",
        color=c.COLOR_GRS,
        about=c.GRS_ABOUT,
        command_roles=c.GRS_COMMAND,
        logo=c.LOGOS["grs"],
    )
    blob = "\n".join((e.description or "") for e in embeds)
    assert "open" in blob.lower()
    assert "not yet open" not in blob.lower()
    assert embeds[-1].title == "Classification"
    assert "LEVEL 1" in (embeds[-1].description or "")


def test_link_view_builds_buttons() -> None:
    view = c.link_view(
        [
            ("Discord Terms", c.url("community.discord_tos"), 0),
            ("Roblox Terms", c.url("community.roblox_tos"), 0),
        ]
    )
    assert len(view.children) == 2


def test_invictus_studio_branding() -> None:
    assert c.STUDIO == "Invictus Studios"
    assert "Invictus Studios" in c.PROPERTY_NOTICE
    assert "Inter Studios" not in c.PROPERTY_NOTICE


# === FILE FOOTER ===
# End of file: tests/test_classification.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
