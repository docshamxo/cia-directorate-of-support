<!--
=== FILE HEADER ===
Title: PULL Request Template
Path: .github/PULL_REQUEST_TEMPLATE.md
Created: 2026-07-14
Created by: docshamxo
Modified:
  - 2026-07-14 | docshamxo | Add CI, Dependabot, and repository validation tooling.
  - 2026-07-14 | docshamxo | Simplify setup and contributor docs.
  - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
  - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
  - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
  - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
  - 2026-07-17 | docshamxo | Sensitivity review checklist and marking vocabulary.
  - 2026-07-17 | docshamxo | Secret-split and supply-chain checklist items.
  - 2026-07-17 | docshamxo | Clarify summary vs test plan; link docs index.
=== END FILE HEADER ===
-->

## Summary

<!-- What changed and why (1–3 bullets). -->

## Test plan

<!-- How you verified. Operators: link OPS / release checklist if live-run related. -->

- [ ] Ran `python tools/validate_repo.py`
- [ ] Ran `python tools/run_all.py --dry-run --delay 0` (and `pytest` if Python helpers changed)

## Sensitivity review

- [ ] No new public staff Drive/share / ORBAT links (use `config/links.staff.local.yaml`)
- [ ] No Discord invite / channel snowflakes / applicant form or tracker URLs committed (use `.env`)
- [ ] No multi-person mid-tier rosters committed (use `personnel.holders.local.yaml`)
- [ ] Markings use community vocabulary only: **PUBLIC** / **STAFF** / **CANDIDATE** (no USG SECRET/CUI/etc.)
- [ ] Affiliation / fiction disclaimer preserved where closers changed
- [ ] Secret classes stay split (no bot token on webhook path; no webhook URLs in YAML)

## Checklist

- [ ] Updated READMEs / `docs/` / `.env.example` / `common/manifest.py` if scripts or webhook keys changed
- [ ] No `.env` / `links.staff.local.yaml` / `personnel.holders.local.yaml` / `.webhook_messages.json` secrets in this PR
- [ ] Dependency / Actions bumps reviewed (pins + CI) if supply-chain files changed
- [ ] Docs map / [docs/README.md](../docs/README.md) updated if new operator docs were added

<!--
=== FILE FOOTER ===
End of file: .github/PULL_REQUEST_TEMPLATE.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
