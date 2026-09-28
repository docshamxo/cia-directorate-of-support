# === FILE HEADER ===
# Title: Open Positions
# Path: units/grs/open_positions.py
# Created: 2026-09-28
# Created by: docshamxo
# Modified:
#   - 2026-09-28 | docshamxo | Add GRS MIDCOM open applications announcer.
# === END FILE HEADER ===

"""
CIA GRS open positions announcer.

Sends the Global Response Staff Middle Command (MIDCOM) application
announcement to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.hero_embed(
            title="OPEN POSITIONS",
            unit="Global Response Staff",
            supporting=(
                "Middle Command (MIDCOM) applications are open. "
                "Read all requirements before submitting."
            ),
            color=c.COLOR_GRS,
            logo=c.LOGOS["grs"],
        ),
        c.embed(
            title="Applications",
            description=(
                "**Global Response Staff (GRS) MIDCOM** is accepting applications."
            ),
            color=c.COLOR_GRS,
            fields=(
                c.link_field(
                    c.command_band_label("MIDCOM"),
                    c.community_link_label("GRS Middle Command (MIDCOM) Application"),
                    c.grs_midcom_application_url(),
                    "Command and operational leadership within GRS.",
                ),
            ),
        ),
        c.embed(
            title="Requirements",
            description=(
                "- Must play on a **PC or laptop**.\n"
                "- Rank requirement: **SSA+**. Applicants with **2 weeks** in OSEC may be "
                "**exempted for 1 week**.\n"
                "- **Above-average combat** ability.\n"
                "- Must be **14+**.\n"
                "- **Do not DM High Command (HICOM)** about applications, results, or status."
            ),
            color=c.COLOR_GRS,
        ),
        c.embed(
            title="Important Information",
            description=(
                "- Read the form carefully and answer every question completely.\n"
                "- Use proper grammar and professionalism.\n"
                "- Application questions → GRS Command only "
                "(**CM** qv4_pendragon · **DCM** idk_manti).\n"
                "- Do not invent Discord pings; contact via the form or listed usernames only."
            ),
            color=c.COLOR_GRS,
        ),
    ]


def send_open_positions() -> None:
    run_announcer(
        webhook_key="WEBHOOK_GRS_OPEN_POSITIONS",
        username=c.BOT_GRS,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["grs"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_open_positions()

# === FILE FOOTER ===
# End of file: units/grs/open_positions.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
