# === FILE HEADER ===
# Title: Chain Of Command
# Path: units/ds/chain_of_command.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Standardize hero title and unit-color disclaimer.
#   - 2026-07-17 | docshamxo | Use chain_intro_embed for proper CoC hierarchy.
#   - 2026-08-30 | docshamxo | Drop OSEC Main Element CM section from OSEC embed.
#   - 2026-09-08 | docshamxo | Refactor hierarchy blocks onto shared CoC builders.
# === END FILE HEADER ===

"""
CIA Directorate of Support chain of command announcer.

Posts the DS organizational hierarchy — including OTE, OSEC, and OSEC sub-units —
to a Discord webhook, including component logos.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import (
    agency_executive_embed,
    ds_leadership_embed,
    office_command_embed,
    run_announcer,
    subunit_command_about,
)


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.chain_intro_embed(unit="Directorate of Support", color=c.COLOR_DS),
        agency_executive_embed(color=c.COLOR_DS),
        ds_leadership_embed(color=c.COLOR_DS, logo=c.LOGOS["ds"]),
        office_command_embed(
            title="Office of Training & Education",
            motto=c.OTE_MOTTO,
            about=c.OTE_ABOUT,
            roles=c.OTE_HIGH_COMMAND,
            color=c.COLOR_DS,
            logo=c.LOGOS["ote"],
        ),
        office_command_embed(
            title="Office of Security",
            motto=c.OSEC_MOTTO,
            about=c.OSEC_ABOUT,
            roles=c.OSEC_HIGH_COMMAND,
            color=c.COLOR_DS,
            logo=c.LOGOS["osec"],
            extra_fields=(("Sub-Units", c.bullets(*c.OSEC_SUB_UNITS)),),
        ),
        office_command_embed(
            title="Global Response Staff",
            about=subunit_command_about(c.GRS_ABOUT),
            roles=c.GRS_COMMAND,
            color=c.COLOR_DS,
            logo=c.LOGOS["grs"],
            roles_field="Command Team",
        ),
        office_command_embed(
            title="Executive Security Detail",
            about=subunit_command_about(c.ESD_ABOUT),
            roles=c.ESD_COMMAND,
            color=c.COLOR_DS,
            logo=c.LOGOS["esd"],
            roles_field="Command Team",
        ),
        c.embed(
            title="OSEC Rank Structure",
            description=(
                "Mid- and field-level ranks shared across the **Office of Security** and its "
                "sub-units (main OSEC, GRS, and ESD)."
            ),
            fields=(
                ("Middle Command", c.ranks_text(*c.OSEC_MIDDLE_COMMAND)),
                ("Low Command", c.ranks_text(*c.OSEC_LOW_COMMAND)),
            ),
        ),
    ]


def send_chain_of_command() -> None:
    run_announcer(
        webhook_key="WEBHOOK_DS_CHAIN_OF_COMMAND",
        username=c.BOT_DS,
        build_embeds=_build_embeds,
        files=lambda: [c.logo_file(path) for path in c.LOGOS.values()],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_chain_of_command()

# === FILE FOOTER ===
# End of file: units/ds/chain_of_command.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
