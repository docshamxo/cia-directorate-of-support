<!--
=== FILE HEADER ===
Title: Branch Protection
Path: docs/BRANCH_PROTECTION.md
Created: 2026-07-17
Created by: docshamxo
Modified:
  - 2026-07-17 | docshamxo | Document recommended main branch protection / rulesets.
=== END FILE HEADER ===
-->

# Branch protection (maintainers)

GitHub cannot always apply these via API for every plan or org policy. Configure them in the repository UI (or org **Rulesets**).

## Recommended ruleset for `main`

Create a **ruleset** (Settings → Rules → Rulesets) targeting `main`, or classic branch protection:

| Setting | Recommended value | Why |
|---------|-------------------|-----|
| Restrict creations / updates / deletions | On for `main` | Force changes through PRs |
| Require a pull request before merging | On | Peer review trail |
| Required approvals | ≥ 1 | Human gate |
| Dismiss stale reviews | On | Re-review after new commits |
| Require review from Code Owners | On | Enforces [`.github/CODEOWNERS`](../.github/CODEOWNERS) |
| Require status checks to pass | On | Block red CI |
| Required checks | **`Validate repository`** (aggregate gate), optionally also matrix/gitleaks/CodeQL | Branch protection currently requires the exact name `Validate repository` |
| Require branches to be up to date | On (if merge queue unused) | Avoid stale merges |
| Require conversation resolution | On | Clear review threads |
| Block force pushes | On | Preserve history |
| Block deletions | On | Protect default branch |
| Do not allow bypassing the above settings | On when feasible (`enforce_admins`) | Same rules for admins |
| Restrict who can push | Maintainers only | No direct pushes to `main` |

After renaming CI jobs, update the required-check list to the exact job names shown under Actions.

## Secret scanning

1. Settings → Code security → enable **Secret scanning**
2. Enable **Push protection**
3. Keep CI gitleaks (checksum-pinned binary) as a second layer; local [`.pre-commit-config.yaml`](../.pre-commit-config.yaml) mirrors it

## Dependabot

[`.github/dependabot.yml`](../.github/dependabot.yml) opens weekly grouped PRs for pip and GitHub Actions. Review SHA-pinned Action digests carefully when merging Actions updates (comment next to each `uses:` shows the human version tag).

## Actions hardening notes

- Third-party Actions are pinned to **immutable commit SHAs** with a `# owner/name@tag` comment for humans and Dependabot.
- Prefer updating via Dependabot PRs that refresh both the SHA and the version comment.
- Do not switch the secret scan to `gitleaks-action` without an org license; the workflow downloads the MIT-licensed CLI with a pinned version + SHA-256.

## Related docs

- [SECURITY.md](../SECURITY.md) — secret playbooks and affiliation notes
- [CONTRIBUTING.md](CONTRIBUTING.md) — local validate / pytest / dry-run loop
- [OPS.md](OPS.md) — live Discord runbook

<!--
=== FILE FOOTER ===
End of file: docs/BRANCH_PROTECTION.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
