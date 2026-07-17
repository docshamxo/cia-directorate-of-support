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
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Align hero supporting line, link grammar, unit-color closer.
#   - 2026-07-17 | docshamxo | Accessible marking notes on public links.
# === END FILE HEADER ===

"""
CIA OTE open positions announcer.

Sends the Office of Training & Education Professor application announcement
to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.hero_embed(
            title="OPEN POSITIONS",
            unit="Office of Training & Education",
            supporting=(
                "OTE is accepting applications for Associate Professor and above. "
                "Review eligibility and important information before submitting."
            ),
            color=c.COLOR_OTE,
            logo=c.LOGOS["ote"],
        ),
        c.embed(
            title="Available Positions",
            description=(
                f"{c.motto_line(c.OTE_MOTTO)}\n\n"
                "As a sub-division under the **Directorate of Support**, personnel from "
                "**all Agency divisions** may apply, with the exception of members holding "
                "**SIS-6+** in their respective division.\n\n"
                "The following staff positions are open for application:"
            ),
            color=c.COLOR_OTE,
            fields=(("Staff Ranks", c.ranks_text(*c.OTE_STAFF_RANKS)),),
        ),
        c.embed(
            title="Eligibility",
            description="Applicants must meet the following rank and training requirements:",
            color=c.COLOR_OTE,
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
            color=c.COLOR_OTE,
        ),
        c.embed(
            title="How to Apply",
            description=(
                "Before submitting, ensure you have **requested to join the OTE Roblox group**."
            ),
            color=c.COLOR_OTE,
            fields=(
                c.link_field(
                    "Application",
                    "CIA OTE | Professor Application",
                    c.url("ote.open_positions.application"),
                ),
                c.link_field(
                    "Roblox Group",
                    "CIA | Office of Training & Education",
                    c.URL_ROBLOX_GROUP_OTE,
                ),
                c.link_field(
                    "Application Tracker",
                    "CIA OTE | Application Tracker",
                    c.url("ote.open_positions.application_tracker"),
                    c.marking_note("PUBLIC"),
                ),
            ),
        ),
        c.disclaimer_embed(links=True, color=c.COLOR_OTE),
    ]


def send_open_positions() -> None:
    run_announcer(
        webhook_key="WEBHOOK_OTE_OPEN_POSITIONS",
        username=c.BOT_OTE,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["ote"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_open_positions()

# === FILE FOOTER ===
# End of file: ote/open_positions.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
