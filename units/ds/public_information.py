# === FILE HEADER ===
# Title: Public Information
# Path: units/ds/public_information.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-10-03 | docshamxo | OIG Levels closer + community emoji link buttons.
# === END FILE HEADER ===

"""CIA DS public information announcer."""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import info_community_link_view, run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    ote_pillars = tuple(c.pillar_field(title, desc) for title, desc in c.OTE_PILLARS)
    embeds = [
        c.hero_embed(
            title="PUBLIC INFORMATION",
            unit="Directorate of Support",
            supporting=("Overview of the Directorate of Support and its subordinate offices."),
            logo=c.LOGOS["ds"],
        ),
        c.embed(
            title="About the Directorate",
            description=f"{c.motto_line(c.DS_MOTTO)}\n\n{c.DS_ABOUT}",
            fields=(
                ("Leadership", c.roles_text(*c.DS_LEADERSHIP)),
                ("Offices", c.bullets(*c.DS_OFFICES)),
            ),
        ),
        c.embed(
            title="Office of Security",
            description=f"{c.motto_line(c.OSEC_MOTTO)}\n\n{c.OSEC_ABOUT}",
            logo=c.LOGOS["osec"],
            fields=(
                ("Global Response Staff (GRS)", c.GRS_ABOUT),
                ("Executive Security Detail (ESD)", c.ESD_ABOUT),
            ),
        ),
        c.embed(
            title="Office of Training & Education",
            description=f"{c.motto_line(c.OTE_MOTTO)}\n\n{c.OTE_ABOUT}",
            logo=c.LOGOS["ote"],
            fields=ote_pillars,
        ),
        c.embed(
            title="Community Links",
            description=(
                "Official Roblox groups and Discord for the Directorate, its offices, "
                "and sub-units. Use the buttons below."
            ),
        ),
    ]
    return c.append_classification_block(
        embeds, c.classification_label("level_1"), color=c.COLOR_DS
    )


def _build_view() -> c.discord.ui.View:
    return info_community_link_view(
        [
            ("🎮 DS Roblox", c.URL_ROBLOX_GROUP_DS, 0),
            ("🎮 OSEC Roblox", c.URL_ROBLOX_GROUP_OSEC, 0),
            ("🎮 GRS Roblox", c.URL_ROBLOX_GROUP_GRS, 0),
            ("🎮 ESD Roblox", c.URL_ROBLOX_GROUP_ESD, 1),
            ("🎮 OTE Roblox", c.URL_ROBLOX_GROUP_OTE, 1),
            ("🏛️ OSEC Discord", c.discord_osec_invite_url(), 2),
            ("🏛️ OTE Discord", c.discord_ote_invite_url(), 2),
        ]
    )


def send_public_information() -> None:
    run_announcer(
        webhook_key="WEBHOOK_DS_PUBLIC_INFORMATION",
        username=c.BOT_DS,
        build_embeds=_build_embeds,
        build_view=_build_view,
        files=lambda: [
            c.logo_file(c.LOGOS["ds"]),
            c.logo_file(c.LOGOS["osec"]),
            c.logo_file(c.LOGOS["ote"]),
        ],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_public_information()

# === FILE FOOTER ===
# End of file: units/ds/public_information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
