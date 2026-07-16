<!--
=== FILE HEADER ===
Title: README
Path: README.md
Created: 2026-07-14
Created by: docshamxo
Modified:
  - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
  - 2026-07-14 | docshamxo | Point clone URL at docshamxo account.
  - 2026-07-14 | docshamxo | Polish repository presentation and align documentation.
  - 2026-07-14 | docshamxo | Remove copyright and license notices.
  - 2026-07-14 | docshamxo | Add CI, Dependabot, and repository validation tooling.
  - 2026-07-14 | docshamxo | Simplify setup and contributor docs.
  - 2026-07-14 | docshamxo | Document every install, setup, and run command explicitly.
  - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
  - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
  - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
  - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
  - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
=== END FILE HEADER ===
-->

<p align="center">
  <img src="assets/logos/DS.png" alt="Directorate of Support" width="148">
</p>

<h1 align="center">CIA Directorate of Support</h1>

<p align="center">
  Discord announcer scripts for DS, OSEC, OTE, GRS, and ESD.<br>
  <em>WE GO AS ONE</em>
</p>

<p align="center">
  <a href="https://github.com/docshamxo/cia-directorate-of-support/actions/workflows/ci.yml"><img src="https://github.com/docshamxo/cia-directorate-of-support/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI"></a>
</p>

---

## Full setup (follow every step)

Do these steps in order. Do not skip any command.

### Step 1 — Install Git

**Windows**

1. Download Git: https://git-scm.com/download/win
2. Run the installer (default options are fine)
3. Open **PowerShell** or **Command Prompt**
4. Run:

```bash
git --version
```

You should see a version number (for example `git version 2.51.0`).

**macOS**

```bash
xcode-select --install
git --version
```

Or install from https://git-scm.com/download/mac and then run:

```bash
git --version
```

**Linux (Debian / Ubuntu)**

```bash
sudo apt update
sudo apt install -y git
git --version
```

**Linux (Fedora)**

```bash
sudo dnf install -y git
git --version
```

---

### Step 2 — Install Python 3.10 or newer

**Windows**

1. Download Python: https://www.python.org/downloads/
2. Run the installer
3. Check **Add python.exe to PATH**
4. Click **Install Now**
5. Close and reopen PowerShell / Command Prompt
6. Run:

```bash
python --version
py --version
python -m pip --version
```

Any of `python` or `py` working is fine. You need version **3.10** or higher (example: `Python 3.12.0`).

If `python` is not found but `py` works, use `py` in every command below instead of `python`.

**macOS**

```bash
brew install python
python3 --version
python3 -m pip --version
```

On macOS/Linux, use `python3` and `python3 -m pip` in every command below if `python` is not found.

**Linux (Debian / Ubuntu)**

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 --version
python3 -m pip --version
```

**Linux (Fedora)**

```bash
sudo dnf install -y python3 python3-pip
python3 --version
python3 -m pip --version
```

---

### Step 3 — Download this repository

```bash
git clone https://github.com/docshamxo/cia-directorate-of-support.git
```

---

### Step 4 — Enter the project folder

```bash
cd cia-directorate-of-support
```

Confirm you are in the right place:

```bash
pwd
```

Windows PowerShell alternative:

```powershell
Get-Location
```

You should be inside a folder named `cia-directorate-of-support`.

List files:

```bash
ls
```

Windows PowerShell alternative:

```powershell
dir
```

You should see files like `README.md`, `bootstrap.py`, `run_all.py`, `requirements.txt`, and folders like `ds`, `osec`, `ote`, `grs`, `esd`, `common`, `assets`, `tools`.

---

### Step 5 — Upgrade pip

Windows:

```bash
python -m pip install --upgrade pip
```

macOS / Linux:

```bash
python3 -m pip install --upgrade pip
```

---

### Step 6 — Install project packages

Windows:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

macOS / Linux:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -e ".[dev]"
```

This installs the local `common` package plus:

- `discord.py`
- `python-dotenv`
- `PyYAML`
- `ruff` (dev extra)

Alternatively you can install runtime pins only with `pip install -r requirements.txt` and set `PYTHONPATH` to the repo root when running scripts.

---

### Step 7 — Create your private `.env` file

Windows (Command Prompt):

```bash
copy .env.example .env
```

Windows (PowerShell):

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

Confirm it exists:

Windows:

```bash
dir .env
```

macOS / Linux:

```bash
ls -la .env
```

`.env` is private. Never commit it to GitHub.

---

### Step 8 — Add Discord webhook URLs

1. Open `.env` in any text editor (Notepad, VS Code, nano, etc.)
2. For each empty `WEBHOOK_...=` line, paste the Discord webhook URL after the `=`
3. Save the file

Example line after editing:

```env
WEBHOOK_DS_CHAIN_OF_COMMAND=https://discord.com/api/webhooks/1234567890/abcdefghijk
```

