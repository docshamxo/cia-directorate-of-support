<!--
=== FILE HEADER ===
Title: Brand
Path: docs/BRAND.md
Created: 2026-07-17
Created by: docshamxo
Modified:
  - 2026-07-17 | docshamxo | Brand use, bot naming, and non-affiliation guidance.
  - 2026-09-08 | docshamxo | CIA {Office} Bot webhook display names.
=== END FILE HEADER ===
-->

# Brand & trademark guidance

This repository powers Discord announcers for an **unofficial Roblox community roleplay**. Keep fiction usable; never present the project as an official USG/CIA product.

Legal terms: [LICENSE](../LICENSE) (MIT + Brand Use and Trademark Notice).

## Non-affiliation (required)

Always keep a clear non-affiliation banner in:

- README hero subtitle
- OTE and OSEC **Rules** Discord channels (regulations hero + one Disclaimer closer)
- SECURITY / CONTRIBUTING affiliation lines

Required meaning (wording may vary): **community project**, **not affiliated with** the United States Government or the Central Intelligence Agency, and community markings are **roleplay vocabulary only**.

On Discord, do **not** repeat the Disclaimer embed on every channel. It belongs **once** on each of the OTE and OSEC Rules posts only. Other channels use a bold unit hero line without restating the full community disclaimer.

## Bot / webhook display names

Edit [`config/branding.yaml`](../config/branding.yaml) `bots:`.

| Rule | Guidance |
|------|----------|
| Pattern | `CIA {Office full name} Bot` |
| DS | `CIA Directorate of Support Bot` |
| OSEC | `CIA Office of Security Bot` |
| OTE | `CIA Office of Training & Education Bot` |
| GRS | `CIA Global Response Staff Bot` |
| ESD | `CIA Executive Security Detail Bot` |
| Avoid | Bare `CIA \| …` pipe-style names |
| Discord limit | Keep names ≤ 80 characters |

Default pattern:

```text
CIA {Office} Bot
```

In-fiction office names in embed **body** copy are fine. Embeds and Rules closers still carry non-affiliation notices.

## Hero eyebrows

Use `hero_embed()` / `chain_intro_embed()` — bold **unit** line under an ALL CAPS title (not a bare “Central Intelligence Agency” banner). Rules channels use the dedicated regulations hero stack instead.

## Link labels

Use `CIA DS | {name}` (via `community_link_label()`). Prefer that over bare `CIA | …` pipe labels. Roblox group titles outside this repo are uncontrolled; labels inside embeds are ours to keep clear.

## What not to change for “brand purity”

- In-fiction rank titles in `personnel.yaml` (RP ORBAT)
- Community mottos and office about-text (fiction flavor)
- Marking vocabulary **PUBLIC** / **STAFF** / **CANDIDATE** (keep; do not invent USG markings)

## Checklist before shipping brand edits

```bash
python tools/validate_repo.py
pytest -q
python tools/run_all.py --dry-run --delay 0
```

Confirm bot names still pass validation (`CIA … Bot` pattern; no `CIA |`).

<!--
=== FILE FOOTER ===
End of file: docs/BRAND.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
