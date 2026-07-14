# === FILE HEADER ===
# Title: Information
# Path: esd/information.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
# === END FILE HEADER ===

"""
CIA ESD information announcer.

Posts the Executive Security Detail overview and community links
to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_ESD_INFORMATION")


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.embed(
            title="INFORMATION",
            description=(
                "*Central Intelligence Agency · Executive Security Detail*\n\n"
                "Welcome to the official Executive Security Detail (ESD) information hub. "
                "This channel provides an unclassified overview of ESD, its mission, "
                "and official community resources."
            ),
            color=c.COLOR_ESD,
        ),
        c.embed(
            title="Executive Security Detail",
            description=(
                "The Executive Security Detail is a sub-unit of the **Office of Security**, "
                "operating under the **Directorate of Support**.\n\n"
                f"{c.ESD_ABOUT}"
            ),
            color=c.COLOR_ESD,
            logo=c.LOGOS["esd"],
            fields=(
                (
                    "Organization",
                    "ESD reports through the **Office of Security** and **Directorate of Support** "
                    "chain of command. Personnel are expected to follow Agency regulations and "
                    "maintain the highest standards of professionalism and discretion.",
                ),
            ),
        ),
        c.embed(
            title="Community Links",
            description="Official Roblox groups for ESD and its parent organizations.",
            color=c.COLOR_ESD,
            fields=(
                (
                    "Executive Security Detail",
                    "*CIA Executive Security Detail Roblox group — coming soon.*",
                ),
                c.link_field(
                    "Office of Security",
                    "CIA Office of Security",
                    c.URL_ROBLOX_GROUP_OSEC,
                ),
                c.link_field(
                    "Directorate of Support",
                    "CIA | Directorate of Support",
                    c.URL_ROBLOX_GROUP_DS,
                ),
            ),
        ),
        c.important_notice_embed(
            unit="ESD",
            color=c.COLOR_ESD,
            parent_units=("Directorate of Support", "Office of Security"),
        ),
        c.disclaimer_embed(links=True),
    ]


def send_esd_information() -> None:
    c.send_webhook(
        WEBHOOK_URL,
        _build_embeds(),
        username=c.BOT_ESD,
        files=[c.logo_file(c.LOGOS["esd"])],
    )


if __name__ == "__main__":
    send_esd_information()

# === FILE FOOTER ===
# End of file: esd/information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