How to get a Discord webhook URL:

1. Open Discord
2. Edit the target channel
3. Open **Integrations** → **Webhooks**
4. Create or copy a webhook URL
5. Paste it into the matching key in `.env`

All keys are listed in the [Announcer list](#announcer-list) below and in [`.env.example`](.env.example).

---

### Step 9 — Optional one-command setup next time

After Git and Python are already installed, these three commands do steps 3–7:

Windows:

```bash
git clone https://github.com/docshamxo/cia-directorate-of-support.git
cd cia-directorate-of-support
python bootstrap.py
```

macOS / Linux:

```bash
git clone https://github.com/docshamxo/cia-directorate-of-support.git
cd cia-directorate-of-support
python3 bootstrap.py
```

`bootstrap.py` will:

1. Copy `.env.example` to `.env` if `.env` does not exist
2. Run `python -m pip install -e ".[dev]"`

You must still complete **Step 8** (paste webhook URLs into `.env`) yourself.

---

## Run commands

Run every command from the project root:

```bash
cd cia-directorate-of-support
```

If `python` does not work on your system, use `python3` instead.

### Run one channel

```bash
python ds/chain_of_command.py
python ds/public_information.py
python ds/server_regulations.py
python osec/information.py
python osec/staff_documents.py
python osec/spp_information.py
python osec/open_positions.py
python ote/coc.py
python ote/public_information.py
python ote/program_overview.py
python ote/staff_documents.py
python ote/open_positions.py
python grs/coc.py
python grs/information.py
python grs/staff_documents.py
python esd/coc.py
python esd/information.py
python esd/staff_documents.py
```

### Run every channel

```bash
python run_all.py
```

That runs all 18 announcers in the order shown in the list above.

Useful flags:

```bash
python run_all.py --dry-run          # preview embeds; do not post
python run_all.py --fail-fast        # stop on first failure
python run_all.py --delay 1.5        # seconds between scripts
python run_all.py --no-skip-empty    # error on empty webhook env vars
```

Live runs create **new** Discord messages each time (they do not edit prior posts).

### Preview one channel without posting

```bash
python ds/chain_of_command.py --dry-run
```

### Check the repo after you edit files

```bash
python tools/sync_file_banners.py
python tools/validate_repo.py
```

`sync_file_banners.py` updates the header and footer on every text file (title, path, created date, created by **docshamxo**, modification log, and footer maintainer line).

---

## Update content

| What you want to change | What to edit |
|-------------------------|--------------|
| Names and ranks | [`config/personnel.yaml`](config/personnel.yaml) |
| Mottos, about text, disclaimers | [`config/organization.yaml`](config/organization.yaml) |
| Server regulations prose | [`config/regulations.yaml`](config/regulations.yaml) |
| Colors, bot names, logo filenames | [`config/branding.yaml`](config/branding.yaml) |
| Document / form / Roblox / Discord links | [`config/links.yaml`](config/links.yaml) |
| One Discord channel's embed layout | The matching script in `ds/`, `osec/`, `ote/`, `grs/`, or `esd/` |
| Which Discord channel a script posts to | That script's key inside `.env` |
| A logo image | Same filename in [`assets/logos/`](assets/logos/) |
| Order of `run_all.py` | [`run_all.py`](run_all.py) |

Most day-to-day updates are YAML edits under [`config/`](config/). See [config/README.md](config/README.md) for the YAML guide and the **Discord Embed Style Guide** (hero pattern, link grammar, closer stack, Discord limits).

### Save and check your changes

```bash
python tools/validate_repo.py
```

### Commit and push your changes to GitHub

```bash
git status
git add path/to/changed-file.py
git status
git commit -m "Describe your change here"
git push
```

Prefer explicit paths over `git add .` so `.env` cannot be staged by mistake.

Full contributor steps: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Folders

```text
config/   Editable YAML (names, links, branding, org text, regulations)
ds/       Directorate of Support
osec/     Office of Security
ote/      Office of Training & Education
grs/      Global Response Staff
esd/      Executive Security Detail
common/   Loads config + Discord helpers + announcer runner
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
| [`esd/`](esd/) | 3 | [README](esd/README.md) |

---

## Announcer list

| # | Run command | `.env` key |
|---|-------------|------------|
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
| 18 | `python esd/staff_documents.py` | `WEBHOOK_ESD_STAFF_DOCUMENTS` |

---

## More docs

| Doc | What it covers |
|-----|----------------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Editing, validating, and pushing changes |
| [config/README.md](config/README.md) | YAML config guide |
| [SECURITY.md](SECURITY.md) | Keeping webhooks private |
| [common/README.md](common/README.md) | Shared library / config loader |
| [tools/README.md](tools/README.md) | Validation tool |
| [`.env.example`](.env.example) | Webhook key template |

<!--
=== FILE FOOTER ===
End of file: README.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
