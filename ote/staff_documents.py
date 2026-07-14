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

STAFF_HANDBOOK_URL = (
    "https://docs.google.com/document/d/1Nhi3xnirH192rIdbMCrGGH5pnhLywQ9EhWxPCoRbY9s/edit?usp=sharing"
)
STAFF_DATABASE_URL = (
    "https://docs.google.com/spreadsheets/d/17Yw1oby46r9pGJXzWSs2cPh3DRaj-ktUQ728GDi09x0/edit?usp=sharing"
)
TRYOUT_DOCUMENT_URL = (
    "https://docs.google.com/document/d/1tNns_L-M1i3SBl7SUwx_Zk1U2Jf8iOU1zRL8zJUnbQQ/edit?usp=drivesdk"
)
GOOGLE_DRIVE_URL = (
    "https://drive.google.com/drive/folders/11g2H9zeEwFbyO2a6dkxpmSGN0qGR4Oe1?usp=sharing"
)
GENERAL_INFO_COC_URL = (
    "https://docs.google.com/document/d/1gZO3E9X_dbNIjJJQc5wsKgryyH6uTryfjQHLSKbq4EA/edit?usp=sharing"
)
STANDARD_TRAINING_GUIDE_URL = (
    "https://docs.google.com/document/d/19M5hFnP5jTy8MlOYUcZ7DqmxAEQN-HDT_thV8TpnaB8/edit?usp=sharing"
)
WEAPONS_ST_GUIDE_URL = (
    "https://docs.google.com/document/d/17v8Z-koVCxP2cTopvU8QYJaTaXbBB7RujmPd7tk-Luk/edit?usp=sharing"
)
GRADUATION_CEREMONY_PROCEDURES_URL = (
    "https://docs.google.com/document/d/1NR61wNgfyEnPiDQ7jZB8NwS8CUCFq7nt1aDN2y6uwKA/edit?usp=sharing"
)


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
                    GOOGLE_DRIVE_URL,
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
                    STAFF_HANDBOOK_URL,
                    "Phase guides.",
                ),
                c.link_field(
                    "General Information",
                    "CIA OTE | General Information & Chain of Command",
                    GENERAL_INFO_COC_URL,
                ),
                c.link_field(
                    "Tryout Document",
                    "OTE Tryout Document",
                    TRYOUT_DOCUMENT_URL,
                ),
                c.link_field(
                    "Graduation",
                    "CIA | Graduation Ceremony Procedures",
                    GRADUATION_CEREMONY_PROCEDURES_URL,
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
                    STANDARD_TRAINING_GUIDE_URL,
                ),
                c.link_field(
                    "Weapons ST",
                    "CIA OTE | Weapons ST Guide",
                    WEAPONS_ST_GUIDE_URL,
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
                    STAFF_DATABASE_URL,
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
