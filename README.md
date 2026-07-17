<!--
=== FILE HEADER ===
Title: README
Path: README.md
Created: 2026-07-14
Created by: docshamxo
Modified:
  - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
  - 2026-07-14 | docshamxo | Point clone URL at docshamxo account.
  - 2026-07-14 | docshamxo | Polish repository presentation and align documentation.
  - 2026-07-14 | docshamxo | Remove copyright and license notices.
  - 2026-07-14 | docshamxo | Add CI, Dependabot, and repository validation tooling.
  - 2026-07-14 | docshamxo | Simplify setup and contributor docs.
  - 2026-07-14 | docshamxo | Document every install, setup, and run command explicitly.
  - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
  - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
  - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
  - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
  - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
  - 2026-07-15 | docshamxo | Document webhook prior-message cleanup via local state.
  - 2026-07-17 | docshamxo | Document full recorded-ID purge and ✅ bot reactions.
  - 2026-07-17 | docshamxo | Shorten README; point operators to OPS runbooks.
  - 2026-07-17 | docshamxo | Document staged rollout, changelog, and release checklist.
  - 2026-07-17 | docshamxo | Add Inter Studios proprietary property notice callout.
=== END FILE HEADER ===
-->

<p align="center">
  <img src="assets/logos/DS.png" alt="Directorate of Support" width="148">
</p>

<h1 align="center">CIA Directorate of Support</h1>

<p align="center">
  Discord announcer scripts for DS, OSEC, OTE, GRS, and ESD.<br>
  <em>WE GO AS ONE</em><br>
  <small>Unofficial Roblox community — not affiliated with the US Government or CIA.</small>
</p>

<blockquote align="center">
  <strong>Property of the Central Intelligence Agency (ROBLOX), Inter Studios</strong><br>
  <small>Proprietary community material — see <a href="NOTICE">NOTICE</a>.</small>
</blockquote>

<p align="center">
  <a href="https://github.com/docshamxo/cia-directorate-of-support/actions/workflows/ci.yml"><img src="https://github.com/docshamxo/cia-directorate-of-support/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI"></a>
</p>

---

## Quick start

Need **Git** and **Python 3.10+** (`python` or `python3` / `py` on Windows).

```bash
git clone https://github.com/docshamxo/cia-directorate-of-support.git
cd cia-directorate-of-support
python bootstrap.py
```

Then edit `.env` (never commit it):

1. Paste webhook URLs into every `WEBHOOK_...=` key you will use ([`.env.example`](.env.example) lists them all).
2. Paste `DISCORD_BOT_TOKEN=` so each successful post gets a ✅ (bot needs **Add Reactions** + **Read Message History**).
3. Optional: `DISCORD_INVITE_URL`, `DISCORD_OSEC_APPLICATION_RESULTS_URL`, and staff Drive overlay (`config/links.staff.local.yaml` from the example).

Without `DISCORD_BOT_TOKEN`, announcers still **post and purge**; they only skip ✅. Webhooks cannot react by themselves.

Validate, then run:

```bash
python tools/validate_repo.py
python run_all.py --dry-run --delay 0
python run_all.py
```

Live sends **post first**, then delete previously recorded webhook messages (IDs in gitignored `.webhook_messages.json`), then add ✅ when the bot token is set. See **[OPS.md](OPS.md)** for reaction and purge troubleshooting. Prefer staged live refreshes: [docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md).

---

## Run one channel

From the repo root:

```bash
python ds/chain_of_command.py
python ds/chain_of_command.py --dry-run
```

`run_all.py` flags: `--dry-run`, `--fail-fast`, `--delay 1.5`, `--no-skip-empty`, `--only ds,osec`, `--list-stages`, `--stage 1`, `--require-reaction`.

---

## Update content

| Change | Edit |
|--------|------|
| Names / ranks | [`config/personnel.yaml`](config/personnel.yaml) |
| Mottos / about / disclaimers | [`config/organization.yaml`](config/organization.yaml) |
| Server regulations | [`config/regulations.yaml`](config/regulations.yaml) |
| Colors / bot names / logos | [`config/branding.yaml`](config/branding.yaml) |
| Public links | [`config/links.yaml`](config/links.yaml) |
| Staff Drive URLs | `config/links.staff.local.yaml` (gitignored) |
| Embed layout | Matching script under `ds/` `osec/` `ote/` `grs/` `esd/` |
| Webhook target | Local `.env` |
| Run order | [`common/manifest.py`](common/manifest.py) |

