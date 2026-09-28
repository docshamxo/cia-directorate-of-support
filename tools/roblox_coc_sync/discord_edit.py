# === FILE HEADER ===
# Title: Discord Webhook Message Edit
# Path: tools/roblox_coc_sync/discord_edit.py
# Created: 2026-09-28
# Created by: docshamxo
# Modified:
#   - 2026-09-28 | docshamxo | PATCH existing webhook message by ID.
# === END FILE HEADER ===

"""Edit an existing Discord webhook message (does not post a new one)."""

from __future__ import annotations

import logging
from collections.abc import Sequence

import discord
import requests
from discord import SyncWebhook

logger = logging.getLogger("cia.roblox_coc_sync.discord_edit")


def edit_webhook_message(
    *,
    webhook_url: str,
    message_id: int,
    embeds: Sequence[discord.Embed],
    username: str,
    files: Sequence[discord.File] | None = None,
    dry_run: bool = False,
) -> None:
    """PATCH ``/webhooks/.../messages/{message_id}`` via discord.py SyncWebhook."""
    if dry_run:
        logger.info(
            "event=dry_run_edit message_id=%s username=%s embeds=%s",
            message_id,
            username,
            len(embeds),
        )
        return

    session = requests.Session()
    try:
        webhook = SyncWebhook.from_url(webhook_url, session=session)
        kwargs: dict = {
            "embeds": list(embeds),
            "username": username,
            "wait": True,
        }
        if files:
            kwargs["files"] = list(files)
        webhook.edit_message(message_id, **kwargs)
        logger.info(
            "event=edit_ok message_id=%s embeds=%s",
            message_id,
            len(embeds),
        )
    finally:
        session.close()


# === FILE FOOTER ===
# End of file: tools/roblox_coc_sync/discord_edit.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
