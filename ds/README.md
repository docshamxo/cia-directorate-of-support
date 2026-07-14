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

- Shared names / org text → [`../common/cia_common.py`](../common/cia_common.py)
- This channel's embeds → the script above

Then run:

```bash
python tools/validate_repo.py
```
