# === FILE HEADER ===
# Title: Open Positions
# Path: ote/open_positions.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
# === END FILE HEADER ===

"""
CIA OTE open positions announcer.

Sends the Office of Training & Education Professor application announcement
to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_OTE_OPEN_POSITIONS")

def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.embed(
            title="OPEN POSITIONS",
            description=(
                "*Central Intelligence Agency · Office of Training & Education*\n\n"
                f"*{c.OTE_MOTTO}*\n\n"
                f"{c.OTE_ABOUT}\n\n"
                "The Office of Training & Education is currently accepting applications for "
                "**Associate Professor** and above. As a sub-division under the "
                "**Directorate of Support**, personnel from **all Agency divisions** may "
                "apply, with the exception of members holding **SIS-6+** in their respective "
                "division.\n\n"
                "Review all eligibility requirements and important information below before "
                "submitting your application."
            ),
            logo=c.LOGOS["ote"],
        ),
        c.embed(
            title="Available Positions",
            description="The following staff positions are open for application:",
            fields=(("Staff Ranks", c.ranks_text(*c.OTE_STAFF_RANKS)),),
        ),
        c.embed(
            title="Eligibility",
            description="Applicants must meet the following rank and training requirements:",
            fields=(
                (
                    "Graduated Officers",
                    "Applicants who are **Graduated Officers [SIS-1+]** may bypass the "
                    "**Officer Training Program (OTP)**.",
                ),
                (
                    "General Staff",
                    "Applicants at **GS-2+** may apply but must be willing to complete the full "
                    "**Officer Training Program (OTP)**.",
                ),
                (
                    "Restrictions",
                    "Applicants at **SIS-6+** rank in their respective office are **not eligible**.",
                ),
            ),
        ),
        c.embed(
            title="Important Information",
            description=(
                "→ Applicants must be **13 years of age or older**.\n"
                "→ Applicants must be **willing to use a microphone**.\n"
                "→ **Past hosting or instructional experience** is preferred.\n"
                "→ The use of **AI** in any application response will result in a "
                "**BLACKLIST** from OTE.\n"
                "→ Use proper grammar, spelling, and professionalism throughout your application.\n"
                "→ All applicants must follow Agency regulations and the OTE chain of command."
            ),
        ),
        c.embed(
            title="How to Apply",
            description=(
                "Before submitting, ensure you have **requested to join the OTE Roblox group**."
            ),
            fields=(
                c.link_field(
                    "Application",
                    "CIA | OTE Professor Application",
                    c.url('ote.open_positions.application'),
                ),
                c.link_field(
                    "Roblox Group",
                    "CIA | Office of Training & Education",
                    c.URL_ROBLOX_GROUP_OTE,
                ),
                c.link_field(
                    "Application Tracker",
                    "CIA OTE | Application Tracker",
                    c.url('ote.open_positions.application_tracker'),
                    "Public tracker for submitted OTE applications and status updates.",
                ),
            ),
        ),
        c.disclaimer_embed(links=True),
    ]


def send_open_positions() -> None:
    c.send_webhook(
        WEBHOOK_URL,
        _build_embeds(),
        username=c.BOT_OTE_ALT,
        files=[c.logo_file(c.LOGOS["ote"])],
    )


if __name__ == "__main__":
    send_open_positions()

# === FILE FOOTER ===
# End of file: ote/open_positions.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
