# === FILE HEADER ===
# Title: Discord Webhook Message Edit
# Path: tools/roblox_coc_sync/discord_edit.py
# Created: 2026-09-28
# Created by: docshamxo
# Modified:
#   - 2026-09-28 | docshamxo | PATCH existing webhook message by ID.
#   - 2026-09-28 | docshamxo | Use edit_message attachments= (no username/files kwargs).
#   - 2026-09-28 | docshamxo | Re-export shared cia_common.edit_webhook_message.
# === END FILE HEADER ===

"""Edit an existing Discord webhook message (does not post a new one)."""

from __future__ import annotations

from common.cia_common import edit_webhook_message

__all__ = ["edit_webhook_message"]


# === FILE FOOTER ===
# End of file: tools/roblox_coc_sync/discord_edit.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
