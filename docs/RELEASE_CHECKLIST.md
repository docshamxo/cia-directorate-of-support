<!--
=== FILE HEADER ===
Title: Release Checklist
Path: docs/RELEASE_CHECKLIST.md
Created: 2026-07-17
Created by: docshamxo
Modified:
  - 2026-07-17 | docshamxo | Operator release / change-management checklist.
=== END FILE HEADER ===
-->

# Release checklist

Use this before and during any live Discord announcer refresh. Prefer staged offices
over a full `python run_all.py` live blast.

## Pre-flight (every host)

- [ ] `git pull origin main` (or deploy the tagged release)
- [ ] Confirm package version matches `VERSION` / `pyproject.toml`
- [ ] `python bootstrap.py` (or refresh venv + `pip install -e ".[dev]"`)
- [ ] `.env` has current `WEBHOOK_*`, `DISCORD_INVITE_URL`, `DISCORD_OSEC_APPLICATION_RESULTS_URL`
- [ ] Optional: `DISCORD_BOT_TOKEN` set if ✅ reactions are required
- [ ] Staff overlay present when refreshing staff channels:
  `config/links.staff.example.yaml` → `config/links.staff.local.yaml` (filled, gitignored)
- [ ] `python tools/validate_repo.py`
- [ ] `pytest -q`
- [ ] Full dry-run: `python run_all.py --dry-run --delay 0`
- [ ] Review [RELEASE_NOTES_OPERATORS.md](RELEASE_NOTES_OPERATORS.md) for behavior changes since last live send

## Staged live rollout (required for production refreshes)

Run **one stage per pass**. Verify Discord before advancing.

```bash
python run_all.py --list-stages
python run_all.py --stage 1 --dry-run --delay 0
python run_all.py --stage 1
# verify DS channels, then:
python run_all.py --stage 2
# … through stage 5 (ESD)
```

| Stage | Office | Notes |
|-------|--------|--------|
| 1 | `ds` | Public core — lowest blast radius |
| 2 | `osec` | Includes staff docs — need local overlay |
| 3 | `ote` | Includes staff docs — need local overlay |
| 4 | `grs` | Includes staff docs — need local overlay |
| 5 | `esd` | Includes staff docs — need local overlay |

Narrow further with `--only` inside a stage if needed:

```bash
python run_all.py --stage osec --only WEBHOOK_OSEC_OPEN_POSITIONS
```

## Abort / recovery

- [ ] On failure: stop advancing stages; fix config; re-dry-run that stage only
- [ ] Empty-channel recovery: see [OPS.md](OPS.md) (reset `.webhook_messages.json` key, then re-send)
- [ ] Webhook rotate: regenerate in Discord → update `.env` → clear that key in state file

## Post-release

- [ ] Spot-check one channel per office in Discord
- [ ] Confirm `.webhook_messages.json` updated (gitignored — do not commit)
- [ ] Note the git SHA / version deployed in your ops log
- [ ] If cutting a GitHub Release: tag `vX.Y.Z` matching `pyproject.toml` and paste CHANGELOG section

## Version bump (maintainers)

1. Update `version` in `pyproject.toml` and `VERSION`
2. Move items under `[Unreleased]` in `CHANGELOG.md` into a new `## [X.Y.Z] — YYYY-MM-DD`
3. Update compare links at the bottom of `CHANGELOG.md`
4. Open PR; merge when CI is green
5. Optional: `gh release create vX.Y.Z --notes-file …`

<!--
=== FILE FOOTER ===
End of file: docs/RELEASE_CHECKLIST.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
