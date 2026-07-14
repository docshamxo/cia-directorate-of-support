"""
CIA GRS chain of command announcer.

Sends the Global Response Staff chain of command to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_GRS_COC")


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.chain_intro_embed(
            unit="Global Response Staff",
            color=c.COLOR_GRS,
            context=(
                "The **Global Response Staff (GRS)** is a sub-unit of the **Office of Security** "
                "under the **Directorate of Support**. GRS leadership reports through the OSEC "
                "and DS chains to Agency leadership."
            ),
        ),
        c.embed(
            title="Directorate of Support",
            description="GRS reports through the Directorate of Support chain of command.",
            color=c.COLOR_GRS,
            fields=(("Leadership", c.roles_text(*c.DS_LEADERSHIP)),),
        ),
        c.embed(
            title="GRS Command",
            description=(
                "Senior leadership responsible for GRS operations and policy.\n\n"
                f"{c.GRS_ABOUT}"
            ),
            color=c.COLOR_GRS,
            fields=(("Command Team", c.roles_text(*c.GRS_COMMAND)),),
        ),
        c.embed(
            title="GRS MIDCOM",
            description="Mid-level leadership responsible for supervision and operational oversight.",
            color=c.COLOR_GRS,
            fields=(("MIDCOM Ranks", c.ranks_text(*c.GRS_ESD_MIDDLE_COMMAND)),),
        ),
        c.embed(
            title="GRS LOWCOM",
            description="Field and operational ranks within the Global Response Staff.",
            color=c.COLOR_GRS,
            fields=(("LOWCOM Ranks", c.ranks_text(*c.GRS_ESD_LOW_COMMAND)),),
        ),
        c.important_notice_embed(
            unit="GRS",
            color=c.COLOR_GRS,
            parent_units=("Directorate of Support", "Office of Security"),
        ),
        c.disclaimer_embed(),
    ]


def send_chain_of_command() -> None:
    c.send_webhook(WEBHOOK_URL, _build_embeds(), username=c.BOT_GRS)


if __name__ == "__main__":
    send_chain_of_command()
