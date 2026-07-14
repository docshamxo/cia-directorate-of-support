"""
CIA OSEC Security Phase Program information announcer.

Posts welcome, training, and required reading for newly accepted
Security Phase Program candidates to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_OSEC_SPP_INFORMATION")

def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.embed(
            title="SECURITY PHASE PROGRAM",
            description=(
                "*Central Intelligence Agency · Office of Security*\n\n"
                f"*{c.OSEC_MOTTO}*\n\n"
                "Welcome to the **Security Phase Program (SPP)**. This channel provides "
                "orientation, training requirements, and required reading for newly "
                "accepted candidates entering the Office of Security."
            ),
            logo=c.LOGOS["osec"],
        ),
        c.embed(
            title="Candidate Welcome",
            description=(
                "Congratulations. You have successfully completed the **Office of Security** "
                "tryout or application process and have been **accepted** into the "
                "**CIA Office of Security**."
            ),
            fields=(
                (
                    "Next Steps",
                    "Join **all required servers and Roblox groups**, then review every required "
                    "document listed below before attending training.",
                ),
                (
                    "Training Window",
                    "You have **14 days** from acceptance to complete the Security Phase Program. "
                    "Failure to progress within this window may result in removal from candidacy.",
                ),
            ),
        ),
        c.embed(
            title="Training Program",
            description=(
                "The Security Phase Program consists of **two mandatory phases**. "
                "Candidates must complete each phase in order before promotion to "
                "**Junior Security Agent**."
            ),
            fields=(
                (
                    "Phase I",
                    "Entirely **classroom-based**. Review all provided material and pass the "
                    "Phase I quiz to advance to **Security Phase II**.\n\n"
                    "If you believe an instructor graded your quiz unfairly, contact a "
                    "**Deputy Director of Security or above** and file a formal report. "
                    "Do not dispute results through unauthorized channels.",
                ),
                (
                    "Phase II",
                    "**In-game** training covering a gate tour, basic duties instruction, "
                    "and a final assessment quiz.",
                ),
                (
                    "In-Game Conduct",
                    "While in game, follow all instructions from your assigned superior. "
                    "Candidates must **not** independently perform **security duties** "
                    "until authorized to do so.",
                ),
            ),
        ),
        c.embed(
            title="Required Reading",
            description=(
                "Review each document in full before training and promotion to "
                "**Junior Security Agent**. Observe all classification markings."
            ),
            fields=(
                c.link_field(
                    "Orientation",
                    "CIA OSEC | Security Phase Candidate Orientation Guide",
                    c.url('osec.spp_information.orientation_guide'),
                    "CONFIDENTIAL. Authorized candidates only.",
                ),
                c.link_field(
                    "Handbook",
                    "CIA Office of Security Handbook",
                    c.url('osec.spp_information.official_handbook'),
                    "CONTROLLED UNCLASSIFIED INFORMATION (CUI). Authorized personnel only.",
                ),
                c.link_field(
                    "Conduct",
                    "Code of Agency Conduct",
                    c.url('osec.spp_information.code_of_agency_conduct'),
                    "UNCLASSIFIED.",
                ),
                c.link_field(
                    "Civilian Access",
                    "CIA | Civilian Access",
                    c.url('osec.spp_information.civilian_access'),
                    "UNCLASSIFIED.",
                ),
            ),
        ),
        c.embed(
            title="Classification & Handling Notice",
            description=(
                "The **Security Phase Candidate Orientation Guide** is classified "
                "**CONFIDENTIAL**. The **CIA Office of Security Handbook** is marked "
                "**CONTROLLED UNCLASSIFIED INFORMATION (CUI)**.\n\n"
                "The **Code of Agency Conduct** and **Civilian Access** documents are "
                "**UNCLASSIFIED**.\n\n"
                "Unauthorized disclosure, redistribution, or leaking of restricted materials "
                "will result in a **BLACKLIST** from the **CIA Office of Security**. "
                "Handle all documents responsibly and do not share them outside authorized "
                "channels or personnel."
            ),
        ),
        c.disclaimer_embed(classified=True),
    ]


def send_osec_spp_information() -> None:
    c.send_webhook(
        WEBHOOK_URL,
        _build_embeds(),
        username=c.BOT_OSEC,
        files=[c.logo_file(c.LOGOS["osec"])],
    )


if __name__ == "__main__":
    send_osec_spp_information()
