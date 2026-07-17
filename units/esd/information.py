# === FILE HEADER ===
# Title: Information
# Path: units/esd/information.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Align public-info template and link grammar.
# === END FILE HEADER ===

"""
CIA ESD information announcer.

Posts the Executive Security Detail overview and community links
to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.hero_embed(
            title="INFORMATION",
            unit="Executive Security Detail",
            supporting=(
                "Unclassified overview of ESD, its mission, and official community resources."
            ),
            color=c.COLOR_ESD,
            logo=c.LOGOS["esd"],
        ),
        c.embed(
            title="About ESD",
            description=(
                "The Executive Security Detail is a sub-unit of the **Office of Security**, "
                "operating under the **Directorate of Support**.\n\n"
                f"{c.ESD_ABOUT}"
            ),
            color=c.COLOR_ESD,
        ),
        c.embed(
            title="Community Links",
            description="Official Roblox groups for ESD and its parent organizations.",
            color=c.COLOR_ESD,
            fields=(
                c.pending_group_field(
                    "Executive Security Detail",
                    c.community_link_label("ESD"),
                ),
                c.link_field(
                    "Office of Security",
                    c.community_link_label("OSEC"),
                    c.URL_ROBLOX_GROUP_OSEC,
                ),
                c.link_field(
                    "Directorate of Support",
                    c.community_link_label("Directorate of Support"),
                    c.URL_ROBLOX_GROUP_DS,
                ),
            ),
        ),
        c.disclaimer_embed(links=True, color=c.COLOR_ESD),
    ]


def send_esd_information() -> None:
    run_announcer(
        webhook_key="WEBHOOK_ESD_INFORMATION",
        username=c.BOT_ESD,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["esd"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_esd_information()

# === FILE FOOTER ===
# End of file: units/esd/information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
