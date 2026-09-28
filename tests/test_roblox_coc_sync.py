# === FILE HEADER ===
# Title: Test Roblox CoC Sync
# Path: tests/test_roblox_coc_sync.py
# Created: 2026-09-28
# Created by: docshamxo
# Modified:
#   - 2026-09-28 | docshamxo | Mapping, vacant, dry-run, config parse tests.
#   - 2026-09-28 | docshamxo | discord_id merge / map / clickable holder tests.
#   - 2026-09-28 | docshamxo | Multi-target DS + OTE CoC parse and embed tests.
# === END FILE HEADER ===

"""Unit tests for Roblox -> CoC sync helpers (no live Discord/Roblox)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest
import yaml

from common import cia_common as c
from tools.roblox_coc_sync.client import GroupMember, GroupRole
from tools.roblox_coc_sync.config import (
    GroupConfig,
    RoleMapping,
    SyncConfig,
    SyncTarget,
    parse_sync_config,
)
from tools.roblox_coc_sync.embeds import build_ds_coc_embeds, build_ote_coc_embeds
from tools.roblox_coc_sync.mapping import (
    HolderOverride,
    apply_holder_overrides,
    base_roles_catalog,
    collect_holder_overrides,
    format_holders,
)
from tools.roblox_coc_sync.sync import SyncSkip, run_once

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_format_holders_vacant() -> None:
    assert format_holders([]) == "VACANT"
    assert format_holders(["", "  "], vacant_label="VACANT") == "VACANT"
    assert format_holders(["Alice", "Bob"]) == "Alice, Bob"


def test_apply_holder_overrides_sets_vacant() -> None:
    catalog = {
        "ds_leadership": (
            c.Role("CDSD", "Component Director", "OldName", discord_id="111"),
            c.Role("DCDSD", "Deputy", "KeepMe", discord_id="222"),
        )
    }
    updated = apply_holder_overrides(
        catalog,
        {("ds_leadership", "CDSD"): "VACANT"},
    )
    assert updated["ds_leadership"][0].holder == "VACANT"
    assert updated["ds_leadership"][0].discord_id is None
    assert updated["ds_leadership"][1].holder == "KeepMe"
    assert updated["ds_leadership"][1].discord_id == "222"


def test_apply_holder_overrides_keeps_personnel_discord_id() -> None:
    catalog = {
        "ds_leadership": (c.Role("CDSD", "Component Director", "OldName", discord_id="10001"),)
    }
    updated = apply_holder_overrides(
        catalog,
        {("ds_leadership", "CDSD"): "RobloxOnlyName"},
    )
    role = updated["ds_leadership"][0]
    assert role.holder == "RobloxOnlyName"
    assert role.discord_id == "10001"
    assert "discord.com/users/10001" in role.format()
    assert "[RobloxOnlyName]" in role.format()


def test_apply_holder_overrides_uses_config_discord_ids_map() -> None:
    catalog = {
        "ds_leadership": (c.Role("CDSD", "Component Director", "OldName", discord_id="111"),)
    }
    cfg = SyncConfig(
        interval_minutes=15,
        targets=(SyncTarget("WEBHOOK_DS_CHAIN_OF_COMMAND", "WEBHOOK_DS_COC_MESSAGE_ID"),),
        groups={},
        mappings=(),
        discord_ids={"robloxuser": "20002", "42": "20002"},
    )
    updated = apply_holder_overrides(
        catalog,
        {
            ("ds_leadership", "CDSD"): HolderOverride(
                holder="RobloxUser",
                roblox_usernames=("RobloxUser",),
                roblox_user_ids=("42",),
            )
        },
        config=cfg,
    )
    role = updated["ds_leadership"][0]
    assert role.holder == "RobloxUser"
    assert role.discord_id == "20002"
    assert "[RobloxUser](https://discord.com/users/20002)" in role.format()


def test_parse_example_config() -> None:
    path = REPO_ROOT / "config" / "roblox_coc_sync.example.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    cfg = parse_sync_config(raw)
    assert cfg.interval_minutes == 15
    assert cfg.target.message_id_env == "WEBHOOK_DS_COC_MESSAGE_ID"
    assert len(cfg.targets) == 2
    assert cfg.targets[0].channel == "ds_coc"
    assert cfg.targets[1].channel == "ote_coc"
    assert cfg.targets[1].layout == "ote_coc"
    assert cfg.targets[1].webhook_env == "WEBHOOK_OTE_COC"
    assert cfg.targets[1].message_id_env == "WEBHOOK_OTE_COC_MESSAGE_ID"
    assert "ds" in cfg.groups
    assert cfg.groups["ds"].group_id == "945806945"
    assert any(m.abbrev == "CDSD" for m in cfg.mappings)
    assert any(m.personnel_key == "ote_high_command" for m in cfg.mappings)
    assert cfg.discord_ids == {}


def test_parse_legacy_singular_target() -> None:
    cfg = parse_sync_config(
        {
            "interval_minutes": 15,
            "target": {
                "channel": "ds_coc",
                "webhook_env": "WEBHOOK_DS_CHAIN_OF_COMMAND",
                "message_id_env": "WEBHOOK_DS_COC_MESSAGE_ID",
            },
            "groups": {},
            "mappings": [
                {
                    "personnel_key": "ds_leadership",
                    "abbrev": "CDSD",
                    "group": "ds",
                    "roblox_rank": 255,
                }
            ],
        }
    )
    assert len(cfg.targets) == 1
    assert cfg.target.channel == "ds_coc"


def test_parse_discord_ids_map() -> None:
    cfg = parse_sync_config(
        {
            "interval_minutes": 15,
            "target": {},
            "groups": {},
            "mappings": [
                {
                    "personnel_key": "ds_leadership",
                    "abbrev": "CDSD",
                    "group": "ds",
                    "roblox_rank": 255,
                }
            ],
            "discord_ids": {"Alice": "30003", "99": "30003"},
        }
    )
    assert cfg.discord_ids["Alice"] == "30003"
    assert cfg.discord_ids["alice"] == "30003"
    assert cfg.discord_ids["99"] == "30003"


def test_build_ds_coc_embeds_includes_overridden_holder() -> None:
    catalog = base_roles_catalog()
    catalog = apply_holder_overrides(
        catalog,
        {("ds_leadership", catalog["ds_leadership"][0].abbrev): "RobloxSyncUser"},
    )
    embeds = build_ds_coc_embeds(catalog)
    blob = "\n".join(
        [
            *(e.description or "" for e in embeds),
            *(f.value for e in embeds for f in e.fields),
        ]
    )
    assert "RobloxSyncUser" in blob
    c.validate_embed_limits(embeds)


def test_build_ote_coc_embeds_preserves_discord_profile_link() -> None:
    catalog = base_roles_catalog()
    first = catalog["ote_high_command"][0]
    assert first.discord_id
    catalog = apply_holder_overrides(
        catalog,
        {("ote_high_command", first.abbrev): "RobloxOteLead"},
    )
    embeds = build_ote_coc_embeds(catalog)
    blob = "\n".join(
        [
            *(e.description or "" for e in embeds),
            *(f.value for e in embeds for f in e.fields),
        ]
    )
    assert "RobloxOteLead" in blob
    assert f"discord.com/users/{first.discord_id}" in blob
    assert "OTE High Command" in "\n".join(e.title or "" for e in embeds)
    c.validate_embed_limits(embeds)


def test_run_once_dry_run_without_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ROBLOX_OPEN_CLOUD_API_KEY", raising=False)
    monkeypatch.delenv("WEBHOOK_DS_COC_MESSAGE_ID", raising=False)
    monkeypatch.delenv("WEBHOOK_OTE_COC_MESSAGE_ID", raising=False)
    path = REPO_ROOT / "config" / "roblox_coc_sync.example.yaml"
    summary = run_once(config_path=path, dry_run=True, channels=["ote_coc"])
    assert isinstance(summary, dict)


def test_run_once_live_skips_without_message_id(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CIA_DRY_RUN", raising=False)
    monkeypatch.setenv("ROBLOX_OPEN_CLOUD_API_KEY", "test-key-not-real")
    monkeypatch.setenv("WEBHOOK_DS_CHAIN_OF_COMMAND", "https://discord.com/api/webhooks/1/abc")
    monkeypatch.setenv("WEBHOOK_OTE_COC", "https://discord.com/api/webhooks/2/def")
    monkeypatch.delenv("WEBHOOK_DS_COC_MESSAGE_ID", raising=False)
    monkeypatch.delenv("WEBHOOK_OTE_COC_MESSAGE_ID", raising=False)

    fake_client = MagicMock()
    fake_client.find_role_by_rank.return_value = GroupRole("1", "Lead", 255)
    fake_client.list_members_for_role.return_value = [
        GroupMember("99", "SyncedUser"),
    ]
    fake_client.find_role_by_name.return_value = None

    path = REPO_ROOT / "config" / "roblox_coc_sync.example.yaml"
    with pytest.raises(SyncSkip, match="WEBHOOK_.*COC_MESSAGE_ID"):
        run_once(config_path=path, dry_run=False, client=fake_client)


def test_collect_overrides_empty_rank_is_vacant() -> None:
    cfg = SyncConfig(
        interval_minutes=15,
        targets=(SyncTarget("WEBHOOK_DS_CHAIN_OF_COMMAND", "WEBHOOK_DS_COC_MESSAGE_ID"),),
        groups={"ds": GroupConfig("ds", "1")},
        mappings=(
            RoleMapping(
                personnel_key="ds_leadership",
                abbrev="CDSD",
                group_key="ds",
                roblox_rank=255,
            ),
        ),
        vacant_label="VACANT",
    )
    client = MagicMock()
    client.find_role_by_rank.return_value = GroupRole("9", "Owner", 255)
    client.list_members_for_role.return_value = []
    overrides = collect_holder_overrides(client, cfg)
    assert overrides[("ds_leadership", "CDSD")].holder == "VACANT"


# === FILE FOOTER ===
# End of file: tests/test_roblox_coc_sync.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
