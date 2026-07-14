# Common

[← Repository root](../README.md)

Shared configuration and Discord helpers used by every announcer script.

## Files

| File | Purpose |
|------|---------|
| [`__init__.py`](__init__.py) | Package marker for `from common import cia_common` |
| [`cia_common.py`](cia_common.py) | Organizational copy, personnel data, colors, logos, embed helpers, webhook send |

## What lives in `cia_common.py`

| Section | Contents |
|---------|----------|
| Assets | Logo paths under `assets/logos/` |
| Branding | Embed colors, bot display names, community URLs |
| Bulletin | DS / OSEC / OTE / GRS / ESD descriptions and mottos |
| Personnel | Roles, ranks, and chain-of-command data |
| Formatting | `roles_text`, `ranks_text`, `bullets`, link helpers |
| Embeds | `embed`, `disclaimer_embed`, `chain_intro_embed`, `important_notice_embed` |
| Delivery | `require_webhook`, `send_webhook` |

## Key APIs

```python
from common import cia_common as c

url = c.require_webhook("WEBHOOK_DS_CHAIN_OF_COMMAND")
c.send_webhook(url, embeds, username=c.BOT_DS)
```

| Helper | Purpose |
|--------|---------|
| `require_webhook(env_key)` | Load a Discord webhook URL from `.env` |
| `embed(...)` | Build a styled Discord embed |
| `send_webhook(...)` | Post embeds (and optional logo files) to a webhook |
| `roles_text` / `ranks_text` / `bullets` | Format CoC and list fields |

Update organizational text and personnel here so all offices stay consistent.
