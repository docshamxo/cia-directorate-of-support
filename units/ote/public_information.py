# === FILE HEADER ===
# Title: Public Information
# Path: units/ote/public_information.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Align public-info template, hero, and link grammar.
#   - 2026-07-17 | docshamxo | Accessible marking notes on public links.
# === END FILE HEADER ===

"""
CIA OTE public information announcer.

Posts the Office of Training & Education overview and community links
to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    ote_pillars = tuple(c.pillar_field(title, desc) for title, desc in c.OTE_PILLARS)

    return [
        c.hero_embed(
            title="PUBLIC INFORMATION",
            unit="Office of Training & Education",
            supporting="Overview of OTE, the Officer Training Program, and community links.",
            color=c.COLOR_OTE,
            logo=c.LOGOS["ote"],
        ),
        c.embed(
            title="About the Office",
            description=(f"{c.motto_line(c.OTE_MOTTO)}\n\n{c.OTE_ABOUT}"),
            color=c.COLOR_OTE,
            fields=ote_pillars,
        ),
        c.embed(
            title="Community Links",
            description="Official documents and Roblox group for OTE.",
            color=c.COLOR_OTE,
            fields=(
                c.link_field(
                    "Program Overview",
                    c.community_link_label("OTE Program Overview"),
                    c.url("ote.public_information.program_overview"),
                    c.marking_note("PUBLIC"),
                ),
                c.link_field(
                    "Office of Training & Education",
                    c.community_link_label("OTE"),
                    c.URL_ROBLOX_GROUP_OTE,
                ),
            ),
        ),
        c.disclaimer_embed(links=True, color=c.COLOR_OTE),
    ]


def send_ote_public_information() -> None:
    run_announcer(
        webhook_key="WEBHOOK_OTE_PUBLIC_INFORMATION",
        username=c.BOT_OTE,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["ote"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_ote_public_information()

# === FILE FOOTER ===
# End of file: units/ote/public_information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
