<!--
=== FILE HEADER ===
Title: CODEOWNERS Enforcement
Path: docs/CODEOWNERS_ENFORCEMENT.md
Created: 2026-07-17
Created by: docshamxo
Modified:
  - 2026-07-17 | docshamxo | Maintainer steps to require Code Owners review on main.
=== END FILE HEADER ===
-->

# CODEOWNERS enforcement (maintainers)

[`.github/CODEOWNERS`](../.github/CODEOWNERS) alone does **not** block merges. GitHub only *suggests* reviewers until branch protection / a ruleset requires owner approval.

## Goal

PRs that touch sensitive paths (`common/`, `config/`, `.github/`, lockfiles, security docs, logos) must get a review from a listed owner before merge to `main`.

## Enable via Rulesets (preferred)

1. Repo **Settings** → **Rules** → **Rulesets** → **New branch ruleset**
2. Target: `main` (or `refs/heads/main`)
3. Enable:
   - **Require a pull request before merging**
   - **Require review from Code Owners**
   - Optionally **Do not allow bypassing the above settings** (equivalent to `enforce_admins`)
4. Keep **Restrict deletions** / force-push blocks as appropriate
5. Save the ruleset

API note: org/repo policies often return 404 for classic branch-protection APIs; use the UI when automation cannot apply these settings.

## Verify

1. Open a test PR that edits `common/cia_common.py` or `config/links.yaml`
2. Confirm the PR shows **Code owners** as required reviewers
3. Confirm merge stays blocked until an owner approves

## Ownership map

See [`.github/CODEOWNERS`](../.github/CODEOWNERS). Expand that file when new secret-adjacent paths appear (for example new workflow directories or packaging metadata).

<!--
=== FILE FOOTER ===
End of file: docs/CODEOWNERS_ENFORCEMENT.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
