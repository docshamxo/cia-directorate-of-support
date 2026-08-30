# === FILE HEADER ===
# Title: Open Positions
# Path: units/ote/open_positions.py
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
#   - 2026-08-30 | docshamxo | Reapply: 24h after graded; max 3 attempts then 1 week.
#   - 2026-08-30 | docshamxo | State SIS-6+ once; tighten eligibility and rules copy.
#   - 2026-08-30 | docshamxo | General Staff eligibility GS-2+ → GS-7+.
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
                "Applications for Associate Professor and above. "
                "Review eligibility before submitting."
            ),
            color=c.COLOR_OTE,
            logo=c.LOGOS["ote"],
        ),
        c.embed(
            title="Available Positions",
            description=(
                f"{c.motto_line(c.OTE_MOTTO)}\n\n"
                "Personnel from **all Agency divisions** may apply. Open staff ranks:"
            ),
            color=c.COLOR_OTE,
            fields=(("Staff Ranks", c.ranks_text(*c.OTE_STAFF_RANKS)),),
        ),
        c.embed(
            title="Eligibility",
            description="Rank and training requirements:",
            color=c.COLOR_OTE,
            fields=(
                (
                    "Graduated Officers",
                    "**Graduated Officers [SIS-1+]** may bypass the **Officer Training Program (OTP)**.",
                ),
                (
                    "General Staff",
                    "**GS-7+** may apply and must complete the full **OTP**.",
                ),
                (
                    "Restrictions",
                    "**SIS-6+** in their respective office are **not eligible**.",
                ),
            ),
        ),
        c.embed(
            title="Important Information",
            description=(
                "→ Must be **13+** and **willing to use a microphone**.\n"
                "→ **Past hosting or instructional experience** preferred.\n"
                "→ **AI** in any response = **BLACKLIST** from OTE.\n"
                "→ Use proper grammar, spelling, and professionalism.\n"
                "→ Reapply only **24 hours** after grading; max **3** applications, then wait a "
                "**full week**."
            ),
            color=c.COLOR_OTE,
        ),
        c.embed(
            title="How to Apply",
            description="Request to join the **OTE Roblox group** before submitting.",
            color=c.COLOR_OTE,
            fields=(
                c.link_field(
                    "Application",
                    c.community_link_label("OTE Professor Application"),
                    c.ote_application_url(),
                ),
                c.link_field(
                    "Roblox Group",
                    c.community_link_label("OTE"),
                    c.URL_ROBLOX_GROUP_OTE,
                ),
            ),
        ),
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
# End of file: units/ote/open_positions.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
