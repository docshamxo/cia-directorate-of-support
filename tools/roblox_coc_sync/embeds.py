# === FILE HEADER ===
# Title: CoC Embed Builder (Sync)
# Path: tools/roblox_coc_sync/embeds.py
# Created: 2026-09-28
# Created by: docshamxo
# Modified:
#   - 2026-09-28 | docshamxo | Build DS CoC embeds from overridden Role catalog.
# === END FILE HEADER ===

"""Rebuild DS Chain of Command embeds using a Role catalog (YAML titles + Roblox holders)."""

from __future__ import annotations

from collections.abc import Mapping

import discord

from common import cia_common as c


def build_ds_coc_embeds(
    catalog: Mapping[str, tuple[c.Role, ...]],
) -> list[discord.Embed]:
    """Mirror ``units/ds/chain_of_command.py`` layout with injectable role holders."""
    agency = catalog.get("agency_executive", c.AGENCY_EXECUTIVE)
    ds = catalog.get("ds_leadership", c.DS_LEADERSHIP)
    ote = catalog.get("ote_high_command", c.OTE_HIGH_COMMAND)
    osec = catalog.get("osec_high_command", c.OSEC_HIGH_COMMAND)
    grs = catalog.get("grs_command", c.GRS_COMMAND)
    esd = catalog.get("esd_command", c.ESD_COMMAND)

    return [
        c.chain_intro_embed(unit="Directorate of Support", color=c.COLOR_DS),
        c.embed(
            title="Agency Executive Leadership",
            description=(
                "**Executive Chain of Command**\n\n"
                "Agency executive leadership sits above all Directorates. The "
                "**Directorate of Support (DS)** chain continues below."
            ),
            fields=(("Executive Leadership", c.roles_text(*agency)),),
        ),
        c.embed(
            title="Directorate of Support",
            description=(
                f"{c.motto_line(c.DS_MOTTO, classification=c.DS_CLASSIFICATION)}\n\n{c.DS_ABOUT}"
            ),
            logo=c.LOGOS["ds"],
            fields=(
                ("Leadership", c.roles_text(*ds)),
                ("Offices", c.bullets(*c.DS_OFFICES)),
            ),
        ),
        c.embed(
            title="Office of Training & Education",
            description=(f"{c.motto_line(c.OTE_MOTTO)}\n\n{c.OTE_ABOUT}"),
            logo=c.LOGOS["ote"],
            fields=(("High Command", c.roles_text(*ote)),),
        ),
        c.embed(
            title="Office of Security",
            description=(f"{c.motto_line(c.OSEC_MOTTO)}\n\n{c.OSEC_ABOUT}"),
            logo=c.LOGOS["osec"],
            fields=(
                ("High Command", c.roles_text(*osec)),
                ("Sub-Units", c.bullets(*c.OSEC_SUB_UNITS)),
            ),
        ),
        c.embed(
            title="Global Response Staff",
            description=(
                "A sub-unit of the **Office of Security** under the "
                "**Directorate of Support**.\n\n"
                f"{c.GRS_ABOUT}"
            ),
            logo=c.LOGOS["grs"],
            fields=(("Command Team", c.roles_text(*grs)),),
        ),
        c.embed(
            title="Executive Security Detail",
            description=(
                "A sub-unit of the **Office of Security** under the "
                "**Directorate of Support**.\n\n"
                f"{c.ESD_ABOUT}"
            ),
            logo=c.LOGOS["esd"],
            fields=(("Command Team", c.roles_text(*esd)),),
        ),
        c.embed(
            title="OSEC Rank Structure",
            description=(
                "Mid- and field-level ranks shared across the **Office of Security** and its "
                "sub-units (main OSEC, GRS, and ESD)."
            ),
            fields=(
                ("Middle Command", c.ranks_text(*c.OSEC_MIDDLE_COMMAND)),
                ("Low Command", c.ranks_text(*c.OSEC_LOW_COMMAND)),
            ),
        ),
    ]


# === FILE FOOTER ===
# End of file: tools/roblox_coc_sync/embeds.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
