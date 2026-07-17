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
  - 2026-07-17 | docshamxo | Tighten tradecraft rules and cross-link OPS runbooks.
  - 2026-07-17 | docshamxo | Link branch protection checklist and pre-commit gitleaks.
=== END FILE HEADER ===
-->

# Security

Webhook URLs and bot tokens can post (and react) in Discord channels. Keep them private.

**Affiliation:** Unofficial Roblox community tooling — **not** affiliated with the United States Government or the Central Intelligence Agency. Markings `PUBLIC` / `STAFF` / `CANDIDATE` are roleplay vocabulary only.

## Compartmentation rules

| Keep local only | Why |
|-----------------|-----|
| `.env` | Webhooks, `DISCORD_BOT_TOKEN`, invite / results URLs |
| `config/links.staff.local.yaml` | Staff Drive / TTP share links |
| `.webhook_messages.json` | Message snowflakes for purge tracking (no secrets, still operational) |

- Create `.env` via `python bootstrap.py` (copies `.env.example`)
- Never commit secrets, paste them into PRs, or share them in chat
- Prefer `git add path/to/file` over `git add .`
- Do **not** put new public staff share links in `config/links.yaml` — use the local overlay
- Public YAML may show `STAFF_LOCAL_REQUIRED` placeholders only

## If a webhook leaks

1. Discord channel → **Integrations** → **Webhooks** → delete or regenerate
2. Update the matching `WEBHOOK_...=` in local `.env`
3. Confirm `.env` is not staged: `git status`
4. Clear that key in `.webhook_messages.json` (old webhook cannot delete its prior posts) — see [OPS.md](OPS.md)
5. Re-run only the affected announcer

## If a bot token leaks

1. Discord Developer Portal → application → **Bot** → **Reset Token**
2. Update `DISCORD_BOT_TOKEN=` in local `.env`
3. Confirm bot still has **Add Reactions** + **Read Message History**
4. Dry-run once, then one live announcer; confirm ✅ (use `--require-reaction` to fail closed)

## If a staff Drive link leaks

1. Google Drive: revoke link access or move to a new folder
2. Update `config/links.staff.local.yaml`
3. Confirm public `config/links.yaml` still has placeholders only
4. Re-run affected staff announcer(s)

## Message ID retention / disposal

- `.webhook_messages.json` stores **message snowflakes only** (no webhook URLs or tokens)
- Delete or prune the file when rotating webhooks, rebuilding a channel, or disposing a workstation
- Live sends **post first**, then delete previously recorded IDs — a failed send should not empty the channel
- Webhooks cannot purge full channel history; unrecorded / manual posts must be deleted in Discord

Operator detail: [OPS.md](OPS.md) (purge + reaction troubleshooting).

## Repository protection (maintainers)

GitHub org/repo settings cannot always be changed via API. Full checklist: [docs/BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md).

In GitHub **Settings**:

1. Enable **Push protection** (Code security → Push protection)
2. Apply a **Ruleset** / branch protection on `main`: require PRs, Code Owner review, and required status checks (`Validate (Python 3.10|3.11|3.12)`, `Secret scan (gitleaks)`, CodeQL `Analyze`). Prefer **Do not allow bypassing the above settings** (`enforce_admins`) when policy allows
3. Keep [`.github/CODEOWNERS`](.github/CODEOWNERS) reviewed on PRs that touch `common/`, `config/`, or `.github/`
4. Install local hooks once: `pip install -e ".[dev]" && pre-commit install` (gitleaks + ruff via [`.pre-commit-config.yaml`](.pre-commit-config.yaml))

## Code scanning

- CodeQL workflow (`.github/workflows/codeql.yml`) analyzes Python on pushes/PRs to `main` plus a weekly schedule (Actions pinned to commit SHAs). Alerts appear under the repository **Security** tab.
- CI also runs a checksum-pinned **gitleaks** binary (not `gitleaks-action`)

## Operational notes

- ✅ reactions need `DISCORD_BOT_TOKEN`; webhooks cannot react alone
- `python run_all.py --dry-run` never posts, deletes, or reacts
- `--require-reaction` / `CIA_REQUIRE_REACTION=1` fails if ✅ cannot be applied
- Full runbooks: [OPS.md](OPS.md)

<!--
=== FILE FOOTER ===
End of file: SECURITY.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
