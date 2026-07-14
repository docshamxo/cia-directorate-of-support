"""
CIA OSEC information announcer.

Posts official Office of Security reference documents and the personnel ORBAT
to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_OSEC_INFORMATION")

URL_HANDBOOK = (
    "https://docs.google.com/document/d/1IsygYp9657PKnGqmQyMxTvi50BCJvWVgTaIW7lZPN2U/edit?usp=sharing"
)
URL_ORBAT = (
    "https://docs.google.com/spreadsheets/d/12pMdf-XiYeHBCX99zO4cmuek8xQr4SL3lAoQcReowWk/edit?usp=sharing"
)
URL_CODE_OF_AGENCY_CONDUCT = (
    "https://docs.google.com/document/d/1McFfJx3IItYHdEdUYdrMT5fiI2spyRu03cif_CyXIZk/edit?usp=sharing"
)
URL_CIVILIAN_ACCESS = (
    "https://docs.google.com/document/d/1M37oQhF5HF5AUHV4qNMgb2GdhFbv1WxbmRYWsgI5MHo/edit?usp=sharing"
)


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.embed(
            title="INFORMATION",
            description=(
                "*Central Intelligence Agency · Office of Security*\n\n"
                f"*{c.OSEC_MOTTO}*\n\n"
                f"{c.OSEC_ABOUT}\n\n"
                "This channel serves as the official reference hub for Office of Security "
                "personnel records and authorized documentation. All personnel are expected "
                "to review applicable materials and observe the classification markings "
                "listed below."
            ),
            logo=c.LOGOS["osec"],
        ),
        c.embed(
            title="Personnel Records",
            description=(
                "The Organization and Assignment Board (ORBAT) is the live record of "
                "Office of Security personnel, assignments, and organizational structure."
            ),
            fields=(
                c.link_field(
                    "ORBAT",
                    "CIA OSEC | ORBAT",
                    URL_ORBAT,
                    "UNCLASSIFIED.",
                ),
            ),
        ),
        c.embed(
            title="Reference Documents",
            description=(
                "Agency-wide and Office of Security reference material. Review each document "
                "in full and comply with its classification level."
            ),
            fields=(
                c.link_field(
                    "Handbook",
                    "CIA Office of Security Handbook",
                    URL_HANDBOOK,
                    "CONTROLLED UNCLASSIFIED INFORMATION (CUI). Authorized personnel only.",
                ),
                c.link_field(
                    "Conduct",
                    "Code of Agency Conduct",
                    URL_CODE_OF_AGENCY_CONDUCT,
                    "UNCLASSIFIED.",
                ),
                c.link_field(
                    "Civilian Access",
                    "CIA | Civilian Access",
                    URL_CIVILIAN_ACCESS,
                    "UNCLASSIFIED.",
                ),
            ),
        ),
        c.embed(
            title="Classification & Handling Notice",
            description=(
                "The **CIA Office of Security Handbook** is marked **CONTROLLED UNCLASSIFIED "
                "INFORMATION (CUI)**. Unauthorized disclosure, redistribution, or leaking of "
                "this document will result in a **BLACKLIST** from the **CIA Office of Security**.\n\n"
                "The **ORBAT**, **Code of Agency Conduct**, and **Civilian Access** documents "
                "are **UNCLASSIFIED** and may be referenced in accordance with Agency policy.\n\n"
                "Handle all materials responsibly. Do not share restricted documents outside "
                "authorized channels or personnel."
            ),
        ),
        c.disclaimer_embed(classified=True),
    ]


def send_osec_information() -> None:
    c.send_webhook(
        WEBHOOK_URL,
        _build_embeds(),
        username=c.BOT_DS,
        files=[c.logo_file(c.LOGOS["osec"])],
    )


if __name__ == "__main__":
    send_osec_information()
