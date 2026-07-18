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
# === END FILE HEADER ===

"""
CIA OSEC staff documents announcer.

Posts official Office of Security staff guides, training material, event
documentation, and certification resources to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.hero_embed(
            title="STAFF DOCUMENTS",
            unit="Office of Security",
            supporting="Authorized OSEC staff documentation index. Need-to-know access only.",
            color=c.COLOR_OSEC,
            logo=c.LOGOS["osec"],
        ),
        c.embed(
            title="Central Repository",
            description=(
                "Primary Google Drive folder containing OSEC handbooks, phase guides, "
                "event documentation, certifications, ORBAT files, and internal forms."
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    "Google Drive",
                    "DS Community | OSEC Google Drive",
                    c.url("osec.staff_documents.google_drive"),
                    c.marking_note("STAFF"),
                ),
            ),
        ),
        c.embed(
            title="Phase & Candidate Guides",
            description=(
                "Official documentation for Security Phase tryouts, candidate progression, "
                "and phase training requirements."
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    "Tryout Guide",
                    "DS Community | OSEC Tryout Guide",
                    c.url("osec.staff_documents.tryout_guide"),
                    c.marking_note("STAFF"),
                ),
                c.link_field(
                    "Phase I - Foundation",
                    "DS Community | OSEC Phase I Guide",
                    c.url("osec.staff_documents.phase_i"),
                    c.marking_note("STAFF"),
                ),
                c.link_field(
                    "Phase II - Intermediate",
                    "DS Community | OSEC Phase II Guide",
                    c.url("osec.staff_documents.phase_ii"),
                    c.marking_note("STAFF"),
                ),
            ),
        ),
        c.embed(
            title="Standard Training",
            description=(
                "Official documentation for the Office of Security Standard Training "
                "system and shared Directorate of Support training references."
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    "Training Revamp",
                    "DS Community | OSEC Standard Training Revamp",
                    c.url("osec.staff_documents.standard_training_revamp"),
                    c.marking_note("STAFF"),
                ),
                c.link_field(
                    "General Standard Training",
                    "DS Community | General Standard Training Guide",
                    c.url("community.general_standard_training_guide"),
                    c.marking_note("STAFF"),
                ),
                c.link_field(
                    "Weapons Standard Training",
                    "DS Community | OSEC Weapons Standard Training Guide",
                    c.url("osec.staff_documents.weapons_standard_training_guide"),
                    c.marking_note("STAFF"),
                ),
            ),
        ),
        c.embed(
            title="Event Guides",
            description=(
                "Official guides for planning, hosting, and supervising Office of "
                "Security events and operational exercises."
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    "Event Guide",
                    "DS Community | OSEC Event Guide",
                    c.url("osec.staff_documents.event_guide"),
                    c.marking_note("STAFF"),
                ),
                c.link_field(
                    "Base Patrol",
                    "DS Community | OSEC Base Patrol Event Guide",
                    c.url("osec.staff_documents.base_patrol_event_guide"),
                    c.marking_note("STAFF"),
                ),
                c.link_field(
                    "Gate Patrol",
                    "DS Community | OSEC Gate Patrol Event Guide",
                    c.url("osec.staff_documents.gate_patrol_event_guide"),
                    c.marking_note("STAFF"),
                ),
                c.link_field(
                    "Killhouse",
                    "DS Community | OSEC Killhouse Event Guide",
                    c.url("osec.staff_documents.killhouse_event_guide"),
                    c.marking_note("STAFF"),
                ),
                c.link_field(
                    "Combat Training",
                    "DS Community | OSEC Combat Training Guide",
                    c.url("osec.staff_documents.combat_training_guide"),
                    c.marking_note("STAFF"),
                ),
            ),
        ),
        c.embed(
            title="Certification Guides",
            description=(
                "Official guides for Office of Security staff certifications and "
                "qualification standards."
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    "Communications & Conduct",
                    "DS Community | OSEC Communications & Conduct Certification Guide",
                    c.url("osec.staff_documents.communications_conduct_certification_guide"),
                    c.marking_note("STAFF"),
                ),
                c.link_field(
                    "Gate",
                    "DS Community | OSEC Gate Certification Guide",
                    c.url("osec.staff_documents.gate_certification_guide"),
                    c.marking_note("STAFF"),
                ),
                c.link_field(
                    "Handcuff",
                    "DS Community | OSEC Handcuff Certification Guide",
                    c.url("osec.staff_documents.handcuff_certification_guide"),
                    c.marking_note("STAFF"),
                ),
            ),
        ),
        c.classification_handling_embed(
            unit="Office of Security",
            authority="CIA Office of Security",
            color=c.COLOR_OSEC,
            restricted=True,
        ),
        c.disclaimer_embed(staff=True, color=c.COLOR_OSEC),
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
