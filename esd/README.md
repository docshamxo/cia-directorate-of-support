# Executive Security Detail (ESD)

[← Repository root](../README.md)

Close-protection unit under the **Office of Security (OSEC)** — personal security for High Value Targets (HVTs), senior leadership, and VIPs.

## Scripts (2)

| Script | Label | Purpose | Environment variable |
|--------|-------|---------|----------------------|
| [`coc.py`](coc.py) | ESD Chain of Command | ESD leadership and hierarchy | `WEBHOOK_ESD_COC` |
| [`information.py`](information.py) | ESD Information | Mission and office information | `WEBHOOK_ESD_INFORMATION` |

## Run

```bash
# From repository root
python esd/coc.py
python esd/information.py
```

## Related

| Unit | Path |
|------|------|
| Office of Security | [`../osec/`](../osec/) |
| Global Response Staff | [`../grs/`](../grs/) |
| Shared library | [`../common/`](../common/) |
