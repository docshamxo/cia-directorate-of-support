<!--
=== FILE HEADER ===
Title: Ops
Path: docs/OPS.md
Created: 2026-07-17
Created by: docshamxo
Modified:
  - 2026-07-17 | docshamxo | Announcer ops runbook (webhooks, state, recovery, bot perms).
  - 2026-07-17 | docshamxo | Expand reaction and purge troubleshooting runbooks.
  - 2026-07-17 | docshamxo | Link staged rollout and release checklist.
  - 2026-07-17 | docshamxo | Loud checkmark default, sibling purge, diagnose tool, bot channel purge.
  - 2026-07-17 | docshamxo | Least-privilege bot invite and secret-split reminders.
  - 2026-07-17 | docshamxo | Note Inter Studios proprietary property notice.
  - 2026-07-17 | docshamxo | Mid-batch failure playbook, exit codes, state reset tool.
  - 2026-07-17 | docshamxo | Move ops runbook to docs/; update unit script paths.
=== END FILE HEADER ===
-->

# Ops runbook

Operator checklist for live Discord announcer runs. Prefer dry-run before every live send.

**Property of the Central Intelligence Agency (ROBLOX), Inter Studios** — see [NOTICE](../NOTICE).

**Doctrine:** webhooks post; the bot only reacts; local state tracks what *this* suite can purge. Do not expect full-channel wipe capability.

For versioned releases and staged office rollout, also use
[RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) and
[RELEASE_NOTES_OPERATORS.md](RELEASE_NOTES_OPERATORS.md).

**Run only this repository** (`cia-directorate-of-support`). Do **not** run the legacy flat scripts under `Downloads\DS` — they post without purge or checkmark reactions and leave orphan messages outside `.webhook_messages.json`.

## Prerequisites

```bash
python bootstrap.py
```

Edit `.env` (never commit) — keep classes split (`WEBHOOK_*` ≠ bot token ≠ staff overlay):

