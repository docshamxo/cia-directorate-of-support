# Common

Shared library used by every announcer script.

| File | Purpose |
|------|---------|
| `cia_common.py` | Logos, colors, bot names, org bulletin text, roles/ranks, embed helpers, webhook send |

## Key helpers

- `require_webhook(env_key)` — load a Discord webhook from `.env`
- `embed(...)` / `send_webhook(...)` — build and post Discord embeds
- `roles_text` / `ranks_text` / `bullets` — formatting for CoC fields

Update personnel and organizational copy here so all offices stay consistent.
