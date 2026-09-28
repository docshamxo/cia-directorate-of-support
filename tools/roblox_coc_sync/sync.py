# === FILE HEADER ===
# Title: Roblox CoC Sync Orchestrator
# Path: tools/roblox_coc_sync/sync.py
# Created: 2026-09-28
# Created by: docshamxo
# Modified:
#   - 2026-09-28 | docshamxo | One-shot sync: Roblox -> embeds -> webhook edit.
#   - 2026-09-28 | docshamxo | Pass sync config into holder overrides for discord_id merge.
#   - 2026-09-28 | docshamxo | Multi-target DS + OTE CoC webhook edits.
# === END FILE HEADER ===

"""One-shot and looped CoC sync entrypoints."""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path

from common import cia_common as c
from common.announcer import is_dry_run, preview_embeds
from tools.roblox_coc_sync.client import RobloxOpenCloudClient
from tools.roblox_coc_sync.config import SyncConfig, SyncTarget, env_or_none, load_sync_config
from tools.roblox_coc_sync.discord_edit import edit_webhook_message
from tools.roblox_coc_sync.embeds import (
    bot_username_for_layout,
    build_embeds_for_layout,
    logo_paths_for_layout,
)
from tools.roblox_coc_sync.mapping import (
    apply_holder_overrides,
    base_roles_catalog,
    collect_holder_overrides,
)

logger = logging.getLogger("cia.roblox_coc_sync")


class SyncSkip(RuntimeError):
    """Non-fatal skip (missing message id / credentials in dry contexts)."""


def run_once(
    *,
    config: SyncConfig | None = None,
    config_path: Path | None = None,
    dry_run: bool | None = None,
    client: RobloxOpenCloudClient | None = None,
    channels: list[str] | None = None,
) -> dict[str, str]:
    """Pull Roblox ranks, rebuild CoC embeds, edit configured webhook message(s).

    Returns a summary dict of (personnel_key/abbrev -> holder) for logging/tests.
    """
    cfg = config or load_sync_config(config_path)
    effective_dry = is_dry_run(dry_run=dry_run) or cfg.dry_run_default
    targets = _select_targets(cfg, channels)

    api_key = env_or_none("ROBLOX_OPEN_CLOUD_API_KEY")
    if client is None:
        if not api_key:
            if effective_dry:
                logger.warning("event=dry_run_no_api_key using YAML holders only (no Roblox pull)")
                catalog = base_roles_catalog()
                overrides: dict = {}
            else:
                raise SyncSkip(
                    "Set ROBLOX_OPEN_CLOUD_API_KEY (Open Cloud user API key with group:read)."
                )
        else:
            client = RobloxOpenCloudClient(api_key)

    if client is not None:
        overrides = collect_holder_overrides(client, cfg)
        catalog = apply_holder_overrides(base_roles_catalog(), overrides, config=cfg)
    else:
        catalog = base_roles_catalog()
        overrides = {}

    def _holder_text(value: object) -> str:
        return value.holder if hasattr(value, "holder") else str(value)

    summary = {f"{k}/{a}": _holder_text(h) for (k, a), h in overrides.items()}
    skips: list[str] = []

    for target in targets:
        try:
            _sync_target(
                target=target,
                catalog=catalog,
                effective_dry=effective_dry,
            )
        except SyncSkip as exc:
            logger.warning(
                "event=target_skip channel=%s reason=%s",
                target.channel,
                exc,
            )
            skips.append(f"{target.channel}: {exc}")

    if skips and not effective_dry:
        if len(skips) == len(targets):
            raise SyncSkip("; ".join(skips))
        logger.warning(
            "event=partial_skip skipped=%s ok=%s",
            len(skips),
            len(targets) - len(skips),
        )

    if effective_dry:
        logger.info(
            "event=dry_run_complete overrides=%s targets=%s",
            len(summary),
            len(targets),
        )
    return summary


def _select_targets(cfg: SyncConfig, channels: list[str] | None) -> tuple[SyncTarget, ...]:
    if not channels:
        return cfg.targets
    wanted = {name.strip() for name in channels if name and name.strip()}
    selected = tuple(t for t in cfg.targets if t.channel in wanted)
    if not selected:
        known = ", ".join(t.channel for t in cfg.targets) or "(none)"
        raise SyncSkip(f"No sync targets matched {sorted(wanted)}; configured channels: {known}")
    return selected


def _sync_target(
    *,
    target: SyncTarget,
    catalog: dict[str, tuple[c.Role, ...]],
    effective_dry: bool,
) -> None:
    embeds = build_embeds_for_layout(target.layout, catalog)
    c.validate_embed_limits(embeds)
    username = bot_username_for_layout(target.layout)

    webhook_url = env_or_none(target.webhook_env)
    message_id_raw = env_or_none(target.message_id_env)

    if effective_dry:
        preview_embeds(
            embeds,
            webhook_key=target.webhook_env,
            username=username,
        )
        return

    if not webhook_url:
        raise SyncSkip(f"Set {target.webhook_env} in .env")
    if not message_id_raw:
        raise SyncSkip(
            f"Set {target.message_id_env} to the Discord webhook message snowflake "
            f"to edit (channel={target.channel})."
        )
    if not message_id_raw.isdigit():
        raise SyncSkip(f"{target.message_id_env} must be a numeric snowflake")

    files = [c.logo_file(path) for path in logo_paths_for_layout(target.layout)]
    edit_webhook_message(
        webhook_url=webhook_url,
        message_id=int(message_id_raw),
        embeds=embeds,
        username=username,
        files=files,
        dry_run=False,
    )
    logger.info(
        "event=target_ok channel=%s layout=%s message_id=%s",
        target.channel,
        target.layout,
        message_id_raw,
    )


def run_loop(
    *,
    config: SyncConfig | None = None,
    config_path: Path | None = None,
    dry_run: bool | None = None,
    once: bool = False,
    channels: list[str] | None = None,
) -> None:
    """Run sync once, or every ``interval_minutes`` until interrupted."""
    cfg = config or load_sync_config(config_path)
    interval_s = cfg.interval_minutes * 60

    while True:
        started = time.monotonic()
        try:
            summary = run_once(config=cfg, dry_run=dry_run, channels=channels)
            logger.info("event=sync_ok holders=%s", summary)
        except SyncSkip as exc:
            logger.warning("event=sync_skip reason=%s", exc)
            if once or is_dry_run(dry_run=dry_run):
                raise
        except Exception:
            logger.exception("event=sync_failed")
            if once:
                raise

        if once:
            return

        elapsed = time.monotonic() - started
        sleep_s = max(5.0, interval_s - elapsed)
        logger.info("event=sleep_until_next seconds=%s", int(sleep_s))
        time.sleep(sleep_s)


def configure_logging(*, verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    logging.getLogger("discord").setLevel(logging.WARNING)
    if os.environ.get("CIA_DRY_RUN"):
        logger.info("CIA_DRY_RUN is set")


# === FILE FOOTER ===
# End of file: tools/roblox_coc_sync/sync.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
