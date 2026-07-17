<!--
=== FILE HEADER ===
Title: DS README
Path: ds/README.md
Created: 2026-07-14
Created by: docshamxo
Modified:
  - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
  - 2026-07-14 | docshamxo | Polish repository presentation and align documentation.
  - 2026-07-14 | docshamxo | Simplify setup and contributor docs.
  - 2026-07-14 | docshamxo | Document every install, setup, and run command explicitly.
  - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
  - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
  - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
  - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
  - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
  - 2026-07-17 | docshamxo | Slim office README; point to OPS for reactions/purge.
=== END FILE HEADER ===
-->

# Directorate of Support (DS)

[← Back to main README](../README.md)

Motto: **WE GO AS ONE**

Setup once at repo root: [README.md](../README.md). Live ops (✅ / purge): [OPS.md](../OPS.md).

## Run (from repo root)

```bash
python ds/chain_of_command.py
python ds/public_information.py
python ds/server_regulations.py
```

Dry-run any script with `--dry-run`. Require ✅ with `--require-reaction` when `DISCORD_BOT_TOKEN` is set.

## Scripts

| Script | Posts | `.env` key |
|--------|-------|------------|
| [`chain_of_command.py`](chain_of_command.py) | DS chain of command | `WEBHOOK_DS_CHAIN_OF_COMMAND` |
| [`public_information.py`](public_information.py) | Public DS information | `WEBHOOK_DS_PUBLIC_INFORMATION` |
| [`server_regulations.py`](server_regulations.py) | Server regulations | `WEBHOOK_DS_SERVER_REGULATIONS` |

## Edit

- Names / ranks / mottos / links → [`../config/`](../config/) YAML
- Embed layout → the script above
- Then: `python tools/validate_repo.py`

<!--
=== FILE FOOTER ===
End of file: ds/README.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
