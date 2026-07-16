<!--
=== FILE HEADER ===
Title: Assets README
Path: assets/README.md
Created: 2026-07-14
Created by: docshamxo
Modified:
  - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
  - 2026-07-14 | docshamxo | Polish repository presentation and align documentation.
  - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
  - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
  - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
  - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
=== END FILE HEADER ===
-->

# Assets

[← Repository root](../README.md)

Media used by Discord embeds and kept for organizational reference.

## Logos (`logos/`)

Referenced by `config/branding.yaml` (loaded through `common/cia_common.py`) as embed thumbnails.

| File | Unit | Code key |
|------|------|----------|
| [`logos/DS.png`](logos/DS.png) | Directorate of Support | `ds` |
| [`logos/OSEC.png`](logos/OSEC.png) | Office of Security | `osec` |
| [`logos/OTE.png`](logos/OTE.png) | Office of Training & Education | `ote` |
| [`logos/GRS.png`](logos/GRS.png) | Global Response Staff | `grs` |
| [`logos/ESD.png`](logos/ESD.png) | Executive Security Detail | `esd` |

## Diagrams (`diagrams/`)

Reference visuals (not attached automatically by announcers).

| File | Description |
|------|-------------|
| [`diagrams/org-overview.png`](diagrams/org-overview.png) | Organization overview |
| [`diagrams/ESDxGRS_v2.png`](diagrams/ESDxGRS_v2.png) | ESD × GRS relationship diagram (v2) |
| [`diagrams/ESGxGRS.png`](diagrams/ESGxGRS.png) | ESG / GRS relationship diagram |

Keep filenames stable; renaming a logo requires a matching update in [`config/branding.yaml`](../config/branding.yaml).

<!--
=== FILE FOOTER ===
End of file: assets/README.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
