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
  - 2026-07-15 | docshamxo | Document CodeQL code scanning via GitHub Actions.
  - 2026-07-17 | docshamxo | Document full recorded-ID purge and DISCORD_BOT_TOKEN for ✅.
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
- `DISCORD_BOT_TOKEN` is a secret (same rules as webhook URLs) — required for ✅ reactions

## If a webhook leaks

1. Open the Discord channel → **Integrations** → **Webhooks**
2. Delete or regenerate the leaked webhook
3. Update the matching `WEBHOOK_...=` line in your local `.env`
4. Confirm `.env` is not staged: `git status`
5. Re-run only the affected announcer (or `python run_all.py`)

## Code scanning

- GitHub **code scanning** runs via Advanced Setup: the CodeQL workflow at `.github/workflows/codeql.yml` analyzes Python on pushes and pull requests to `main`, plus a weekly schedule
- Results appear under the repository **Security** tab (Code scanning alerts)

## Operational notes

- Live announcer runs **delete every recorded webhook message ID** for that channel (local `.webhook_messages.json`), then post the new embed(s)
- IDs that fail to delete are kept in state and retried on the next run (they are not dropped when the new post is recorded)
- After each successful post, the suite adds ✅ via the Discord bot API when `DISCORD_BOT_TOKEN` is set (webhooks cannot react on their own)
- Webhooks cannot purge full channel history — only messages this webhook posted and recorded can be removed automatically
- Older posts from before cleanup was enabled (or never recorded) must be deleted manually in Discord
- Use `python run_all.py --dry-run` to preview embeds without posting, deleting, or reacting
- If `run_all.py` fails mid-batch after a successful post, the next re-run for that channel will clear the recorded message(s) before posting again

<!--
=== FILE FOOTER ===
End of file: SECURITY.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
