# === FILE HEADER ===
# Title: Information
# Path: units/esd/information.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Align public-info template and link grammar.
#   - 2026-08-04 | docshamxo | Align ESD information hero with PUBLIC channel template.
#   - 2026-08-04 | docshamxo | Omit Disclaimer embed on ESD public information.
#   - 2026-08-30 | docshamxo | Wire ESD Roblox group link into community embed.
#   - 2026-08-30 | docshamxo | Add ESD tryout / application requirements embed.
#   - 2026-09-08 | docshamxo | Refactor onto shared information-channel frame builders.
# === END FILE HEADER ===

"""
CIA ESD public information announcer.

Posts the Executive Security Detail overview and community links
to a Discord webhook.
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

_UNIT = "Executive Security Detail"
_ABBREV = "ESD"
_COLOR = c.COLOR_ESD


def _build_embeds() -> list[c.discord.Embed]:
    return [
        info_hero_embed(
            unit_full=_UNIT,
            unit_abbrev=_ABBREV,
            color=_COLOR,
            logo=c.LOGOS["esd"],
        ),
        info_about_embed(
            unit_full=_UNIT,
            unit_abbrev=_ABBREV,
            about=c.ESD_ABOUT,
            color=_COLOR,
            subunit_parent="Office of Security",
        ),
        info_tryout_requirements_embed(
            unit_abbrev=_ABBREV,
            combat_requirement=c.ESD_TRYOUT_COMBAT,
            color=_COLOR,
        ),
        info_community_links_embed(
            unit_abbrev=_ABBREV,
            color=_COLOR,
            fields=(
                c.link_field(
                    "Executive Security Detail",
                    c.community_link_label("ESD"),
                    c.URL_ROBLOX_GROUP_ESD,
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


def send_esd_information() -> None:
    run_announcer(
        webhook_key="WEBHOOK_ESD_INFORMATION",
        username=c.BOT_ESD,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["esd"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_esd_information()

# === FILE FOOTER ===
# End of file: units/esd/information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
