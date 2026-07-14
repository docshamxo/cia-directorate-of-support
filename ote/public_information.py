# === FILE HEADER ===
# Title: Public Information
# Path: ote/public_information.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
# === END FILE HEADER ===

"""
CIA OTE public information announcer.

Posts the Office of Training & Education overview and community links
to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_OTE_PUBLIC_INFORMATION")

def _build_embeds() -> list[c.discord.Embed]:
    ote_pillars = tuple(c.pillar_field(title, desc) for title, desc in c.OTE_PILLARS)

    return [
        c.embed(
            description=(
                "**Office of Training & Education Overview**\n\n"
                f"*{c.OTE_MOTTO}*\n\n"
                f"{c.OTE_ABOUT}"
            ),
            logo=c.LOGOS["ote"],
        ),
        c.embed(
            title="Program Pillars",
            description="The Officer Training Program is organized around three core pillars.",
            fields=ote_pillars,
        ),
        c.embed(
            title="Program Overview",
            description=(
                "How OTE is organized, who may apply or participate, how the chain of command "
                "works, what each phase covers, and how scheduling and key dates are handled. "
                "Read this first when you join or when policy or structure changes.\n\n"
                f"{c.link('CIA | Officer Training Program Overview', c.url('ote.public_information.program_overview'))}"
            ),
        ),
        c.embed(
            title="CIA OTE Roblox Group",
            description=c.link("Join the CIA OTE Roblox Group", c.URL_ROBLOX_GROUP_OTE),
        ),
        c.embed(description="**Stay informed. Stay prepared.**"),
        c.disclaimer_embed(),
    ]


def send_ote_public_information() -> None:
    c.send_webhook(
        WEBHOOK_URL,
        _build_embeds(),
        username=c.BOT_OTE,
        files=[c.logo_file(c.LOGOS["ote"])],
    )


if __name__ == "__main__":
    send_ote_public_information()

# === FILE FOOTER ===
# End of file: ote/public_information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
