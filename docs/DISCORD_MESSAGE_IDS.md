<!--
=== FILE HEADER ===
Title: Discord webhook message IDs
Path: docs/DISCORD_MESSAGE_IDS.md
Created: 2026-09-28
Created by: docshamxo
Modified:
  - 2026-09-28 | docshamxo | Record OTE + OSEC webhook message snowflakes for edit-in-place.
  - 2026-09-28 | docshamxo | Note OTE/DS CoC IDs are consumed by roblox_coc_sync.
=== END FILE HEADER ===
-->

# Discord webhook message IDs

Public Discord snowflakes for **edit-in-place** (webhook `PATCH` / Roblox→Discord sync).
These are not secrets. Webhook **URLs** stay in gitignored `.env` only.

Set the matching `*_MESSAGE_ID` keys in local `.env` (see `.env.example`).
`WEBHOOK_OTE_COC_MESSAGE_ID` and `WEBHOOK_DS_COC_MESSAGE_ID` are used by
`python -m tools.roblox_coc_sync` — see [ROBLOX_COC_SYNC.md](ROBLOX_COC_SYNC.md).

## Recorded anchors (2026-09-28)

| Purpose | Env key | Message ID | Channel | Guild |
|---------|---------|------------|---------|-------|
| OTE Open Positions | `WEBHOOK_OTE_OPEN_POSITIONS_MESSAGE_ID` | `1546939157899780249` | `1505011919269007440` | `1450874817459912789` (OTE) |
| OTE Program Overview | `WEBHOOK_OTE_PROGRAM_OVERVIEW_MESSAGE_ID` | `1554039682675900467` | `1450874818504298566` | `1450874817459912789` (OTE) |
| OTE Chain of Command | `WEBHOOK_OTE_COC_MESSAGE_ID` | `1554041080259805256` | `1450874818328264811` | `1450874817459912789` (OTE) |
| OSEC Chain of Command | `WEBHOOK_OSEC_COC_MESSAGE_ID` | `1554041066376790046` | `1442014373538168934` | `1442014369507446918` (OSEC) |

### Links

- [OTE Open Positions](https://discord.com/channels/1450874817459912789/1505011919269007440/1546939157899780249)
- [OTE Program Overview](https://discord.com/channels/1450874817459912789/1450874818504298566/1554039682675900467)
- [OTE CoC](https://discord.com/channels/1450874817459912789/1450874818328264811/1554041080259805256)
- [OSEC CoC](https://discord.com/channels/1442014369507446918/1442014373538168934/1554041066376790046)

## Naming

Message ID env keys follow the webhook key + `_MESSAGE_ID`:

- `WEBHOOK_OTE_OPEN_POSITIONS` → `WEBHOOK_OTE_OPEN_POSITIONS_MESSAGE_ID`
- `WEBHOOK_OTE_PROGRAM_OVERVIEW` → `WEBHOOK_OTE_PROGRAM_OVERVIEW_MESSAGE_ID`
- `WEBHOOK_OTE_COC` → `WEBHOOK_OTE_COC_MESSAGE_ID`
- OSEC CoC has no announcer webhook key in-repo yet; use `WEBHOOK_OSEC_COC_MESSAGE_ID` for the live CoC channel message.
- Roblox CoC sync uses `WEBHOOK_DS_COC_MESSAGE_ID` (`WEBHOOK_DS_CHAIN_OF_COMMAND`) and
  `WEBHOOK_OTE_COC_MESSAGE_ID` (`WEBHOOK_OTE_COC`) — see `docs/ROBLOX_COC_SYNC.md`.

## How to capture another ID

1. Discord → User Settings → Advanced → **Developer Mode** ON.
2. Right-click the webhook message → **Copy Message ID**.
3. Paste into `.env` under the matching `*_MESSAGE_ID` key.

<!--
=== FILE FOOTER ===
End of file: docs/DISCORD_MESSAGE_IDS.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
