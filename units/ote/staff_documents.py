# === FILE HEADER ===
# Title: Staff Documents
# Path: units/ote/staff_documents.py
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
#   - 2026-07-17 | docshamxo | Replace single Staff Handbook with Phase I/II/III documents.
#   - 2026-07-17 | docshamxo | Text marking notes and clearer field labels.
#   - 2026-07-17 | docshamxo | Use DS Community link labels (brand/legal).
#   - 2026-07-17 | docshamxo | Consolidate sections; shared Marking: STAFF notes.
#   - 2026-07-17 | docshamxo | Add General Standard Training Guide (shared community link).
#   - 2026-08-30 | docshamxo | Drop duplicate General Information; regroup training links.
#   - 2026-09-08 | docshamxo | Refactor onto shared staff-docs frame; fix CIA DS | labels.
# === END FILE HEADER ===

"""
CIA OTE staff documents announcer.

Posts official Office of Training & Education staff guides, training material,
and personnel records to a Discord webhook.
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

_UNIT = "Office of Training & Education"
_ABBREV = "OTE"
_COLOR = c.COLOR_OTE


def _build_embeds() -> list[c.discord.Embed]:
    return [
        staff_docs_hero_embed(
            unit_full=_UNIT,
            unit_abbrev=_ABBREV,
            color=_COLOR,
            logo=c.LOGOS["ote"],
        ),
        staff_docs_central_embed(
            unit_abbrev=_ABBREV,
            drive_url_key="ote.staff_documents.google_drive",
            drive_link_name="OTE Google Drive",
            color=_COLOR,
            extra_fields=(
                staff_docs_link(
                    "General Information & CoC",
                    "OTE General Information & Chain of Command",
                    "ote.staff_documents.general_info_coc",
                ),
            ),
        ),
        staff_docs_section_embed(
            title="Phase Documents",
            description=(
                "Official OTP Staff Handbook documents covering each phase of the "
                "Office of Training & Education program."
            ),
            color=_COLOR,
            fields=(
                staff_docs_link(
                    "Phase I",
                    "OTE OTP Staff Handbook Phase I",
                    "ote.staff_documents.phase_i",
                ),
                staff_docs_link(
                    "Phase II",
                    "OTE OTP Staff Handbook Phase II",
                    "ote.staff_documents.phase_ii",
                ),
                staff_docs_link(
                    "Phase III",
                    "OTE OTP Staff Handbook Phase III",
                    "ote.staff_documents.phase_iii",
                ),
            ),
        ),
        staff_docs_section_embed(
            title="Tryouts & Ceremonies",
            description=(
                "Official documentation for candidate screening and graduation "
                "ceremony procedures."
            ),
            color=_COLOR,
            fields=(
                staff_docs_link(
                    "Tryout Guide",
                    "OTE Tryout Guide",
                    "ote.staff_documents.tryout_guide",
                ),
                staff_docs_link(
                    "Graduation",
                    "OTE Graduation Ceremony Procedures",
                    "ote.staff_documents.graduation_ceremony_procedures",
                ),
            ),
        ),
        staff_docs_section_embed(
            title="Training Materials",
            description=(
                "Official OTE training guides and shared Directorate of Support "
                "standard training references."
            ),
            color=_COLOR,
            fields=(
                staff_docs_link(
                    "Standard Training",
                    "OTE Standard Training Guide",
                    "ote.staff_documents.standard_training_guide",
                ),
                staff_docs_link(
                    "Weapons Standard Training",
                    "OTE Weapons Standard Training Guide",
                    "ote.staff_documents.weapons_st_guide",
                ),
                staff_docs_link(
                    "General Standard Training",
                    "General Standard Training Guide",
                    "community.general_standard_training_guide",
                ),
            ),
        ),
        staff_docs_section_embed(
            title="Personnel Records",
            description=(
                "Official documentation for staff assignments and program tracking "
                "within the Office of Training & Education."
            ),
            color=_COLOR,
            fields=(
                staff_docs_link(
                    "Staff Database (ORBAT)",
                    "OTE Staff Database (ORBAT)",
                    "ote.staff_documents.staff_database",
                ),
            ),
        ),
        staff_docs_handling_embed(unit_full=_UNIT, color=_COLOR),
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
# End of file: units/ote/staff_documents.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
