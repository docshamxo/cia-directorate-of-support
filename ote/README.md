# Office of Training & Education (OTE)

Runs the Agency Officer Training Program. Motto: **SCIENTIA EST LUX LUCIS**

| Script | Channel purpose | Env var |
|--------|-----------------|---------|
| `coc.py` | OTE chain of command | `WEBHOOK_OTE_COC` |
| `public_information.py` | Public OTE overview | `WEBHOOK_OTE_PUBLIC_INFORMATION` |
| `program_overview.py` | Officer Training Program overview | `WEBHOOK_OTE_PROGRAM_OVERVIEW` |
| `staff_documents.py` | Staff / instructor documentation | `WEBHOOK_OTE_STAFF_DOCUMENTS` |
| `open_positions.py` | Open training / staff roles | `WEBHOOK_OTE_OPEN_POSITIONS` |

```bash
python ote/coc.py
python ote/public_information.py
python ote/program_overview.py
python ote/staff_documents.py
python ote/open_positions.py
```
