# Office of Security (OSEC)

[← Repository root](../README.md)

Internal security office under the **Directorate of Support (DS)**.  
Motto: **PROTECT · DETECT · RESPOND**

Sub-units: **Global Response Staff (GRS)** · **Executive Security Detail (ESD)**

## Scripts (4)

| Script | Label | Purpose | Environment variable |
|--------|-------|---------|----------------------|
| [`information.py`](information.py) | OSEC Information | Mission and office information | `WEBHOOK_OSEC_INFORMATION` |
| [`staff_documents.py`](staff_documents.py) | OSEC Staff Documents | Staff documentation, certifications, and resources | `WEBHOOK_OSEC_STAFF_DOCUMENTS` |
| [`spp_information.py`](spp_information.py) | OSEC Security Phase Program | Security Phase Program details | `WEBHOOK_OSEC_SPP_INFORMATION` |
| [`open_positions.py`](open_positions.py) | OSEC Open Positions | Recruiting and open billets | `WEBHOOK_OSEC_OPEN_POSITIONS` |

## Run

```bash
# From repository root
python osec/information.py
python osec/staff_documents.py
python osec/spp_information.py
python osec/open_positions.py
```

## Related

| Unit | Path |
|------|------|
| Directorate of Support | [`../ds/`](../ds/) |
| Global Response Staff | [`../grs/`](../grs/) |
| Executive Security Detail | [`../esd/`](../esd/) |
| Shared library | [`../common/`](../common/) |
