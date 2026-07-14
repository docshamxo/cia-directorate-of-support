# === FILE HEADER ===
# Title: Program Overview
# Path: ote/program_overview.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
# === END FILE HEADER ===

"""
CIA OTE program overview announcer.

Sends the Officer Training Program overview, graduation procedures, and
official community links to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_OTE_PROGRAM_OVERVIEW")

def _build_embeds() -> list[c.discord.Embed]:
    ote_pillars = tuple(c.pillar_field(title, desc) for title, desc in c.OTE_PILLARS)

    return [
        c.embed(
            title="OFFICER TRAINING PROGRAM",
            description=(
                "*Central Intelligence Agency · Office of Training & Education*\n\n"
                f"*{c.OTE_MOTTO}*\n\n"
                f"{c.OTE_ABOUT}\n\n"
                "Official reference hub for the **Officer Training Program**. "
                "Review these materials when you join, when policy or structure changes, "
                "or before hosting training, phases, or graduation ceremonies."
            ),
            logo=c.LOGOS["ote"],
        ),
        c.embed(
            title="Program Pillars",
            description="The Officer Training Program is organized around three core pillars.",
            fields=ote_pillars,
        ),
        c.embed(
            title="Official Documents",
            description=(
                "Authorized guides and procedures for OTE personnel, instructors, "
                "and program leadership."
            ),
            fields=(
                c.link_field(
                    "Program Overview",
                    "CIA | Officer Training Program Overview",
                    c.url('ote.program_overview.program_overview'),
                    "Organization, eligibility, chain of command, phases, and scheduling.",
                ),
                c.link_field(
                    "Graduation",
                    "CIA | Graduation Ceremony Procedures",
                    c.url('ote.program_overview.graduation_ceremony_procedures'),
                    "Planning and conducting official OTE graduation ceremonies.",
                ),
            ),
        ),
        c.embed(
            title="Community Links",
            description="Official Roblox groups for the Directorate of Support and OTE.",
            fields=(
                c.link_field(
                    "Directorate of Support",
                    "CIA | Directorate of Support",
                    c.URL_ROBLOX_GROUP_DS,
                ),
                c.link_field(
                    "Office of Training & Education",
                    "CIA | Office of Training & Education",
                    c.URL_ROBLOX_GROUP_OTE,
                ),
            ),
        ),
        c.embed(description="**Stay informed. Stay prepared.**"),
        c.disclaimer_embed(links=True),
    ]


def send_officer_training_program_overview() -> None:
    c.send_webhook(
        WEBHOOK_URL,
        _build_embeds(),
        username=c.BOT_OTE,
        files=[c.logo_file(c.LOGOS["ote"])],
    )


if __name__ == "__main__":
    send_officer_training_program_overview()

# === FILE FOOTER ===
# End of file: ote/program_overview.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
