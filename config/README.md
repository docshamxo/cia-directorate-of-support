<!--
=== FILE HEADER ===
Title: Config README
Path: config/README.md
Created: 2026-07-14
Created by: docshamxo
Modified:
  - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
=== END FILE HEADER ===
-->

# Config

[← Back to main README](../README.md)

Editable data for the announcers. Change these files instead of hardcoding values in Python.

| File | What to edit here |
|------|-------------------|
| [`branding.yaml`](branding.yaml) | Colors, bot usernames, logo filenames |
| [`organization.yaml`](organization.yaml) | Mottos, about text, offices, disclaimers |
| [`personnel.yaml`](personnel.yaml) | Chain-of-command names and ranks |
| [`links.yaml`](links.yaml) | Document, form, Roblox, and Discord URLs |

## Examples

**Change a holder name**

Edit `personnel.yaml`:

```yaml
ds_leadership:
  - abbrev: DCDSD
    title: Deputy Component Director, Directorate of Support
    holder: NewUsername
```

**Change a document link**

Edit `links.yaml`:

```yaml
osec:
  information:
    handbook: https://docs.google.com/document/d/NEW_ID/edit
```

**Change a color**

Edit `branding.yaml`:

```yaml
colors:
  grs: "0xFFD700"
```

## After editing

```bash
cd cia-directorate-of-support
python tools/validate_repo.py
python ds/chain_of_command.py
```

<!--
=== FILE FOOTER ===
End of file: config/README.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
