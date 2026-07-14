# Global Response Staff (GRS)

[← Repository root](../README.md)

Operational security element under the **Office of Security (OSEC)** — rapid deployment, high-threat site security, and direct-action support.

## Scripts (3)

| Script | Label | Purpose | Environment variable |
|--------|-------|---------|----------------------|
| [`coc.py`](coc.py) | GRS Chain of Command | GRS leadership and hierarchy | `WEBHOOK_GRS_COC` |
| [`information.py`](information.py) | GRS Information | Mission and office information | `WEBHOOK_GRS_INFORMATION` |
| [`staff_documents.py`](staff_documents.py) | GRS Staff Documents | Staff documentation and resources | `WEBHOOK_GRS_STAFF_DOCUMENTS` |

## Run

```bash
# From repository root
python grs/coc.py
python grs/information.py
python grs/staff_documents.py
```

## Related

| Unit | Path |
|------|------|
| Office of Security | [`../osec/`](../osec/) |
| Executive Security Detail | [`../esd/`](../esd/) |
| Shared library | [`../common/`](../common/) |
