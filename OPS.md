<!--
=== FILE HEADER ===
Title: Ops
Path: OPS.md
Created: 2026-07-17
Created by: docshamxo
Modified:
  - 2026-07-17 | docshamxo | Announcer ops runbook (webhooks, state, recovery, bot perms).
  - 2026-07-17 | docshamxo | Loud checkmark default, sibling purge, diagnose tool, bot channel purge.
=== END FILE HEADER ===
-->

# Ops runbook

Operational checklist for live Discord announcer runs. Prefer dry-run first.

**Run only this repository** (`cia-directorate-of-support`). Do **not** run the legacy flat scripts under `Downloads\DS` — they post without purge or checkmark reactions and leave orphan messages outside `.webhook_messages.json`.

## Prerequisites

```bash
python bootstrap.py
# Edit .env: WEBHOOK_*, DISCORD_BOT_TOKEN, DISCORD_INVITE_URL,
# DISCORD_OSEC_APPLICATION_RESULTS_URL
# Optional staff overlay:
copy config\links.staff.example.yaml config\links.staff.local.yaml
# then fill real Drive URLs
```

```bash
python tools/validate_repo.py
python tools/diagnose_webhook_state.py
python run_all.py --dry-run --delay 0
```

## Bot permissions for checkmarks (required for live)

Live runs **fail closed** when `DISCORD_BOT_TOKEN` is missing (unless you pass `--allow-skip-reaction`).

1. Create a bot at https://discord.com/developers/applications
2. Invite it to the server with at least:
   - **Add Reactions**
   - **Read Message History**
   - Access to every announcer channel (role / category overrides)
3. Optional for `--bot-channel-purge`: also grant **Manage Messages**
4. Paste the token into `DISCORD_BOT_TOKEN=` in `.env` (never invent or commit a token)

```bash
# Fail if reactions cannot be applied (default):
python run_all.py

# Intentionally post without checkmarks:
python run_all.py --allow-skip-reaction
```

Webhooks cannot react by themselves — without a bot token, posts used to “succeed” while silently skipping checkmarks. That is no longer the default.

## Rotate a webhook

1. Discord channel → **Integrations** → **Webhooks** → regenerate or create new
2. Update the matching `WEBHOOK_...=` in `.env`
3. Clear that key from `.webhook_messages.json` (or delete the file)
4. Dry-run the single script, then live-send once

```bash
python ds/public_information.py --dry-run
python ds/public_information.py
```

## Reset local message state

`.webhook_messages.json` maps `WEBHOOK_*` keys → lists of message IDs.

- Delete the whole file to forget all tracked posts
- Or remove one key to reset a single channel
- Next live send will post without deleting prior tracked messages (manual cleanup may be needed)
- Diagnose: `python tools/diagnose_webhook_state.py`

## Shared webhook URLs (common purge bug)

If two `WEBHOOK_*` keys paste the **same** Discord webhook URL (example: OTE Public Information + OTE Program Overview), each used to track IDs under a separate key and only purged its own — so the other announcer’s posts piled up.

Current behavior: `send_webhook` detects sibling keys that share the same webhook ID and **purges all of their recorded IDs** together. Prefer one webhook per channel when possible.

`run_all.py` and `diagnose_webhook_state.py` warn when duplicates are present.

## Empty-channel / stale-message recovery

If a channel was emptied accidentally:

1. Confirm the webhook URL in `.env` still points at the correct channel
2. Reset state for that webhook key (see above)
3. Re-run the announcer once (post-then-delete only removes IDs already in state)
4. Manually delete any leftover stale messages Discord still shows

Safer purge behavior: **new message is posted first**; IDs are recorded immediately; old recorded IDs are deleted afterward. A failed send should leave prior content intact.

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

## Filtered / staggered runs

```bash
python run_all.py --only ds
python run_all.py --only WEBHOOK_GRS_COC,esd
python run_all.py --delay 2.0
python run_all.py --only WEBHOOK_OTE_PUBLIC_INFORMATION,WEBHOOK_OTE_PROGRAM_OVERVIEW
```

## Staff announcers without local overlay

Staff scripts fail closed on live send if embeds still contain `STAFF_LOCAL_REQUIRED` / `example.invalid` placeholders. Dry-run warns but continues (CI-safe).

<!--
=== FILE FOOTER ===
End of file: OPS.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
