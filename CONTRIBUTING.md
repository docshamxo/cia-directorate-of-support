# Contributing

Follow the full install steps in [README.md](README.md) first (`git`, Python, clone, packages, `.env`).

## Everyday edits

Prefer editing YAML under [`config/`](config/) instead of hardcoding values in Python.

| What you want to change | Where to edit |
|-------------------------|---------------|
| Names, ranks | [`config/personnel.yaml`](config/personnel.yaml) |
| Mottos, about text, disclaimers | [`config/organization.yaml`](config/organization.yaml) |
| Colors, bot usernames, logo filenames | [`config/branding.yaml`](config/branding.yaml) |
| Document / form / community links | [`config/links.yaml`](config/links.yaml) |
| One channel's Discord embed layout | The script in `ds/`, `osec/`, `ote/`, `grs/`, or `esd/` |
| Webhook target channel | Your local `.env` (never commit it) |
| Logo image files | [`assets/logos/`](assets/logos/) — keep the same filenames |
| Run order for everything | [`run_all.py`](run_all.py) |

In announcer scripts, load links with:

```python
c.url('osec.information.handbook')
```

## After you change code or config

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

5. Add any document URLs to [`config/links.yaml`](config/links.yaml) and read them with `c.url('...')`.
6. Add the webhook key to [`.env.example`](.env.example):

```env
WEBHOOK_OSEC_NEW_CHANNEL=
```

7. Add the same key to your local `.env` and paste the webhook URL.
8. Add the script to [`run_all.py`](run_all.py).
9. Update that office README.
10. Update the announcer list in [README.md](README.md).
11. Run:

```bash
python tools/validate_repo.py
```

12. Commit and push:

```bash
git status
git add .
git commit -m "Add new announcer script"
git push
```
