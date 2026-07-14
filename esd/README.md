# Executive Security Detail (ESD)

[← Back to main README](../README.md)

Parent: OSEC

## Install / setup (once)

```bash
python setup.py
```

Then put Discord webhook URLs in `.env`.

## Run

```bash
python esd/coc.py
python esd/information.py
```

## Scripts

| Script | What it posts | `.env` key |
|--------|---------------|------------|
| [`coc.py`](coc.py) | ESD chain of command | `WEBHOOK_ESD_COC` |
| [`information.py`](information.py) | ESD information | `WEBHOOK_ESD_INFORMATION` |

## Edit

- Shared names / org text → [`../common/cia_common.py`](../common/cia_common.py)
- This channel's embeds → the script above