- `WEBHOOK_*` — one URL per announcer you will run
- `DISCORD_BOT_TOKEN` — **required for live** (see [Reactions](#reactions--discord_bot_token))
- `DISCORD_INVITE_URL`, `DISCORD_OSEC_APPLICATION_RESULTS_URL` — community URLs kept out of public YAML
- `OSEC_LOWCOM_APPLICATION_URL`, `OSEC_MIDCOM_APPLICATION_URL`, `OTE_APPLICATION_URL` — applicant intake forms
- `OTE_APPLICATION_TRACKER_URL` — optional staff/ops tracker (never post publicly)

Optional staff overlay:

```bash
# Windows
copy config\links.staff.example.yaml config\links.staff.local.yaml
# macOS / Linux
cp config/links.staff.example.yaml config/links.staff.local.yaml
```

Optional mid-tier roster overlay:

```bash
# Windows
copy config\personnel.holders.example.yaml config\personnel.holders.local.yaml
# macOS / Linux
cp config/personnel.holders.example.yaml config/personnel.holders.local.yaml
```

Fill real Drive URLs in the local file, then:

```bash
python tools/validate_repo.py
python tools/diagnose_webhook_state.py
python run_all.py --dry-run --delay 0
```

## Alerting exit codes

`run_all.py` uses Nagios-style exit codes so monitors can page correctly:

| Code | Meaning | When |
|------|---------|------|
| **0** | OK | All runnable announcers succeeded (skips allowed unless `--strict-skips`) |
| **1** | WARNING | Nothing runnable (all skipped), or `--strict-skips` with skips |
| **2** | CRITICAL | One or more hard failures |
| **3** | UNKNOWN | Unexpected runner/control error |

Per-announcer conventions (direct script invoke): **0** success, **10** intentional skip, **20** config/fail-closed.

```bash
python run_all.py --dry-run --delay 0 --report .run_report.json
```

---

## Live send behavior (know this)

On a successful live send for a tracked webhook key:

1. **Post** the new message (`wait=True`)
2. **Purge** previously recorded message IDs for that key (and sibling keys sharing the same webhook URL)
3. **Record** new IDs (+ any IDs that failed to delete)
4. **React** checkmark via `DISCORD_BOT_TOKEN` (required unless `--allow-skip-reaction`)

A failed post does **not** delete prior content. Webhooks cannot list or wipe full channel history — only recorded IDs from *this* webhook are removable automatically.

---

## Reactions — `DISCORD_BOT_TOKEN`

Webhooks cannot add reactions. The checkmark is applied by a separate bot HTTP call after a successful post.

Live runs **fail closed** when `DISCORD_BOT_TOKEN` is missing (unless you pass `--allow-skip-reaction`).

### Setup

1. Create an application + bot at https://discord.com/developers/applications
2. Invite the bot to the target server with at least:
   - **Add Reactions**
   - **Read Message History**
   - Access to every announcer channel (role / category overrides)
3. Optional for `--bot-channel-purge`: also grant **Manage Messages** (do not grant Administrator or Manage Webhooks)
4. Paste the token into `.env` (never into a webhook URL field; never invent or commit a token):

```env
DISCORD_BOT_TOKEN=your-bot-token-here
```

5. Confirm with a single channel:

```bash
python units/ds/public_information.py --dry-run
python units/ds/public_information.py
```

You should see `Added checkmark to N webhook message(s)` (or a clear error if the token is missing).

### Intentionally skip reactions

```bash
python run_all.py --allow-skip-reaction
# or per-script:
python units/ds/public_information.py --allow-skip-reaction
```

Webhooks cannot react by themselves — without a bot token, live runs now exit non-zero by default instead of silently skipping checkmarks.

### Troubleshoot: no checkmark / reaction warnings

| Symptom | Check | Fix |
|---------|-------|-----|
| `DISCORD_BOT_TOKEN not set` on live run | `.env` has empty or missing token | Paste token; restart shell if env was cached |
| `Failed to add checkmark … (HTTP 401/403)` | Token reset / wrong app; bot not in server | Reset token in Developer Portal; re-invite bot |
| `Failed to add checkmark … (HTTP 403/50001)` | Missing channel perms | Grant **Add Reactions** + **Read Message History** on the channel/category |
| `Failed to add checkmark … (HTTP 404)` | Message/channel gone or wrong guild | Confirm webhook still targets the channel the bot can see |
| Rate-limit warnings then success | Normal under burst | Increase `--delay` on `run_all.py` |
| Posts OK, never checkmark, no warning | Old code or wrong cwd | Run from repo root; pull latest `main` |

**Compartmentation:** treat the bot token like a webhook URL — local `.env` only; never paste into PRs, issues, or chat. If leaked, see [SECURITY.md](../SECURITY.md).

---

## Purge — local message state

State file: **`.webhook_messages.json`** (gitignored). Maps each `WEBHOOK_*` key -> list of Discord message snowflakes. No URLs or tokens are stored.

Diagnose: `python tools/diagnose_webhook_state.py`

### Shared webhook URLs (sibling purge)

If two `WEBHOOK_*` keys paste the **same** Discord webhook URL (example: OTE Public Information + OTE Program Overview), each used to track IDs under a separate key and only purged its own — so the other announcer's posts piled up.

Current behavior: `send_webhook` detects sibling keys that share the same webhook ID and **purges all of their recorded IDs** together. Prefer one webhook per channel when possible.

`run_all.py` and `diagnose_webhook_state.py` warn when duplicates are present.

### Rotate a webhook

1. Channel -> **Integrations** -> **Webhooks** -> regenerate or create new
2. Update the matching `WEBHOOK_...=` in `.env`
3. Clear that key from `.webhook_messages.json` (or delete the whole file)
4. Dry-run, then live-send once:

```bash
python units/ds/public_information.py --dry-run
python units/ds/public_information.py
```

Old messages from the **previous** webhook URL cannot be deleted by the new webhook — remove leftovers in Discord manually if needed.

### Reset local message state

- Delete `.webhook_messages.json` -> forget all tracked posts
- Or remove one JSON key -> reset a single channel
- Next live send **posts without deleting** prior tracked messages (manual cleanup may be needed)

### Empty-channel / duplicate recovery

If a channel looks wrong (empty, duplicates, stale embeds):

1. Confirm `.env` webhook still points at the **correct** channel
2. Reset state for that key (see above)
3. Re-run the announcer **once** — post-then-purge only removes IDs already in state
4. Manually delete any leftover / untracked messages in Discord

### Orphan messages (not in state)

Messages from before state tracking, from `Downloads\DS`, or from a **different** webhook in the same channel cannot be deleted by webhook ID state alone.

Options:

1. Manual delete in Discord
2. Optional bot-assisted cleanup (bot needs **Manage Messages** + **Read Message History**):

```bash
python run_all.py --only ote --bot-channel-purge
# or: set CIA_BOT_CHANNEL_PURGE=1
```

This deletes other recent **webhook-authored** messages in the channel while keeping the newly posted IDs. Human messages are left alone.

### Troubleshoot: purge

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Old posts remain after re-run | IDs never recorded (first run, deleted state, different machine) | Manual delete in Discord; next successful send records new IDs |
| Old posts remain; state has IDs | Webhook rotated; old webhook owned those messages | Manual delete; clear state key; re-run |
| `Could not delete prior message … (HTTP 404)` | Already gone | Benign; ID is dropped from tracking |
| `Could not delete … (HTTP 401/404)` after rotate | State still lists IDs from old webhook | Clear that key; clean channel manually |
| Channel emptied unexpectedly | Unlikely on failed send (post-first design) | Confirm you did not delete manually; restore by re-running announcer |
| Duplicates after every run | State not writing (permissions / wrong directory) | Run from repo root; ensure `.webhook_messages.json` is writable and not redirected |
| Rate-limited deletes | Burst / many IDs | Suite retries with sleep; raise `--delay` |

**Limit:** this suite cannot purge full channel history or other bots' messages — only recorded IDs from the active webhook.

```bash
python tools/reset_webhook_state.py --list
python tools/reset_webhook_state.py --key WEBHOOK_DS_PUBLIC_INFORMATION
python tools/reset_webhook_state.py --all --yes
```

---

## Mid-batch failures

`run_all.py` continues after failures by default (unless `--fail-fast`). Successful channels already have their new posts live; failed ones keep prior content if the send never succeeded.

### Symptoms

- Summary shows `Failed: N` and exit code **2** (CRITICAL)
- Resume hint: `python run_all.py --from path/to/script.py`
- Optional JSON report via `--report` lists timings and stderr tails

### Response

1. **Do not wipe all state** — per-channel state is independent
2. Read the failure reason / stderr tail (or `.run_report.json`)
3. Fix the cause (webhook URL, staff overlay, rate limit, bot token, embed limits)
4. Resume or retry:

```bash
python run_all.py --from units/osec/staff_documents.py
python run_all.py --only WEBHOOK_OSEC_STAFF_DOCUMENTS
python run_all.py --retry 1 --fail-fast
```

5. If a channel looks empty after a partial purge, clear only that key and re-send once
6. Dry-run first when unsure: `python run_all.py --dry-run --from ... --delay 0`

Observability: structured `event=` log lines; page on exit **2**, triage on **1**, ignore **0**.

---

## Filtered / staged office runs

Prefer **one office stage per live pass** after hardening or large config changes:

```bash
python run_all.py --list-stages
python run_all.py --stage 1 --dry-run --delay 0
python run_all.py --stage 1
python run_all.py --stage osec
python run_all.py --only ds
python run_all.py --only WEBHOOK_GRS_COC,esd
python run_all.py --only WEBHOOK_OTE_PUBLIC_INFORMATION,WEBHOOK_OTE_PROGRAM_OVERVIEW
python run_all.py --stage grs --only coc
python run_all.py --delay 2.0
python run_all.py --fail-fast
python run_all.py --allow-skip-reaction
python run_all.py --bot-channel-purge
python run_all.py --from units/grs/coc.py
python run_all.py --retry 1 --report .run_report.json
python run_all.py --strict-skips
```

---

## Staff announcers without local overlay

Staff scripts **fail closed** on live send if embeds still contain `STAFF_LOCAL_REQUIRED` / `example.invalid` placeholders (exit **20**). Dry-run warns but continues (CI-safe). Copy the staff example overlay and fill real URLs before live staff posts.

---

## Quick reference

| Goal | Command / action |
|------|------------------|
| Preview all | `python run_all.py --dry-run --delay 0` |
| Live all | `python run_all.py` (requires `DISCORD_BOT_TOKEN`) |
| Diagnose state | `python tools/diagnose_webhook_state.py` |
| Post without checkmark | `--allow-skip-reaction` or `CIA_ALLOW_SKIP_REACTION=1` |
| Bot channel cleanup | `--bot-channel-purge` or `CIA_BOT_CHANNEL_PURGE=1` |
| Forget purge targets | Delete or prune `.webhook_messages.json` |
| Live all | `python run_all.py` |
| Require ✅ | `--require-reaction` or `CIA_REQUIRE_REACTION=1` |
| Forget purge targets | `python tools/reset_webhook_state.py --key WEBHOOK_...` |
| Resume mid-batch | `python run_all.py --from path/to/script.py` |
| Secrets leaked | [SECURITY.md](../SECURITY.md) rotation playbooks |

<!--
=== FILE FOOTER ===
End of file: docs/OPS.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
