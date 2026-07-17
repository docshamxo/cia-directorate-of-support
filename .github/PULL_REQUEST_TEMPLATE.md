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
=== END FILE HEADER ===
-->

## Summary

<!-- What changed and why -->

## Sensitivity review

- [ ] No new public staff Drive/share links (use `config/links.staff.local.yaml`)
- [ ] No Discord invite / channel snowflakes committed (use `.env`)
- [ ] Markings use community vocabulary only: **PUBLIC** / **STAFF** / **CANDIDATE** (no USG SECRET/CUI/etc.)
- [ ] Affiliation / fiction disclaimer preserved where closers changed

## Checklist

- [ ] Ran `python tools/validate_repo.py`
- [ ] Ran `python run_all.py --dry-run --delay 0` (and `pytest` if Python helpers changed)
- [ ] Updated READMEs / `.env.example` / `common/manifest.py` if scripts or webhook keys changed
- [ ] No `.env` / `links.staff.local.yaml` / `.webhook_messages.json` secrets in this PR

<!--
=== FILE FOOTER ===
End of file: .github/PULL_REQUEST_TEMPLATE.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
