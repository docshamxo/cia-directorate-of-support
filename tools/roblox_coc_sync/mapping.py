# === FILE HEADER ===
# Title: Roblox → CoC Mapping
# Path: tools/roblox_coc_sync/mapping.py
# Created: 2026-09-28
# Created by: docshamxo
# Modified:
#   - 2026-09-28 | docshamxo | Map Roblox ranks onto personnel Role tuples.
#   - 2026-09-28 | docshamxo | Keep/merge discord_id so CoC profile links stay clickable.
# === END FILE HEADER ===

"""Apply Roblox group members onto CoC Role holders."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass

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


@dataclass(frozen=True, slots=True)
class HolderOverride:
    """Roblox-derived holder text plus ids used to resolve Discord profile links."""

    holder: str
    roblox_usernames: tuple[str, ...] = ()
    roblox_user_ids: tuple[str, ...] = ()


def base_roles_catalog() -> dict[str, tuple[c.Role, ...]]:
    """Snapshot current YAML-backed Role tuples (titles/abbrevs source of truth)."""
    return {key: getattr(c, attr) for key, attr in PERSONNEL_ROLE_ATTRS.items() if hasattr(c, attr)}


def format_holders(usernames: list[str], *, vacant_label: str = "VACANT") -> str:
    cleaned = [name.strip() for name in usernames if name and name.strip()]
    if not cleaned:
        return vacant_label
    return ", ".join(cleaned)


def resolve_discord_id(
    *,
    holder: str,
    existing: c.Role,
    vacant_label: str = "VACANT",
    discord_ids: Mapping[str, str] | None = None,
    roblox_usernames: tuple[str, ...] = (),
    roblox_user_ids: tuple[str, ...] = (),
) -> str | None:
    """Pick a Discord snowflake for a Roblox-synced holder.

    Order:
    1. Vacant → None
    2. Optional ``discord_ids`` map (Roblox username or user id)
    3. Existing ``personnel.yaml`` ``discord_id`` on the same abbrev slot
    """
    vacant = (vacant_label or "VACANT").strip().upper()
    if not holder or holder.strip().upper() == vacant or holder.strip().upper() == "VACANT":
        return None

    id_map = discord_ids or {}
    for name in roblox_usernames or tuple(
        part.strip() for part in holder.split(",") if part.strip()
    ):
        mapped = id_map.get(name) or id_map.get(name.lower())
        if mapped:
            return mapped
    for uid in roblox_user_ids:
        mapped = id_map.get(uid) or id_map.get(str(uid).strip())
        if mapped:
            return mapped

    return getattr(existing, "discord_id", None)


def apply_holder_overrides(
    catalog: Mapping[str, tuple[c.Role, ...]],
    overrides: Mapping[tuple[str, str], str | HolderOverride],
    *,
    config: SyncConfig | None = None,
) -> dict[str, tuple[c.Role, ...]]:
    """Return a new catalog with holder text replaced for (personnel_key, abbrev).

    Keeps clickable Discord profile links by merging Roblox display names with:
    - ``config.discord_ids`` (roblox username / user id → discord snowflake), else
    - existing ``Role.discord_id`` from personnel.yaml when the abbrev matches.
    """
    vacant_label = (config.vacant_label if config else "VACANT") or "VACANT"
    id_map = (config.discord_ids if config else None) or {}
    result: dict[str, tuple[c.Role, ...]] = {}
    for key, roles in catalog.items():
        updated: list[c.Role] = []
        for role in roles:
            raw = overrides.get((key, role.abbrev))
            if raw is None:
                updated.append(role)
                continue
            if isinstance(raw, HolderOverride):
                override = raw.holder
                usernames = raw.roblox_usernames
                user_ids = raw.roblox_user_ids
            else:
                override = raw
                usernames = tuple(part.strip() for part in override.split(",") if part.strip())
                user_ids = ()

            kwargs: dict[str, object] = {
                "abbrev": role.abbrev,
                "title": role.title,
                "holder": override,
            }
            if "discord_id" in getattr(c.Role, "__dataclass_fields__", {}):
                kwargs["discord_id"] = resolve_discord_id(
                    holder=override,
                    existing=role,
                    vacant_label=vacant_label,
                    discord_ids=id_map,
                    roblox_usernames=usernames,
                    roblox_user_ids=user_ids,
                )
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
) -> dict[tuple[str, str], HolderOverride]:
    """Query Roblox for each mapping and return (personnel_key, abbrev) → override."""
    overrides: dict[tuple[str, str], HolderOverride] = {}
    for mapping in config.mappings:
        group = config.groups.get(mapping.group_key)
        if group is None:
            logger.warning(
                "event=missing_group mapping=%s/%s group=%s",
                mapping.personnel_key,
                mapping.abbrev,
                mapping.group_key,
            )
            overrides[(mapping.personnel_key, mapping.abbrev)] = HolderOverride(
                holder=config.vacant_label
            )
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
            overrides[(mapping.personnel_key, mapping.abbrev)] = HolderOverride(
                holder=config.vacant_label
            )
            continue

        members = client.list_members_for_role(
            group.group_id,
            role,
            max_members=mapping.max_holders,
        )
        sliced = members[: mapping.max_holders]
        usernames = tuple(m.username for m in sliced)
        user_ids = tuple(m.user_id for m in sliced)
        holder = format_holders(list(usernames), vacant_label=config.vacant_label)
        overrides[(mapping.personnel_key, mapping.abbrev)] = HolderOverride(
            holder=holder,
            roblox_usernames=usernames,
            roblox_user_ids=user_ids,
        )
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
