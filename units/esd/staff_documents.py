# === FILE HEADER ===
# Title: Staff Documents
# Path: units/esd/staff_documents.py
# Created: 2026-07-15
# Created by: docshamxo
# Modified:
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Unify staff-docs template and unit-color closers.
#   - 2026-07-17 | docshamxo | Text marking notes and clearer field labels.
#   - 2026-07-17 | docshamxo | Add General Standard Training Guide (shared community link).
#   - 2026-07-17 | docshamxo | Add handbook, FPCON, phase, and tryout guides.
#   - 2026-07-17 | docshamxo | Collapse Phase I/II into single Phase Guide; drop Phase II.
#   - 2026-09-07 | docshamxo | Add After Action Report Google Form to staff documents.
#   - 2026-09-08 | docshamxo | Refactor onto shared staff-docs frame builders.
# === END FILE HEADER ===

"""
CIA ESD staff documents announcer.

Posts official Executive Security Detail staff guides and shared Drive
resources to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import (
    run_announcer,
    staff_docs_central_embed,
    staff_docs_handling_embed,
    staff_docs_hero_embed,
    staff_docs_link,
    staff_docs_section_embed,
)

_UNIT = "Executive Security Detail"
_ABBREV = "ESD"
_COLOR = c.COLOR_ESD


def _build_embeds() -> list[c.discord.Embed]:
    return [
        staff_docs_hero_embed(
            unit_full=_UNIT,
            unit_abbrev=_ABBREV,
            color=_COLOR,
            logo=c.LOGOS["esd"],
        ),
        staff_docs_central_embed(
            unit_abbrev=_ABBREV,
            drive_url_key="esd.staff_documents.google_drive",
            drive_link_name="ESD Google Drive",
            color=_COLOR,
        ),
        staff_docs_section_embed(
            title="Handbook & Force Protection",
            description=(
                "Official ESD handbook and force protection condition protocols "
                "for Executive Security Detail operations."
            ),
            color=_COLOR,
            fields=(
                staff_docs_link(
                    "Official Handbook",
                    "ESD Official Handbook",
                    "esd.staff_documents.handbook",
                ),
                staff_docs_link(
                    "FPCON Protocols",
                    "ESD Force Protection Conditions and Protocols",
                    "esd.staff_documents.fpcon",
                ),
            ),
        ),
        staff_docs_section_embed(
            title="Phase & Candidate Guides",
            description=(
                "Official documentation for ESD tryouts and candidate progression "
                "through the phase program."
            ),
            color=_COLOR,
            fields=(
                staff_docs_link(
                    "Tryout Guide",
                    "ESD Tryout Guide",
                    "esd.staff_documents.tryout_guide",
                ),
                staff_docs_link(
                    "Phase Guide",
                    "ESD Phase Guide",
                    "esd.staff_documents.phase_guide",
                ),
            ),
        ),
        staff_docs_section_embed(
            title="Training Materials",
            description=(
                "Official shared Directorate of Support standard training references "
                "for Executive Security Detail."
            ),
            color=_COLOR,
            fields=(
                staff_docs_link(
                    "General Standard Training",
                    "General Standard Training Guide",
                    "community.general_standard_training_guide",
                ),
            ),
        ),
        staff_docs_section_embed(
            title="Reports & Forms",
            description=(
                "Official operational reporting forms for Executive Security Detail staff."
            ),
            color=_COLOR,
            fields=(
                staff_docs_link(
                    "After Action Report",
                    "ESD After Action Reports",
                    "esd.staff_documents.after_action_report",
                ),
            ),
        ),
        staff_docs_handling_embed(unit_full=_UNIT, color=_COLOR),
    ]


def send_esd_staff_documents() -> None:
    run_announcer(
        webhook_key="WEBHOOK_ESD_STAFF_DOCUMENTS",
        username=c.BOT_ESD,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["esd"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_esd_staff_documents()

# === FILE FOOTER ===
# End of file: units/esd/staff_documents.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
