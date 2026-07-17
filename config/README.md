<!--
=== FILE HEADER ===
Title: Config README
Path: config/README.md
Created: 2026-07-14
Created by: docshamxo
Modified:
  - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
  - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
  - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
  - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
  - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
  - 2026-07-17 | docshamxo | Document shared Marking: PUBLIC/STAFF/CANDIDATE link notes.
=== END FILE HEADER ===
-->

# Config

[← Back to main README](../README.md)

Editable data for the announcers. Change these files instead of hardcoding values in Python.

| File | What to edit here |
|------|-------------------|
| [`branding.yaml`](branding.yaml) | Colors, bot usernames, logo filenames, property notice |
| [`organization.yaml`](organization.yaml) | Mottos, about text, offices, disclaimers, affiliation / property notices |
| [`personnel.yaml`](personnel.yaml) | Chain-of-command names and ranks (mid-tier rosters via local holders overlay) |
| [`personnel.holders.example.yaml`](personnel.holders.example.yaml) | Example mid-tier roster overlay (copy → `personnel.holders.local.yaml`) |
| [`links.yaml`](links.yaml) | Public document and Roblox URLs (staff Drive / ORBAT via local overlay; applicant forms via `.env`) |
| [`links.staff.example.yaml`](links.staff.example.yaml) | Example staff Drive / ORBAT overlay (copy → `links.staff.local.yaml`) |
| [`regulations.yaml`](regulations.yaml) | Server regulations prose |

## Discord Embed Style Guide

Discord supports markdown emphasis only — no custom fonts. Typography means `**bold**`, `*italic*`, title casing, and embed chrome (color bar, thumbnail).

### Design contract

| Element | Rule |
|---------|------|
| **Hero** | ALL CAPS `title=` + italic eyebrow `*Unofficial community RP · {Unit}*` + one short supporting sentence |
| **Body section titles** | Title Case |
| **Links** | `[CIA {UNIT} \| {Document}](url)` with optional italic note; community groups: `CIA \| {Group}` |
| **Link notes** | Prefer shared Marking: PUBLIC. / Marking: STAFF. / Marking: CANDIDATE. (c.MARKING_*). Put authorization detail in the Handling Notice, not on every field. |
| **Closers (order)** | optional Classification & Handling Notice → optional Important Notice → Disclaimer (always last, unit color) |
| **Logo** | Thumbnail on the **first** branded embed; attach matching logo file(s) |

### Closing-stack vocabulary

| Title | Use for |
|-------|---------|
| **Important Notice** | Chain of command / conduct only |
| **Classification & Handling Notice** | Restricted document hubs (community marking language -- not USG classification) |
| **Important Information** | Application rules only |
| **Disclaimer** | Always last; title `Disclaimer · Unofficial Community`; pass `color=` for the unit; use `links=True` when the message has URLs, `staff=True` (or `classified=True`) for restricted doc hubs |

Community marking vocabulary: **PUBLIC** / **STAFF** / **CANDIDATE** (roleplay only — not USG classification). Bot usernames and brand rules: [BRAND.md](../docs/BRAND.md).

**Tone:** Public channels stay welcoming and scannable. Staff / candidate channels stay need-to-know -- short heroes, short link notes, one handling closer.

### Channel templates

- **Public info:** hero → about → community links → links disclaimer
- **Internal info:** hero → about → reference docs → Classification & Handling Notice → classified disclaimer
- **Staff documents:** hero → Central Repository → topic sections (Title Case, no numbers) → Classification & Handling Notice → classified disclaimer


### Accessibility

Full guidance: [Accessible Discord channel content](../docs/ACCESSIBILITY.md).

| Rule | Practice |
|------|----------|
| **Color not sole signal** | Name the unit in title/eyebrow/body; sidebar color is decorative |
| **Markings in text** | `c.marking_note("PUBLIC")` / `c.marking_note("STAFF", "…")` |
| **No emoji-only critical info** | Field names/titles need words; validated by `validate_embed_accessibility` |
| **Clear field names** | Expand `LOWCOM`/`MIDCOM`/`ORBAT` on first use (`c.command_band_label`) |

### Discord limits

- ≤ **10 embeds** per webhook message
- Field name ≤ 256 characters; field value ≤ 1024 characters
- Embed description ≤ 4096 characters; embed title ≤ 256 characters
- Total message content across embeds is subject to Discord’s overall payload limits

Use this checklist when editing announcers or YAML copy.

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
python units/ds/chain_of_command.py
```

<!--
=== FILE FOOTER ===
End of file: config/README.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
