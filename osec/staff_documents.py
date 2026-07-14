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

GOOGLE_DRIVE_URL = (
    "https://drive.google.com/drive/folders/1LogIJ8er2ZjD2K39lPtoutdXKDoY2TY5?usp=sharing"
)
URL_TRYOUT_GUIDE = (
    "https://docs.google.com/document/d/1Fc7WK5voKnZ3hKlJQ_2O7ZDQFtht4xOHssqhJcmun30/edit?usp=sharing"
)
URL_PHASE_I = (
    "https://docs.google.com/document/d/1cGKf1xudnZ85K5oS9_esmXGPhWfGd-R3INE8SAWgcgM/edit?usp=sharing"
)
URL_PHASE_II = (
    "https://docs.google.com/document/d/14T05B4HiCdDact6nfTGu2AUk5DnFQYPsfyIe-Dwpb2U/edit?usp=sharing"
)
URL_STANDARD_TRAINING_REVAMP = (
    "https://docs.google.com/document/d/1PQC9MAqWDu1E3SfyFaxfwVfPR9bPUyaLjmEsvznzTyA/edit?usp=sharing"
)
URL_GENERAL_STANDARD_TRAINING_GUIDE = (
    "https://docs.google.com/document/d/1GV-c5lNL6mcx0Wuf-Jl5D2gT-H7rhgley9dQSMUNs6w/edit?usp=sharing"
)
URL_WEAPONS_STANDARD_TRAINING_GUIDE = (
    "https://docs.google.com/document/d/1nXByNDFTpbJe9nqpU6kLoifWaomedmYlo9lqagC2aDE/edit?usp=sharing"
)
URL_EVENT_GUIDE = (
    "https://docs.google.com/document/d/19cl5R83V_hFVrxUB1qOFpWFtV3B0CNXW0VJyETrUIJA/edit?usp=sharing"
)
URL_BASE_PATROL_EVENT_GUIDE = (
    "https://docs.google.com/document/d/1Lst9iRUTUtwJgBJwQz4bBjAhHPShZM3x11EMtlqkdmY/edit?usp=sharing"
)
URL_KILLHOUSE_EVENT_GUIDE = (
    "https://docs.google.com/document/d/1DTTVhVso1i5Hy1D3VbPhR-YEoGiZZWu5fFu-VSbmh8o/edit?usp=sharing"
)
URL_GATE_PATROL_EVENT_GUIDE = (
    "https://docs.google.com/document/d/1VrJb7lhuOoJFDJNY1VzN5jidg0Q-QtNe8ZujcoOnmac/edit?usp=sharing"
)
URL_COMBAT_TRAINING_GUIDE = (
    "https://docs.google.com/document/d/12nhTqR41kDZSuftVun0jWjs0PiIvbGA8zez80o3PjYM/edit?usp=sharing"
)
URL_COMMUNICATIONS_CONDUCT_CERTIFICATION_GUIDE = (
    "https://docs.google.com/document/d/1YqhSGzf3Y5ozGCASrj-9vACDWzodN3rZe0pN9rr43Ew/edit?usp=sharing"
)
URL_GATE_CERTIFICATION_GUIDE = (
    "https://docs.google.com/document/d/1hP7mbb8kH1gV56z6TSpmBduurdL6hlInGaefkJoikOE/edit?usp=sharing"
)
URL_HANDCUFF_CERTIFICATION_GUIDE = (
    "https://docs.google.com/document/d/133zQJvT1Slzs7S1Oou6fWpPLz_wdeq0tDr6Kf1z-YAY/edit?usp=sharing"
)


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
                    GOOGLE_DRIVE_URL,
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
                c.link_field("Tryout", "CIA OSEC | Tryout Guide", URL_TRYOUT_GUIDE),
                c.link_field("Phase I", "CIA OSEC | Phase I Guide", URL_PHASE_I),
                c.link_field("Phase II", "CIA OSEC | Phase II Guide", URL_PHASE_II),
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
                    URL_STANDARD_TRAINING_REVAMP,
                ),
                c.link_field(
                    "General Standard Training",
                    "CIA | General Standard Training Guide",
                    URL_GENERAL_STANDARD_TRAINING_GUIDE,
                ),
                c.link_field(
                    "Weapons Standard Training",
                    "CIA | Weapons Standard Training Guide",
                    URL_WEAPONS_STANDARD_TRAINING_GUIDE,
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
                c.link_field("Event Guide", "CIA OSEC | Event Guide", URL_EVENT_GUIDE),
                c.link_field(
                    "Base Patrol",
                    "CIA OSEC | Base Patrol Event Guide",
                    URL_BASE_PATROL_EVENT_GUIDE,
                ),
                c.link_field(
                    "Gate Patrol",
                    "CIA OSEC | Gate Patrol Event Guide",
                    URL_GATE_PATROL_EVENT_GUIDE,
                ),
                c.link_field(
                    "Killhouse",
                    "CIA OSEC | Killhouse Event Guide",
                    URL_KILLHOUSE_EVENT_GUIDE,
                ),
                c.link_field(
                    "Combat Training",
                    "CIA OSEC | Combat Training Guide",
                    URL_COMBAT_TRAINING_GUIDE,
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
                    URL_COMMUNICATIONS_CONDUCT_CERTIFICATION_GUIDE,
                ),
                c.link_field(
                    "Gate",
                    "CIA OSEC | Gate Certification Guide",
                    URL_GATE_CERTIFICATION_GUIDE,
                ),
                c.link_field(
                    "Handcuff",
                    "CIA OSEC | Handcuff Certification Guide",
                    URL_HANDCUFF_CERTIFICATION_GUIDE,
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
