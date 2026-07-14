# === FILE HEADER ===
# Title: Setup
# Path: setup.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Simplify setup and contributor docs.
#   - 2026-07-14 | docshamxo | Document every install, setup, and run command explicitly.
# === END FILE HEADER ===

"""
One-command setup for new contributors.

Usage (from the repository root):
    python setup.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"
ENV_EXAMPLE = ROOT / ".env.example"
REQUIREMENTS = ROOT / "requirements.txt"


def main() -> None:
    print("CIA Directorate of Support — setup\n")

    if not ENV_EXAMPLE.is_file():
        raise SystemExit("Missing .env.example. Are you in the repository root?")

    if ENV_PATH.exists():
        print("1) .env already exists — left unchanged")
    else:
        shutil.copy(ENV_EXAMPLE, ENV_PATH)
        print("1) Created .env from .env.example")

    print("2) Installing Python packages...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS)],
        cwd=ROOT,
    )

    print(
        "\nSetup complete.\n"
        "Next steps (do not skip):\n"
        "  1. Open .env in a text editor\n"
        "  2. Paste each Discord webhook URL after the matching WEBHOOK_...=\n"
        "  3. Save .env\n"
        "  4. Run one channel:  python ds/chain_of_command.py\n"
        "  5. Or run all:       python run_all.py\n"
        "\n"
        "Full step-by-step guide (Git + Python install included): README.md\n"
    )


if __name__ == "__main__":
    main()

# === FILE FOOTER ===
# End of file: setup.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
