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
#   - 2026-09-28 | docshamxo | Include GRS and ESD MIDCOM applications in OSEC open positions.
# === END FILE HEADER ===

"""
CIA OSEC open positions announcer.

Sends LOWCOM and MIDCOM application announcements (including GRS and ESD
Middle Command) to the OSEC open-positions Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    embeds = [
        c.hero_embed(
            title="OPEN POSITIONS",
            unit="Office of Security",
            supporting=(
                "OSEC Lower Command (LOWCOM) and Middle Command (MIDCOM), plus "
                "Global Response Staff (GRS) and Executive Security Detail (ESD) "
                "Middle Command (MIDCOM) applications. "
                "Read all requirements before submitting."
            ),
            color=c.COLOR_OSEC,
            logo=c.LOGOS["osec"],
        ),
        c.embed(
            title="OSEC Applications",
            description=(
                f"{c.motto_line(c.OSEC_MOTTO)}\n\n"
                "Positions typically open **Sunday** after the weekly quota reset.\n"
                f"{c.last_updated_line()}"
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    c.command_band_label("LOWCOM"),
                    "CIA DS | OSEC Lower Command (LOWCOM) Application",
                    c.osec_lowcom_application_url(),
                    "Base operations and standards across ranks.",
                ),
                c.link_field(
                    c.command_band_label("MIDCOM"),
                    "CIA DS | OSEC Middle Command (MIDCOM) Application",
                    c.osec_midcom_application_url(),
                    "Tryouts, phases, events, and LOWCOM supervision.",
                ),
            ),
        ),
        c.embed(
            title="GRS MIDCOM (OPEN)",
            description=(
                f"{c.motto_line(c.DS_MOTTO)}\n\n"
                "An application for the **Global Response Staff (GRS)** is currently open. "
                "GRS is a sub-unit of the **Office of Security (OSEC)**, operating under the "
                "**Directorate of Support (DS)** — OSEC's dedicated tactical element for "
                "rapid-response security, covert protection, mission support, stealth and "
                "tradecraft, and deployments.\n\n"
                "**Requirements**\n"
                "- Must play on a **PC or laptop**.\n"
                "- Requirement for being **SSA** and in **OSEC for two weeks** is "
                "**exempted for 1 week**.\n"
                "- Demonstrate **above-average combat** skills.\n"
                "- Must be at least **14** years of age (OSEC-wide requirement).\n"
                "- **Do not DM** any GRS High Command (HICOM) about application status — "
                "doing so is an **instant denial**."
            ),
            color=c.COLOR_GRS,
            fields=(
                c.link_field(
                    c.command_band_label("MIDCOM"),
                    c.community_link_label("GRS Middle Command (MIDCOM) Application"),
                    c.grs_midcom_application_url(),
                    "Command and operational leadership within GRS.",
                ),
                ("Command", c.roles_text(*c.GRS_COMMAND)),
            ),
        ),
        c.embed(
            title="ESD MIDCOM (OPEN)",
            description=(
                f"{c.motto_line(c.DS_MOTTO)}\n\n"
                "An application for the **Executive Security Detail (ESD)** is currently open. "
                "ESD is a sub-unit of the **Office of Security (OSEC)**, operating under the "
                "**Directorate of Support (DS)** — a close-protection unit for senior leadership "
                "and designated principals during travel and operations.\n\n"
                "**Requirements**\n"
                "- Must play on a **PC or laptop**.\n"
                "- Rank requirement: **SSA+**.\n"
                "- Minimum **2 weeks** in OSEC.\n"
                "- **Strong defensive combat** skills.\n"
                "- Must be at least **14** years of age (OSEC-wide requirement).\n"
                "- **Do not DM** any ESD High Command (HICOM) about application status — "
                "doing so is an **instant denial**."
            ),
            color=c.COLOR_ESD,
            fields=(
                c.link_field(
                    c.command_band_label("MIDCOM"),
                    c.community_link_label("ESD Middle Command (MIDCOM) Application"),
                    c.esd_midcom_application_url(),
                    "Command and protective operations leadership within ESD.",
                ),
                ("Command", c.roles_text(*c.ESD_COMMAND)),
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
                "- OSEC application questions → OSEC High Command only:\n"
                f"{c.roles_text(*c.OSEC_HIGH_COMMAND)}\n"
                "- GRS / ESD application questions → that unit's Command only "
                "(see sections above)."
            ),
            color=c.COLOR_OSEC,
        ),
    ]
    return c.append_classification_block(
        embeds, c.classification_label("level_1"), color=c.COLOR_OSEC
    )


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
