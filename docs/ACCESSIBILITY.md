<!--
=== FILE HEADER ===
Title: Accessibility
Path: docs/ACCESSIBILITY.md
Created: 2026-07-17
Created by: docshamxo
Modified:
  - 2026-07-17 | docshamxo | Inclusive design rules for Discord channel embeds.
=== END FILE HEADER ===
-->

# Accessible Discord channel content

[← Back to main README](../README.md) · [Embed style guide](../config/README.md#discord-embed-style-guide)

Discord announces **titles, descriptions, and field names/values** to screen readers. Embed **sidebar color**, thumbnails, and emoji reactions are weak or silent signals. Write every channel so meaning survives without color or emoji.

## Rules (must)

1. **Color is never the only signal.** Unit colors (`COLOR_DS`, `COLOR_GRS`, …) are decorative. Always name the unit in the hero eyebrow, title, or body. DS / OSEC / OTE currently share the same blue — text is the only way to tell them apart.
2. **Markings are words.** Use `c.marking_note("PUBLIC")` / `c.marking_note("STAFF", "…")` (or equivalent prose). Do not imply sensitivity with color alone.
3. **No emoji-only critical info.** Titles, field names, and field values must include letters or digits. Emoji may decorate; they must not carry the only meaning. Runtime check: `validate_embed_accessibility` (runs inside `validate_embed_limits`).
4. **Expand abbreviations on first use.** Prefer `c.command_band_label("LOWCOM")` → `Lower Command (LOWCOM)`, and `Order of Battle (ORBAT)` over bare `ORBAT`.
5. **Field names must stand alone.** A field name should make sense when read aloud without seeing the link label or color bar (e.g. `Code of Agency Conduct`, not only `Conduct`).

## Helpers

```python
from common import cia_common as c

c.command_band_label("MIDCOM")           # Middle Command (MIDCOM)
c.marking_note("STAFF", "Authorized OSEC staff only.")
c.has_text_signal("✅")                  # False
c.validate_embed_accessibility(embeds)   # also called from validate_embed_limits
```

## Channel author checklist

- [ ] Hero uses `hero_embed` / `chain_intro_embed` (unit named in eyebrow)
- [ ] Body titles name the topic in plain Title Case words
- [ ] Link fields use expanded names + `marking_note` when sensitivity matters
- [ ] Closers keep explicit titles: Classification & Handling Notice / Important Notice / Disclaimer
- [ ] Dry-run preview still readable if you ignore color: `python path/to/script.py --dry-run`

## Out of scope

Bot ✅ reactions after a successful post are operational status for moderators, not channel content. Do not rely on reactions to communicate policy to members.

<!--
=== FILE FOOTER ===
End of file: docs/ACCESSIBILITY.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
