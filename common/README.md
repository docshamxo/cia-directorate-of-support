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
