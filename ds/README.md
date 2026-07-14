# Directorate of Support (DS)

[← Repository root](../README.md)

Directorate-level Discord announcers. Motto: **WE GO AS ONE**

Parent unit for **OTE** and **OSEC**.

## Scripts (3)

| Script | Label | Purpose | Environment variable |
|--------|-------|---------|----------------------|
| [`chain_of_command.py`](chain_of_command.py) | DS Chain of Command | Agency executive leadership through DS, OTE, OSEC, GRS, and ESD | `WEBHOOK_DS_CHAIN_OF_COMMAND` |
| [`public_information.py`](public_information.py) | DS Public Information | Public-facing Directorate information | `WEBHOOK_DS_PUBLIC_INFORMATION` |
| [`server_regulations.py`](server_regulations.py) | Server Regulations | Server rules and regulations | `WEBHOOK_DS_SERVER_REGULATIONS` |

## Run

```bash
# From repository root
python ds/chain_of_command.py
python ds/public_information.py
python ds/server_regulations.py
```

## Related

| Unit | Path |
|------|------|
| Shared library | [`../common/`](../common/) |
| Office of Security | [`../osec/`](../osec/) |
| Office of Training & Education | [`../ote/`](../ote/) |
