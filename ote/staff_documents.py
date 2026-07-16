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
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Update OTE tryout guide and reorganize staff documents. (#12)
#   - 2026-07-15 | docshamxo | Title Case sections without numbers; shared handling copy.
# === END FILE HEADER ===

"""
CIA OTE staff documents announcer.

Posts official Office of Training & Education staff guides, training material,
and personnel records to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.hero_embed(
            title="STAFF DOCUMENTS",
            unit="Office of Training & Education",
            supporting=(
                "Official repository for authorized OTE staff documentation. "
                "Access is strictly limited to authorized personnel."
            ),
            color=c.COLOR_OTE,
            logo=c.LOGOS["ote"],
        ),
        c.embed(
            title="Central Repository",
            description=(
                "Primary Google Drive folder for applications, forms, guides, "
                "and supporting files referenced throughout this channel."
            ),
            color=c.COLOR_OTE,
            fields=(
                c.link_field(
                    "Google Drive",
                    "CIA OTE | Google Drive",
                    c.url("ote.staff_documents.google_drive"),
                    "Authorized OTE staff only.",
                ),
            ),
        ),
        c.embed(
            title="Policy & Handbook",
            description="Core references for structure, expectations, and chain of command.",
            color=c.COLOR_OTE,
            fields=(
                c.link_field(
                    "Staff Handbook",
                    "CIA OTE | Staff Handbook",
                    c.url("ote.staff_documents.staff_handbook"),
                    "Authorized OTE staff only.",
                ),
                c.link_field(
                    "General Information",
                    "CIA OTE | General Information & Chain of Command",
                    c.url("ote.staff_documents.general_info_coc"),
                    "Authorized OTE staff only.",
                ),
            ),
        ),
        c.embed(
            title="Tryouts & Ceremonies",
            description="Candidate screening and official ceremony procedures.",
            color=c.COLOR_OTE,
            fields=(
                c.link_field(
                    "Tryout Guide",
                    "CIA OTE | Tryout Guide",
                    c.url("ote.staff_documents.tryout_guide"),
                    "Authorized OTE staff only.",
                ),
                c.link_field(
                    "Graduation",
                    "CIA OTE | Graduation Ceremony Procedures",
                    c.url("ote.staff_documents.graduation_ceremony_procedures"),
                    "Authorized OTE staff only.",
                ),
            ),
        ),
        c.embed(
            title="Training Materials",
            description="Standard instruction guides used for OTE training delivery.",
            color=c.COLOR_OTE,
            fields=(
                c.link_field(
                    "Standard Training",
                    "CIA OTE | Standard Training Guide",
                    c.url("ote.staff_documents.standard_training_guide"),
                    "Authorized OTE staff only.",
                ),
                c.link_field(
                    "Weapons ST",
                    "CIA OTE | Weapons ST Guide",
                    c.url("ote.staff_documents.weapons_st_guide"),
                    "Authorized OTE staff only.",
                ),
            ),
        ),
        c.embed(
            title="Personnel Records",
            description="Live tracking for staff assignments and program records.",
            color=c.COLOR_OTE,
            fields=(
                c.link_field(
                    "Staff Database",
                    "CIA OTE | ORBAT",
                    c.url("ote.staff_documents.staff_database"),
                    "Authorized OTE staff only.",
                ),
            ),
        ),
        c.classification_handling_embed(
            unit="OTE",
            authority="CIA Directorate of Support",
            color=c.COLOR_OTE,
        ),
        c.disclaimer_embed(classified=True, color=c.COLOR_OTE),
    ]


def send_ote_staff_documents() -> None:
    run_announcer(
        webhook_key="WEBHOOK_OTE_STAFF_DOCUMENTS",
        username=c.BOT_OTE,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["ote"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_ote_staff_documents()

# === FILE FOOTER ===
# End of file: ote/staff_documents.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
