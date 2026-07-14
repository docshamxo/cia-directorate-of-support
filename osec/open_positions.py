# === FILE HEADER ===
# Title: Open Positions
# Path: osec/open_positions.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
# === END FILE HEADER ===

"""
CIA OSEC open positions announcer.

Sends LOWCOM and MIDCOM application announcements to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_OSEC_OPEN_POSITIONS")

def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.embed(
            description=(
                "**Open Positions**\n"
                "**Central Intelligence Agency | Office of Security**\n\n"
                f"*{c.OSEC_MOTTO}*\n\n"
                f"{c.OSEC_ABOUT}\n\n"
                "Applications for **LOWCOM** and **MIDCOM** positions are linked below. "
                "Read all requirements before submitting."
            ),
            logo=c.LOGOS["osec"],
        ),
        c.embed(
            title="LOWCOM Application",
            description=(
                "LOWCOM members operate within the Office, assisting with **base operations** "
                "and maintaining standards across all ranks.\n\n"
                f"{c.link('CIA | Office of Security LOWCOM Application', c.url('osec.open_positions.lowcom_application'))}"
            ),
        ),
        c.embed(
            title="MIDCOM Application",
            description=(
                "MIDCOM members lead within the Office, assisting with **base operations, tryouts, "
                "phases, and events**. They help bring in new recruits, host events, manage LOWCOM "
                "personnel, and support a wide range of operational duties.\n\n"
                f"{c.link('CIA | Office of Security MIDCOM Application', c.url('osec.open_positions.midcom_application'))}"
            ),
        ),
        c.embed(
            title="Application Schedule",
            description=(
                "Positions tend to open every **Sunday**, following the weekly quota reset.\n\n"
                f"*Last updated: {c.url('osec.open_positions.last_updated')}*"
            ),
        ),
        c.embed(
            title="Important Information",
            description=(
                "→ The use of **AI**, trolling, sharing answers, requesting answers, or asking for "
                "application results will result in an **automatic failure**.\n"
                "→ Be patient after submitting your application. **Do not contact staff** asking for "
                "updates, results, or status regarding your submission. This will result in an "
                "**immediate failure**.\n"
                "→ Proper grammar and professionalism are required at all times. Every question must "
                "be answered in **at least two complete sentences**. Failure to meet this requirement "
                "will result in a failed application.\n"
                "→ After receiving a **passing** application result, you must wait a **full week** "
                "before reapplying for a higher position."
            ),
        ),
        c.embed(
            title="Application Contact",
            description=(
                "Questions or concerns regarding these applications should be directed **only** to:\n"
                f"{c.roles_text(*c.OSEC_HIGH_COMMAND[:3])}"
            ),
        ),
        c.embed(
            title="Application Results",
            description=(
                "**Do not ask for results, updates, or status.** Doing so is an instant fail.\n\n"
                f"You will be pinged in [#application-results]({c.url('osec.open_positions.application_results_channel')}) "
                "when your application has been graded."
            ),
        ),
        c.disclaimer_embed(),
    ]


def send_open_positions() -> None:
    c.send_webhook(
        WEBHOOK_URL,
        _build_embeds(),
        username=c.BOT_OSEC,
        files=[c.logo_file(c.LOGOS["osec"])],
    )


if __name__ == "__main__":
    send_open_positions()

# === FILE FOOTER ===
# End of file: osec/open_positions.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
