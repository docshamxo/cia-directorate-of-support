# === FILE HEADER ===
# Title: Public Information
# Path: ds/public_information.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
# === END FILE HEADER ===

"""
CIA DS public information announcer.

Posts the Directorate of Support organizational bulletin and community links
to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_DS_PUBLIC_INFORMATION")


def _build_embeds() -> list[c.discord.Embed]:
    ote_pillars = tuple(c.pillar_field(title, desc) for title, desc in c.OTE_PILLARS)

    return [
        c.embed(
            title="PUBLIC INFORMATION",
            description=(
                "*YFPA's CIA · Organizational Bulletin*\n\n"
                f"**DIRECTORATE OF SUPPORT**\n"
                f"*{c.DS_MOTTO} · Classification: {c.DS_CLASSIFICATION}*\n\n"
                "Unclassified overview of the Directorate of Support and its subordinate offices."
            ),
        ),
        c.embed(
            title="About the Directorate",
            description=c.DS_ABOUT,
            logo=c.LOGOS["ds"],
            fields=(
                ("Leadership", c.roles_text(*c.DS_LEADERSHIP)),
                ("Offices", c.bullets(*c.DS_OFFICES)),
            ),
        ),
        c.embed(
            title="Office of Security",
            description=(
                f"*{c.OSEC_MOTTO}*\n\n"
                f"{c.OSEC_ABOUT}"
            ),
            logo=c.LOGOS["osec"],
            fields=(
                ("Global Response Staff (GRS)", c.GRS_ABOUT),
                ("Executive Security Detail (ESD)", c.ESD_ABOUT),
            ),
        ),
        c.embed(
            title="Office of Training & Education",
            description=(
                f"*{c.OTE_MOTTO}*\n\n"
                f"{c.OTE_ABOUT}"
            ),
            logo=c.LOGOS["ote"],
            fields=ote_pillars,
        ),
        c.embed(
            title="Community Links",
            description=(
                "Official Roblox groups and Discord for the Directorate, its offices, "
                "and sub-units."
            ),
            fields=(
                c.link_field(
                    "Directorate of Support",
                    "CIA Directorate of Support",
                    c.URL_ROBLOX_GROUP_DS,
                ),
                c.link_field(
                    "Office of Security",
                    "CIA Office of Security",
                    c.URL_ROBLOX_GROUP_OSEC,
                ),
                c.link_field(
                    "Global Response Staff",
                    "CIA Global Response Staff",
                    c.URL_ROBLOX_GROUP_GRS,
                ),
                (
                    "Executive Security Detail",
                    "*CIA Executive Security Detail Roblox group — coming soon.*",
                ),
                c.link_field(
                    "Office of Training & Education",
                    "CIA Office of Training & Education",
                    c.URL_ROBLOX_GROUP_OTE,
                ),
                c.link_field(
                    "Discord",
                    "Permanent Discord Invite",
                    c.URL_DISCORD_INVITE,
                ),
            ),
        ),
        c.disclaimer_embed(links=True),
    ]


def send_public_information() -> None:
    logo_files = [
        c.logo_file(c.LOGOS["ds"]),
        c.logo_file(c.LOGOS["osec"]),
        c.logo_file(c.LOGOS["ote"]),
    ]
    c.send_webhook(
        WEBHOOK_URL,
        _build_embeds(),
        username=c.BOT_DS,
        files=logo_files,
    )


if __name__ == "__main__":
    send_public_information()

# === FILE FOOTER ===
# End of file: ds/public_information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
