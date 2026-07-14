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
# === END FILE HEADER ===

"""
CIA OSEC staff documents announcer.

Posts official Office of Security staff guides, training material, event
documentation, and certification resources to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_OSEC_STAFF_DOCUMENTS")

def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.embed(
            title="STAFF DOCUMENTS",
            description=(
                "*Central Intelligence Agency · Office of Security*\n\n"
                f"*{c.OSEC_MOTTO}*\n\n"
                "This channel serves as the official repository for authorized Office of "
                "Security staff documentation. Access is **strictly limited** to "
                "authorized personnel. Review, use, and handle all materials in "
                "accordance with their classification level."
            ),
            logo=c.LOGOS["osec"],
        ),
        c.embed(
            title="Central Repository",
            description=(
                "Primary Google Drive folder containing OSEC handbooks, phase guides, "
                "event documentation, certifications, ORBAT files, and internal forms."
            ),
            fields=(
                c.link_field(
                    "Google Drive",
                    "CIA OSEC | Google Drive",
                    c.url('osec.staff_documents.google_drive'),
                    "Authorized OSEC staff only.",
                ),
            ),
        ),
        c.embed(
            title="Phase & Candidate Guides",
            description=(
                "Official documentation for Security Phase tryouts, candidate progression, "
                "and phase training requirements."
            ),
            fields=(
                c.link_field("Tryout", "CIA OSEC | Tryout Guide", c.url('osec.staff_documents.tryout_guide')),
                c.link_field("Phase I", "CIA OSEC | Phase I Guide", c.url('osec.staff_documents.phase_i')),
                c.link_field("Phase II", "CIA OSEC | Phase II Guide", c.url('osec.staff_documents.phase_ii')),
            ),
        ),
        c.embed(
            title="Standard Training Program",
            description=(
                "Official documentation for the Office of Security Standard Training "
                "system and instructor reference material."
            ),
            fields=(
                c.link_field(
                    "Training Revamp",
                    "CIA | Standard Training Revamp",
                    c.url('osec.staff_documents.standard_training_revamp'),
                ),
                c.link_field(
                    "General Standard Training",
                    "CIA | General Standard Training Guide",
                    c.url('osec.staff_documents.general_standard_training_guide'),
                ),
                c.link_field(
                    "Weapons Standard Training",
                    "CIA | Weapons Standard Training Guide",
                    c.url('osec.staff_documents.weapons_standard_training_guide'),
                ),
            ),
        ),
        c.embed(
            title="Event Guides",
            description=(
                "Official guides for planning, hosting, and supervising Office of "
                "Security events and operational exercises."
            ),
            fields=(
                c.link_field("Event Guide", "CIA OSEC | Event Guide", c.url('osec.staff_documents.event_guide')),
                c.link_field(
                    "Base Patrol",
                    "CIA OSEC | Base Patrol Event Guide",
                    c.url('osec.staff_documents.base_patrol_event_guide'),
                ),
                c.link_field(
                    "Gate Patrol",
                    "CIA OSEC | Gate Patrol Event Guide",
                    c.url('osec.staff_documents.gate_patrol_event_guide'),
                ),
                c.link_field(
                    "Killhouse",
                    "CIA OSEC | Killhouse Event Guide",
                    c.url('osec.staff_documents.killhouse_event_guide'),
                ),
                c.link_field(
                    "Combat Training",
                    "CIA OSEC | Combat Training Guide",
                    c.url('osec.staff_documents.combat_training_guide'),
                ),
            ),
        ),
        c.embed(
            title="Certification Guides",
            description=(
                "Official guides for Office of Security staff certifications and "
                "qualification standards."
            ),
            fields=(
                c.link_field(
                    "Communications & Conduct",
                    "CIA OSEC | Communications & Conduct Certification Guide",
                    c.url('osec.staff_documents.communications_conduct_certification_guide'),
                ),
                c.link_field(
                    "Gate",
                    "CIA OSEC | Gate Certification Guide",
                    c.url('osec.staff_documents.gate_certification_guide'),
                ),
                c.link_field(
                    "Handcuff",
                    "CIA OSEC | Handcuff Certification Guide",
                    c.url('osec.staff_documents.handcuff_certification_guide'),
                ),
            ),
        ),
        c.embed(
            title="Classification & Handling Notice",
            description=(
                "All documents listed in this channel are classified up to the **SECRET** "
                "level unless otherwise marked.\n\n"
                "Unauthorized disclosure, redistribution, or leaking of any restricted "
                "material will result in a **BLACKLIST** from the **CIA Office of Security**.\n\n"
                "Handle all staff documents responsibly. Do not share materials outside "
                "authorized channels or personnel."
            ),
        ),
        c.disclaimer_embed(classified=True),
    ]


def send_osec_staff_documents() -> None:
    c.send_webhook(
        WEBHOOK_URL,
        _build_embeds(),
        username=c.BOT_DS,
        files=[c.logo_file(c.LOGOS["osec"])],
    )


if __name__ == "__main__":
    send_osec_staff_documents()

# === FILE FOOTER ===
# End of file: osec/staff_documents.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
