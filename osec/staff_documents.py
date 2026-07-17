# === FILE HEADER ===
# Title: Staff Documents
# Path: osec/staff_documents.py
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
# === END FILE HEADER ===

"""
CIA OSEC staff documents announcer.

Posts the Office of Security staff Drive index and core phase guides.
Detailed TTP / event / certification packs live in the Drive folder (need-to-know).
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
            supporting=(
                "Official repository for authorized Office of Security staff documentation. "
                "Access is strictly limited to authorized personnel."
            ),
            color=c.COLOR_OSEC,
            logo=c.LOGOS["osec"],
        ),
        c.embed(
            title="Central Repository",
            description=(
                "Primary Google Drive folder containing OSEC handbooks, phase guides, "
                "event documentation, certifications, ORBAT files, and internal forms. "
                "Use the Drive index as the source of truth for TTP titles not listed here."
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    "Google Drive",
                    "DS Community | OSEC Google Drive",
                    c.url("osec.staff_documents.google_drive"),
                    c.marking_note("STAFF", "Authorized OSEC staff only."),
                ),
            ),
        ),
        c.embed(
            title="Phase & Candidate Guides",
            description=(
                "Core documentation for Security Phase tryouts and candidate progression. "
                "Additional training, event, and certification guides are in Drive."
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    "Tryout Guide",
                    "DS Community | OSEC Tryout Guide",
                    c.url("osec.staff_documents.tryout_guide"),
                    c.marking_note("STAFF", "Authorized OSEC staff only."),
                ),
                c.link_field(
                    "Phase I ΓÇö Foundation",
                    "DS Community | OSEC Phase I Guide",
                    c.url("osec.staff_documents.phase_i"),
                    c.marking_note("STAFF", "Authorized OSEC staff only."),
                ),
                c.link_field(
                    "Phase II ΓÇö Intermediate",
                    "DS Community | OSEC Phase II Guide",
                    c.url("osec.staff_documents.phase_ii"),
                    c.marking_note("STAFF", "Authorized OSEC staff only."),
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
# End of file: osec/staff_documents.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
