# === FILE HEADER ===
# Title: Public Information
# Path: ds/public_information.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Standardize eyebrow, link grammar, and public-info template.
# === END FILE HEADER ===

"""
CIA DS public information announcer.

Posts the Directorate of Support organizational bulletin and community links
to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    ote_pillars = tuple(c.pillar_field(title, desc) for title, desc in c.OTE_PILLARS)

    return [
        c.hero_embed(
            title="PUBLIC INFORMATION",
            unit="Directorate of Support",
            supporting=(
                "Unclassified overview of the Directorate of Support and its subordinate offices."
            ),
            logo=c.LOGOS["ds"],
        ),
        c.embed(
            title="About the Directorate",
            description=(
                f"{c.motto_line(c.DS_MOTTO, classification=c.DS_CLASSIFICATION)}\n\n{c.DS_ABOUT}"
            ),
            fields=(
                ("Leadership", c.roles_text(*c.DS_LEADERSHIP)),
                ("Offices", c.bullets(*c.DS_OFFICES)),
            ),
        ),
        c.embed(
            title="Office of Security",
            description=(f"{c.motto_line(c.OSEC_MOTTO)}\n\n{c.OSEC_ABOUT}"),
            logo=c.LOGOS["osec"],
            fields=(
                ("Global Response Staff (GRS)", c.GRS_ABOUT),
                ("Executive Security Detail (ESD)", c.ESD_ABOUT),
            ),
        ),
        c.embed(
            title="Office of Training & Education",
            description=(f"{c.motto_line(c.OTE_MOTTO)}\n\n{c.OTE_ABOUT}"),
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
                    "CIA | Directorate of Support",
                    c.URL_ROBLOX_GROUP_DS,
                ),
                c.link_field(
                    "Office of Security",
                    "CIA | Office of Security",
                    c.URL_ROBLOX_GROUP_OSEC,
                ),
                c.link_field(
                    "Global Response Staff",
                    "CIA | Global Response Staff",
                    c.URL_ROBLOX_GROUP_GRS,
                ),
                c.pending_group_field(
                    "Executive Security Detail",
                    "CIA | Executive Security Detail",
                ),
                c.link_field(
                    "Office of Training & Education",
                    "CIA | Office of Training & Education",
                    c.URL_ROBLOX_GROUP_OTE,
                ),
                c.link_field(
                    "Discord",
                    "CIA | Discord Invite",
                    c.URL_DISCORD_INVITE,
                ),
            ),
        ),
        c.disclaimer_embed(links=True, color=c.COLOR_DS),
    ]


def send_public_information() -> None:
    run_announcer(
        webhook_key="WEBHOOK_DS_PUBLIC_INFORMATION",
        username=c.BOT_DS,
        build_embeds=_build_embeds,
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
# End of file: ds/public_information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
