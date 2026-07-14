# Tools

[← Back to main README](../README.md)

## Run the validator

From the repository root:

```bash
cd cia-directorate-of-support
python tools/validate_repo.py
```

macOS / Linux if needed:

```bash
python3 tools/validate_repo.py
```

## What it checks

- every script listed in `run_all.py` exists
- webhook keys in code match `.env.example`
- logo files are present
- Python files compile

Run this after any script, catalog, or webhook-key change.
