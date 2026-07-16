# === FILE HEADER ===
# Title: COC
# Path: ote/coc.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
# === END FILE HEADER ===

"""
CIA OTE chain of command announcer.

Sends the Office of Training & Education chain of command to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_OTE_COC")


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.chain_intro_embed(
            unit="Office of Training & Education",
            color=c.COLOR_OTE,
            context=(
                f"*{c.OTE_MOTTO}*\n\n"
                "The Office of Training & Education sits under the **Directorate of Support**. "
                "OTE leadership reports through the DS chain to Agency leadership."
            ),
        ),
        c.embed(
            title="Directorate of Support",
            description="OTE reports through the Directorate of Support chain of command.",
            color=c.COLOR_OTE,
            fields=(("Leadership", c.roles_text(*c.DS_LEADERSHIP)),),
        ),
        c.embed(
            title="OTE High Command",
            description="Senior leadership responsible for OTE operations and policy.",
            color=c.COLOR_OTE,
            fields=(("Command Team", c.roles_text(*c.OTE_HIGH_COMMAND)),),
        ),
        c.embed(
            title="OTE Staff",
            description="Instructional and training staff ranks within the Office.",
            color=c.COLOR_OTE,
            fields=(("Staff Ranks", c.ranks_text(*c.OTE_STAFF_RANKS)),),
        ),
        c.important_notice_embed(
            unit="OTE",
            color=c.COLOR_OTE,
            parent_units=("Directorate of Support",),
        ),
        c.disclaimer_embed(),
    ]


def send_chain_of_command() -> None:
    c.send_webhook(WEBHOOK_URL, _build_embeds(), username=c.BOT_OTE_ALT)


if __name__ == "__main__":
    send_chain_of_command()

# === FILE FOOTER ===
# End of file: ote/coc.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
