# Directorate of Support (DS)

[← Back to main README](../README.md)

Motto: **WE GO AS ONE**

## Install / setup (once)

From the repository root:

```bash
python setup.py
```

Then put Discord webhook URLs in `.env`.

## Run

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
