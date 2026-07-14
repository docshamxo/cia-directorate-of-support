# === FILE HEADER ===
# Title: COC
# Path: esd/coc.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
# === END FILE HEADER ===

"""
CIA ESD chain of command announcer.

Sends the Executive Security Detail chain of command to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_ESD_COC")


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.chain_intro_embed(
            unit="Executive Security Detail",
            color=c.COLOR_ESD,
            context=(
                "The **Executive Security Detail (ESD)** is a sub-unit of the **Office of Security** "
                "under the **Directorate of Support**. ESD leadership reports through the OSEC "
                "and DS chains to Agency leadership."
            ),
        ),
        c.embed(
            title="Directorate of Support",
            description="ESD reports through the Directorate of Support chain of command.",
            color=c.COLOR_ESD,
            fields=(("Leadership", c.roles_text(*c.DS_LEADERSHIP)),),
        ),
        c.embed(
            title="ESD Command",
            description=(
                "Senior leadership responsible for ESD operations and policy.\n\n"
                f"{c.ESD_ABOUT}"
            ),
            color=c.COLOR_ESD,
            fields=(("Command Team", c.roles_text(*c.ESD_COMMAND)),),
        ),
        c.embed(
            title="ESD MIDCOM",
            description="Mid-level leadership responsible for supervision and operational oversight.",
            color=c.COLOR_ESD,
            fields=(("MIDCOM Ranks", c.ranks_text(*c.GRS_ESD_MIDDLE_COMMAND)),),
        ),
        c.embed(
            title="ESD LOWCOM",
            description="Field and operational ranks within the Executive Security Detail.",
            color=c.COLOR_ESD,
            fields=(("LOWCOM Ranks", c.ranks_text(*c.GRS_ESD_LOW_COMMAND)),),
        ),
        c.important_notice_embed(
            unit="ESD",
            color=c.COLOR_ESD,
            parent_units=("Directorate of Support", "Office of Security"),
        ),
        c.disclaimer_embed(),
    ]


def send_chain_of_command() -> None:
    c.send_webhook(WEBHOOK_URL, _build_embeds(), username=c.BOT_ESD)


if __name__ == "__main__":
    send_chain_of_command()

# === FILE FOOTER ===
# End of file: esd/coc.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
