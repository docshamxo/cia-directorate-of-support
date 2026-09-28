# === FILE HEADER ===
# Title: COC
# Path: units/ote/coc.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Attach OTE logo and unit-color disclaimer.
#   - 2026-09-08 | docshamxo | Include Agency EL and full DS CoC above OTE command.
#   - 2026-09-08 | docshamxo | Standardize hierarchy blocks onto shared CoC builders.
# === END FILE HEADER ===

"""
CIA OTE chain of command announcer.

Sends the Office of Training & Education chain of command to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import (
    agency_executive_embed,
    ds_leadership_embed,
    logo_files,
    office_command_embed,
    run_announcer,
)


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.chain_intro_embed(
            unit="Office of Training & Education",
            color=c.COLOR_OTE,
            logo=c.LOGOS["ote"],
            context=(
                f"{c.motto_line(c.OTE_MOTTO)}\n\n"
                "The Office of Training & Education sits under the **Directorate of Support**. "
                "OTE leadership reports through the DS chain to Agency leadership."
            ),
        ),
        agency_executive_embed(color=c.COLOR_OTE),
        ds_leadership_embed(color=c.COLOR_OTE, logo=c.LOGOS["ds"]),
        office_command_embed(
            title="Office of Training & Education",
            motto=c.OTE_MOTTO,
            about=c.OTE_ABOUT,
            roles=c.OTE_HIGH_COMMAND,
            color=c.COLOR_OTE,
            logo=c.LOGOS["ote"],
        ),
        c.embed(
            title="OTE Staff",
            description="Instructional and training staff ranks within the Office.",
            color=c.COLOR_OTE,
            fields=(("Staff Ranks", c.ranks_text(*c.OTE_STAFF_RANKS)),),
        ),
        c.important_notice_embed(
            unit="OTE", color=c.COLOR_OTE, parent_units=("Directorate of Support",)
        ),
    ]


def send_chain_of_command() -> None:
    run_announcer(
        webhook_key="WEBHOOK_OTE_COC",
        username=c.BOT_OTE,
        build_embeds=_build_embeds,
        files=lambda: logo_files("ds", "ote"),
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_chain_of_command()

# === FILE FOOTER ===
# End of file: units/ote/coc.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
