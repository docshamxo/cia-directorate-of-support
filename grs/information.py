# === FILE HEADER ===
# Title: Information
# Path: grs/information.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Align internal info template and closing vocabulary.
# === END FILE HEADER ===

"""
CIA GRS information announcer.

Posts the Global Response Staff overview and reference documentation
to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.hero_embed(
            title="INFORMATION",
            unit="Global Response Staff",
            supporting=(
                "Official reference hub for Global Response Staff mission overview and "
                "authorized documentation."
            ),
            color=c.COLOR_GRS,
            logo=c.LOGOS["grs"],
        ),
        c.embed(
            title="About GRS",
            description=(
                "The Global Response Staff is a sub-unit of the **Office of Security**, "
                "operating under the **Directorate of Support**.\n\n"
                f"{c.GRS_ABOUT}"
            ),
            color=c.COLOR_GRS,
        ),
        c.embed(
            title="Reference Documents",
            description="Key GRS reference material for personnel and candidates.",
            color=c.COLOR_GRS,
            fields=(
                c.link_field(
                    "Handbook",
                    "CIA GRS | Handbook",
                    c.url("grs.information.handbook"),
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


def send_grs_information() -> None:
    run_announcer(
        webhook_key="WEBHOOK_GRS_INFORMATION",
        username=c.BOT_GRS,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["grs"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_grs_information()

# === FILE FOOTER ===
# End of file: grs/information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
