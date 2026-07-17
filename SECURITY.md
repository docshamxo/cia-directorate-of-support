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
  - 2026-07-17 | docshamxo | Secret-split taxonomy, least privilege, supply chain, CODEOWNERS docs.
  - 2026-07-17 | docshamxo | Link branch protection checklist and pre-commit gitleaks.
  - 2026-07-17 | docshamxo | Add Inter Studios proprietary property notice.
=== END FILE HEADER ===
-->

# Security

Webhook URLs and bot tokens can post (and react) in Discord channels. Keep them private.

**Affiliation:** Unofficial Roblox community tooling — **not** affiliated with the United States Government or the Central Intelligence Agency. Markings `PUBLIC` / `STAFF` / `CANDIDATE` are roleplay vocabulary only.

**Property of the Central Intelligence Agency (ROBLOX), Inter Studios** — see [NOTICE](NOTICE).

## Secret split (compartmentation)

Keep credential classes separated — do not collapse them into one file or one Discord client path:

| Class | Where it lives | Who can use it | Notes |
|-------|----------------|----------------|-------|
| Channel webhooks (`WEBHOOK_*`) | Local `.env` only | Webhook HTTP client | Channel-scoped post/delete; **never** pass `bot_token` into `SyncWebhook.from_url` |
| Bot token (`DISCORD_BOT_TOKEN`) | Local `.env` only | Separate bot HTTP client for ✅ | Reactions only; see least privilege below |
| Community URLs (invite / channel link) | Local `.env` | Announcer embeds | Not committed in `config/links.yaml` |
| Staff Drive / TTP URLs | `config/links.staff.local.yaml` (gitignored) | Staff announcers | Public YAML keeps `STAFF_LOCAL_REQUIRED` placeholders |
| Message ID state | `.webhook_messages.json` (gitignored) | Local purge tracking | Snowflakes only — no URLs or tokens |

`python tools/validate_repo.py` fails if Discord webhook URLs or bot-token-shaped strings appear in tracked config/docs, or if `.env.example` secret values are non-empty.

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

## Least privilege

- **Webhooks:** one webhook per target channel; regenerate per channel if leaked — do not reuse one webhook across unrelated channels
- **Bot:** invite with **only** **Add Reactions** + **Read Message History**. Do **not** grant Administrator, Manage Messages, Manage Webhooks, or Mentions-related elevated perms
- **CI:** workflows default to `permissions: contents: read` (CodeQL adds `security-events: write` only for uploading analysis)
- **Mentions:** live webhook sends use `AllowedMentions.none()` so embeds cannot ping `@everyone` / roles / users
- **Logos:** `confined_logo_path` / `logo_file` only open bare filenames under `assets/logos/` (path traversal rejected)

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

Full checklist: [docs/BRANCH_PROTECTION.md](docs/BRANCH_PROTECTION.md). CODEOWNERS UI steps: [docs/CODEOWNERS_ENFORCEMENT.md](docs/CODEOWNERS_ENFORCEMENT.md).

In GitHub **Settings** (not always API-configurable):

1. Enable **Push protection** (Code security → Push protection)
2. Prefer rulesets / branch protection on `main` (PR required; required check **Validate repository**; consider `enforce_admins`)
3. **Require review from Code Owners** — the CODEOWNERS file alone does not block merges
4. Install local hooks once: `pip install -e ".[dev]" && pre-commit install` (gitleaks + ruff via [`.pre-commit-config.yaml`](.pre-commit-config.yaml))

## Supply chain

- Runtime deps are **exact pins** in `requirements.txt` / `pyproject.toml`
- CI pins GitHub Actions by **commit SHA** (version tag in a trailing comment) and verifies the gitleaks release **SHA-256** before extract
- Dependabot opens weekly PRs for `pip` and `github-actions`; review diff + CI before merge
- Prefer `pip install -e ".[dev]"` from the locked pins in this repo over ad-hoc upgrades on ops hosts
- CI runs `pip-audit` on `requirements.txt` / `requirements-dev.txt`
- CI enforces a **70%** statement coverage floor on `common/` (`pytest-cov`)

## Code scanning

CodeQL workflow (`.github/workflows/codeql.yml`) analyzes Python on pushes/PRs to `main` plus a weekly schedule. Alerts appear under the repository **Security** tab. CI also runs gitleaks (pinned binary + checksum) on full history.

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
