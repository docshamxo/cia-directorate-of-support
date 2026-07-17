# === FILE HEADER ===
# Title: Program Overview
# Path: ote/program_overview.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Align link grammar, hero supporting line, unit-color closer.
#   - 2026-07-17 | docshamxo | Accessible marking notes on public links.
# === END FILE HEADER ===

"""
CIA OTE program overview announcer.

Sends the Officer Training Program overview, graduation procedures, and
official community links to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    ote_pillars = tuple(c.pillar_field(title, desc) for title, desc in c.OTE_PILLARS)

    return [
        c.hero_embed(
            title="OFFICER TRAINING PROGRAM",
            unit="Office of Training & Education",
            supporting=(
                "Official reference hub for the Officer Training Program — organization, "
                "phases, graduation, and community links."
            ),
            color=c.COLOR_OTE,
            logo=c.LOGOS["ote"],
        ),
        c.embed(
            title="Program Pillars",
            description=(f"{c.motto_line(c.OTE_MOTTO)}\n\n{c.OTE_ABOUT}"),
            color=c.COLOR_OTE,
            fields=ote_pillars,
        ),
        c.embed(
            title="Official Documents",
            description=(
                "Authorized guides and procedures for OTE personnel, instructors, "
                "and program leadership."
            ),
            color=c.COLOR_OTE,
            fields=(
                c.link_field(
                    "Program Overview",
                    "CIA OTE | Program Overview",
                    c.url("ote.program_overview.program_overview"),
                    c.marking_note("PUBLIC"),
                ),
                c.link_field(
                    "Graduation",
                    "CIA OTE | Graduation Ceremony Procedures",
                    c.url("ote.program_overview.graduation_ceremony_procedures"),
                    c.marking_note("PUBLIC"),
                ),
            ),
        ),
        c.embed(
            title="Community Links",
            description="Official Roblox groups for the Directorate of Support and OTE.",
            color=c.COLOR_OTE,
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
        c.disclaimer_embed(links=True, color=c.COLOR_OTE),
    ]


def send_officer_training_program_overview() -> None:
    run_announcer(
        webhook_key="WEBHOOK_OTE_PROGRAM_OVERVIEW",
        username=c.BOT_OTE,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["ote"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_officer_training_program_overview()

# === FILE FOOTER ===
# End of file: ote/program_overview.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
