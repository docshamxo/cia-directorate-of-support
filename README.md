# CIA Directorate of Support

Discord announcer scripts for the **Directorate of Support (DS)** community — chain of command, public information, staff documents, open positions, and server regulations.

> Motto: **WE GO AS ONE**

## Structure

```
cia-directorate-of-support/
├── assets/
│   ├── logos/          # DS, OSEC, OTE, GRS, ESD logos
│   └── diagrams/       # Org / relationship diagrams
├── common/             # Shared config, roles, Discord helpers
├── ds/                 # Directorate-level announcements
├── osec/               # Office of Security
├── ote/                # Office of Training & Education
├── grs/                # Global Response Staff
├── esd/                # Executive Security Detail
├── run_all.py          # Run every announcer in order
├── .env.example        # Webhook URL template
└── requirements.txt
```

Each office folder has its own README describing the scripts it contains.

## Offices

| Office | Role |
|--------|------|
| **DS** | Directorate backbone — CoC, public info, server regulations |
| **OSEC** | Internal security — information, staff docs, SPP, open positions |
| **OTE** | Officer Training Program — CoC, curriculum, staffing |
| **GRS** | Operational security element under OSEC |
| **ESD** | Close protection / HVT security under OSEC |

## Setup

1. **Clone and install**

   ```bash
   git clone https://github.com/shameerrao/cia-directorate-of-support.git
   cd cia-directorate-of-support
   python -m pip install -r requirements.txt
   ```

2. **Configure webhooks**

   ```bash
   copy .env.example .env   # Windows
   # cp .env.example .env   # macOS / Linux
   ```

   Paste each Discord webhook URL into `.env`. Never commit `.env`.

3. **Run a single announcer**

   ```bash
   python ds/chain_of_command.py
   python osec/information.py
   ```

4. **Run everything**

   ```bash
   python run_all.py
   ```

   Only run `run_all.py` when you intend to refresh every channel.

## Security notes

- Discord webhook URLs are secrets. They live in `.env` (gitignored).
- Rotate any webhook that was previously hard-coded in shared copies of this project.
- Treat staff-document announcers as higher sensitivity than public channels.

## Dependencies

- Python 3.10+
- `discord.py` (SyncWebhook + embeds)
- `python-dotenv` (loads `.env`)
