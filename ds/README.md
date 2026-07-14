<!--
=== FILE HEADER ===
Title: DS README
Path: ds/README.md
Created: 2026-07-14
Created by: docshamxo
Modified:
  - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
  - 2026-07-14 | docshamxo | Polish repository presentation and align documentation.
  - 2026-07-14 | docshamxo | Simplify setup and contributor docs.
  - 2026-07-14 | docshamxo | Document every install, setup, and run command explicitly.
  - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
  - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
  - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
=== END FILE HEADER ===
-->

# Directorate of Support (DS)

[← Back to main README](../README.md)

Motto: **WE GO AS ONE**

## First-time setup

Follow **every** step in the root [README.md](../README.md) (Git, Python, clone, packages, `.env`).

Short version after Git and Python are installed:

```bash
git clone https://github.com/docshamxo/cia-directorate-of-support.git
cd cia-directorate-of-support
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
```

macOS / Linux use:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
cp .env.example .env
```

Then open `.env` and paste the webhook URLs. Never commit `.env`.

## Run these scripts

From the repository root (`cd cia-directorate-of-support`):

```bash
python ds/chain_of_command.py
python ds/public_information.py
python ds/server_regulations.py
```

## Scripts

| Script | What it posts | `.env` key |
|--------|---------------|------------|
| [`chain_of_command.py`](chain_of_command.py) | Full DS chain of command | `WEBHOOK_DS_CHAIN_OF_COMMAND` |
| [`public_information.py`](public_information.py) | Public DS information | `WEBHOOK_DS_PUBLIC_INFORMATION` |
| [`server_regulations.py`](server_regulations.py) | Server regulations | `WEBHOOK_DS_SERVER_REGULATIONS` |

## Edit

- Names / ranks / mottos / links → [`../config/`](../config/) YAML files
- This channel's embed layout → the script above

Then run:

```bash
python tools/validate_repo.py
```

<!--
=== FILE FOOTER ===
End of file: ds/README.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
