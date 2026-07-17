# === FILE HEADER ===
# Title: COC
# Path: units/esd/coc.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Attach ESD logo on chain-of-command hero.
# === END FILE HEADER ===

"""
CIA ESD chain of command announcer.

Sends the Executive Security Detail chain of command to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer, subunit_coc_embeds


def _build_embeds() -> list[c.discord.Embed]:
    return subunit_coc_embeds(
        unit_full="Executive Security Detail",
        unit_abbrev="ESD",
        color=c.COLOR_ESD,
        about=c.ESD_ABOUT,
        command_roles=c.ESD_COMMAND,
        logo=c.LOGOS["esd"],
    )


def send_chain_of_command() -> None:
    run_announcer(
        webhook_key="WEBHOOK_ESD_COC",
        username=c.BOT_ESD,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["esd"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_chain_of_command()

# === FILE FOOTER ===
# End of file: units/esd/coc.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
