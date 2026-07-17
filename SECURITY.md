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
  - 2026-07-17 | docshamxo | Affiliation, rotation playbooks, staff overlay, push protection notes.
  - 2026-07-17 | docshamxo | Add Inter Studios proprietary property notice.
=== END FILE HEADER ===
-->

# Security

Webhook URLs and bot tokens can post into Discord channels. Keep them private.

**Affiliation:** This repository supports an **unofficial Roblox community**. It is **not affiliated with** the United States Government or the Central Intelligence Agency. Community markings (`PUBLIC` / `STAFF` / `CANDIDATE`) are roleplay vocabulary only.

**Property of the Central Intelligence Agency (ROBLOX), Inter Studios** — see [NOTICE](NOTICE).

## Rules

- Store secrets only in your local `.env`
- Use `python bootstrap.py` to create `.env` from `.env.example`
- Never commit `.env`, paste webhooks into PRs, or share them in chat
- Prefer explicit `git add path/to/file` over `git add .` when staging changes
- `.webhook_messages.json` is local state (message IDs only) — it is gitignored; do not commit it
- `DISCORD_BOT_TOKEN` is a secret (same rules as webhook URLs) — required for ✅ reactions
- `DISCORD_INVITE_URL` and `DISCORD_OSEC_APPLICATION_RESULTS_URL` live in `.env` (not in public YAML)
- Staff Drive / TTP URLs belong in gitignored `config/links.staff.local.yaml` (copy from `config/links.staff.example.yaml`)
- Do **not** commit new public staff share links; keep them in the local overlay

## If a webhook leaks

1. Open the Discord channel → **Integrations** → **Webhooks**
2. Delete or regenerate the leaked webhook
3. Update the matching `WEBHOOK_...=` line in your local `.env`
4. Confirm `.env` is not staged: `git status`
5. Optionally reset local message IDs for that key in `.webhook_messages.json` (see [OPS.md](OPS.md))
6. Re-run only the affected announcer (or `python run_all.py`)

## If a bot token leaks

1. Discord Developer Portal → your application → **Bot** → **Reset Token**
2. Update `DISCORD_BOT_TOKEN=` in local `.env`
3. Confirm the bot still has **Add Reactions** + **Read Message History** in the target server
4. Re-run a single dry-run then one live announcer to verify ✅ reactions

## If a staff Drive link leaks

1. In Google Drive, change sharing on the folder/doc (remove link access or rotate to a new folder)
2. Update `config/links.staff.local.yaml` with the new URLs
3. Confirm the public `config/links.yaml` still shows `STAFF_LOCAL_REQUIRED` placeholders only
4. Re-run the affected staff announcer(s)

## Message ID retention / disposal

- `.webhook_messages.json` stores **message snowflakes only** (no webhook URLs or tokens)
- Delete the file (or prune keys) when rotating webhooks, rebuilding a channel, or disposing local state
- Live sends **post first**, record new IDs immediately, then delete previously recorded IDs — a failed send should not empty the channel
- When two `WEBHOOK_*` keys share one Discord webhook URL, purge clears **all sibling** recorded IDs
- Webhooks cannot purge full channel history; unrecorded/manual/`Downloads\DS` posts must be deleted in Discord or via optional `--bot-channel-purge` (bot needs **Manage Messages**)
- Diagnose: `python tools/diagnose_webhook_state.py`

## Repository protection (maintainers)

GitHub org/repo settings cannot always be changed via API. In the repository **Settings**:

1. Enable **Push protection** for secret scanning (Settings → Code security → Push protection)
2. Consider **Rulesets** / branch protection on `main` with **Require a pull request** and, if appropriate, **Do not allow bypassing the above settings** (`enforce_admins`)
3. Keep [`.github/CODEOWNERS`](.github/CODEOWNERS) reviewed on PRs that touch `common/`, `config/`, or `.github/`

## Code scanning

- GitHub **code scanning** runs via Advanced Setup: the CodeQL workflow at `.github/workflows/codeql.yml` analyzes Python on pushes and pull requests to `main`, plus a weekly schedule
- Results appear under the repository **Security** tab (Code scanning alerts)

## Operational notes

- After each successful post, the suite **requires** a checkmark via the Discord bot API (`DISCORD_BOT_TOKEN`). Live runs exit non-zero if the token is missing or reactions fail — use `--allow-skip-reaction` / `CIA_ALLOW_SKIP_REACTION=1` only intentionally
- Bot needs **Add Reactions** + **Read Message History** (+ channel access); optional **Manage Messages** for `--bot-channel-purge`
- Use `python run_all.py --dry-run` to preview embeds without posting, deleting, or reacting
- See [OPS.md](OPS.md) for runbook steps (rotate webhook, shared URLs, reset state, empty-channel recovery, bot perms)

<!--
=== FILE FOOTER ===
End of file: SECURITY.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
