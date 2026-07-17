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
  - 2026-07-17 | docshamxo | Link branch protection checklist and pre-commit gitleaks.
  - 2026-07-17 | docshamxo | Privacy / data governance section; applicant env overlays.
=== END FILE HEADER ===
-->

# Security

Webhook URLs and bot tokens can post into Discord channels. Keep them private.

**Affiliation:** This repository supports an **unofficial Roblox community**. It is **not affiliated with** the United States Government or the Central Intelligence Agency. Community markings (`PUBLIC` / `STAFF` / `CANDIDATE`) are roleplay vocabulary only.

## Privacy / data governance

This suite posts community roleplay content to Discord. Treat Roblox usernames, applicant forms, trackers, and ORBAT sheets as sensitive community data.

| Data | Where it lives | Rule |
|------|----------------|------|
| Webhooks / bot token | `.env` (gitignored) | Never commit or paste into PRs |
| Discord invite / channel snowflakes | `.env` | Not in `config/links.yaml` |
| Applicant intake forms | `.env` (`OSEC_*_APPLICATION_URL`, `OTE_APPLICATION_URL`) | Rotate without writing IDs into git history |
| Applicant status tracker | `.env` (`OTE_APPLICATION_TRACKER_URL`) | **Staff/ops only** — do not post in public channels |
| Staff Drive / ORBAT / TTP | `config/links.staff.local.yaml` | Placeholders only in public `links.yaml` |
| Mid-tier named rosters (e.g. multi CM) | `config/personnel.holders.local.yaml` | Committed YAML keeps `VACANT`; fill locally |
| High-command holders | `config/personnel.yaml` | Minimal public CoC names only — no bulk rosters |
| Webhook message IDs | `.webhook_messages.json` | Local snowflakes only; dispose on rotation / exit |

**Applicant handling:** Forms collect applicant answers. Prefer env-backed form URLs so operators can rotate links after campaigns. Never commit tracker spreadsheet IDs. The public OTE open-positions announcer links the application form only — not the tracker.

**Roster minimization:** Do not expand `personnel.yaml` with full membership lists. Multi-holder Mid/Main Element slots use the holders overlay. Rank ladders without holders are fine in public YAML.

## Rules

- Store secrets only in your local `.env`
- Use `python bootstrap.py` to create `.env` from `.env.example`
- Never commit `.env`, paste webhooks into PRs, or share them in chat
- Prefer explicit `git add path/to/file` over `git add .` when staging changes
- `.webhook_messages.json` is local state (message IDs only) — it is gitignored; do not commit it
- `DISCORD_BOT_TOKEN` is a secret (same rules as webhook URLs) — required for ✅ reactions
- `DISCORD_INVITE_URL`, `DISCORD_OSEC_APPLICATION_RESULTS_URL`, and applicant form/tracker URLs live in `.env` (not in public YAML)
- Staff Drive / TTP / ORBAT URLs belong in gitignored `config/links.staff.local.yaml` (copy from `config/links.staff.example.yaml`)
- Mid-tier roster holders belong in gitignored `config/personnel.holders.local.yaml` (copy from `config/personnel.holders.example.yaml`)
- Do **not** commit new public staff share links or applicant tracker IDs; keep them in local overlays / `.env`

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

- `.webhook_messages.json` stores **message snowflakes only** (no webhook URLs, tokens, usernames, or embed text)
- **Retention:** keep only while you need purge-before-repost for the same channels; it is **not** an audit log
- **Disposal:** delete the file (or prune keys) when rotating webhooks, rebuilding a channel, decommissioning an ops host, or leaving the project
- Live sends **post first**, then delete previously recorded IDs — a failed send should not empty the channel
- Webhooks cannot purge full channel history; unrecorded/manual posts must be deleted in Discord
- Do not back up `.webhook_messages.json` into shared drives or commit history

## Repository protection (maintainers)

GitHub org/repo settings cannot always be changed via API. Full checklist: [docs/BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md).

In the repository **Settings**:

1. Enable **Push protection** for secret scanning (Settings → Code security → Push protection)
2. Apply a **Ruleset** / branch protection on `main`: require PRs, Code Owner review, and required status checks (`Validate (Python 3.10|3.11|3.12)`, `Secret scan (gitleaks)`, CodeQL `Analyze`). Prefer **Do not allow bypassing the above settings** (`enforce_admins`) when policy allows
3. Keep [`.github/CODEOWNERS`](.github/CODEOWNERS) reviewed on PRs that touch `common/`, `config/`, or `.github/`
4. Install local hooks once: `pip install -e ".[dev]" && pre-commit install` (gitleaks + ruff via [`.pre-commit-config.yaml`](.pre-commit-config.yaml))

## Code scanning

- GitHub **code scanning** runs via Advanced Setup: the CodeQL workflow at `.github/workflows/codeql.yml` analyzes Python on pushes and pull requests to `main`, plus a weekly schedule (Actions pinned to commit SHAs)
- Results appear under the repository **Security** tab (Code scanning alerts)
- CI also runs a checksum-pinned **gitleaks** binary (not `gitleaks-action`)

## Operational notes

- After each successful post, the suite adds ✅ via the Discord bot API when `DISCORD_BOT_TOKEN` is set (webhooks cannot react on their own)
- Use `python run_all.py --dry-run` to preview embeds without posting, deleting, or reacting
- Pass `--require-reaction` (or `CIA_REQUIRE_REACTION=1`) to fail if ✅ cannot be applied
- See [OPS.md](OPS.md) for runbook steps (rotate webhook, reset state, empty-channel recovery, bot perms)

<!--
=== FILE FOOTER ===
End of file: SECURITY.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
