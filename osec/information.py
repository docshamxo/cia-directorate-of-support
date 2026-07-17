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
#   - 2026-07-17 | docshamxo | Clearer field names and text marking notes for accessibility.
#   - 2026-07-17 | docshamxo | Use DS Community link labels (brand/legal).
#   - 2026-07-17 | docshamxo | Shared marking notes; leaner mixed-marking handling closer.
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
            supporting="Reference hub for OSEC records and authorized documentation.",
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
                "Agency-wide and Office of Security reference material. Observe each "
                "document's community marking."
            ),
            color=c.COLOR_OSEC,
            fields=(
                c.link_field(
                    "Order of Battle (ORBAT)",
                    "DS Community | OSEC Order of Battle (ORBAT)",
                    c.url("osec.information.orbat"),
                    c.marking_note("PUBLIC"),
                ),
                c.link_field(
                    "Handbook",
                    "DS Community | OSEC Handbook",
                    c.url("osec.information.handbook"),
                    c.marking_note("STAFF"),
                ),
                c.link_field(
                    "Code of Agency Conduct",
                    "DS Community | OSEC Code of Agency Conduct",
                    c.url("osec.information.code_of_agency_conduct"),
                    c.marking_note("PUBLIC"),
                ),
                c.link_field(
                    "Civilian Access",
                    "DS Community | OSEC Civilian Access",
                    c.url("osec.information.civilian_access"),
                    c.marking_note("PUBLIC"),
                ),
            ),
        ),
        c.embed(
            title="Classification & Handling Notice",
            description=(
                "**Handbook** -- **STAFF**. Unauthorized disclosure or redistribution will "
                "result in a **BLACKLIST** from the **CIA Office of Security**.\n\n"
                "**Order of Battle (ORBAT)**, **Code of Agency Conduct**, and "
                "**Civilian Access** -- **PUBLIC**.\n\n"
                "Do not share restricted documents outside authorized channels or personnel."
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
