<!--
=== FILE HEADER ===
Title: Ops
Path: OPS.md
Created: 2026-07-17
Created by: docshamxo
Modified:
  - 2026-07-17 | docshamxo | Announcer ops runbook (webhooks, state, recovery, bot perms).
  - 2026-07-17 | docshamxo | Expand reaction and purge troubleshooting runbooks.
  - 2026-07-17 | docshamxo | Link staged rollout and release checklist.
=== END FILE HEADER ===
-->

# Ops runbook

Operator checklist for live Discord announcer runs. Prefer dry-run before every live send.

**Doctrine:** webhooks post; the bot only reacts; local state tracks what *this* suite can purge. Do not expect full-channel wipe capability.

For versioned releases and staged office rollout, also use
[docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md) and
[docs/RELEASE_NOTES_OPERATORS.md](docs/RELEASE_NOTES_OPERATORS.md).

## Prerequisites

```bash
python bootstrap.py
```

Edit `.env` (never commit):

- `WEBHOOK_*` — one URL per announcer you will run
- `DISCORD_BOT_TOKEN` — required for ✅ (see [Reactions](#reactions--discord_bot_token))
- `DISCORD_INVITE_URL`, `DISCORD_OSEC_APPLICATION_RESULTS_URL` — community URLs kept out of public YAML

Optional staff overlay:

```bash
# Windows
copy config\links.staff.example.yaml config\links.staff.local.yaml
# macOS / Linux
cp config/links.staff.example.yaml config/links.staff.local.yaml
```

Fill real Drive URLs in the local file, then:

```bash
python tools/validate_repo.py
python run_all.py --dry-run --delay 0
```

---

## Live send behavior (know this)

On a successful live send for a tracked webhook key:

1. **Post** the new message (`wait=True`)
2. **Purge** previously recorded message IDs for that key (from `.webhook_messages.json`)
3. **Record** new IDs (+ any IDs that failed to delete)
4. **React** ✅ via `DISCORD_BOT_TOKEN` when set

A failed post does **not** delete prior content. Webhooks cannot list or wipe full channel history — only recorded IDs from *this* webhook are removable automatically.

---

## Reactions — `DISCORD_BOT_TOKEN`

Webhooks cannot add reactions. ✅ is applied by a separate bot HTTP call after a successful post.

### Setup

1. Create an application + bot at https://discord.com/developers/applications
2. Invite the bot to the target server with at least:
   - **Add Reactions**
   - **Read Message History**
3. Paste the token into `.env`:

```env
DISCORD_BOT_TOKEN=your-bot-token-here
```

4. Confirm with a single channel:

```bash
python ds/public_information.py --dry-run
python ds/public_information.py
```

You should see `Added ✅ to N webhook message(s)` (or a clear warning if the token is missing).

### Fail closed (optional)

```bash
python ds/public_information.py --require-reaction
# or
CIA_REQUIRE_REACTION=1 python run_all.py --only ds
```

Without `--require-reaction`, missing/failed reactions warn and the send still counts as success.

### Troubleshoot: no ✅ / reaction warnings

| Symptom | Check | Fix |
|---------|-------|-----|
| `DISCORD_BOT_TOKEN not set — skipped ✅` | `.env` has empty or missing token | Paste token; restart shell if env was cached |
| `Failed to add ✅ … (HTTP 401/403)` | Token reset / wrong app; bot not in server | Reset token in Developer Portal; re-invite bot |
| `Failed to add ✅ … (HTTP 403/50001)` | Missing channel perms | Grant **Add Reactions** + **Read Message History** on the channel/category |
| `Failed to add ✅ … (HTTP 404)` | Message/channel gone or wrong guild | Confirm webhook still targets the channel the bot can see |
| Rate-limit warnings then success | Normal under burst | Increase `--delay` on `run_all.py` |
| Posts OK, never ✅, no warning | Old code or wrong cwd | Run from repo root; pull latest `main` |

**Compartmentation:** treat the bot token like a webhook URL — local `.env` only; never paste into PRs, issues, or chat. If leaked, see [SECURITY.md](SECURITY.md).

---

## Purge — local message state

State file: **`.webhook_messages.json`** (gitignored). Maps each `WEBHOOK_*` key → list of Discord message snowflakes. No URLs or tokens are stored.

### Rotate a webhook

1. Channel → **Integrations** → **Webhooks** → regenerate or create new
2. Update the matching `WEBHOOK_...=` in `.env`
3. Clear that key from `.webhook_messages.json` (or delete the whole file)
4. Dry-run, then live-send once:

```bash
python ds/public_information.py --dry-run
python ds/public_information.py
```

Old messages from the **previous** webhook URL cannot be deleted by the new webhook — remove leftovers in Discord manually if needed.

### Reset local message state

- Delete `.webhook_messages.json` → forget all tracked posts
- Or remove one JSON key → reset a single channel
- Next live send **posts without deleting** prior tracked messages (manual cleanup may be needed)

### Empty-channel / duplicate recovery

If a channel looks wrong (empty, duplicates, stale embeds):

1. Confirm `.env` webhook still points at the **correct** channel
2. Reset state for that key (see above)
3. Re-run the announcer **once** — post-then-purge only removes IDs already in state
4. Manually delete any leftover / untracked messages in Discord

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
python run_all.py --stage grs --only coc
python run_all.py --delay 2.0
python run_all.py --fail-fast
```

---

## Staff announcers without local overlay

Staff scripts **fail closed** on live send if embeds still contain `STAFF_LOCAL_REQUIRED` / `example.invalid` placeholders. Dry-run warns but continues (CI-safe). Copy the staff example overlay and fill real URLs before live staff posts.

---

## Quick reference

| Goal | Command / action |
|------|------------------|
| Preview all | `python run_all.py --dry-run --delay 0` |
| Live all | `python run_all.py` |
| Require ✅ | `--require-reaction` or `CIA_REQUIRE_REACTION=1` |
| Forget purge targets | Delete or prune `.webhook_messages.json` |
| Secrets leaked | [SECURITY.md](SECURITY.md) rotation playbooks |

<!--
=== FILE FOOTER ===
End of file: OPS.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
