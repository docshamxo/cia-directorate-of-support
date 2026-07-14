<p align="center">
  <img src="assets/logos/DS.png" alt="Directorate of Support" width="148">
</p>

<h1 align="center">CIA Directorate of Support</h1>

<p align="center">
  Discord announcer scripts for DS, OSEC, OTE, GRS, and ESD.<br>
  <em>WE GO AS ONE</em>
</p>

<p align="center">
  <a href="https://github.com/docshamxo/cia-directorate-of-support/actions/workflows/ci.yml"><img src="https://github.com/docshamxo/cia-directorate-of-support/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
</p>

---

## Quick start

You need **Python 3.10+**.

```bash
git clone https://github.com/docshamxo/cia-directorate-of-support.git
cd cia-directorate-of-support
python setup.py
```

`setup.py` installs dependencies and creates a local `.env` file.

1. Open `.env`
2. Paste each Discord webhook URL next to the matching `WEBHOOK_...` key
3. Save the file

Do **not** commit `.env`.

---

## Run

Always run commands from the repository root.

**One channel**

```bash
python ds/chain_of_command.py
```

**All channels (17)**

```bash
python run_all.py
```

More examples:

```bash
python osec/information.py
python ote/coc.py
python grs/staff_documents.py
python esd/information.py
```

Each office folder has its own README with every script listed.

---

## Update content

| Task | File / folder |
|------|----------------|
| Change names, ranks, mottos, org blurbs | [`common/cia_common.py`](common/cia_common.py) |
| Change one channel's embeds | Script in `ds/`, `osec/`, `ote/`, `grs/`, or `esd/` |
| Point a script at a different Discord channel | Edit that key in `.env` |
| Replace a logo | Same filename in [`assets/logos/`](assets/logos/) |

After edits:

```bash
python tools/validate_repo.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for adding new announcers.

---

## Folders

```text
ds/       Directorate of Support
osec/     Office of Security
ote/      Office of Training & Education
grs/      Global Response Staff
esd/      Executive Security Detail
common/   Shared text, roles, Discord helpers
assets/   Logos and diagrams
tools/    Validation helpers
```

```text
Directorate of Support (DS)
├── Office of Training & Education (OTE)
└── Office of Security (OSEC)
    ├── Global Response Staff (GRS)
    └── Executive Security Detail (ESD)
```

| Folder | Scripts | Guide |
|--------|---------|-------|
| [`ds/`](ds/) | 3 | [README](ds/README.md) |
| [`osec/`](osec/) | 4 | [README](osec/README.md) |
| [`ote/`](ote/) | 5 | [README](ote/README.md) |
| [`grs/`](grs/) | 3 | [README](grs/README.md) |
| [`esd/`](esd/) | 2 | [README](esd/README.md) |

---

## Announcer list

Scripts run by `python run_all.py`, in order:

| # | Command | `.env` key |
|---|---------|------------|
| 1 | `python ds/chain_of_command.py` | `WEBHOOK_DS_CHAIN_OF_COMMAND` |
| 2 | `python ds/public_information.py` | `WEBHOOK_DS_PUBLIC_INFORMATION` |
| 3 | `python ds/server_regulations.py` | `WEBHOOK_DS_SERVER_REGULATIONS` |
| 4 | `python osec/information.py` | `WEBHOOK_OSEC_INFORMATION` |
| 5 | `python osec/staff_documents.py` | `WEBHOOK_OSEC_STAFF_DOCUMENTS` |
| 6 | `python osec/spp_information.py` | `WEBHOOK_OSEC_SPP_INFORMATION` |
| 7 | `python osec/open_positions.py` | `WEBHOOK_OSEC_OPEN_POSITIONS` |
| 8 | `python ote/coc.py` | `WEBHOOK_OTE_COC` |
| 9 | `python ote/public_information.py` | `WEBHOOK_OTE_PUBLIC_INFORMATION` |
| 10 | `python ote/program_overview.py` | `WEBHOOK_OTE_PROGRAM_OVERVIEW` |
| 11 | `python ote/staff_documents.py` | `WEBHOOK_OTE_STAFF_DOCUMENTS` |
| 12 | `python ote/open_positions.py` | `WEBHOOK_OTE_OPEN_POSITIONS` |
| 13 | `python grs/coc.py` | `WEBHOOK_GRS_COC` |
| 14 | `python grs/information.py` | `WEBHOOK_GRS_INFORMATION` |
| 15 | `python grs/staff_documents.py` | `WEBHOOK_GRS_STAFF_DOCUMENTS` |
| 16 | `python esd/coc.py` | `WEBHOOK_ESD_COC` |
| 17 | `python esd/information.py` | `WEBHOOK_ESD_INFORMATION` |

---

## More docs

| Doc | What it covers |
|-----|----------------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Editing and adding scripts |
| [SECURITY.md](SECURITY.md) | Keeping webhooks private |
| [common/README.md](common/README.md) | Shared library |
| [tools/README.md](tools/README.md) | Validation tool |
| [`.env.example`](.env.example) | Webhook key template |
