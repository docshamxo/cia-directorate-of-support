# === FILE HEADER ===
# Title: Bootstrap
# Path: bootstrap.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial creation
# === END FILE HEADER ===

"""
One-command setup for new contributors.

Usage (from the repository root):
    python bootstrap.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"
ENV_EXAMPLE = ROOT / ".env.example"


def main() -> None:
    print("CIA Directorate of Support — bootstrap\n")

    if not ENV_EXAMPLE.is_file():
        raise SystemExit("Missing .env.example. Are you in the repository root?")

    if ENV_PATH.exists():
        print("1) .env already exists — left unchanged")
    else:
        shutil.copy(ENV_EXAMPLE, ENV_PATH)
        print("1) Created .env from .env.example")

    print("2) Installing package (editable) and dependencies...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
        cwd=ROOT,
    )
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
        cwd=ROOT,
    )

    print(
        "\nSetup complete.\n"
        "Next steps (do not skip):\n"
        "  1. Open .env in a text editor\n"
        "  2. Paste each Discord webhook URL after the matching WEBHOOK_...=\n"
        "  3. Save .env\n"
        "  4. Preview one channel:  python ds/chain_of_command.py --dry-run\n"
        "  5. Or run all (live):    python run_all.py\n"
        "\n"
        "Full step-by-step guide (Git + Python install included): README.md\n"
    )


if __name__ == "__main__":
    main()

# === FILE FOOTER ===
# End of file: bootstrap.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
