# === FILE HEADER ===
# Title: Staff Documents
# Path: grs/staff_documents.py
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
# === END FILE HEADER ===

"""
CIA GRS staff documents announcer.

Posts official Global Response Staff guides, training material, and
certification resources to a Discord webhook.
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
            supporting=(
                "Official repository for authorized GRS staff documentation. "
                "Access is strictly limited to authorized personnel."
            ),
            color=c.COLOR_GRS,
            logo=c.LOGOS["grs"],
        ),
        c.embed(
            title="Central Repository",
            description="Primary folder for all GRS staff files, guides, and forms.",
            color=c.COLOR_GRS,
            fields=(
                c.link_field(
                    "Google Drive",
                    "CIA GRS | Google Drive",
                    c.url("grs.staff_documents.google_drive"),
                    "Authorized GRS staff only.",
                ),
            ),
        ),
        c.embed(
            title="Training & Operational Guides",
            description="Official guides for GRS personnel, training, tryouts, and operations.",
            color=c.COLOR_GRS,
            fields=(
                c.link_field(
                    "Handbook",
                    "CIA GRS | Handbook",
                    c.url("grs.staff_documents.handbook"),
                    "Authorized GRS staff only.",
                ),
                c.link_field(
                    "Breach Training",
                    "CIA GRS | Breach Training Guide",
                    c.url("grs.staff_documents.breach_training_guide"),
                    "Authorized GRS staff only.",
                ),
                c.link_field(
                    "Tryouts",
                    "CIA GRS | Tryout Guide",
                    c.url("grs.staff_documents.tryout_guide"),
                    "Authorized GRS staff only.",
                ),
            ),
        ),
        c.embed(
            title="Certifications",
            description="Official certification documentation for GRS personnel.",
            color=c.COLOR_GRS,
            fields=(
                c.link_field(
                    "Breaching Certification",
                    "CIA GRS | Breaching Certificate",
                    c.url("grs.staff_documents.breaching_certificate"),
                    "Authorized GRS staff only.",
                ),
            ),
        ),
        c.classification_handling_embed(
            unit="GRS",
            authority="CIA Directorate of Support",
            color=c.COLOR_GRS,
        ),
        c.disclaimer_embed(classified=True, color=c.COLOR_GRS),
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
# End of file: grs/staff_documents.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
