# Office of Security (OSEC)

[← Back to main README](../README.md)

Motto: **PROTECT · DETECT · RESPOND**  
Parent: DS · Sub-units: GRS, ESD

## Install / setup (once)

```bash
python setup.py
```

Then put Discord webhook URLs in `.env`.

## Run

```bash
python osec/information.py
python osec/staff_documents.py
python osec/spp_information.py
python osec/open_positions.py
```

## Scripts

| Script | What it posts | `.env` key |
|--------|---------------|------------|
| [`information.py`](information.py) | OSEC information | `WEBHOOK_OSEC_INFORMATION` |
| [`staff_documents.py`](staff_documents.py) | Staff documents | `WEBHOOK_OSEC_STAFF_DOCUMENTS` |
| [`spp_information.py`](spp_information.py) | Security Phase Program | `WEBHOOK_OSEC_SPP_INFORMATION` |
| [`open_positions.py`](open_positions.py) | Open positions | `WEBHOOK_OSEC_OPEN_POSITIONS` |

## Edit

- Shared names / org text → [`../common/cia_common.py`](../common/cia_common.py)
- This channel's embeds → the script above
