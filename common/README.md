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
  - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
  - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
  - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
  - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
  - 2026-07-15 | docshamxo | Document embed style helpers (hero, motto, closers).
  - 2026-07-17 | docshamxo | Document accessibility helpers.
=== END FILE HEADER ===
-->

# Common

[← Back to main README](../README.md)

[`cia_common.py`](cia_common.py) loads YAML from [`../config/`](../config/) and provides Discord helpers.
[`announcer.py`](announcer.py) provides `run_announcer` and shared CoC layouts.
[`manifest.py`](manifest.py) is the announcer catalog and staged office order.
[`rollout.py`](rollout.py) implements `--only` / `--stage` selection for `run_all.py`.

Full embed contract: [Discord Embed Style Guide](../config/README.md#discord-embed-style-guide).
Accessibility: [docs/ACCESSIBILITY.md](../docs/ACCESSIBILITY.md).

## Do not hardcode here

Put editable values in config instead:

| Data | Config file |
|------|-------------|
| Colors, bots, logo filenames | [`../config/branding.yaml`](../config/branding.yaml) |
| Mottos / about text / handling notices | [`../config/organization.yaml`](../config/organization.yaml) |
| Chain of command | [`../config/personnel.yaml`](../config/personnel.yaml) |
| Links | [`../config/links.yaml`](../config/links.yaml) |
| Server regulations | [`../config/regulations.yaml`](../config/regulations.yaml) |

## Embed helpers

```python
from common import cia_common as c

# Hero: ALL CAPS title + italic community-RP eyebrow + supporting sentence
c.hero_embed(
    title="INFORMATION",
    unit="Office of Security",
    supporting="Short supporting sentence.",
    color=c.COLOR_OSEC,
    logo=c.LOGOS["osec"],
)

c.agency_eyebrow("Office of Security")          # *Unofficial community RP · …*
c.community_link_label("OSEC")                  # DS Community | OSEC
c.motto_line(c.OSEC_MOTTO)                      # *PROTECT · DETECT · RESPOND*
c.link_field("Handbook", c.community_link_label("OSEC Handbook"), url, "STAFF.")
c.pending_group_field("ESD", c.community_link_label("ESD"))

c.classification_handling_embed(unit="OSEC", authority="CIA Office of Security", color=c.COLOR_OSEC)
c.important_notice_embed(unit="OTE", color=c.COLOR_OTE, parent_units=("Directorate of Support",))
c.disclaimer_embed(links=True, color=c.COLOR_OSEC)  # color= required; unofficial-community title
```

Closers order: Classification & Handling Notice (optional) → Important Notice (CoC only) → Disclaimer · Unofficial Community (always last).

Brand / bot naming: [BRAND.md](../BRAND.md).

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
python units/ds/chain_of_command.py
```

<!--
=== FILE FOOTER ===
End of file: common/README.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
