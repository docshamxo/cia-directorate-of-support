<!--
=== FILE HEADER ===
Title: Units index
Path: units/README.md
Created: 2026-07-17
Created by: docshamxo
Modified:
  - 2026-07-17 | docshamxo | Index office announcer folders after reorg.
=== END FILE HEADER ===
-->

# Units

Discord announcer scripts by office. Run from the **repository root** so `common/` imports resolve.

| Office | Folder | Guide |
|--------|--------|-------|
| Directorate of Support | [`ds/`](ds/) | [README](ds/README.md) |
| Office of Security | [`osec/`](osec/) | [README](osec/README.md) |
| Office of Training & Education | [`ote/`](ote/) | [README](ote/README.md) |
| Global Response Staff | [`grs/`](grs/) | [README](grs/README.md) |
| Executive Security Detail | [`esd/`](esd/) | [README](esd/README.md) |

Catalog / run order: [`common/manifest.py`](../common/manifest.py). Batch runner: [`run_all.py`](../run_all.py). Ops: [`docs/OPS.md`](../docs/OPS.md).

```bash
python units/ds/chain_of_command.py --dry-run
python run_all.py --only ds --dry-run --delay 0
python run_all.py --stage osec --dry-run --delay 0
```

`--only ds` and `--stage osec` still use short office names; script paths in the catalog are `units/<office>/...`.

<!--
=== FILE FOOTER ===
End of file: units/README.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
