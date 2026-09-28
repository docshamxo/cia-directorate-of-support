# === FILE HEADER ===
# Title: Staff Documents
# Path: units/osec/staff_documents.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Unify staff-docs template, link grammar, unit-color closers.
#   - 2026-07-17 | docshamxo | Prefer Drive root + fewer TTP titles; STAFF markings.
#   - 2026-07-17 | docshamxo | Text marking notes and clearer field labels.
#   - 2026-07-17 | docshamxo | Use DS Community link labels (brand/legal).
#   - 2026-07-17 | docshamxo | Replace mojibake em dashes with ASCII in phase titles.
#   - 2026-07-17 | docshamxo | Add General Standard Training Guide (shared community link).
#   - 2026-07-18 | docshamxo | Restore full OSEC staff training, event, and cert link list.
#   - 2026-08-04 | docshamxo | Remove Unofficial Community disclaimer from OSEC staff docs.
#   - 2026-09-08 | docshamxo | Refactor onto shared staff-docs frame builders.
# === END FILE HEADER ===

"""
CIA OSEC staff documents announcer.

Posts official Office of Security staff guides, training material, event
documentation, and certification resources to a Discord webhook.
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

_UNIT = "Office of Security"
_ABBREV = "OSEC"
_COLOR = c.COLOR_OSEC


def _build_embeds() -> list[c.discord.Embed]:
    return [
        staff_docs_hero_embed(
            unit_full=_UNIT,
            unit_abbrev=_ABBREV,
            color=_COLOR,
            logo=c.LOGOS["osec"],
        ),
        staff_docs_central_embed(
            unit_abbrev=_ABBREV,
            drive_url_key="osec.staff_documents.google_drive",
            drive_link_name="OSEC Google Drive",
            color=_COLOR,
        ),
        staff_docs_section_embed(
            title="Phase & Candidate Guides",
            description=(
                "Official documentation for Security Phase tryouts, candidate progression, "
                "and phase training requirements."
            ),
            color=_COLOR,
            fields=(
                staff_docs_link(
                    "Tryout Guide",
                    "OSEC Tryout Guide",
                    "osec.staff_documents.tryout_guide",
                ),
                staff_docs_link(
                    "Phase I - Foundation",
                    "OSEC Phase I Guide",
                    "osec.staff_documents.phase_i",
                ),
                staff_docs_link(
                    "Phase II - Intermediate",
                    "OSEC Phase II Guide",
                    "osec.staff_documents.phase_ii",
                ),
            ),
        ),
        staff_docs_section_embed(
            title="Training Materials",
            description=(
                "Official documentation for the Office of Security Standard Training "
                "system and shared Directorate of Support training references."
            ),
            color=_COLOR,
            fields=(
                staff_docs_link(
                    "Training Revamp",
                    "OSEC Standard Training Revamp",
                    "osec.staff_documents.standard_training_revamp",
                ),
                staff_docs_link(
                    "General Standard Training",
                    "General Standard Training Guide",
                    "community.general_standard_training_guide",
                ),
                staff_docs_link(
                    "Weapons Standard Training",
                    "OSEC Weapons Standard Training Guide",
                    "osec.staff_documents.weapons_standard_training_guide",
                ),
            ),
        ),
        staff_docs_section_embed(
            title="Event Guides",
            description=(
                "Official guides for planning, hosting, and supervising Office of "
                "Security events and operational exercises."
            ),
            color=_COLOR,
            fields=(
                staff_docs_link(
                    "Event Guide",
                    "OSEC Event Guide",
                    "osec.staff_documents.event_guide",
                ),
                staff_docs_link(
                    "Base Patrol",
                    "OSEC Base Patrol Event Guide",
                    "osec.staff_documents.base_patrol_event_guide",
                ),
                staff_docs_link(
                    "Gate Patrol",
                    "OSEC Gate Patrol Event Guide",
                    "osec.staff_documents.gate_patrol_event_guide",
                ),
                staff_docs_link(
                    "Killhouse",
                    "OSEC Killhouse Event Guide",
                    "osec.staff_documents.killhouse_event_guide",
                ),
                staff_docs_link(
                    "Combat Training",
                    "OSEC Combat Training Guide",
                    "osec.staff_documents.combat_training_guide",
                ),
            ),
        ),
        staff_docs_section_embed(
            title="Certification Guides",
            description=(
                "Official guides for Office of Security staff certifications and "
                "qualification standards."
            ),
            color=_COLOR,
            fields=(
                staff_docs_link(
                    "Communications & Conduct",
                    "OSEC Communications & Conduct Certification Guide",
                    "osec.staff_documents.communications_conduct_certification_guide",
                ),
                staff_docs_link(
                    "Gate",
                    "OSEC Gate Certification Guide",
                    "osec.staff_documents.gate_certification_guide",
                ),
                staff_docs_link(
                    "Handcuff",
                    "OSEC Handcuff Certification Guide",
                    "osec.staff_documents.handcuff_certification_guide",
                ),
            ),
        ),
        staff_docs_handling_embed(unit_full=_UNIT, color=_COLOR),
    ]


def send_osec_staff_documents() -> None:
    run_announcer(
        webhook_key="WEBHOOK_OSEC_STAFF_DOCUMENTS",
        username=c.BOT_OSEC,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["osec"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_osec_staff_documents()

# === FILE FOOTER ===
# End of file: units/osec/staff_documents.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
