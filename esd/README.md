# Executive Security Detail (ESD)

[← Back to main README](../README.md)

Parent: OSEC

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

Then run:

```bash
python tools/validate_repo.py
```
