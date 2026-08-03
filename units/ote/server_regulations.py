# === FILE HEADER ===
# Title: Server Regulations
# Path: units/ote/server_regulations.py
# Created: 2026-08-02
# Created by: docshamxo
# Modified:
#   - 2026-08-02 | docshamxo | OTE rules channel — same regulations as OSEC with OTE office name.
# === END FILE HEADER ===

"""
CIA OTE server regulations announcer.

Posts the same communications-server regulations as DS/OSEC, branded for the
Office of Training & Education, to the OTE Rules webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return c.server_regulations_embeds(
        office="Office of Training & Education",
        motto=c.OTE_MOTTO,
        logo=c.LOGOS["ote"],
        color=c.COLOR_OTE,
    )


def send_ote_server_regulations() -> None:
    run_announcer(
        webhook_key="WEBHOOK_OTE_RULES",
        username=c.BOT_OTE,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["ote"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_ote_server_regulations()

# === FILE FOOTER ===
# End of file: units/ote/server_regulations.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
