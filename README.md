# CIA Directorate of Support

Discord announcer scripts for the **Directorate of Support (DS)** community â€” chain of command, public information, staff documents, open positions, and server regulations.

> Motto: **WE GO AS ONE**

## Structure

```
cia-directorate-of-support/
â”œâ”€â”€ assets/
â”‚   â”œâ”€â”€ logos/          # DS, OSEC, OTE, GRS, ESD logos
â”‚   â””â”€â”€ diagrams/       # Org / relationship diagrams
â”œâ”€â”€ common/             # Shared config, roles, Discord helpers
â”œâ”€â”€ ds/                 # Directorate-level announcements
â”œâ”€â”€ osec/               # Office of Security
â”œâ”€â”€ ote/                # Office of Training & Education
â”œâ”€â”€ grs/                # Global Response Staff
â”œâ”€â”€ esd/                # Executive Security Detail
â”œâ”€â”€ run_all.py          # Run every announcer in order
â”œâ”€â”€ .env.example        # Webhook URL template
â””â”€â”€ requirements.txt
```

Each office folder has its own README describing the scripts it contains.

## Offices

| Office | Role |
|--------|------|
| **DS** | Directorate backbone â€” CoC, public info, server regulations |
| **OSEC** | Internal security â€” information, staff docs, SPP, open positions |
| **OTE** | Officer Training Program â€” CoC, curriculum, staffing |
| **GRS** | Operational security element under OSEC |
| **ESD** | Close protection / HVT security under OSEC |

## Setup

1. **Clone and install**

   ```bash
   git clone https://github.com/docshamxo/cia-directorate-of-support.git
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
