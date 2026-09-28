# === FILE HEADER ===
# Title: Roblox → CoC Mapping
# Path: tools/roblox_coc_sync/mapping.py
# Created: 2026-09-28
# Created by: docshamxo
# Modified:
#   - 2026-09-28 | docshamxo | Map Roblox ranks onto personnel Role tuples.
# === END FILE HEADER ===

"""Apply Roblox group members onto CoC Role holders."""

from __future__ import annotations

import logging
from collections.abc import Mapping

from common import cia_common as c

from tools.roblox_coc_sync.client import GroupRole, RobloxOpenCloudClient
from tools.roblox_coc_sync.config import RoleMapping, SyncConfig

logger = logging.getLogger("cia.roblox_coc_sync.mapping")

PERSONNEL_ROLE_ATTRS: dict[str, str] = {
    "agency_executive": "AGENCY_EXECUTIVE",
    "ds_leadership": "DS_LEADERSHIP",
    "ote_high_command": "OTE_HIGH_COMMAND",
    "osec_high_command": "OSEC_HIGH_COMMAND",
    "grs_command": "GRS_COMMAND",
    "esd_command": "ESD_COMMAND",
}


def base_roles_catalog() -> dict[str, tuple[c.Role, ...]]:
    """Snapshot current YAML-backed Role tuples (titles/abbrevs source of truth)."""
    return {
        key: getattr(c, attr)
        for key, attr in PERSONNEL_ROLE_ATTRS.items()
        if hasattr(c, attr)
    }


def format_holders(usernames: list[str], *, vacant_label: str = "VACANT") -> str:
    cleaned = [name.strip() for name in usernames if name and name.strip()]
    if not cleaned:
        return vacant_label
    return ", ".join(cleaned)


def apply_holder_overrides(
    catalog: Mapping[str, tuple[c.Role, ...]],
    overrides: Mapping[tuple[str, str], str],
) -> dict[str, tuple[c.Role, ...]]:
    """Return a new catalog with holder text replaced for (personnel_key, abbrev)."""
    result: dict[str, tuple[c.Role, ...]] = {}
    for key, roles in catalog.items():
        updated: list[c.Role] = []
        for role in roles:
            override = overrides.get((key, role.abbrev))
            if override is None:
                updated.append(role)
                continue
            # Rebuild Role with Roblox holder. Drop discord_id when present so
            # stale Discord profile links are not shown for a new Roblox name.
            kwargs: dict[str, object] = {
                "abbrev": role.abbrev,
                "title": role.title,
                "holder": override,
            }
            if "discord_id" in getattr(c.Role, "__dataclass_fields__", {}):
                kwargs["discord_id"] = None
            updated.append(c.Role(**kwargs))  # type: ignore[arg-type]
        result[key] = tuple(updated)
    return result


def resolve_role_for_mapping(
    client: RobloxOpenCloudClient,
    *,
    group_id: str,
    mapping: RoleMapping,
) -> GroupRole | None:
    if mapping.roblox_rank is not None:
        found = client.find_role_by_rank(group_id, mapping.roblox_rank)
        if found:
            return found
    if mapping.roblox_role_name:
        return client.find_role_by_name(group_id, mapping.roblox_role_name)
    return None


def collect_holder_overrides(
    client: RobloxOpenCloudClient,
    config: SyncConfig,
) -> dict[tuple[str, str], str]:
    """Query Roblox for each mapping and return (personnel_key, abbrev) → holder text."""
    overrides: dict[tuple[str, str], str] = {}
    for mapping in config.mappings:
        group = config.groups.get(mapping.group_key)
        if group is None:
            logger.warning(
                "event=missing_group mapping=%s/%s group=%s",
                mapping.personnel_key,
                mapping.abbrev,
                mapping.group_key,
            )
            overrides[(mapping.personnel_key, mapping.abbrev)] = config.vacant_label
            continue

        role = resolve_role_for_mapping(client, group_id=group.group_id, mapping=mapping)
        if role is None:
            logger.warning(
                "event=role_not_found group=%s rank=%s name=%s mapping=%s/%s",
                group.group_id,
                mapping.roblox_rank,
                mapping.roblox_role_name,
                mapping.personnel_key,
                mapping.abbrev,
            )
            overrides[(mapping.personnel_key, mapping.abbrev)] = config.vacant_label
            continue

        members = client.list_members_for_role(
            group.group_id,
            role,
            max_members=mapping.max_holders,
        )
        usernames = [m.username for m in members[: mapping.max_holders]]
        holder = format_holders(usernames, vacant_label=config.vacant_label)
        overrides[(mapping.personnel_key, mapping.abbrev)] = holder
        logger.info(
            "event=mapped personnel=%s abbrev=%s holder=%s roblox_rank=%s",
            mapping.personnel_key,
            mapping.abbrev,
            holder,
            role.rank,
        )
    return overrides


# === FILE FOOTER ===
# End of file: tools/roblox_coc_sync/mapping.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
