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
                "Middle Command (MIDCOM) applications are open. "
                "Read all requirements before submitting."
            ),
            color=c.COLOR_ESD,
            logo=c.LOGOS["esd"],
        ),
        c.embed(
            title="Applications",
            description=(
                f"{c.motto_line(c.DS_MOTTO)}\n\n"
                "An application for the **Executive Security Detail (ESD)** is currently open. "
                "ESD is a sub-unit of the **Office of Security (OSEC)**, operating under the "
                "**Directorate of Support (DS)** — a close-protection unit for senior leadership "
                "and designated principals during travel and operations."
            ),
            color=c.COLOR_ESD,
            fields=(
                c.link_field(
                    c.command_band_label("MIDCOM"),
                    c.community_link_label("ESD Middle Command (MIDCOM) Application"),
                    c.esd_midcom_application_url(),
                    "Command and protective operations leadership within ESD.",
                ),
            ),
        ),
        c.embed(
            title="Requirements",
            description=(
                "- Must play on a **PC or laptop**.\n"
                "- Rank requirement: **SSA+**.\n"
                "- Minimum **2 weeks** in OSEC.\n"
                "- **Strong defensive combat** skills.\n"
                "- Must be at least **14** years of age (OSEC-wide requirement).\n"
                "- **Do not DM** any ESD High Command (HICOM) about application status — "
                "doing so is an **instant denial**."
            ),
            color=c.COLOR_ESD,
        ),
        c.embed(
            title="Important Information",
            description=(
                "- Read the form carefully and answer every question completely.\n"
                "- Use proper grammar and professionalism.\n"
                "- Application questions → ESD Command only:\n"
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
