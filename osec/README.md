# Office of Security (OSEC)

Internal security office under DS. Motto: **PROTECT · DETECT · RESPOND**

| Script | Channel purpose | Env var |
|--------|-----------------|---------|
| `information.py` | OSEC mission / public office info | `WEBHOOK_OSEC_INFORMATION` |
| `staff_documents.py` | Staff docs, certifications, resources | `WEBHOOK_OSEC_STAFF_DOCUMENTS` |
| `spp_information.py` | Security Phase Program details | `WEBHOOK_OSEC_SPP_INFORMATION` |
| `open_positions.py` | Recruiting / open billets | `WEBHOOK_OSEC_OPEN_POSITIONS` |

Sub-units: **GRS**, **ESD** (see sibling folders).

```bash
python osec/information.py
python osec/staff_documents.py
python osec/spp_information.py
python osec/open_positions.py
```
