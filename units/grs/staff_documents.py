# === FILE HEADER ===
# Title: Staff Documents
# Path: units/grs/staff_documents.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Unify staff-docs template and unit-color closers.
#   - 2026-07-17 | docshamxo | Prefer Drive root + handbook; STAFF markings.
#   - 2026-07-17 | docshamxo | Text marking notes and clearer field labels.
# === END FILE HEADER ===

"""
CIA GRS staff documents announcer.

Posts the Global Response Staff Drive index and handbook. Additional TTP packs
live in Drive (need-to-know).
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.hero_embed(
            title="STAFF DOCUMENTS",
            unit="Global Response Staff",
            supporting="Authorized GRS staff documentation index. Need-to-know access only.",
            color=c.COLOR_GRS,
            logo=c.LOGOS["grs"],
        ),
        c.embed(
            title="Central Repository",
            description=(
                "Primary folder for all GRS staff files, guides, and forms. "
                "Use Drive for training and certification packs not listed here."
            ),
            color=c.COLOR_GRS,
            fields=(
                c.link_field(
                    "Google Drive",
                    "DS Community | GRS Google Drive",
                    c.url("grs.staff_documents.google_drive"),
                    c.marking_note("STAFF"),
                ),
                c.link_field(
                    "Handbook",
                    "DS Community | GRS Handbook",
                    c.url("grs.staff_documents.handbook"),
                    c.marking_note("STAFF"),
                ),
            ),
        ),
        c.classification_handling_embed(
            unit="GRS",
            authority="CIA Directorate of Support",
            color=c.COLOR_GRS,
        ),
        c.disclaimer_embed(staff=True, color=c.COLOR_GRS),
    ]


def send_grs_staff_documents() -> None:
    run_announcer(
        webhook_key="WEBHOOK_GRS_STAFF_DOCUMENTS",
        username=c.BOT_GRS,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["grs"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_grs_staff_documents()

# === FILE FOOTER ===
# End of file: units/grs/staff_documents.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
