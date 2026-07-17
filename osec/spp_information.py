# === FILE HEADER ===
# Title: SPP Information
# Path: osec/spp_information.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Align hero, link grammar, and unit-color closers.
#   - 2026-07-17 | docshamxo | Community markings CANDIDATE/STAFF/PUBLIC.
# === END FILE HEADER ===

"""
CIA OSEC Security Phase Program information announcer.

Posts welcome, training, and required reading for newly accepted
Security Phase Program candidates to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.hero_embed(
            title="SECURITY PHASE PROGRAM",
            unit="Office of Security",
            supporting=(
                "Orientation, training requirements, and required reading for newly "
                "accepted Security Phase Program candidates."
            ),
            color=c.COLOR_OSEC,
            logo=c.LOGOS["osec"],
        ),
        c.embed(
            title="Candidate Welcome",
            description=(
                "Congratulations. You have successfully completed the **Office of Security** "
                "tryout or application process and have been **accepted** into the "
                "**CIA Office of Security**."
            ),
            color=c.COLOR_OSEC,
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
            color=c.COLOR_OSEC,
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
                "**Junior Security Agent**. Observe all community markings."
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    "Orientation",
                    "CIA OSEC | Security Phase Candidate Orientation Guide",
                    c.url("osec.spp_information.orientation_guide"),
                    "CANDIDATE. Authorized candidates only.",
                ),
                c.link_field(
                    "Handbook",
                    "CIA OSEC | Handbook",
                    c.url("osec.spp_information.official_handbook"),
                    "STAFF. Authorized OSEC staff only.",
                ),
                c.link_field(
                    "Conduct",
                    "CIA OSEC | Code of Agency Conduct",
                    c.url("osec.spp_information.code_of_agency_conduct"),
                    "PUBLIC.",
                ),
                c.link_field(
                    "Civilian Access",
                    "CIA OSEC | Civilian Access",
                    c.url("osec.spp_information.civilian_access"),
                    "PUBLIC.",
                ),
            ),
        ),
        c.embed(
            title="Classification & Handling Notice",
            description=(
                "The **Security Phase Candidate Orientation Guide** is marked **CANDIDATE**. "
                "The **CIA OSEC | Handbook** is marked **STAFF**.\n\n"
                "The **Code of Agency Conduct** and **Civilian Access** documents are "
                "**PUBLIC**.\n\n"
                "Unauthorized disclosure, redistribution, or leaking of restricted materials "
                "will result in a **BLACKLIST** from the **CIA Office of Security**. "
                "Handle all documents responsibly and do not share them outside authorized "
                "channels or personnel."
            ),
            color=c.COLOR_OSEC,
        ),
        c.disclaimer_embed(staff=True, color=c.COLOR_OSEC),
    ]


def send_osec_spp_information() -> None:
    run_announcer(
        webhook_key="WEBHOOK_OSEC_SPP_INFORMATION",
        username=c.BOT_OSEC,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["osec"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_osec_spp_information()

# === FILE FOOTER ===
# End of file: osec/spp_information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
