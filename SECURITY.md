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
  - 2026-07-15 | docshamxo | Document local webhook message ID state and cleanup limits.
=== END FILE HEADER ===
-->

# Security

Webhook URLs can post into Discord channels. Keep them private.

## Rules

- Store them only in your local `.env`
- Use `python bootstrap.py` to create `.env` from `.env.example`
- Never commit `.env`, paste webhooks into PRs, or share them in chat
- Prefer explicit `git add path/to/file` over `git add .` when staging changes
- `.webhook_messages.json` is local state (message IDs only) — it is gitignored; do not commit it

## If a webhook leaks

1. Open the Discord channel → **Integrations** → **Webhooks**
2. Delete or regenerate the leaked webhook
3. Update the matching `WEBHOOK_...=` line in your local `.env`
4. Confirm `.env` is not staged: `git status`
5. Re-run only the affected announcer (or `python run_all.py`)

## Operational notes

- Live announcer runs **delete previously recorded webhook message(s)** for that channel (IDs in local `.webhook_messages.json`), then post the new embed(s)
- Webhooks cannot purge full channel history — only messages this webhook posted and recorded can be removed automatically
- Older posts from before cleanup was enabled (or never recorded) must be deleted manually in Discord
- Use `python run_all.py --dry-run` to preview embeds without posting or deleting
- If `run_all.py` fails mid-batch after a successful post, the next re-run for that channel will clear the recorded message(s) before posting again

<!--
=== FILE FOOTER ===
End of file: SECURITY.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
