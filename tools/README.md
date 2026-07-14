<!--
=== FILE HEADER ===
Title: Tools README
Path: tools/README.md
Created: 2026-07-14
Created by: docshamxo
Modified:
  - 2026-07-14 | docshamxo | Add CI, Dependabot, and repository validation tooling.
  - 2026-07-14 | docshamxo | Simplify setup and contributor docs.
  - 2026-07-14 | docshamxo | Document every install, setup, and run command explicitly.
  - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
  - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
=== END FILE HEADER ===
-->

# Tools

[← Back to main README](../README.md)

## Sync file headers and footers

Every text file must have a header and footer. Refresh them after edits:

```bash
cd cia-directorate-of-support
python tools/sync_file_banners.py
```

Header fields:

- Title
- Path
- Created date
- Created by (`docshamxo`)
- Modified log (date | docshamxo | commit message)

Footer fields:

- End of file path
- Maintained by (`docshamxo`)

Image files (`.png`, etc.) are skipped.

## Run the validator

```bash
cd cia-directorate-of-support
python tools/validate_repo.py
```

macOS / Linux if needed:

```bash
python3 tools/sync_file_banners.py
python3 tools/validate_repo.py
```

## What the validator checks

- every script listed in `run_all.py` exists
- webhook keys in code match `.env.example`
- logo files are present
- config YAML files load
- every tracked text file has a header and footer
- Python files compile

Run this after any script, catalog, config, or webhook-key change.

<!--
=== FILE FOOTER ===
End of file: tools/README.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
