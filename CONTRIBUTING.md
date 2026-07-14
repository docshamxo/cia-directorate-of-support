# Contributing

Follow the full install steps in [README.md](README.md) first (`git`, Python, clone, packages, `.env`).

## Everyday edits

| What you want to change | Where to edit |
|-------------------------|---------------|
| Names, ranks, mottos, org text | [`common/cia_common.py`](common/cia_common.py) |
| One channel's Discord embeds | The script in `ds/`, `osec/`, `ote/`, `grs/`, or `esd/` |
| Webhook target channel | Your local `.env` (never commit it) |
| Logos | [`assets/logos/`](assets/logos/) — keep the same filenames |
| Run order for everything | [`run_all.py`](run_all.py) |

## After you change code

From the repository root:

```bash
cd cia-directorate-of-support
python tools/validate_repo.py
```

macOS / Linux if needed:

```bash
python3 tools/validate_repo.py
```

## Commit and push

```bash
git status
git add .
git status
git commit -m "Describe your change here"
git push
```

If this is your first push from a new clone of your fork:

```bash
git push -u origin HEAD
```

CI on GitHub runs the same validation automatically.

## Adding a new announcer

Do every step:

1. Copy an existing script in the correct office folder.
2. Rename it.
3. Edit the embeds in that new script.
4. Change the webhook line to a new key, for example:

```python
WEBHOOK_URL = c.require_webhook("WEBHOOK_OSEC_NEW_CHANNEL")
```

5. Add the same key to [`.env.example`](.env.example):

```env
WEBHOOK_OSEC_NEW_CHANNEL=
```

6. Add the same key to your local `.env` and paste the webhook URL.
7. Add the script to [`run_all.py`](run_all.py).
8. Update that office README.
9. Update the announcer list in [README.md](README.md).
10. Run:

```bash
python tools/validate_repo.py
```

11. Commit and push:

```bash
git status
git add .
git commit -m "Add new announcer script"
git push
```
