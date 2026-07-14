# Global Response Staff (GRS)

Operational security element under **OSEC** — rapid deployment and high-threat site security.

| Script | Channel purpose | Env var |
|--------|-----------------|---------|
| `coc.py` | GRS chain of command | `WEBHOOK_GRS_COC` |
| `information.py` | GRS mission / office information | `WEBHOOK_GRS_INFORMATION` |
| `staff_documents.py` | GRS staff documentation | `WEBHOOK_GRS_STAFF_DOCUMENTS` |

```bash
python grs/coc.py
python grs/information.py
python grs/staff_documents.py
```
