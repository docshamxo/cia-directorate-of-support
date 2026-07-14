# Office of Training & Education (OTE)

[← Back to main README](../README.md)

Motto: **SCIENTIA EST LUX LUCIS**  
Parent: DS

## Install / setup (once)

```bash
python setup.py
```

Then put Discord webhook URLs in `.env`.

## Run

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

- Shared names / org text → [`../common/cia_common.py`](../common/cia_common.py)
- This channel's embeds → the script above
