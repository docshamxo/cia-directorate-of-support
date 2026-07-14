<p align="center">
  <img src="assets/logos/DS.png" alt="Directorate of Support" width="148">
</p>

<h1 align="center">CIA Directorate of Support</h1>

<p align="center">
  Discord announcer suite for the Directorate of Support (DS) and subordinate offices.<br>
  <em>WE GO AS ONE</em>
</p>

<p align="center">
  <a href="https://github.com/docshamxo/cia-directorate-of-support/actions/workflows/ci.yml"><img src="https://github.com/docshamxo/cia-directorate-of-support/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
</p>

<p align="center">
  <a href="#repository-layout">Layout</a> ·
  <a href="#organization">Organization</a> ·
  <a href="#announcer-catalog">Catalog</a> ·
  <a href="#setup">Setup</a> ·
  <a href="#usage">Usage</a> ·
  <a href="SECURITY.md">Security</a>
</p>

---

## Overview

This repository publishes structured Discord embeds for:

- Chain of command
- Public / office information
- Staff documentation
- Open positions
- Server regulations
- Security Phase Program (OSEC)

Shared organizational copy, roles, ranks, colors, logos, and webhook helpers live in [`common/`](common/). Office-specific announcers live in their own folders, each with a dedicated README.

| Requirement | Version |
|-------------|---------|
| Python | 3.10+ |
| `discord.py` | >= 2.3.0 |
| `python-dotenv` | >= 1.0.0 |

---

## Repository layout

```text
cia-directorate-of-support/
├── README.md                 # This file
├── SECURITY.md               # Webhook / secret handling
├── requirements.txt
├── ruff.toml                 # Lint configuration
├── .env.example              # Webhook variable template (17 keys)
├── run_all.py                # Runs all 17 announcers in order
├── .github/
│   ├── workflows/ci.yml      # CI: Ruff + repository validation
│   ├── dependabot.yml        # Weekly dependency updates
│   └── PULL_REQUEST_TEMPLATE.md
├── tools/
│   ├── README.md
│   └── validate_repo.py      # Catalog / webhook / asset checks
├── assets/
│   ├── README.md
│   ├── logos/                # DS, OSEC, OTE, GRS, ESD
│   └── diagrams/             # Reference org charts
├── common/
│   ├── README.md
│   ├── __init__.py
│   └── cia_common.py         # Shared config + Discord helpers
├── ds/                       # Directorate-level (3 scripts)
├── osec/                     # Office of Security (4 scripts)
├── ote/                      # Office of Training & Education (5 scripts)
├── grs/                      # Global Response Staff (3 scripts)
└── esd/                      # Executive Security Detail (2 scripts)
```

---

## Organization

```text
Directorate of Support (DS)
├── Office of Training & Education (OTE)
└── Office of Security (OSEC)
    ├── Global Response Staff (GRS)
    └── Executive Security Detail (ESD)
```

| Unit | Motto | Folder | Scripts | README |
|------|-------|--------|---------|--------|
| **DS** | WE GO AS ONE | [`ds/`](ds/) | 3 | [ds/README.md](ds/README.md) |
| **OSEC** | PROTECT · DETECT · RESPOND | [`osec/`](osec/) | 4 | [osec/README.md](osec/README.md) |
| **OTE** | SCIENTIA EST LUX LUCIS | [`ote/`](ote/) | 5 | [ote/README.md](ote/README.md) |
| **GRS** | — | [`grs/`](grs/) | 3 | [grs/README.md](grs/README.md) |
| **ESD** | — | [`esd/`](esd/) | 2 | [esd/README.md](esd/README.md) |

Shared library: [`common/`](common/) · Media: [`assets/`](assets/)

---

## Announcer catalog

Complete list of scripts executed by `run_all.py` (17 total), in run order:

