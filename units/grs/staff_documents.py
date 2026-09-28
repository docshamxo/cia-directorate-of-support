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
#   - 2026-07-17 | docshamxo | Add General Standard Training Guide (shared community link).
#   - 2026-09-08 | docshamxo | Refactor onto shared staff-docs frame builders.
# === END FILE HEADER ===

"""
CIA GRS staff documents announcer.

Posts the Global Response Staff Drive index and handbook. Additional TTP packs
live in Drive (need-to-know).
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import (
    run_announcer,
    staff_docs_central_embed,
    staff_docs_handling_embed,
    staff_docs_hero_embed,
    staff_docs_link,
    staff_docs_section_embed,
)

_UNIT = "Global Response Staff"
_ABBREV = "GRS"
_COLOR = c.COLOR_GRS


def _build_embeds() -> list[c.discord.Embed]:
    return [
        staff_docs_hero_embed(
            unit_full=_UNIT,
            unit_abbrev=_ABBREV,
            color=_COLOR,
            logo=c.LOGOS["grs"],
        ),
        staff_docs_central_embed(
            unit_abbrev=_ABBREV,
            drive_url_key="grs.staff_documents.google_drive",
            drive_link_name="GRS Google Drive",
            color=_COLOR,
            extra_fields=(
                staff_docs_link(
                    "Handbook",
                    "GRS Handbook",
                    "grs.staff_documents.handbook",
                ),
            ),
        ),
        staff_docs_section_embed(
            title="Training Materials",
            description=(
                "Official shared Directorate of Support standard training references "
                "for Global Response Staff."
            ),
            color=_COLOR,
            fields=(
                staff_docs_link(
                    "General Standard Training",
                    "General Standard Training Guide",
                    "community.general_standard_training_guide",
                ),
            ),
        ),
        staff_docs_handling_embed(unit_full=_UNIT, color=_COLOR),
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
