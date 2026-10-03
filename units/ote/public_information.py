# === FILE HEADER ===
# Title: Public Information
# Path: units/ote/public_information.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-10-03 | docshamxo | OIG Levels closer + community/document link buttons.
# === END FILE HEADER ===

"""CIA OTE public information announcer."""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import (
    info_about_embed,
    info_community_link_view,
    info_community_links_embed,
    info_hero_embed,
    run_announcer,
)

_UNIT = "Office of Training & Education"
_ABBREV = "OTE"
_COLOR = c.COLOR_OTE


def _build_embeds() -> list[c.discord.Embed]:
    ote_pillars = tuple(c.pillar_field(title, desc) for title, desc in c.OTE_PILLARS)
    embeds = [
        info_hero_embed(
            unit_full=_UNIT,
            unit_abbrev=_ABBREV,
            color=_COLOR,
            logo=c.LOGOS["ote"],
        ),
        info_about_embed(
            unit_full=_UNIT,
            unit_abbrev=_ABBREV,
            about=c.OTE_ABOUT,
            motto=c.OTE_MOTTO,
            color=_COLOR,
            fields=ote_pillars,
        ),
        info_community_links_embed(
            unit_abbrev=_ABBREV,
            color=_COLOR,
            description=(
                "Official documents and Roblox groups for the Office of Training & Education "
                "and its parent Directorate of Support. Use the buttons below."
            ),
            fields=(),
        ),
    ]
    return c.append_classification_block(
        embeds, c.classification_label("level_1"), color=_COLOR
    )


def _build_view() -> c.discord.ui.View:
    return info_community_link_view(
        [
            (
                "📄 Program Overview",
                c.url("ote.public_information.program_overview"),
                0,
            ),
            ("🎮 OTE Roblox", c.URL_ROBLOX_GROUP_OTE, 1),
            ("🎮 DS Roblox", c.URL_ROBLOX_GROUP_DS, 1),
        ]
    )


def send_ote_public_information() -> None:
    run_announcer(
        webhook_key="WEBHOOK_OTE_PUBLIC_INFORMATION",
        username=c.BOT_OTE,
        build_embeds=_build_embeds,
        build_view=_build_view,
        files=[c.logo_file(c.LOGOS["ote"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_ote_public_information()

# === FILE FOOTER ===
# End of file: units/ote/public_information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