Day-to-day work is YAML under [`config/`](config/). Embed style guide: [config/README.md](config/README.md).

```bash
python tools/validate_repo.py
pytest -q
```

Prefer `git add path/to/file` over `git add .` so `.env` cannot be staged. Full flow: [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Offices

```text
Directorate of Support (DS)
├── Office of Training & Education (OTE)
└── Office of Security (OSEC)
    ├── Global Response Staff (GRS)
    └── Executive Security Detail (ESD)
```

| Folder | Scripts | Guide |
|--------|---------|-------|
| [`ds/`](ds/) | 3 | [README](ds/README.md) |
| [`osec/`](osec/) | 4 | [README](osec/README.md) |
| [`ote/`](ote/) | 5 | [README](ote/README.md) |
| [`grs/`](grs/) | 3 | [README](grs/README.md) |
| [`esd/`](esd/) | 3 | [README](esd/README.md) |

Also: `config/` (YAML), `common/` (shared helpers), `assets/` (logos), `tools/` (validators).

---

## Announcer list

| # | Command | `.env` key |
|---|---------|------------|
| 1 | `python ds/chain_of_command.py` | `WEBHOOK_DS_CHAIN_OF_COMMAND` |
| 2 | `python ds/public_information.py` | `WEBHOOK_DS_PUBLIC_INFORMATION` |
| 3 | `python ds/server_regulations.py` | `WEBHOOK_DS_SERVER_REGULATIONS` |
| 4 | `python osec/information.py` | `WEBHOOK_OSEC_INFORMATION` |
| 5 | `python osec/staff_documents.py` | `WEBHOOK_OSEC_STAFF_DOCUMENTS` |
| 6 | `python osec/spp_information.py` | `WEBHOOK_OSEC_SPP_INFORMATION` |
| 7 | `python osec/open_positions.py` | `WEBHOOK_OSEC_OPEN_POSITIONS` |
| 8 | `python ote/coc.py` | `WEBHOOK_OTE_COC` |
| 9 | `python ote/public_information.py` | `WEBHOOK_OTE_PUBLIC_INFORMATION` |
| 10 | `python ote/program_overview.py` | `WEBHOOK_OTE_PROGRAM_OVERVIEW` |
| 11 | `python ote/staff_documents.py` | `WEBHOOK_OTE_STAFF_DOCUMENTS` |
| 12 | `python ote/open_positions.py` | `WEBHOOK_OTE_OPEN_POSITIONS` |
| 13 | `python grs/coc.py` | `WEBHOOK_GRS_COC` |
| 14 | `python grs/information.py` | `WEBHOOK_GRS_INFORMATION` |
| 15 | `python grs/staff_documents.py` | `WEBHOOK_GRS_STAFF_DOCUMENTS` |
| 16 | `python esd/coc.py` | `WEBHOOK_ESD_COC` |
| 17 | `python esd/information.py` | `WEBHOOK_ESD_INFORMATION` |
| 18 | `python esd/staff_documents.py` | `WEBHOOK_ESD_STAFF_DOCUMENTS` |

---

## Docs map

| Doc | Use when |
|-----|----------|
| **[OPS.md](OPS.md)** | Live runs, ✅ reactions, purge / state recovery |
| [docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md) | Staged office live release checklist |
| [docs/RELEASE_NOTES_OPERATORS.md](docs/RELEASE_NOTES_OPERATORS.md) | Operator notes after hardening (1.1.0) |
| [CHANGELOG.md](CHANGELOG.md) | Version history (Keep a Changelog) |
| [SECURITY.md](SECURITY.md) | Secrets, leak rotation, compartmentation |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Edits, validation, new announcers |
| [NOTICE](NOTICE) | Proprietary ownership (Inter Studios) |
| [config/README.md](config/README.md) | YAML + Discord embed style |
| [`.env.example`](.env.example) | Webhook / token template |

<!--
=== FILE FOOTER ===
End of file: README.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
