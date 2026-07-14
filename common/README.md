<!--
=== FILE HEADER ===
Title: Common README
Path: common/README.md
Created: 2026-07-14
Created by: docshamxo
Modified:
  - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
  - 2026-07-14 | docshamxo | Polish repository presentation and align documentation.
  - 2026-07-14 | docshamxo | Simplify setup and contributor docs.
  - 2026-07-14 | docshamxo | Document every install, setup, and run command explicitly.
  - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
=== END FILE HEADER ===
-->

# Common

[← Back to main README](../README.md)

[`cia_common.py`](cia_common.py) loads YAML from [`../config/`](../config/) and provides Discord helpers.

## Do not hardcode here

Put editable values in config instead:

| Data | Config file |
|------|-------------|
| Colors, bots, logo filenames | [`../config/branding.yaml`](../config/branding.yaml) |
| Mottos / about text | [`../config/organization.yaml`](../config/organization.yaml) |
| Chain of command | [`../config/personnel.yaml`](../config/personnel.yaml) |
| Links | [`../config/links.yaml`](../config/links.yaml) |

## Useful helpers

```python
from common import cia_common as c

c.require_webhook('WEBHOOK_DS_CHAIN_OF_COMMAND')
c.url('osec.information.handbook')
c.embed(description='...', logo=c.LOGOS['ds'])
c.send_webhook(url, embeds, username=c.BOT_DS)
```

## After editing config

```bash
cd cia-directorate-of-support
python tools/validate_repo.py
python ds/chain_of_command.py
```

<!--
=== FILE FOOTER ===
End of file: common/README.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
