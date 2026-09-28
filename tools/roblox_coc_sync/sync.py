# === FILE HEADER ===
# Title: Roblox CoC Sync Orchestrator
# Path: tools/roblox_coc_sync/sync.py
# Created: 2026-09-28
# Created by: docshamxo
# Modified:
#   - 2026-09-28 | docshamxo | One-shot sync: Roblox → embeds → webhook edit.
#   - 2026-09-28 | docshamxo | Pass sync config into holder overrides for discord_id merge.
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
from tools.roblox_coc_sync.config import SyncConfig, env_or_none, load_sync_config
from tools.roblox_coc_sync.discord_edit import edit_webhook_message
from tools.roblox_coc_sync.embeds import build_ds_coc_embeds
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
) -> dict[str, str]:
    """Pull Roblox ranks, rebuild DS CoC embeds, edit webhook message by ID.

    Returns a summary dict of (personnel_key/abbrev → holder) for logging/tests.
    """
    cfg = config or load_sync_config(config_path)
    effective_dry = is_dry_run(dry_run=dry_run) or cfg.dry_run_default

    api_key = env_or_none("ROBLOX_OPEN_CLOUD_API_KEY")
    if client is None:
        if not api_key:
            if effective_dry:
                logger.warning("event=dry_run_no_api_key using YAML holders only (no Roblox pull)")
                catalog = base_roles_catalog()
                overrides: dict[tuple[str, str], str] = {}
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

    embeds = build_ds_coc_embeds(catalog)
    c.validate_embed_limits(embeds)

    webhook_url = env_or_none(cfg.target.webhook_env)
    message_id_raw = env_or_none(cfg.target.message_id_env)

    def _holder_text(value: object) -> str:
        return value.holder if hasattr(value, "holder") else str(value)

    if effective_dry:
        preview_embeds(
            embeds,
            webhook_key=cfg.target.webhook_env,
            username=c.BOT_DS,
        )
        summary = {f"{k}/{a}": _holder_text(h) for (k, a), h in overrides.items()}
        logger.info("event=dry_run_complete overrides=%s", len(summary))
        return summary

    if not webhook_url:
        raise SyncSkip(f"Set {cfg.target.webhook_env} in .env")
    if not message_id_raw:
        raise SyncSkip(
            f"Set {cfg.target.message_id_env} to the Discord webhook message snowflake "
            "to edit (post once via units/ds/chain_of_command.py, then copy the message ID)."
        )
    if not message_id_raw.isdigit():
        raise SyncSkip(f"{cfg.target.message_id_env} must be a numeric snowflake")

    files = [c.logo_file(path) for path in c.LOGOS.values()]
    edit_webhook_message(
        webhook_url=webhook_url,
        message_id=int(message_id_raw),
        embeds=embeds,
        username=c.BOT_DS,
        files=files,
        dry_run=False,
    )
    return {f"{k}/{a}": _holder_text(h) for (k, a), h in overrides.items()}


def run_loop(
    *,
    config: SyncConfig | None = None,
    config_path: Path | None = None,
    dry_run: bool | None = None,
    once: bool = False,
) -> None:
    """Run sync once, or every ``interval_minutes`` until interrupted."""
    cfg = config or load_sync_config(config_path)
    interval_s = cfg.interval_minutes * 60

    while True:
        started = time.monotonic()
        try:
            summary = run_once(config=cfg, dry_run=dry_run)
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
    # Avoid leaking webhook tokens if discord/http libs log URLs.
    logging.getLogger("discord").setLevel(logging.WARNING)
    if os.environ.get("CIA_DRY_RUN"):
        logger.info("CIA_DRY_RUN is set")


# === FILE FOOTER ===
# End of file: tools/roblox_coc_sync/sync.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
