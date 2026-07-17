<!--
=== FILE HEADER ===
Title: Release Notes Operators
Path: docs/RELEASE_NOTES_OPERATORS.md
Created: 2026-07-17
Created by: docshamxo
Modified:
  - 2026-07-17 | docshamxo | Operator notes for 1.1.0 after hardening PRs.
=== END FILE HEADER ===
-->

# Operator release notes — 1.1.0

**Audience:** people who run live Discord refreshes.  
**Version:** `1.1.0` (`pyproject.toml` / `VERSION`)  
**Hardening PRs merged into main:** [#17](https://github.com/docshamxo/cia-directorate-of-support/pull/17),
[#18](https://github.com/docshamxo/cia-directorate-of-support/pull/18),
[#19](https://github.com/docshamxo/cia-directorate-of-support/pull/19)

Read this once before the next live send after pulling main.

## What changed for you

### Safer purge order (PR #17 / #18)

Live runs **post the new message first**, then delete previously recorded message IDs
from `.webhook_messages.json`. A failed send should leave prior content intact.

- Only IDs this host recorded are deleted — not full channel history.
- Do not commit `.webhook_messages.json`.

### Checkmark reactions (PR #17 / #18)

If `DISCORD_BOT_TOKEN` is set (bot needs **Add Reactions** + **Read Message History**),
successful posts get a ✅. Without a token, posts still send; reactions are skipped.

### Compartmentation / staff links (PR #18)

- Public `config/links.yaml` no longer holds real staff Drive URLs.
- Copy `config/links.staff.example.yaml` → `config/links.staff.local.yaml` and fill URLs
  on the **ops host only** (gitignored).
- Staff announcers **fail closed on live** if `STAFF_LOCAL_REQUIRED` / `example.invalid`
  remain. Dry-run warns but continues (CI-safe).
- Set `DISCORD_INVITE_URL` and `DISCORD_OSEC_APPLICATION_RESULTS_URL` in `.env`.

### Filtered and staged runs (PR #18 + release engineering)

Do **not** default to a full live `python run_all.py` after large hardening changes.

```bash
python run_all.py --list-stages
python run_all.py --stage 1 --dry-run --delay 0
python run_all.py --stage 1          # DS only
python run_all.py --only ds,osec     # ad-hoc filter
```

Full procedure: [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md). Ops details: [OPS.md](OPS.md).

### Content note (PR #19)

GRS/ESD LOWCOM ladder includes **SSA**. Re-run CoC stages (4–5) if those channels
still show the pre-SSA ladder.

## Recommended first live refresh after 1.1.0

1. Complete pre-flight on [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md).
2. Stage 1 (DS) dry-run → live → Discord verify.
3. Stages 2–5 only after staff overlay is filled (skip staff scripts with `--only`
   if overlay is not ready yet).
4. Abort on first failed stage; do not continue.

## Do not

- Commit `.env`, `links.staff.local.yaml`, or `.webhook_messages.json`
- Wipe Discord channels manually expecting `run_all` to rebuild from empty state
  without resetting the matching state key (see docs/OPS.md)
- Rely on USG-style markings — community vocabulary only: **PUBLIC** / **STAFF** / **CANDIDATE**

<!--
=== FILE FOOTER ===
End of file: docs/RELEASE_NOTES_OPERATORS.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
