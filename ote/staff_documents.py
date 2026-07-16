# === FILE HEADER ===
# Title: Staff Documents
# Path: ote/staff_documents.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Reorganize OTE staff documents channel; update tryout guide. (#11)
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
                "Official repository for authorized OTE staff documentation.\n"
                "Use the sections below in order: **Drive hub → policy → "
                "tryouts & ceremonies → training → records**.\n\n"
                "Access is **strictly limited** to authorized personnel."
            ),
            color=c.COLOR_OTE,
            logo=c.LOGOS["ote"],
        ),
        c.embed(
            title="1 · Drive Hub",
            description=(
                "Start here. The shared Drive holds applications, forms, guides, "
                "and supporting files referenced throughout this channel."
            ),
            color=c.COLOR_OTE,
            fields=(
                c.link_field(
                    "Google Drive",
                    "CIA OTE | Google Drive",
                    c.url("ote.staff_documents.google_drive"),
                    "Primary folder for all OTE staff files.",
                ),
            ),
        ),
        c.embed(
            title="2 · Policy & Handbook",
            description="Core references for structure, expectations, and chain of command.",
            color=c.COLOR_OTE,
            fields=(
                c.link_field(
                    "Staff Handbook",
                    "CIA OTE | Officer Training Program Staff Handbook",
                    c.url("ote.staff_documents.staff_handbook"),
                    "Program structure, phases, and staff standards.",
                ),
                c.link_field(
                    "General Information",
                    "CIA OTE | General Information & Chain of Command",
                    c.url("ote.staff_documents.general_info_coc"),
                    "Organization overview and reporting structure.",
                ),
            ),
        ),
        c.embed(
            title="3 · Tryouts & Ceremonies",
            description="Candidate screening and official ceremony procedures.",
            color=c.COLOR_OTE,
            fields=(
                c.link_field(
                    "Tryout Guide",
                    "CIA OTE | Tryout Guide",
                    c.url("ote.staff_documents.tryout_guide"),
                    "Hosting standards, phases, and evaluation guidance.",
                ),
                c.link_field(
                    "Graduation",
                    "CIA | Graduation Ceremony Procedures",
                    c.url("ote.staff_documents.graduation_ceremony_procedures"),
                    "Planning and conducting official OTE graduations.",
                ),
            ),
        ),
        c.embed(
            title="4 · Training Materials",
            description="Standard instruction guides used for OTE training delivery.",
            color=c.COLOR_OTE,
            fields=(
                c.link_field(
                    "Standard Training",
                    "CIA OTE | Standard Training Guide",
                    c.url("ote.staff_documents.standard_training_guide"),
                    "General ST curriculum and hosting reference.",
                ),
                c.link_field(
                    "Weapons ST",
                    "CIA OTE | Weapons ST Guide",
                    c.url("ote.staff_documents.weapons_st_guide"),
                    "Weapons standard training curriculum and reference.",
                ),
            ),
        ),
        c.embed(
            title="5 · Personnel Records",
            description="Live tracking for staff assignments and program records.",
            color=c.COLOR_OTE,
            fields=(
                c.link_field(
                    "Staff Database",
                    "CIA OTE | ORBAT",
                    c.url("ote.staff_documents.staff_database"),
                    "Official staff records, assignments, and tracking.",
                ),
            ),
        ),
        c.embed(
            title="Classification & Handling Notice",
            description=(
                "All documents listed in this channel are intended for **authorized OTE "
                "personnel only**.\n\n"
                "Unauthorized disclosure, redistribution, or leaking of any restricted "
                "material may result in disciplinary action under the "
                "**CIA Directorate of Support**.\n\n"
                "Questions may be forwarded to **OTE HICOM**. Do not share materials "
                "outside authorized channels or personnel."
            ),
            color=c.COLOR_OTE,
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
