# === FILE HEADER ===
# Title: Staff Documents
# Path: esd/staff_documents.py
# Created: 2026-07-15
# Created by: docshamxo
# Modified:
#   - 2026-07-15 | docshamxo | Add ESD staff documents announcer with Google Drive link.
# === END FILE HEADER ===

"""
CIA ESD staff documents announcer.

Posts official Executive Security Detail staff guides and shared Drive
resources to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_ESD_STAFF_DOCUMENTS")


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.embed(
            title="STAFF DOCUMENTS",
            description=(
                "*Central Intelligence Agency · Executive Security Detail*\n\n"
                f"{c.ESD_ABOUT}\n\n"
                "This channel serves as the official repository for authorized ESD "
                "staff documentation. The Executive Security Detail is a sub-unit of the "
                "**Office of Security** under the **Directorate of Support**.\n\n"
                "Access is **strictly limited** to authorized personnel. Review, use, "
                "and handle all materials responsibly."
            ),
            color=c.COLOR_ESD,
            logo=c.LOGOS["esd"],
        ),
        c.embed(
            title="Central Repository",
            description="Primary folder for all ESD staff files, guides, and forms.",
            color=c.COLOR_ESD,
            fields=(
                c.link_field(
                    "Google Drive",
                    "CIA ESD | Google Drive",
                    c.url('esd.staff_documents.google_drive'),
                    "Authorized ESD staff only.",
                ),
            ),
        ),
        c.embed(
            title="Classification & Handling Notice",
            description=(
                "All documents listed in this channel are intended for **authorized ESD "
                "personnel only**.\n\n"
                "Unauthorized disclosure, redistribution, or leaking of any restricted "
                "material may result in a **BLACKLIST** from the **CIA Directorate of Support**.\n\n"
                "Handle all staff documents responsibly. Do not share materials outside "
                "authorized channels or personnel."
            ),
            color=c.COLOR_ESD,
        ),
        c.disclaimer_embed(classified=True),
    ]


def send_esd_staff_documents() -> None:
    c.send_webhook(
        WEBHOOK_URL,
        _build_embeds(),
        username=c.BOT_ESD,
        files=[c.logo_file(c.LOGOS["esd"])],
    )


if __name__ == "__main__":
    send_esd_staff_documents()

# === FILE FOOTER ===
# End of file: esd/staff_documents.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
