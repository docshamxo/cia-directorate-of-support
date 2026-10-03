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
| [`branding.yaml`](branding.yaml) | Colors, bot usernames, logos, studio / property notice (Invictus Studios) |
| [`organization.yaml`](organization.yaml) | Mottos, about text, offices, disclaimers, affiliation / property notices |
| [`classification.yaml`](classification.yaml) | OIG Levels vocabulary (LEVEL 1–X) for embed closers |
| [`personnel.yaml`](personnel.yaml) | Chain-of-command names and ranks (high command and small command teams only) |
| [`links.yaml`](links.yaml) | Public document and Roblox URLs (staff Drive / ORBAT via local overlay; applicant forms via `.env`) |
| [`links.staff.example.yaml`](links.staff.example.yaml) | Example staff Drive / ORBAT overlay (copy → `links.staff.local.yaml`) |
| [`regulations.yaml`](regulations.yaml) | Server regulations prose |

## Discord Embed Style Guide

Discord supports markdown emphasis only — no custom fonts. Typography means `**bold**`, `*italic*`, title casing, and embed chrome (color bar, thumbnail).

### Design contract

| Element | Rule |
|---------|------|
| **Hero** | ALL CAPS `title=` + bold `**{Unit}**` + one short supporting sentence. Rules channels use the DIRECTORATE OF SUPPORT stack (office + Community Server Regulations + one unofficial-RP line). |
| **Body section titles** | Title Case |
| **Links** | `[CIA {UNIT} \| {Document}](url)` with optional italic note; community groups: `CIA \| {Group}` |
| **Link notes** | Prefer `Classification: LEVEL 1.` / `LEVEL 2.` (`c.marking_note`). Prefer emoji link buttons for hub URLs. |
| **Closers (order)** | optional Important Notice → **Classification** LEVEL block. No Disclaimer on live channels (OIG-aligned). |
| **Logo** | Thumbnail on the **first** branded embed; attach matching logo file(s) |

### Closing-stack vocabulary

| Title | Use for |
|-------|---------|
| **Important Notice** | Chain of command / conduct only |
| **Classification** | Final LEVEL block (`append_classification_block`) — LEVEL 1 public / LEVEL 2 staff |
| **Important Information** | Application rules only |

Community classification vocabulary: **LEVEL 1** … **LEVEL X** (roleplay only — not USG; see `classification.yaml`). Property notice (Invictus Studios) lives in config/docs only — not Discord footers. Bot usernames: [BRAND.md](../docs/BRAND.md).

**Tone:** Public channels stay welcoming and scannable. Staff channels stay need-to-know — short heroes, Drive/handbook buttons, one Classification closer.

### Channel templates

- **Public info:** hero → about → community links (+ buttons) → Classification LEVEL 1
- **Internal info:** hero → about → reference docs → Classification LEVEL 2
- **Staff documents:** hero → Central Repository → topic sections → Classification LEVEL 2 (+ Drive/handbook buttons)
- **Rules:** regulations → Governing Policies → Classification LEVEL 1 (+ TOS/CAC buttons)


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
