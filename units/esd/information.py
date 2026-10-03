# === FILE HEADER ===
# Title: Information
# Path: units/esd/information.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-10-03 | docshamxo | OIG Levels + community link buttons; ESD open framing.
# === END FILE HEADER ===

"""CIA ESD public information announcer."""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import (
    info_about_embed,
    info_community_link_view,
    info_community_links_embed,
    info_hero_embed,
    info_tryout_requirements_embed,
    run_announcer,
)

_UNIT = "Executive Security Detail"
_ABBREV = "ESD"
_COLOR = c.COLOR_ESD


def _build_embeds() -> list[c.discord.Embed]:
    embeds = [
        info_hero_embed(
            unit_full=_UNIT,
            unit_abbrev=_ABBREV,
            color=_COLOR,
            logo=c.LOGOS["esd"],
            supporting=(
                f"Public overview of {_ABBREV}. The unit is **open** for qualified "
                "applicants — mission, tryout requirements, and community resources."
            ),
        ),
        info_about_embed(
            unit_full=_UNIT,
            unit_abbrev=_ABBREV,
            about=c.ESD_ABOUT,
            color=_COLOR,
            subunit_parent="Office of Security",
        ),
        info_tryout_requirements_embed(
            unit_abbrev=_ABBREV,
            combat_requirement=c.ESD_TRYOUT_COMBAT,
            color=_COLOR,
        ),
        info_community_links_embed(
            unit_abbrev=_ABBREV,
            color=_COLOR,
            description=(
                f"Official Roblox communities for {_ABBREV} and related Agency services. "
                "Use the buttons below."
            ),
            fields=(),
        ),
    ]
    return c.append_classification_block(embeds, c.classification_label("level_1"), color=_COLOR)


def _build_view() -> c.discord.ui.View:
    return info_community_link_view(
        [
            ("🎮 ESD Roblox", c.URL_ROBLOX_GROUP_ESD, 0),
            ("🎮 OSEC Roblox", c.URL_ROBLOX_GROUP_OSEC, 0),
            ("🎮 DS Roblox", c.URL_ROBLOX_GROUP_DS, 0),
        ]
    )


def send_esd_information() -> None:
    run_announcer(
        webhook_key="WEBHOOK_ESD_INFORMATION",
        username=c.BOT_ESD,
        build_embeds=_build_embeds,
        build_view=_build_view,
        files=[c.logo_file(c.LOGOS["esd"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_esd_information()

# === FILE FOOTER ===
# End of file: units/esd/information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