| # | Script | Label | Environment variable |
|---|--------|-------|----------------------|
| 1 | [`ds/chain_of_command.py`](ds/chain_of_command.py) | DS Chain of Command | `WEBHOOK_DS_CHAIN_OF_COMMAND` |
| 2 | [`ds/public_information.py`](ds/public_information.py) | DS Public Information | `WEBHOOK_DS_PUBLIC_INFORMATION` |
| 3 | [`ds/server_regulations.py`](ds/server_regulations.py) | Server Regulations | `WEBHOOK_DS_SERVER_REGULATIONS` |
| 4 | [`osec/information.py`](osec/information.py) | OSEC Information | `WEBHOOK_OSEC_INFORMATION` |
| 5 | [`osec/staff_documents.py`](osec/staff_documents.py) | OSEC Staff Documents | `WEBHOOK_OSEC_STAFF_DOCUMENTS` |
| 6 | [`osec/spp_information.py`](osec/spp_information.py) | OSEC Security Phase Program | `WEBHOOK_OSEC_SPP_INFORMATION` |
| 7 | [`osec/open_positions.py`](osec/open_positions.py) | OSEC Open Positions | `WEBHOOK_OSEC_OPEN_POSITIONS` |
| 8 | [`ote/coc.py`](ote/coc.py) | OTE Chain of Command | `WEBHOOK_OTE_COC` |
| 9 | [`ote/public_information.py`](ote/public_information.py) | OTE Public Information | `WEBHOOK_OTE_PUBLIC_INFORMATION` |
| 10 | [`ote/program_overview.py`](ote/program_overview.py) | OTE Program Overview | `WEBHOOK_OTE_PROGRAM_OVERVIEW` |
| 11 | [`ote/staff_documents.py`](ote/staff_documents.py) | OTE Staff Documents | `WEBHOOK_OTE_STAFF_DOCUMENTS` |
| 12 | [`ote/open_positions.py`](ote/open_positions.py) | OTE Open Positions | `WEBHOOK_OTE_OPEN_POSITIONS` |
| 13 | [`grs/coc.py`](grs/coc.py) | GRS Chain of Command | `WEBHOOK_GRS_COC` |
| 14 | [`grs/information.py`](grs/information.py) | GRS Information | `WEBHOOK_GRS_INFORMATION` |
| 15 | [`grs/staff_documents.py`](grs/staff_documents.py) | GRS Staff Documents | `WEBHOOK_GRS_STAFF_DOCUMENTS` |
| 16 | [`esd/coc.py`](esd/coc.py) | ESD Chain of Command | `WEBHOOK_ESD_COC` |
| 17 | [`esd/information.py`](esd/information.py) | ESD Information | `WEBHOOK_ESD_INFORMATION` |

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/docshamxo/cia-directorate-of-support.git
cd cia-directorate-of-support
python -m pip install -r requirements.txt
```

### 2. Configure webhooks

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Fill every `WEBHOOK_*` value in `.env` with the matching Discord channel webhook URL.  
`.env` is gitignored and must never be committed. See [SECURITY.md](SECURITY.md).

### 3. Verify assets

Embed thumbnails load from:

| Key | File |
|-----|------|
| `ds` | [`assets/logos/DS.png`](assets/logos/DS.png) |
| `osec` | [`assets/logos/OSEC.png`](assets/logos/OSEC.png) |
| `ote` | [`assets/logos/OTE.png`](assets/logos/OTE.png) |
| `grs` | [`assets/logos/GRS.png`](assets/logos/GRS.png) |
| `esd` | [`assets/logos/ESD.png`](assets/logos/ESD.png) |

---

## Usage

Run from the repository root.

**Single announcer**

```bash
python ds/chain_of_command.py
python osec/information.py
python ote/coc.py
```

**Full refresh (all 17)**

```bash
python run_all.py
```

Only run `run_all.py` when you intend to update every configured channel.

**Validate repository health**

```bash
python tools/validate_repo.py
```

CI runs the same checks (plus Ruff) on every push and pull request to `main`.

---

## Documentation index

| Document | Description |
|----------|-------------|
| [ds/README.md](ds/README.md) | Directorate scripts |
| [osec/README.md](osec/README.md) | Office of Security scripts |
| [ote/README.md](ote/README.md) | Office of Training & Education scripts |
| [grs/README.md](grs/README.md) | Global Response Staff scripts |
| [esd/README.md](esd/README.md) | Executive Security Detail scripts |
| [common/README.md](common/README.md) | Shared library reference |
| [assets/README.md](assets/README.md) | Logos and diagrams inventory |
| [tools/README.md](tools/README.md) | Validation utilities |
| [SECURITY.md](SECURITY.md) | Secret handling |
| [`.env.example`](.env.example) | Webhook variable template |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | Continuous integration |
