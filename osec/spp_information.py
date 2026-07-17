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
#   - 2026-07-17 | docshamxo | Accessible field names and marking notes.
#   - 2026-07-17 | docshamxo | Use DS Community link labels (brand/legal).
#   - 2026-07-17 | docshamxo | Clearer candidate hierarchy; shared marking notes.
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
                "Orientation, training requirements, and required reading for accepted "
                "Security Phase Program candidates."
            ),
            color=c.COLOR_OSEC,
            logo=c.LOGOS["osec"],
        ),
        c.embed(
            title="Candidate Welcome",
            description=(
                "You have completed the **Office of Security** tryout or application process "
                "and are **accepted** into the **CIA Office of Security**."
            ),
            color=c.COLOR_OSEC,
            fields=(
                (
                    "Next Steps",
                    "Join **all required servers and Roblox groups**, then review every "
                    "required document below before training.",
                ),
                (
                    "Training Window",
                    "Complete the Security Phase Program within **14 days** of acceptance. "
                    "Failure to progress may result in removal from candidacy.",
                ),
            ),
        ),
        c.embed(
            title="Training Program",
            description=(
                "Two mandatory phases, completed in order, before promotion to "
                "**Junior Security Agent**."
            ),
            color=c.COLOR_OSEC,
            fields=(
                (
                    "Phase I",
                    "**Classroom-based.** Review all material and pass the Phase I quiz to "
                    "advance." + "\n\n"
                    "If you believe a quiz was graded unfairly, contact a "
                    "**Deputy Director of Security or above** and file a formal report. "
                    "Do not dispute results through unauthorized channels.",
                ),
                (
                    "Phase II",
                    "**In-game** training: gate tour, basic duties, and a final assessment quiz.",
                ),
                (
                    "In-Game Conduct",
                    "Follow instructions from your assigned superior. Do **not** perform "
                    "**security duties** independently until authorized.",
                ),
            ),
        ),
        c.embed(
            title="Required Reading",
            description=(
                "Review each document in full before training and promotion. Observe community "
                "markings."
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    "Orientation",
                    "DS Community | OSEC Security Phase Candidate Orientation Guide",
                    c.url("osec.spp_information.orientation_guide"),
                    c.marking_note("CANDIDATE"),
                ),
                c.link_field(
                    "Handbook",
                    "DS Community | OSEC Handbook",
                    c.url("osec.spp_information.official_handbook"),
                    c.marking_note("STAFF"),
                ),
                c.link_field(
                    "Code of Agency Conduct",
                    "DS Community | OSEC Code of Agency Conduct",
                    c.url("osec.spp_information.code_of_agency_conduct"),
                    c.marking_note("PUBLIC"),
                ),
                c.link_field(
                    "Civilian Access",
                    "DS Community | OSEC Civilian Access",
                    c.url("osec.spp_information.civilian_access"),
                    c.marking_note("PUBLIC"),
                ),
            ),
        ),
        c.embed(
            title="Classification & Handling Notice",
            description=(
                "**Orientation Guide** -- **CANDIDATE**. **Handbook** -- **STAFF**. "
                "**Code of Agency Conduct** and **Civilian Access** -- **PUBLIC**." + "\n\n"
                "Unauthorized disclosure or redistribution of restricted materials will "
                "result in a **BLACKLIST** from the **CIA Office of Security**. "
                "Do not share outside authorized channels or personnel."
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
