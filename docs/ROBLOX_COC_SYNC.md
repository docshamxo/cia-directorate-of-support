<!--
=== FILE HEADER ===
Title: Roblox CoC Sync
Path: docs/ROBLOX_COC_SYNC.md
Created: 2026-09-28
Created by: docshamxo
Modified:
  - 2026-09-28 | docshamxo | Ops guide for 15-minute Roblox -> Discord CoC edit sync.
  - 2026-09-28 | docshamxo | Document clickable discord_id merge + optional map.
  - 2026-09-28 | docshamxo | Dual targets: DS CoC + OTE CoC (WEBHOOK_OTE_COC_MESSAGE_ID).
=== END FILE HEADER ===
-->

# Roblox -> Discord Chain of Command sync

Polls **Roblox Open Cloud Groups Read** for members in mapped rolesets, rebuilds
**DS** and/or **OTE** Chain of Command embeds (same layouts as
`units/ds/chain_of_command.py` and `units/ote/coc.py`), and **edits** existing
Discord webhook messages by ID every **15 minutes**.

Does **not** rewrite `config/personnel.yaml`. Agency EL stays on YAML unless you add
mappings. No Roblox cookies — use an Open Cloud **API key** only.

## Sync targets

| Channel key | Layout | Webhook env | Message ID env |
|-------------|--------|-------------|----------------|
| `ds_coc` | Full DS CoC | `WEBHOOK_DS_CHAIN_OF_COMMAND` | `WEBHOOK_DS_COC_MESSAGE_ID` |
| `ote_coc` | OTE CoC (DS leadership + OTE HICOM + staff ranks) | `WEBHOOK_OTE_COC` | `WEBHOOK_OTE_COC_MESSAGE_ID` |

Recorded snowflakes (when known): [docs/DISCORD_MESSAGE_IDS.md](DISCORD_MESSAGE_IDS.md).

Filter at runtime: `python -m tools.roblox_coc_sync --once --channel ote_coc`.

## What you must provide

| Item | Where | Notes |
|------|--------|--------|
| Open Cloud API key | `.env` -> `ROBLOX_OPEN_CLOUD_API_KEY` | **User-owned** key (not group-owned). Scope: **group:read**. Create at [Creator Hub -> Open Cloud](https://create.roblox.com/dashboard/credentials). |
| Group IDs | `.env` / example YAML defaults | DS `945806945`, OSEC `288542436`, OTE `1003614105`, GRS `450710337`, ESD via `ROBLOX_GROUP_ID_ESD`. |
| Rank map | `config/roblox_coc_sync.yaml` | Copy from `roblox_coc_sync.example.yaml`; set real `roblox_rank` (or `roblox_role_name`) per CoC slot. **OTE HICOM ranks are placeholders until confirmed in Creator Hub.** |
| DS webhook + message ID | `.env` -> `WEBHOOK_DS_CHAIN_OF_COMMAND`, `WEBHOOK_DS_COC_MESSAGE_ID` | Same webhook that posted the DS CoC message. |
| OTE webhook + message ID | `.env` -> `WEBHOOK_OTE_COC`, `WEBHOOK_OTE_COC_MESSAGE_ID` | Same webhook that posted the OTE CoC message. |

### How to get a webhook message ID

1. Post once (`python units/ds/chain_of_command.py` or `python units/ote/coc.py`), or use an existing CoC message.
2. Discord -> User Settings -> Advanced -> **Developer Mode** ON.
3. Right-click the CoC message -> **Copy Message ID**.
4. Paste into `.env`:

```env
WEBHOOK_DS_COC_MESSAGE_ID=1234567890123456789
WEBHOOK_OTE_COC_MESSAGE_ID=1554041080259805256
```

The sync **PATCHes** those messages; it does not post a second CoC. A missing message
ID on one target skips only that target (other configured targets still run).

## Setup

```bash
python tools/bootstrap.py
copy config\roblox_coc_sync.example.yaml config\roblox_coc_sync.yaml
# Edit roblox_coc_sync.yaml ranks to match Creator Hub rolesets (especially OTE).
```

Add to `.env` (never commit):

```env
ROBLOX_OPEN_CLOUD_API_KEY=
ROBLOX_GROUP_ID_DS=945806945
ROBLOX_GROUP_ID_OSEC=288542436
ROBLOX_GROUP_ID_OTE=1003614105
ROBLOX_GROUP_ID_GRS=450710337
ROBLOX_GROUP_ID_ESD=630084317
WEBHOOK_DS_CHAIN_OF_COMMAND=
WEBHOOK_DS_COC_MESSAGE_ID=
WEBHOOK_OTE_COC=
WEBHOOK_OTE_COC_MESSAGE_ID=
# Optional override (default 15):
# ROBLOX_COC_SYNC_INTERVAL_MINUTES=15
```

## Run

Dry-run (no Discord edit; Roblox pull if API key set):

```bash
python -m tools.roblox_coc_sync --once --dry-run
python -m tools.roblox_coc_sync --once --dry-run --channel ote_coc
```

One live edit (all configured targets with webhook + message ID set):

```bash
python -m tools.roblox_coc_sync --once
python -m tools.roblox_coc_sync --once --channel ote_coc
```

Long-running 15-minute loop (keep a terminal open or use Task Scheduler):

```bash
python -m tools.roblox_coc_sync --loop
```

### Windows Task Scheduler (recommended on this machine)

1. Action: Start a program
   - Program: `python` (or full path to your venv `python.exe`)
   - Arguments: `-m tools.roblox_coc_sync --once`
   - Start in: repo root (`...\cia-directorate-of-support`)
2. Trigger: repeat every **15 minutes**, indefinitely.
3. Run whether user is logged on or not (optional); ensure `.env` is readable.

Prefer Task Scheduler + `--once` over a background loop if the PC sleeps often.

## Behavior notes

- Empty Roblox rank -> holder **`VACANT`**.
- HTTP **429** -> exponential backoff / `Retry-After`.
- Missing message ID or webhook on a live run -> that target is skipped; if **all**
  targets skip -> exit **10** (no crash loop poison).
- Usernames come from the public Users API (`users.roblox.com`).
- **Clickable Discord profile links:** Roblox does not provide Discord IDs. Without a
  link source, holders render as plain text (not `[name](https://discord.com/users/<id>)`).
  Sync keeps links by:
  1. Optional `discord_ids` map in `roblox_coc_sync.yaml` (Roblox username **or** Roblox
     user id -> Discord snowflake), or
  2. Existing `discord_id` on the same abbrev in `personnel.yaml` (Roblox display name
     merged with that snowflake).
- Optional local config path: `ROBLOX_COC_SYNC_CONFIG=C:\path\to\roblox_coc_sync.yaml`

## API reference

- List roles: `GET https://apis.roblox.com/cloud/v2/groups/{groupId}/roles`
- List memberships: `GET .../memberships?filter=role=='groups/{groupId}/roles/{roleId}'`
- Auth header: `x-api-key: <key>`

## Related

- Manual CoC posts: `units/ds/chain_of_command.py`, `units/ote/coc.py`
- Message ID registry: [DISCORD_MESSAGE_IDS.md](DISCORD_MESSAGE_IDS.md)
- Holders source (titles): `config/personnel.yaml` (this sync overrides display holders only at edit time)

<!--
=== FILE FOOTER ===
End of file: docs/ROBLOX_COC_SYNC.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
