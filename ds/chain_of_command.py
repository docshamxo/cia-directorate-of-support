# === FILE HEADER ===
# Title: Chain Of Command
# Path: ds/chain_of_command.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
# === END FILE HEADER ===

"""
CIA Directorate of Support chain of command announcer.

Posts the DS organizational hierarchy — including OTE, OSEC, and OSEC sub-units —
to a Discord webhook, including component logos.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_DS_CHAIN_OF_COMMAND")


def _build_intro_embed() -> c.discord.Embed:
    return c.embed(
        description=(
            "**Chain of Command (CoC)**\n\n"
            f"{c.CHAIN_OF_COMMAND_INTRO}"
        ),
    )


def _build_agency_embed() -> c.discord.Embed:
    return c.embed(
        title="Agency Executive Leadership",
        description=(
            "*Central Intelligence Agency · Executive Chain of Command*\n\n"
            "Agency executive leadership sits above all Directorates. The "
            "**Directorate of Support (DS)** chain continues below."
        ),
        fields=(("Executive Leadership", c.roles_text(*c.AGENCY_EXECUTIVE)),),
    )


def _build_ds_embed() -> c.discord.Embed:
    return c.embed(
        title="Directorate of Support",
        description=(
            f"*{c.DS_MOTTO} · Classification: {c.DS_CLASSIFICATION}*\n\n"
            f"{c.DS_ABOUT}"
        ),
        logo=c.LOGOS["ds"],
        fields=(
            ("Leadership", c.roles_text(*c.DS_LEADERSHIP)),
            ("Offices", c.bullets(*c.DS_OFFICES)),
        ),
    )


def _build_ote_embed() -> c.discord.Embed:
    return c.embed(
        title="Office of Training & Education",
        description=(
            f"*{c.OTE_MOTTO}*\n\n"
            f"{c.OTE_ABOUT}"
        ),
        logo=c.LOGOS["ote"],
        fields=(("High Command", c.roles_text(*c.OTE_HIGH_COMMAND)),),
    )


def _build_osec_embed() -> c.discord.Embed:
    return c.embed(
        title="Office of Security",
        description=(
            f"*{c.OSEC_MOTTO}*\n\n"
            f"{c.OSEC_ABOUT}"
        ),
        logo=c.LOGOS["osec"],
        fields=(
            ("High Command", c.roles_text(*c.OSEC_HIGH_COMMAND)),
            ("Main Element — Chief Marshals", c.roles_text(*c.OSEC_MAIN_CHIEF_MARSHALS)),
            ("Sub-Units", c.bullets(*c.OSEC_SUB_UNITS)),
        ),
    )


def _build_grs_embed() -> c.discord.Embed:
    return c.embed(
        title="Global Response Staff",
        description=(
            "A sub-unit of the **Office of Security** under the **Directorate of Support**.\n\n"
            f"{c.GRS_ABOUT}"
        ),
        logo=c.LOGOS["grs"],
        fields=(("Command Team", c.roles_text(*c.GRS_COMMAND)),),
    )


def _build_esd_embed() -> c.discord.Embed:
    return c.embed(
        title="Executive Security Detail",
        description=(
            "A sub-unit of the **Office of Security** under the **Directorate of Support**.\n\n"
            f"{c.ESD_ABOUT}"
        ),
        logo=c.LOGOS["esd"],
        fields=(("Command Team", c.roles_text(*c.ESD_COMMAND)),),
    )


def _build_ranks_embed() -> c.discord.Embed:
    return c.embed(
        title="OSEC Rank Structure",
        description=(
            "Mid- and field-level ranks shared across the **Office of Security** and its "
            "sub-units (main OSEC, GRS, and ESD)."
        ),
        fields=(
            ("Middle Command", c.ranks_text(*c.OSEC_MIDDLE_COMMAND)),
            ("Low Command", c.ranks_text(*c.OSEC_LOW_COMMAND)),
        ),
    )


def _build_embeds() -> list[c.discord.Embed]:
    return [
        _build_intro_embed(),
        _build_agency_embed(),
        _build_ds_embed(),
        _build_ote_embed(),
        _build_osec_embed(),
        _build_grs_embed(),
        _build_esd_embed(),
        _build_ranks_embed(),
        c.disclaimer_embed(),
    ]


def send_chain_of_command() -> None:
    logo_files = [c.logo_file(path) for path in c.LOGOS.values()]
    c.send_webhook(
        WEBHOOK_URL,
        _build_embeds(),
        username=c.BOT_DS,
        files=logo_files,
    )


if __name__ == "__main__":
    send_chain_of_command()

# === FILE FOOTER ===
# End of file: ds/chain_of_command.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
