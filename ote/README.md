<!--
=== FILE HEADER ===
Title: OTE README
Path: ote/README.md
Created: 2026-07-14
Created by: docshamxo
Modified:
  - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
  - 2026-07-14 | docshamxo | Polish repository presentation and align documentation.
  - 2026-07-14 | docshamxo | Simplify setup and contributor docs.
  - 2026-07-14 | docshamxo | Document every install, setup, and run command explicitly.
  - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
=== END FILE HEADER ===
-->

# Office of Training & Education (OTE)

[← Back to main README](../README.md)

Motto: **SCIENTIA EST LUX LUCIS**  
Parent: DS

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
python ote/coc.py
python ote/public_information.py
python ote/program_overview.py
python ote/staff_documents.py
python ote/open_positions.py
```

## Scripts

| Script | What it posts | `.env` key |
|--------|---------------|------------|
| [`coc.py`](coc.py) | OTE chain of command | `WEBHOOK_OTE_COC` |
| [`public_information.py`](public_information.py) | Public OTE information | `WEBHOOK_OTE_PUBLIC_INFORMATION` |
| [`program_overview.py`](program_overview.py) | Officer Training Program overview | `WEBHOOK_OTE_PROGRAM_OVERVIEW` |
| [`staff_documents.py`](staff_documents.py) | Staff documents | `WEBHOOK_OTE_STAFF_DOCUMENTS` |
| [`open_positions.py`](open_positions.py) | Open positions | `WEBHOOK_OTE_OPEN_POSITIONS` |

## Edit

- Names / ranks / mottos / links → [`../config/`](../config/) YAML files
- This channel's embed layout → the script above

Then run:

```bash
python tools/validate_repo.py
```

<!--
=== FILE FOOTER ===
End of file: ote/README.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
