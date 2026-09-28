# === FILE HEADER ===
# Title: Open Positions
# Path: units/esd/open_positions.py
# Created: 2026-09-28
# Created by: docshamxo
# Modified:
#   - 2026-09-28 | docshamxo | Add ESD MIDCOM open applications announcer.
# === END FILE HEADER ===

"""
CIA ESD open positions announcer.

Sends the Executive Security Detail Middle Command (MIDCOM) application
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
            unit="Executive Security Detail",
            supporting=(
                "Applications for Middle Command (MIDCOM) positions are linked below. "
                "Read all requirements before submitting."
            ),
            color=c.COLOR_ESD,
            logo=c.LOGOS["esd"],
        ),
        c.embed(
            title="Applications",
            description=(
                "An application for the **Executive Security Detail (ESD)** — OSEC's "
                "close-protection element under the Directorate of Support — is currently "
                "open.\n\n"
                f"*Last updated: {c.url('esd.open_positions.last_updated')}*"
            ),
            color=c.COLOR_ESD,
            fields=(
                c.link_field(
                    c.command_band_label("MIDCOM"),
                    c.community_link_label("ESD Middle Command (MIDCOM) Application"),
                    c.esd_midcom_application_url(),
                    "Protective-command billets within Executive Security Detail.",
                ),
            ),
        ),
        c.embed(
            title="Requirements",
            description=(
                "- Play on a **PC or laptop**.\n"
                "- Rank requirement: **SSA+**.\n"
                "- At least **2 weeks** in OSEC.\n"
                "- Demonstrate **strong defensive combat** skills.\n"
                "- Be at least **14 years of age** (OSEC-wide requirement)."
            ),
            color=c.COLOR_ESD,
        ),
        c.embed(
            title="Important Information",
            description=(
                "- **Do not DM** any ESD High Command (HICOM) about application status, "
                "results, or updates — that is an **instant denial**.\n"
                "- The use of **AI**, trolling, sharing answers, requesting answers, or asking "
                "for application results will result in an **automatic failure**.\n"
                "- Proper grammar and professionalism are required.\n"
                "- Application questions may be directed **only** to ESD Command:\n"
                f"{c.roles_text(*c.ESD_COMMAND)}"
            ),
            color=c.COLOR_ESD,
        ),
    ]


def send_open_positions() -> None:
    run_announcer(
        webhook_key="WEBHOOK_ESD_OPEN_POSITIONS",
        username=c.BOT_ESD,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["esd"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_open_positions()

# === FILE FOOTER ===
# End of file: units/esd/open_positions.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
