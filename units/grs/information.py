# === FILE HEADER ===
# Title: Information
# Path: units/grs/information.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-10-03 | docshamxo | OIG Levels + community link buttons; GRS open framing.
# === END FILE HEADER ===

"""CIA GRS public information announcer."""

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

_UNIT = "Global Response Staff"
_ABBREV = "GRS"
_COLOR = c.COLOR_GRS


def _build_embeds() -> list[c.discord.Embed]:
    embeds = [
        info_hero_embed(
            unit_full=_UNIT,
            unit_abbrev=_ABBREV,
            color=_COLOR,
            logo=c.LOGOS["grs"],
            supporting=(
                f"Public overview of {_ABBREV}. The unit is **open** for qualified "
                "applicants — mission, tryout requirements, and community resources."
            ),
        ),
        info_about_embed(
            unit_full=_UNIT,
            unit_abbrev=_ABBREV,
            about=c.GRS_ABOUT,
            color=_COLOR,
            subunit_parent="Office of Security",
        ),
        info_tryout_requirements_embed(
            unit_abbrev=_ABBREV,
            combat_requirement=c.GRS_TRYOUT_COMBAT,
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
            ("🎮 GRS Roblox", c.URL_ROBLOX_GROUP_GRS, 0),
            ("🎮 OSEC Roblox", c.URL_ROBLOX_GROUP_OSEC, 0),
            ("🎮 DS Roblox", c.URL_ROBLOX_GROUP_DS, 0),
        ]
    )


def send_grs_information() -> None:
    run_announcer(
        webhook_key="WEBHOOK_GRS_INFORMATION",
        username=c.BOT_GRS,
        build_embeds=_build_embeds,
        build_view=_build_view,
        files=[c.logo_file(c.LOGOS["grs"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_grs_information()

# === FILE FOOTER ===
# End of file: units/grs/information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
