# === FILE HEADER ===
# Title: Information
# Path: units/grs/information.py
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
#   - 2026-07-17 | docshamxo | Accessible marking notes.
#   - 2026-08-03 | docshamxo | Remove Reference Documents section from GRS information.
#   - 2026-08-04 | docshamxo | Treat GRS information as a PUBLIC channel.
#   - 2026-08-04 | docshamxo | Omit Disclaimer embed on GRS public information.
# === END FILE HEADER ===

"""
CIA GRS public information announcer.

Posts the Global Response Staff overview to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.hero_embed(
            title="PUBLIC INFORMATION",
            unit="Global Response Staff",
            supporting=(
                "Public overview of the GRS mission and place in the Directorate of Support."
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
# End of file: units/grs/information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
