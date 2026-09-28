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
                "Applications for Middle Command (MIDCOM) positions are linked below. "
                "Read all requirements before submitting."
            ),
            color=c.COLOR_GRS,
            logo=c.LOGOS["grs"],
        ),
        c.embed(
            title="Applications",
            description=(
                "An application for the **Global Response Staff (GRS)** — OSEC's dedicated "
                "tactical element under the Directorate of Support — is currently open.\n\n"
                f"*Last updated: {c.url('grs.open_positions.last_updated')}*"
            ),
            color=c.COLOR_GRS,
            fields=(
                c.link_field(
                    c.command_band_label("MIDCOM"),
                    c.community_link_label("GRS Middle Command (MIDCOM) Application"),
                    c.grs_midcom_application_url(),
                    "Rapid-response command billets within Global Response Staff.",
                ),
            ),
        ),
        c.embed(
            title="Requirements",
            description=(
                "- Play on a **PC or laptop**.\n"
                "- The usual requirement to be **SSA+** and in **OSEC for two weeks** is "
                "**exempted for 1 week**.\n"
                "- Demonstrate **above-average combat** skills.\n"
                "- Be at least **14 years of age** (OSEC-wide requirement)."
            ),
            color=c.COLOR_GRS,
        ),
        c.embed(
            title="Important Information",
            description=(
                "- **Do not DM** any GRS High Command (HICOM) about application status, "
                "results, or updates — that is an **instant denial**.\n"
                "- The use of **AI**, trolling, sharing answers, requesting answers, or asking "
                "for application results will result in an **automatic failure**.\n"
                "- Proper grammar and professionalism are required.\n"
                "- Application questions may be directed **only** to GRS Command:\n"
                f"{c.roles_text(*c.GRS_COMMAND)}"
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
