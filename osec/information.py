# === FILE HEADER ===
# Title: Information
# Path: osec/information.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Align internal info template and link grammar.
#   - 2026-07-17 | docshamxo | Community markings PUBLIC/STAFF.
# === END FILE HEADER ===

"""
CIA OSEC information announcer.

Posts official Office of Security reference documents and the personnel ORBAT
to a Discord webhook.
"""

from __future__ import annotations

import sys

from common import cia_common as c
from common.announcer import run_announcer


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.hero_embed(
            title="INFORMATION",
            unit="Office of Security",
            supporting=(
                "Official reference hub for Office of Security personnel records and "
                "authorized documentation."
            ),
            color=c.COLOR_OSEC,
            logo=c.LOGOS["osec"],
        ),
        c.embed(
            title="About the Office",
            description=(f"{c.motto_line(c.OSEC_MOTTO)}\n\n{c.OSEC_ABOUT}"),
            color=c.COLOR_OSEC,
        ),
        c.embed(
            title="Reference Documents",
            description=(
                "Agency-wide and Office of Security reference material. Review each document "
                "in full and observe its community marking."
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    "ORBAT",
                    "CIA OSEC | ORBAT",
                    c.url("osec.information.orbat"),
                    "PUBLIC.",
                ),
                c.link_field(
                    "Handbook",
                    "CIA OSEC | Handbook",
                    c.url("osec.information.handbook"),
                    "STAFF. Authorized OSEC staff only.",
                ),
                c.link_field(
                    "Conduct",
                    "CIA OSEC | Code of Agency Conduct",
                    c.url("osec.information.code_of_agency_conduct"),
                    "PUBLIC.",
                ),
                c.link_field(
                    "Civilian Access",
                    "CIA OSEC | Civilian Access",
                    c.url("osec.information.civilian_access"),
                    "PUBLIC.",
                ),
            ),
        ),
        c.embed(
            title="Classification & Handling Notice",
            description=(
                "The **CIA OSEC | Handbook** is marked **STAFF**. Unauthorized disclosure, "
                "redistribution, or leaking of this document will result in a **BLACKLIST** "
                "from the **CIA Office of Security**.\n\n"
                "The **ORBAT**, **Code of Agency Conduct**, and **Civilian Access** documents "
                "are **PUBLIC** and may be referenced in accordance with community policy.\n\n"
                "Handle all materials responsibly. Do not share restricted documents outside "
                "authorized channels or personnel."
            ),
            color=c.COLOR_OSEC,
        ),
        c.disclaimer_embed(staff=True, color=c.COLOR_OSEC),
    ]


def send_osec_information() -> None:
    run_announcer(
        webhook_key="WEBHOOK_OSEC_INFORMATION",
        username=c.BOT_OSEC,
        build_embeds=_build_embeds,
        files=[c.logo_file(c.LOGOS["osec"])],
        dry_run="--dry-run" in sys.argv,
    )


if __name__ == "__main__":
    send_osec_information()

# === FILE FOOTER ===
# End of file: osec/information.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
