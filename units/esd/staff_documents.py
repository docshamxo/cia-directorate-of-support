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
# === END FILE HEADER ===

"""
CIA ESD staff documents announcer.

Posts official Executive Security Detail staff guides and shared Drive
resources to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.hero_embed(
            title="STAFF DOCUMENTS",
            unit="Executive Security Detail",
            supporting="Authorized ESD staff documentation index. Need-to-know access only.",
            color=c.COLOR_ESD,
            logo=c.LOGOS["esd"],
        ),
        c.embed(
            title="Central Repository",
            description="Primary folder for all ESD staff files, guides, and forms.",
            color=c.COLOR_ESD,
            fields=(
                c.link_field(
                    "Google Drive",
                    "DS Community | ESD Google Drive",
                    c.url("esd.staff_documents.google_drive"),
                    c.marking_note("STAFF"),
                ),
            ),
        ),
        c.embed(
            title="Handbook & Force Protection",
            description="Core ESD handbook and force protection condition protocols.",
            color=c.COLOR_ESD,
            fields=(
                c.link_field(
                    "Official Handbook",
                    "DS Community | ESD Official Handbook",
                    c.url("esd.staff_documents.handbook"),
                    c.marking_note("STAFF"),
                ),
                c.link_field(
                    "FPCON Protocols",
                    "DS Community | ESD Force Protection Conditions and Protocols",
                    c.url("esd.staff_documents.fpcon"),
                    c.marking_note("STAFF"),
                ),
            ),
        ),
        c.embed(
            title="Phase & Tryout Guides",
            description="Core documentation for ESD tryouts and candidate progression.",
            color=c.COLOR_ESD,
            fields=(
                c.link_field(
                    "Tryout Guide",
                    "DS Community | ESD Tryout Guide",
                    c.url("esd.staff_documents.tryout_guide"),
                    c.marking_note("STAFF"),
                ),
                c.link_field(
                    "Phase Guide",
                    "DS Community | ESD Phase Guide",
                    c.url("esd.staff_documents.phase_guide"),
                    c.marking_note("STAFF"),
                ),
            ),
        ),
        c.embed(
            title="Training Materials",
            description="Shared Directorate of Support standard training references.",
            color=c.COLOR_ESD,
            fields=(
                c.link_field(
                    "General Standard Training",
                    "DS Community | General Standard Training Guide",
                    c.url("community.general_standard_training_guide"),
                    c.marking_note("STAFF"),
                ),
            ),
        ),
        c.classification_handling_embed(
            unit="ESD",
            authority="CIA Directorate of Support",
            color=c.COLOR_ESD,
        ),
        c.disclaimer_embed(staff=True, color=c.COLOR_ESD),
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
