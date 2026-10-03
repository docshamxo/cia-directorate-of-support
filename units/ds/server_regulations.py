# === FILE HEADER ===
# Title: Server Regulations
# Path: units/ds/server_regulations.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-10-03 | docshamxo | OIG Levels closer + policy link buttons; drop Disclaimer.
# === END FILE HEADER ===

"""CIA DS server regulations announcer."""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return c.server_regulations_embeds()


def send_server_regulations() -> None:
    run_announcer(
        webhook_key="WEBHOOK_DS_SERVER_REGULATIONS",
        username=c.BOT_DS,
        build_embeds=_build_embeds,
        build_view=c.rules_policy_view,
        files=[c.logo_file(c.LOGOS["ds"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_server_regulations()

# === FILE FOOTER ===
# End of file: units/ds/server_regulations.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
