<!--
=== FILE HEADER ===
Title: Security
Path: SECURITY.md
Created: 2026-07-14
Created by: docshamxo
Modified:
  - 2026-07-14 | docshamxo | Polish repository presentation and align documentation.
  - 2026-07-14 | docshamxo | Simplify setup and contributor docs.
  - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
  - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
  - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
  - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
=== END FILE HEADER ===
-->

# Security

Webhook URLs can post into Discord channels. Keep them private.

## Rules

- Store them only in your local `.env`
- Use `python bootstrap.py` to create `.env` from `.env.example`
- Never commit `.env`, paste webhooks into PRs, or share them in chat
- Prefer explicit `git add path/to/file` over `git add .` when staging changes

## If a webhook leaks

1. Open the Discord channel → **Integrations** → **Webhooks**
2. Delete or regenerate the leaked webhook
3. Update the matching `WEBHOOK_...=` line in your local `.env`
4. Confirm `.env` is not staged: `git status`
5. Re-run only the affected announcer (or `python run_all.py`)

## Operational notes

- Live announcer runs **create new Discord messages**; they do not edit or replace prior posts
- Use `python run_all.py --dry-run` to preview embeds without posting
- If `run_all.py` fails mid-batch, read the summary, fix the failing script, then re-run (expect duplicate messages in channels that already succeeded unless you clear them manually in Discord)

<!--
=== FILE FOOTER ===
End of file: SECURITY.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
