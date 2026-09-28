# === FILE HEADER ===
# Title: Open Positions
# Path: units/osec/open_positions.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Standardize hero, link grammar, and links disclaimer.
#   - 2026-07-15 | docshamxo | Tighten open-positions embed density.
#   - 2026-07-17 | docshamxo | Accessible LOWCOM/MIDCOM field names and first-use expansions.
#   - 2026-07-17 | docshamxo | Use DS Community link labels (brand/legal).
#   - 2026-07-17 | docshamxo | Replace mojibake bullets/dashes with ASCII in Important Info.
#   - 2026-08-30 | docshamxo | Reapply: 24h after graded; max 3 attempts then 1 week.
#   - 2026-08-30 | docshamxo | Application questions: full OSEC HICOM incl. Superintendent.
#   - 2026-08-30 | docshamxo | Last updated line uses post date (not static YAML).
#   - 2026-08-30 | docshamxo | Merge results rules; tighten Important Information copy.
# === END FILE HEADER ===

"""
CIA OSEC open positions announcer.

Sends LOWCOM and MIDCOM application announcements to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.hero_embed(
            title="OPEN POSITIONS",
            unit="Office of Security",
            supporting=(
                "Lower Command (LOWCOM) and Middle Command (MIDCOM) applications. "
                "Read all requirements before submitting."
            ),
            color=c.COLOR_OSEC,
            logo=c.LOGOS["osec"],
        ),
        c.embed(
            title="Applications",
            description=(
                f"{c.motto_line(c.OSEC_MOTTO)}\n\n"
                "Positions typically open **Sunday** after the weekly quota reset.\n"
                f"{c.last_updated_line()}"
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    c.command_band_label("LOWCOM"),
                    "DS Community | OSEC Lower Command (LOWCOM) Application",
                    c.osec_lowcom_application_url(),
                    "Base operations and standards across ranks.",
                ),
                c.link_field(
                    c.command_band_label("MIDCOM"),
                    "DS Community | OSEC Middle Command (MIDCOM) Application",
                    c.osec_midcom_application_url(),
                    "Tryouts, phases, events, and LOWCOM supervision.",
                ),
            ),
        ),
        c.embed(
            title="Important Information",
            description=(
                "- **AI**, trolling, sharing answers, requesting answers, or asking for results = "
                "**automatic failure**.\n"
                "- **Do not contact staff** for updates, results, or status — **immediate failure**.\n"
                f"- Graded results: you will be pinged in "
                f"[#application-results]({c.osec_application_results_url()}).\n"
                "- Use proper grammar and professionalism. Answer every question in "
                "**at least two complete sentences**.\n"
                "- Reapply only **24 hours** after your application is **graded**.\n"
                "- Maximum **3** applications, then wait a **full week** before applying again.\n"
                "- Application questions → OSEC High Command only:\n"
                f"{c.roles_text(*c.OSEC_HIGH_COMMAND)}"
            ),
            color=c.COLOR_OSEC,
        ),
    ]


def send_open_positions() -> None:
    run_announcer(
        webhook_key="WEBHOOK_OSEC_OPEN_POSITIONS",
        username=c.BOT_OSEC,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["osec"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_open_positions()

# === FILE FOOTER ===
# End of file: units/osec/open_positions.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
