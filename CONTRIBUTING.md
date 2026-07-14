# Contributing

Keep changes small and run the checks before you push.

## Everyday edits

| What you want to change | Where to edit |
|-------------------------|---------------|
| Names, ranks, mottos, org text | [`common/cia_common.py`](common/cia_common.py) |
| One channel's Discord embeds | The script in `ds/`, `osec/`, `ote/`, `grs/`, or `esd/` |
| Webhook target channel | Your local `.env` (never commit it) |
| Logos | [`assets/logos/`](assets/logos/) — keep the same filenames |
| Run order for everything | [`run_all.py`](run_all.py) |

## After you change code

```bash
python tools/validate_repo.py
```

Then commit and open a pull request. CI runs the same checks automatically.

## Adding a new announcer

1. Create the script in the right office folder (copy an existing one).
2. Use `c.require_webhook("WEBHOOK_...")` for the Discord URL.
3. Add the matching key to [`.env.example`](.env.example) and your local `.env`.
4. Register it in [`run_all.py`](run_all.py).
5. Update that office's README and the catalog in the root README.
6. Run `python tools/validate_repo.py`.
