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
  - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
  - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
  - 2026-07-17 | docshamxo | Document diagnose_webhook_state.py diagnostic tool.
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

## Diagnose webhook state

Before a live run, inspect `.env` webhook keys, duplicate URLs, and local message ID state:

```bash
cd cia-directorate-of-support
python tools/diagnose_webhook_state.py
```

The tool reports:

- whether `DISCORD_BOT_TOKEN` is set (required for live runs unless `--allow-skip-reaction`)
- `WEBHOOK_*` keys that share the same Discord webhook ID (sibling purge)
- recorded message IDs in `.webhook_messages.json` per announcer
- stale/orphan state keys not in the announcer catalog

Use this after rotating webhooks, debugging duplicate posts, or recovering from an empty channel. See [OPS.md](../OPS.md).
## Reset webhook message state
Empty-channel / mid-batch recovery (edits gitignored `.webhook_messages.json` only):
python tools/reset_webhook_state.py --list
python tools/reset_webhook_state.py --key WEBHOOK_DS_PUBLIC_INFORMATION
python tools/reset_webhook_state.py --all --yes
See [OPS.md](../OPS.md).

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
