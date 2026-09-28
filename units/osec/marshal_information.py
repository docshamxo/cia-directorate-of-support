# === FILE HEADER ===
# Title: Marshal Information
# Path: units/osec/marshal_information.py
# Created: 2026-09-08
# Created by: docshamxo
# Modified:
#   - 2026-09-08 | docshamxo | Add Chief Marshal Hub for #marshal-information.
#   - 2026-09-08 | docshamxo | ORBAT edit access via Google Groups / HICOM email.
#   - 2026-09-08 | docshamxo | Duty channel links for logs, enrollments, LoA, supervision.
#   - 2026-09-08 | docshamxo | Split log channels; link #marshal-reports.
# === END FILE HEADER ===

"""
CIA OSEC Chief Marshal Hub announcer.

Posts Chief Marshal [CM] responsibilities, duty/log channel links, weekly
reporting requirements, ORBAT Google Groups access, and the CM guide to the
marshal-information Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.hero_embed(
            title="CHIEF MARSHAL HUB",
            unit="Office of Security",
            supporting=(
                "Tools and duties for Chief Marshals [CM]: enrollments, logs, "
                "Leave of Absence handling, and OSEC ORBAT maintenance."
            ),
            color=c.COLOR_OSEC,
            logo=c.LOGOS["osec"],
        ),
        c.embed(
            title="Promotion Welcome",
            description=(
                "Congrats on your promotion to a **Chief Marshal [CM]** within the "
                "**Office of Security**. A Chief Marshal gets access to a plethora of "
                "tools to help with logs, enrollments, and maintaining the Order of "
                "Battle (**ORBAT**)."
            ),
            color=c.COLOR_OSEC,
            fields=(
                (
                    "Access Marking",
                    c.marking_note(
                        "STAFF",
                        "Chief Marshal need-to-know. Do not share outside authorized channels.",
                    ),
                ),
            ),
        ),
        c.embed(
            title="Core Responsibilities",
            description="A Chief Marshal is responsible for the following duties.",
            color=c.COLOR_OSEC,
            fields=(
                (
                    "Enrollments",
                    "Processing **all enrollments**.",
                ),
                (
                    "Leave of Absence",
                    "Reviewing and accepting LoA / inactivity requests that are "
                    "**less than 10 days**, and replying to members' LoA requests when "
                    "they return from leave.",
                ),
                (
                    "ORBAT",
                    "Maintaining the **OSEC ORBAT** accurately.",
                ),
                (
                    "Supervision",
                    "Supervising new staff members for **Phase 2** and **Tryouts**.",
                ),
            ),
        ),
        c.embed(
            title="Duty Channels",
            description=(
                "Check these channels for enrollments, inactivity / LoA, and supervision. "
                "Use the linked channel — do not process requests elsewhere."
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    "Enrollments",
                    "CIA DS | OSEC Enrollments",
                    c.osec_enrollments_channel_url(),
                    "Process all enrollments here.",
                ),
                c.link_field(
                    "Leave of Absence / Inactivity",
                    "CIA DS | OSEC Leave of Absence (Inactivity Request)",
                    c.osec_loa_channel_url(),
                    "Review/accept LoA under 10 days; reply when members return.",
                ),
                c.link_field(
                    "Supervision",
                    "CIA DS | OSEC Supervision",
                    c.osec_supervision_channel_url(),
                    "Phase 2 and Tryout supervision logs and follow-up.",
                ),
            ),
        ),
        c.embed(
            title="Log Review Channels",
            description=(
                "Review and accept the following logs in their dedicated channels."
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    "Patrol Logs",
                    "CIA DS | OSEC Patrol Logs",
                    c.osec_patrol_logs_channel_url(),
                ),
                c.link_field(
                    "Event Logs",
                    "CIA DS | OSEC Event Logs",
                    c.osec_event_logs_channel_url(),
                ),
                c.link_field(
                    "Tryout Logs",
                    "CIA DS | OSEC Tryout Logs",
                    c.osec_tryout_logs_channel_url(),
                ),
                c.link_field(
                    "Phase Logs",
                    "CIA DS | OSEC Phase Logs",
                    c.osec_phase_logs_channel_url(),
                ),
                c.link_field(
                    "Supervision Logs",
                    "CIA DS | OSEC Supervision",
                    c.osec_supervision_channel_url(),
                    "Same channel as Phase 2 / Tryout supervision duty.",
                ),
            ),
        ),
        c.embed(
            title="ORBAT Edit Access",
            description=(
                "Chief Marshals must be on the authorized **Google Group** before they "
                "can edit the OSEC ORBAT."
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    "Google Group",
                    "CIA DS | OSEC ORBAT Google Group",
                    c.url("osec.marshal_information.google_groups"),
                    c.marking_note("STAFF", "Membership required to edit the ORBAT."),
                ),
                (
                    "How to Get Access",
                    "Reach out to **HICOM** and send them the **email address** you want "
                    "added to the Google Group list. You cannot edit the ORBAT until you "
                    "are added.",
                ),
            ),
        ),
        c.embed(
            title="Weekly Reports & Required Reading",
            description=(
                "Chief Marshals submit a weekly report to HICOM/HQ as a performance "
                "review, and must read the CM guide upon promotion."
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    "Weekly Report",
                    "CIA DS | OSEC Marshal Reports",
                    c.osec_marshal_reports_channel_url(),
                    "Submit your weekly performance review here (format in channel).",
                ),
                c.link_field(
                    "Chief Marshal Guide",
                    "CIA DS | OSEC Chief Marshal Guide",
                    c.url("osec.marshal_information.cm_guide"),
                    c.marking_note("STAFF", "Required reading on promotion."),
                ),
            ),
        ),
        c.classification_handling_embed(
            unit="Office of Security",
            authority="CIA Office of Security",
            color=c.COLOR_OSEC,
            restricted=True,
        ),
    ]


def send_osec_marshal_information() -> None:
    run_announcer(
        webhook_key="WEBHOOK_OSEC_MARSHAL_INFORMATION",
        username=c.BOT_OSEC,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["osec"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_osec_marshal_information()

# === FILE FOOTER ===
# End of file: units/osec/marshal_information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
