# === FILE HEADER ===
# Title: Staff Documents
# Path: ote/staff_documents.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
# === END FILE HEADER ===

"""
CIA OTE staff documents announcer.

Posts official Office of Training & Education staff guides, training material,
and personnel records to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_OTE_STAFF_DOCUMENTS")

def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.embed(
            title="STAFF DOCUMENTS",
            description=(
                "*Central Intelligence Agency · Office of Training & Education*\n\n"
                f"*{c.OTE_MOTTO}*\n\n"
                "Official and classified CIA staff documents are maintained in this channel.\n"
                "Access is **strictly limited** to authorized personnel."
            ),
            logo=c.LOGOS["ote"],
        ),
        c.embed(
            title="Central Repository",
            description="Primary folder for all OTE staff files, guides, and forms.",
            fields=(
                c.link_field(
                    "Google Drive",
                    "CIA OTE Google Drive",
                    c.url('ote.staff_documents.google_drive'),
                    "Applications, feedback forms, guides, and shared resources.",
                ),
            ),
        ),
        c.embed(
            title="Program & Policy",
            description="Core references for staff structure, policy, and onboarding.",
            fields=(
                c.link_field(
                    "Staff Handbook",
                    "CIA OTE | Officer Training Program Staff Handbook",
                    c.url('ote.staff_documents.staff_handbook'),
                    "Phase guides.",
                ),
                c.link_field(
                    "General Information",
                    "CIA OTE | General Information & Chain of Command",
                    c.url('ote.staff_documents.general_info_coc'),
                ),
                c.link_field(
                    "Tryout Document",
                    "OTE Tryout Document",
                    c.url('ote.staff_documents.tryout_document'),
                ),
                c.link_field(
                    "Graduation",
                    "CIA | Graduation Ceremony Procedures",
                    c.url('ote.staff_documents.graduation_ceremony_procedures'),
                    "Planning and conducting official OTE graduation ceremonies.",
                ),
            ),
        ),
        c.embed(
            title="Training Guides",
            description="Standard training materials for OTE instruction.",
            fields=(
                c.link_field(
                    "Standard Training",
                    "CIA OTE | Standard Training Guide",
                    c.url('ote.staff_documents.standard_training_guide'),
                ),
                c.link_field(
                    "Weapons ST",
                    "CIA OTE | Weapons ST Guide",
                    c.url('ote.staff_documents.weapons_st_guide'),
                ),
            ),
        ),
        c.embed(
            title="Staff Records",
            description="Live database for personnel tracking and assignments.",
            fields=(
                c.link_field(
                    "Staff Database",
                    "CIA OTE | ORBAT",
                    c.url('ote.staff_documents.staff_database'),
                    "Official staff records, assignments, and tracking.",
                ),
            ),
        ),
        c.embed(
            title="Important Notice",
            description=(
                "Unauthorized access, sharing, or distribution is **prohibited** "
                "and may result in disciplinary action.\n\n"
                "Questions may be forwarded to **OTE HICOM**."
            ),
        ),
        c.disclaimer_embed(classified=True),
    ]


def send_ote_staff_documents() -> None:
    c.send_webhook(
        WEBHOOK_URL,
        _build_embeds(),
        username=c.BOT_OTE,
        files=[c.logo_file(c.LOGOS["ote"])],
    )


if __name__ == "__main__":
    send_ote_staff_documents()

# === FILE FOOTER ===
# End of file: ote/staff_documents.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
