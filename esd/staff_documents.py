# === FILE HEADER ===
# Title: Staff Documents
# Path: esd/staff_documents.py
# Created: 2026-07-15
# Created by: docshamxo
# Modified:
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Unify staff-docs template and unit-color closers.
#   - 2026-07-17 | docshamxo | Text marking notes and clearer field labels.
# === END FILE HEADER ===

"""
CIA ESD staff documents announcer.

Posts official Executive Security Detail staff guides and shared Drive
resources to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.hero_embed(
            title="STAFF DOCUMENTS",
            unit="Executive Security Detail",
            supporting="Authorized ESD staff documentation index. Need-to-know access only.",
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
                    "DS Community | ESD Google Drive",
                    c.url("esd.staff_documents.google_drive"),
                    c.marking_note("STAFF"),
                ),
            ),
        ),
        c.classification_handling_embed(
            unit="ESD",
            authority="CIA Directorate of Support",
            color=c.COLOR_ESD,
        ),
        c.disclaimer_embed(staff=True, color=c.COLOR_ESD),
    ]


def send_esd_staff_documents() -> None:
    run_announcer(
        webhook_key="WEBHOOK_ESD_STAFF_DOCUMENTS",
        username=c.BOT_ESD,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["esd"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_esd_staff_documents()

# === FILE FOOTER ===
# End of file: esd/staff_documents.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
