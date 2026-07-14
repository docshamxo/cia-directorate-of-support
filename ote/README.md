# Office of Training & Education (OTE)

[← Repository root](../README.md)

Training office under the **Directorate of Support (DS)**. Operates the Agency Officer Training Program.  
Motto: **SCIENTIA EST LUX LUCIS**

## Scripts (5)

| Script | Label | Purpose | Environment variable |
|--------|-------|---------|----------------------|
| [`coc.py`](coc.py) | OTE Chain of Command | OTE leadership and hierarchy | `WEBHOOK_OTE_COC` |
| [`public_information.py`](public_information.py) | OTE Public Information | Public-facing OTE overview | `WEBHOOK_OTE_PUBLIC_INFORMATION` |
| [`program_overview.py`](program_overview.py) | OTE Program Overview | Officer Training Program overview | `WEBHOOK_OTE_PROGRAM_OVERVIEW` |
| [`staff_documents.py`](staff_documents.py) | OTE Staff Documents | Instructor and staff documentation | `WEBHOOK_OTE_STAFF_DOCUMENTS` |
| [`open_positions.py`](open_positions.py) | OTE Open Positions | Open training and staff roles | `WEBHOOK_OTE_OPEN_POSITIONS` |

## Run

```bash
# From repository root
python ote/coc.py
python ote/public_information.py
python ote/program_overview.py
python ote/staff_documents.py
python ote/open_positions.py
```

## Related

| Unit | Path |
|------|------|
| Directorate of Support | [`../ds/`](../ds/) |
| Shared library | [`../common/`](../common/) |
