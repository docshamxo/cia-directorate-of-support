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
  - 2026-07-17 | docshamxo | Clarify contributor path; cross-link OPS reaction/purge docs.
  - 2026-07-17 | docshamxo | Document pre-commit hooks and coverage floor.
=== END FILE HEADER ===
-->

# Contributing

Install once via the root [README.md](README.md) (`git`, Python 3.10+, clone, `python bootstrap.py`, edit `.env`).

Unofficial Roblox community project — not affiliated with the US Government or CIA. Markings: **PUBLIC** / **STAFF** / **CANDIDATE** only.

## Sensitivity

- Never commit `.env`, `config/links.staff.local.yaml`, or `.webhook_messages.json`
- Staff Drive / TTP URLs → local overlay only (not public `config/links.yaml`)
- Discord invites / channel URLs → `.env` (`DISCORD_INVITE_URL`, `DISCORD_OSEC_APPLICATION_RESULTS_URL`)
- Keep affiliation / fiction disclaimer text in closers
- Live ops (✅ / purge): [OPS.md](OPS.md) · leak rotation: [SECURITY.md](SECURITY.md)

## Everyday edits

Prefer YAML under [`config/`](config/) over hardcoding in Python.

| Change | Where |
|--------|-------|
| Names, ranks | [`config/personnel.yaml`](config/personnel.yaml) |
| Mottos, about, disclaimers | [`config/organization.yaml`](config/organization.yaml) |
| Regulations prose | [`config/regulations.yaml`](config/regulations.yaml) |
| Colors, bot usernames, logos | [`config/branding.yaml`](config/branding.yaml) |
| Public links | [`config/links.yaml`](config/links.yaml) |
| Staff Drive / TTP URLs | `config/links.staff.local.yaml` (from [`links.staff.example.yaml`](config/links.staff.example.yaml)) |
| Embed layout | Script in `ds/`, `osec/`, `ote/`, `grs/`, or `esd/` |
| Webhook target | Local `.env` (never commit) |
| Logo files | [`assets/logos/`](assets/logos/) — keep filenames |
| Run order / catalog | [`common/manifest.py`](common/manifest.py) |

In announcer scripts:

```python
c.url('osec.information.handbook')
```

```python
from common.announcer import run_announcer

run_announcer(
    webhook_key="WEBHOOK_OSEC_INFORMATION",
    username=c.BOT_OSEC,
    build_embeds=_build_embeds,
    dry_run="--dry-run" in sys.argv,
)
```

## Validate before push

From the repository root:

```bash
python tools/validate_repo.py
pytest -q
python run_all.py --dry-run --delay 0
```

`pytest -q` enforces a **40%** statement coverage floor on `common/` (see `pyproject.toml`). Raise coverage with tests rather than lowering the floor.

Optional local secret/lint hooks (same gitleaks rev as CI):

```bash
pip install -e ".[dev]"
pre-commit install
pre-commit run --all-files
```

Use `python3` / `python3 -m pytest` on macOS/Linux if needed.

File header/footer banners are **optional**. Refresh: `python tools/sync_file_banners.py`. Enforce: `CIA_REQUIRE_BANNERS=1 python tools/validate_repo.py`.

Branch protection for maintainers: [docs/BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md).

## Commit and push

```bash
git status
git add path/to/changed-file.py
git status
git commit -m "Describe your change here"
git push
```

Prefer explicit paths over `git add .`. First push from a new fork branch: `git push -u origin HEAD`. CI runs the same validation on GitHub.

## Adding a new announcer

1. Copy an existing script in the correct office folder; rename it.
2. Edit embeds; point `run_announcer(..., webhook_key=...)` at a new key (e.g. `WEBHOOK_OSEC_NEW_CHANNEL`).
3. Public URLs → [`config/links.yaml`](config/links.yaml) via `c.url('...')`. Staff URLs → local overlay.
4. Add the key to [`.env.example`](.env.example) and your local `.env`.
5. Register the script in [`common/manifest.py`](common/manifest.py).
6. Update the office README and the announcer list in [README.md](README.md).
7. Validate:

```bash
python tools/validate_repo.py
pytest -q
python run_all.py --dry-run --delay 0
```

8. Commit with explicit paths (include `.env.example`, never `.env`).

<!--
=== FILE FOOTER ===
End of file: CONTRIBUTING.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
