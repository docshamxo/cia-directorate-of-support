<!--
=== FILE HEADER ===
Title: Changelog
Path: docs/CHANGELOG.md
Created: 2026-07-17
Created by: docshamxo
Modified:
  - 2026-07-17 | docshamxo | Initial changelog for 1.1.0 release engineering.
=== END FILE HEADER ===
-->

# Changelog

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
(`MAJOR.MINOR.PATCH` in `pyproject.toml` / `docs/VERSION`).

## [Unreleased]

### Changed

- Application reapply rules (OSEC + OTE open positions): wait **24 hours** after grading
  before reapplying; max **3** applications then wait a **full week**.
- OSEC open positions: application questions may go to full OSEC High Command (includes
  Superintendent). Optional `discord_id` on `config/personnel.yaml` holders for clickable
  Discord profile links in CoC / contact embeds.
- Populate `discord_id` for ClassifiedInvictus, docshamxo, liveurlite, Rattler_289,
  Shaikhuu, crazybijij2, xBlq_h, jayheart592010, AndyShotSecond, and Astroshard21.
- Fill GRS command: CM Kyongqie, DCM Arthas_1124 (with profile links).
- Last-updated / effective dates stamp from the send date (no static YAML date).
- Property notice appears once in the effective-date footer (not also in disclaimer body).
- Reorganize layout: office announcers under `units/<office>/`; ops runbook at `docs/OPS.md`.
- Clean root layout: docs/tools/requirements folders; `python tools/run_all.py`.

### Planned

- Nothing else queued.

## [1.1.0] — 2026-07-17

Operator-facing release after webhook purge hardening, cross-cutting compartmentation,
and staged rollout tooling. See [RELEASE_NOTES_OPERATORS.md](RELEASE_NOTES_OPERATORS.md)
and [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md).

### Added

- Staged office rollout for `run_all.py`: `--stage`, `--list`, `--list-stages`
  (DS → OSEC → OTE → GRS → ESD).
- `common/rollout.py` selection helpers; `ROLLOUT_STAGES` in `common/manifest.py`.
- Release checklist and operator release notes under `docs/`.
- This changelog, `VERSION`, and package version **1.1.0**.
- Ops runbook (`OPS.md`), staff link overlay example, CODEOWNERS, pytest suite
  for webhook helpers (from hardening PR #18).

### Changed

- Safer live sends: post-then-delete recorded webhook IDs; optional ✅ via bot token
  (PRs #17, #18).
- Community markings (**PUBLIC** / **STAFF** / **CANDIDATE**); staff Drive URLs
  moved to gitignored local overlay; Discord invite/results URLs in `.env`.
- `AllowedMentions.none()`, logo path confinement, embed-limit preflight, webhook
  state file lock.
- GRS/ESD LOWCOM rank ladder includes SSA (PR #19).
- `--only` also matches script basename/stem (e.g. `coc`).

### Security

- Expanded `SECURITY.md` (rotation, Drive revoke, message-ID disposal, push-protection notes).
- Staff announcers fail closed on live send when `STAFF_LOCAL_REQUIRED` / `example.invalid`
  placeholders remain.

## [1.0.0] — 2026-07-14

### Added

- Initial DS / OSEC / OTE / GRS / ESD Discord announcer suite, YAML config, CI,
  Dependabot, and repository validation tooling.

[Unreleased]: https://github.com/docshamxo/cia-directorate-of-support/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/docshamxo/cia-directorate-of-support/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/docshamxo/cia-directorate-of-support/releases/tag/v1.0.0

<!--
=== FILE FOOTER ===
End of file: docs/CHANGELOG.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
