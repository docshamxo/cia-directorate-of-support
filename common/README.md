# Common

[← Back to main README](../README.md)

Shared settings used by every announcer.

## Main file

[`cia_common.py`](cia_common.py) — edit this to update:

- mottos and office descriptions
- chain-of-command names / ranks
- Discord bot display names
- logo paths, colors, and embed helpers

## After editing

From the repository root:

```bash
cd cia-directorate-of-support
python tools/validate_repo.py
```

Then run the announcer you care about, for example:

```bash
python ds/chain_of_command.py
```

macOS / Linux if needed:

```bash
python3 tools/validate_repo.py
python3 ds/chain_of_command.py
```
