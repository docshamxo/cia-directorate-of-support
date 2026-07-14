# Tools

[← Back to main README](../README.md)

```bash
python tools/validate_repo.py
```

Checks that:

- every script in `run_all.py` exists
- webhook keys match `.env.example`
- logos are present
- Python files compile

Run this after you change scripts or env keys.
