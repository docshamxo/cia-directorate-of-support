<!--
=== FILE HEADER ===
Title: Contributing
Path: CONTRIBUTING.md
Created: 2026-07-14
Created by: docshamxo
Modified:
  - 2026-07-14 | docshamxo | Simplify setup and contributor docs.
  - 2026-07-14 | docshamxo | Document every install, setup, and run command explicitly.
  - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
  - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
  - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
  - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
  - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
  - 2026-07-17 | docshamxo | Sensitivity rules, marking vocabulary, optional banners, manifest.
=== END FILE HEADER ===
-->

# Contributing

Follow the full install steps in [README.md](README.md) first (`git`, Python, clone, `python bootstrap.py`, `.env`).

This is an **unofficial Roblox community** project — not affiliated with the US Government or CIA. Use community markings only: **PUBLIC** / **STAFF** / **CANDIDATE**.

## Sensitivity rules

- Never commit `.env`, `config/links.staff.local.yaml`, or `.webhook_messages.json`
- Do not add new public staff Drive/share links to `config/links.yaml` — put them in the local staff overlay
- Discord invites and channel snowflakes belong in `.env` (`DISCORD_INVITE_URL`, `DISCORD_OSEC_APPLICATION_RESULTS_URL`)
- Keep affiliation / fiction disclaimer text when editing closers

## Everyday edits

Prefer editing YAML under [`config/`](config/) instead of hardcoding values in Python.

| What you want to change | Where to edit |
|-------------------------|---------------|
| Names, ranks | [`config/personnel.yaml`](config/personnel.yaml) |
| Mottos, about text, disclaimers | [`config/organization.yaml`](config/organization.yaml) |
| Server regulations prose | [`config/regulations.yaml`](config/regulations.yaml) |
| Colors, bot usernames, logo filenames | [`config/branding.yaml`](config/branding.yaml) |
| Public document / form / community links | [`config/links.yaml`](config/links.yaml) |
| Staff Drive / TTP URLs | `config/links.staff.local.yaml` (from [`links.staff.example.yaml`](config/links.staff.example.yaml)) |
| One channel's Discord embed layout | The script in `ds/`, `osec/`, `ote/`, `grs/`, or `esd/` |
| Webhook target channel | Your local `.env` (never commit it) |
| Logo image files | [`assets/logos/`](assets/logos/) — keep the same filenames |
| Run order / catalog | [`common/manifest.py`](common/manifest.py) |

In announcer scripts, load links with:

```python
c.url('osec.information.handbook')
```

Post (or dry-run) through the shared runner:

```python
from common.announcer import run_announcer

run_announcer(
    webhook_key="WEBHOOK_OSEC_INFORMATION",
    username=c.BOT_OSEC,
    build_embeds=_build_embeds,
    dry_run="--dry-run" in sys.argv,
)
```

## After you change code or config

From the repository root:

```bash
cd cia-directorate-of-support
python tools/validate_repo.py
pytest -q
python run_all.py --dry-run --delay 0
```

macOS / Linux if needed:

```bash
python3 tools/validate_repo.py
python3 -m pytest -q
python3 run_all.py --dry-run --delay 0
```

File header/footer banners are **optional**. To refresh them: `python tools/sync_file_banners.py`. To enforce in validation: `CIA_REQUIRE_BANNERS=1 python tools/validate_repo.py`.

## Commit and push

```bash
git status
git add path/to/changed-file.py
git status
git commit -m "Describe your change here"
git push
```

Prefer explicit paths over `git add .` so secrets in `.env` cannot be staged accidentally.

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
4. Point `run_announcer(..., webhook_key=...)` at a new key, for example `WEBHOOK_OSEC_NEW_CHANNEL`.
5. Add any **public** document URLs to [`config/links.yaml`](config/links.yaml) and read them with `c.url('...')`. Staff URLs go in the local overlay.
6. Add the webhook key to [`.env.example`](.env.example):

```env
WEBHOOK_OSEC_NEW_CHANNEL=
```

7. Add the same key to your local `.env` and paste the webhook URL.
8. Add the script to [`common/manifest.py`](common/manifest.py) (path, label, webhook key).
9. Update that office README.
10. Update the announcer list in [README.md](README.md).
11. Run:

```bash
python tools/validate_repo.py
pytest -q
python run_all.py --dry-run --delay 0
```

12. Commit and push with explicit paths:

```bash
git status
git add osec/new_channel.py common/manifest.py .env.example README.md
git commit -m "Add new announcer script"
git push
```

Ops runbook: [OPS.md](OPS.md). Security playbooks: [SECURITY.md](SECURITY.md).

<!--
=== FILE FOOTER ===
End of file: CONTRIBUTING.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
