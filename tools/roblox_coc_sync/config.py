# === FILE HEADER ===
# Title: Roblox CoC Sync Config
# Path: tools/roblox_coc_sync/config.py
# Created: 2026-09-28
# Created by: docshamxo
# Modified:
#   - 2026-09-28 | docshamxo | Load YAML mapping + env overrides.
#   - 2026-09-28 | docshamxo | Optional roblox->discord_id map for clickable CoC links.
#   - 2026-09-28 | docshamxo | Multi-target sync (DS + OTE CoC layouts).
# === END FILE HEADER ===

"""Load roblox_coc_sync YAML and resolve env placeholders."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = REPO_ROOT / "config" / "roblox_coc_sync.yaml"
EXAMPLE_CONFIG_PATH = REPO_ROOT / "config" / "roblox_coc_sync.example.yaml"

KNOWN_LAYOUTS = frozenset({"ds_coc", "ote_coc"})


@dataclass(frozen=True, slots=True)
class GroupConfig:
    key: str
    group_id: str


@dataclass(frozen=True, slots=True)
class RoleMapping:
    """One CoC slot synced from a Roblox group rank/role."""

    personnel_key: str
    abbrev: str
    group_key: str
    roblox_rank: int | None = None
    roblox_role_name: str | None = None
    max_holders: int = 1


@dataclass(frozen=True, slots=True)
class SyncTarget:
    webhook_env: str
    message_id_env: str
    channel: str = "ds_coc"
    layout: str = "ds_coc"


@dataclass(frozen=True, slots=True)
class SyncConfig:
    interval_minutes: int
    targets: tuple[SyncTarget, ...]
    groups: dict[str, GroupConfig]
    mappings: tuple[RoleMapping, ...]
    vacant_label: str = "VACANT"
    dry_run_default: bool = False
    # Keys: Roblox username (case-insensitive) or Roblox user id -> Discord snowflake.
    discord_ids: dict[str, str] | None = None

    @property
    def target(self) -> SyncTarget:
        """First sync target (backward-compatible accessor)."""
        return self.targets[0]


def resolve_config_path(explicit: Path | None = None) -> Path:
    if explicit is not None:
        return explicit
    env_path = os.environ.get("ROBLOX_COC_SYNC_CONFIG", "").strip()
    if env_path:
        return Path(env_path)
    if DEFAULT_CONFIG_PATH.is_file():
        return DEFAULT_CONFIG_PATH
    return EXAMPLE_CONFIG_PATH


def load_sync_config(path: Path | None = None) -> SyncConfig:
    config_path = resolve_config_path(path)
    if not config_path.is_file():
        raise FileNotFoundError(
            f"Missing sync config at {config_path}. "
            f"Copy {EXAMPLE_CONFIG_PATH.name} -> roblox_coc_sync.yaml and edit ranks."
        )
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return parse_sync_config(raw)


def parse_sync_config(raw: dict[str, Any]) -> SyncConfig:
    targets = _parse_targets(raw)

    groups: dict[str, GroupConfig] = {}
    for key, item in (raw.get("groups") or {}).items():
        group_id = _resolve_group_id(key, item or {})
        if not group_id:
            continue
        groups[str(key)] = GroupConfig(key=str(key), group_id=group_id)

    mappings: list[RoleMapping] = []
    for item in raw.get("mappings") or []:
        rank = item.get("roblox_rank")
        role_name = item.get("roblox_role_name")
        if rank is None and not role_name:
            raise ValueError(
                f"Mapping {item.get('personnel_key')}/{item.get('abbrev')} "
                "needs roblox_rank or roblox_role_name"
            )
        mappings.append(
            RoleMapping(
                personnel_key=str(item["personnel_key"]),
                abbrev=str(item["abbrev"]),
                group_key=str(item["group"]),
                roblox_rank=int(rank) if rank is not None else None,
                roblox_role_name=str(role_name) if role_name else None,
                max_holders=max(1, int(item.get("max_holders") or 1)),
            )
        )

    interval = int(
        os.environ.get("ROBLOX_COC_SYNC_INTERVAL_MINUTES") or raw.get("interval_minutes") or 15
    )
    return SyncConfig(
        interval_minutes=max(1, interval),
        targets=targets,
        groups=groups,
        mappings=tuple(mappings),
        vacant_label=str(raw.get("vacant_label") or "VACANT"),
        dry_run_default=bool(raw.get("dry_run_default") or False),
        discord_ids=_parse_discord_ids(raw.get("discord_ids")),
    )


def _parse_targets(raw: dict[str, Any]) -> tuple[SyncTarget, ...]:
    """Accept ``targets:`` list or legacy singular ``target:``."""
    targets_raw = raw.get("targets")
    if targets_raw is None and raw.get("target") is not None:
        targets_raw = [raw["target"]]
    if not targets_raw:
        targets_raw = [
            {
                "channel": "ds_coc",
                "layout": "ds_coc",
                "webhook_env": "WEBHOOK_DS_CHAIN_OF_COMMAND",
                "message_id_env": "WEBHOOK_DS_COC_MESSAGE_ID",
            }
        ]

    parsed: list[SyncTarget] = []
    seen_channels: set[str] = set()
    for item in targets_raw:
        item = item or {}
        channel = str(item.get("channel") or "ds_coc").strip() or "ds_coc"
        layout = str(item.get("layout") or channel or "ds_coc").strip() or "ds_coc"
        if layout not in KNOWN_LAYOUTS:
            raise ValueError(
                f"Unknown sync layout {layout!r} for channel {channel!r}; "
                f"expected one of {sorted(KNOWN_LAYOUTS)}"
            )
        if channel in seen_channels:
            raise ValueError(f"Duplicate sync target channel {channel!r}")
        seen_channels.add(channel)

        defaults = _defaults_for_layout(layout)
        parsed.append(
            SyncTarget(
                webhook_env=str(item.get("webhook_env") or defaults["webhook_env"]),
                message_id_env=str(item.get("message_id_env") or defaults["message_id_env"]),
                channel=channel,
                layout=layout,
            )
        )
    return tuple(parsed)


def _defaults_for_layout(layout: str) -> dict[str, str]:
    if layout == "ote_coc":
        return {
            "webhook_env": "WEBHOOK_OTE_COC",
            "message_id_env": "WEBHOOK_OTE_COC_MESSAGE_ID",
        }
    return {
        "webhook_env": "WEBHOOK_DS_CHAIN_OF_COMMAND",
        "message_id_env": "WEBHOOK_DS_COC_MESSAGE_ID",
    }


def _parse_discord_ids(raw: object | None) -> dict[str, str]:
    """Parse optional roblox username / user id -> Discord snowflake map."""
    if not isinstance(raw, dict):
        return {}
    out: dict[str, str] = {}
    for key, value in raw.items():
        if value is None:
            continue
        snowflake = str(value).strip()
        if not snowflake:
            continue
        if not snowflake.isdigit():
            raise ValueError(
                f"discord_ids[{key!r}] must be a numeric Discord snowflake, got {value!r}"
            )
        key_str = str(key).strip()
        if not key_str:
            continue
        out[key_str] = snowflake
        out[key_str.lower()] = snowflake
    return out


def _resolve_group_id(key: str, item: dict[str, Any]) -> str:
    env_name = str(item.get("group_id_env") or f"ROBLOX_GROUP_ID_{key.upper()}")
    from_env = os.environ.get(env_name, "").strip()
    if from_env:
        return from_env
    default = item.get("default_group_id") or item.get("group_id") or ""
    return str(default).strip()


def env_or_none(name: str) -> str | None:
    value = os.environ.get(name, "").strip()
    return value or None


# === FILE FOOTER ===
# End of file: tools/roblox_coc_sync/config.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
