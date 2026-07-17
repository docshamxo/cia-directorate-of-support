# === FILE HEADER ===
# Title: Server Regulations
# Path: units/ds/server_regulations.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Attach DS logo on server regulations hero.
# === END FILE HEADER ===

"""
CIA DS server regulations announcer.

Posts the Directorate of Support communications server regulations
to a Discord webhook.
"""

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
        files=[c.logo_file(c.LOGOS["ds"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_server_regulations()

# === FILE FOOTER ===
# End of file: units/ds/server_regulations.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
