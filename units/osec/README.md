<!--
=== FILE HEADER ===
Title: OSEC README
Path: units/osec/README.md
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

# Office of Security (OSEC)

[← Back to main README](../README.md)

Motto: **PROTECT · DETECT · RESPOND**  
Parent: DS · Sub-units: GRS, ESD

Setup once at repo root: [README.md](../../README.md). Live ops (✅ / purge): [OPS.md](../../docs/OPS.md). Staff Drive URLs need `config/links.staff.local.yaml` before live staff posts.

## Run (from repo root)

```bash
python units/osec/information.py
python units/osec/staff_documents.py
python units/osec/spp_information.py
python units/osec/open_positions.py
```

Dry-run with `--dry-run`. Require ✅ with `--require-reaction` when `DISCORD_BOT_TOKEN` is set.

## Scripts

| Script | Posts | `.env` key |
|--------|-------|------------|
| [`information.py`](information.py) | OSEC information | `WEBHOOK_OSEC_INFORMATION` |
| [`staff_documents.py`](staff_documents.py) | Staff documents | `WEBHOOK_OSEC_STAFF_DOCUMENTS` |
| [`spp_information.py`](spp_information.py) | Security Phase Program | `WEBHOOK_OSEC_SPP_INFORMATION` |
| [`open_positions.py`](open_positions.py) | Open positions | `WEBHOOK_OSEC_OPEN_POSITIONS` |

## Edit

- Names / ranks / mottos / links → [`../config/`](../../config/) YAML
- Embed layout → the script above
- Then: `python tools/validate_repo.py`

<!--
=== FILE FOOTER ===
End of file: units/osec/README.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
