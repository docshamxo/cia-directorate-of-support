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
#   - 2026-08-30 | docshamxo | Add GRS tryout / application requirements embed.
#   - 2026-09-08 | docshamxo | Refactor onto shared information-channel frame; add Community Links.
# === END FILE HEADER ===

"""
CIA GRS public information announcer.

Posts the Global Response Staff overview to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import (
    info_about_embed,
    info_community_links_embed,
    info_hero_embed,
    info_tryout_requirements_embed,
    run_announcer,
)

_UNIT = "Global Response Staff"
_ABBREV = "GRS"
_COLOR = c.COLOR_GRS


def _build_embeds() -> list[c.discord.Embed]:
    return [
        info_hero_embed(
            unit_full=_UNIT,
            unit_abbrev=_ABBREV,
            color=_COLOR,
            logo=c.LOGOS["grs"],
        ),
        info_about_embed(
            unit_full=_UNIT,
            unit_abbrev=_ABBREV,
            about=c.GRS_ABOUT,
            color=_COLOR,
            subunit_parent="Office of Security",
        ),
        info_tryout_requirements_embed(
            unit_abbrev=_ABBREV,
            combat_requirement=c.GRS_TRYOUT_COMBAT,
            color=_COLOR,
        ),
        info_community_links_embed(
            unit_abbrev=_ABBREV,
            color=_COLOR,
            fields=(
                c.link_field(
                    "Global Response Staff",
                    c.community_link_label("GRS"),
                    c.URL_ROBLOX_GROUP_GRS,
                ),
                c.link_field(
                    "Office of Security",
                    c.community_link_label("OSEC"),
                    c.URL_ROBLOX_GROUP_OSEC,
                ),
                c.link_field(
                    "Directorate of Support",
                    c.community_link_label("Directorate of Support"),
                    c.URL_ROBLOX_GROUP_DS,
                ),
            ),
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
