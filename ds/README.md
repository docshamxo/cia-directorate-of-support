# Directorate of Support (DS)

Directorate-level Discord announcements.

| Script | Channel purpose | Env var |
|--------|-----------------|---------|
| `chain_of_command.py` | Full DS CoC (agency → DS → OTE/OSEC → GRS/ESD) | `WEBHOOK_DS_CHAIN_OF_COMMAND` |
| `public_information.py` | Public-facing DS information | `WEBHOOK_DS_PUBLIC_INFORMATION` |
| `server_regulations.py` | Server rules and regulations | `WEBHOOK_DS_SERVER_REGULATIONS` |

```bash
python ds/chain_of_command.py
python ds/public_information.py
python ds/server_regulations.py
```
