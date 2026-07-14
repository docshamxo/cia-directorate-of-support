# Global Response Staff (GRS)

[← Back to main README](../README.md)

Parent: OSEC

## Install / setup (once)

```bash
python setup.py
```

Then put Discord webhook URLs in `.env`.

## Run

```bash
python grs/coc.py
python grs/information.py
python grs/staff_documents.py
```

## Scripts

| Script | What it posts | `.env` key |
|--------|---------------|------------|
| [`coc.py`](coc.py) | GRS chain of command | `WEBHOOK_GRS_COC` |
| [`information.py`](information.py) | GRS information | `WEBHOOK_GRS_INFORMATION` |
| [`staff_documents.py`](staff_documents.py) | Staff documents | `WEBHOOK_GRS_STAFF_DOCUMENTS` |

## Edit

- Shared names / org text → [`../common/cia_common.py`](../common/cia_common.py)
- This channel's embeds → the script above
