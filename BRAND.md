<!--
=== FILE HEADER ===
Title: Brand
Path: BRAND.md
Created: 2026-07-17
Created by: docshamxo
Modified:
  - 2026-07-17 | docshamxo | Brand use, bot naming, and non-affiliation guidance.
=== END FILE HEADER ===
-->

# Brand & trademark guidance

This repository powers Discord announcers for an **unofficial Roblox community roleplay**. Keep fiction usable; never present the project as an official USG/CIA product.

Legal terms: [LICENSE](LICENSE) (MIT + Brand Use and Trademark Notice).

## Non-affiliation (required)

Always keep a clear non-affiliation banner in:

- README hero subtitle
- Discord disclaimer closers (`config/organization.yaml` → `copy.disclaimer*`)
- SECURITY / CONTRIBUTING affiliation lines

Required meaning (wording may vary): **unofficial community**, **not affiliated with** the United States Government or the Central Intelligence Agency, and community markings are **roleplay vocabulary only**.

## Bot / webhook display names

Edit [`config/branding.yaml`](config/branding.yaml) `bots:`.

| Rule | Guidance |
|------|----------|
| Include a community marker | Every name must contain `Community` or `(RP)` |
| Prefer short office tags | Example: `DS Community (RP) · OSEC` |
| Avoid official-looking sole names | Do **not** use bare `CIA \| Office of …` as the webhook username |
| Discord limit | Keep names ≤ 80 characters |

Default pattern used in this repo:

```text
DS Community (RP) · {OfficeTag}
```

In-fiction office names in embed **body** copy are fine. The **webhook username** is what Discord shows as the speaker — that is where impersonation risk is highest.

## Hero eyebrows

Use `agency_eyebrow()` / `hero_embed()` — they must frame the unit as **unofficial community RP**, not as a bare “Central Intelligence Agency” banner.

## Link labels

Prefer community-framed link text (example: `DS Community | OSEC`) over labels that read like an official agency hyperlink (`CIA | Office of Security`). Roblox group titles outside this repo are uncontrolled; labels inside embeds are ours to keep clear.

## What not to change for “brand purity”

- In-fiction rank titles in `personnel.yaml` (RP ORBAT)
- Community mottos and office about-text (fiction flavor)
- Marking vocabulary **PUBLIC** / **STAFF** / **CANDIDATE** (keep; do not invent USG markings)

## Checklist before shipping brand edits

```bash
python tools/validate_repo.py
pytest -q
python run_all.py --dry-run --delay 0
```

Confirm bot names still pass validation (community / RP marker required).

<!--
=== FILE FOOTER ===
End of file: BRAND.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
