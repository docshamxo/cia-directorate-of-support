# === FILE HEADER ===
# Title: Information
# Path: grs/information.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
# === END FILE HEADER ===

"""
CIA GRS information announcer.

Posts the Global Response Staff overview and community links
to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_GRS_INFORMATION")

def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.embed(
            title="INFORMATION",
            description=(
                "*Central Intelligence Agency · Global Response Staff*\n\n"
                "Welcome to the official Global Response Staff (GRS) information hub. "
                "This channel provides an unclassified overview of GRS, its mission, "
                "and official community resources."
            ),
            color=c.COLOR_GRS,
        ),
        c.embed(
            title="Global Response Staff",
            description=(
                "The Global Response Staff is a sub-unit of the **Office of Security**, "
                "operating under the **Directorate of Support**.\n\n"
                f"{c.GRS_ABOUT}"
            ),
            color=c.COLOR_GRS,
            logo=c.LOGOS["grs"],
            fields=(
                (
                    "Organization",
                    "GRS reports through the **Office of Security** and **Directorate of Support** "
                    "chain of command. Personnel are expected to follow Agency regulations and "
                    "maintain professionalism at all times.",
                ),
            ),
        ),
        c.embed(
            title="Reference Documents",
            description="Key GRS reference material for personnel and candidates.",
            color=c.COLOR_GRS,
            fields=(
                c.link_field(
                    "Handbook",
                    "CIA GRS | Handbook",
                    c.url('\1'),
                    "Primary reference for GRS policy and standards.",
                ),
            ),
        ),
        c.embed(
            title="Community Links",
            description="Official Roblox groups for GRS and its parent organizations.",
            color=c.COLOR_GRS,
            fields=(
                c.link_field(
                    "Global Response Staff",
                    "CIA | Global Response Staff",
                    c.URL_ROBLOX_GROUP_GRS,
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
            unit="GRS",
            color=c.COLOR_GRS,
            parent_units=("Directorate of Support", "Office of Security"),
        ),
        c.disclaimer_embed(links=True),
    ]


def send_grs_information() -> None:
    c.send_webhook(
        WEBHOOK_URL,
        _build_embeds(),
        username=c.BOT_GRS,
        files=[c.logo_file(c.LOGOS["grs"])],
    )


if __name__ == "__main__":
    send_grs_information()

# === FILE FOOTER ===
# End of file: grs/information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
