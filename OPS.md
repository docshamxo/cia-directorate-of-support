<!--
=== FILE HEADER ===
Title: Ops
Path: OPS.md
Created: 2026-07-17
Created by: docshamxo
Modified:
  - 2026-07-17 | docshamxo | Announcer ops runbook (webhooks, state, recovery, bot perms).
=== END FILE HEADER ===
-->

# Ops runbook

Operational checklist for live Discord announcer runs. Prefer dry-run first.

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
python run_all.py --dry-run --delay 0
```

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

## Empty-channel recovery

If a channel was emptied accidentally:

1. Confirm the webhook URL in `.env` still points at the correct channel
2. Reset state for that webhook key (see above)
3. Re-run the announcer once (post-then-delete only removes IDs already in state)
4. Manually delete any leftover stale messages Discord still shows

Safer purge behavior: **new message is posted first**; old recorded IDs are deleted afterward. A failed send should leave prior content intact.

## Bot permissions for ✅

1. Create a bot at https://discord.com/developers/applications
2. Invite it to the server with at least **Add Reactions** and **Read Message History**
3. Paste the token into `DISCORD_BOT_TOKEN=`
4. Optional: `python run_all.py --only ds --require-reaction` (via per-script `--require-reaction`) to fail closed if reactions cannot be applied

Webhooks cannot react by themselves — without a bot token, posts still send but skip ✅.

## Filtered / staggered runs

```bash
python run_all.py --only ds
python run_all.py --only WEBHOOK_GRS_COC,esd
python run_all.py --delay 2.0
```

## Staff announcers without local overlay

Staff scripts fail closed on live send if embeds still contain `STAFF_LOCAL_REQUIRED` / `example.invalid` placeholders. Dry-run warns but continues (CI-safe).

<!--
=== FILE FOOTER ===
End of file: OPS.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
