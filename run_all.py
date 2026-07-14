# === FILE HEADER ===
# Title: Run All
# Path: run_all.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
# === END FILE HEADER ===

"""
Run all CIA Directorate of Support Discord announcer scripts.

Usage (from the repository root):
    python run_all.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

SCRIPTS: tuple[tuple[str, str], ...] = (
    ("ds/chain_of_command.py", "DS Chain of Command"),
    ("ds/public_information.py", "DS Public Information"),
    ("ds/server_regulations.py", "Server Regulations"),
    ("osec/information.py", "OSEC Information"),
    ("osec/staff_documents.py", "OSEC Staff Documents"),
    ("osec/spp_information.py", "OSEC Security Phase Program"),
    ("osec/open_positions.py", "OSEC Open Positions"),
    ("ote/coc.py", "OTE Chain of Command"),
    ("ote/public_information.py", "OTE Public Information"),
    ("ote/program_overview.py", "OTE Program Overview"),
    ("ote/staff_documents.py", "OTE Staff Documents"),
    ("ote/open_positions.py", "OTE Open Positions"),
    ("grs/coc.py", "GRS Chain of Command"),
    ("grs/information.py", "GRS Information"),
    ("grs/staff_documents.py", "GRS Staff Documents"),
    ("esd/coc.py", "ESD Chain of Command"),
    ("esd/information.py", "ESD Information"),
)


def run_all() -> None:
    print(f"Running {len(SCRIPTS)} announcer scripts from {REPO_ROOT}\n")

    for relative, label in SCRIPTS:
        path = REPO_ROOT / relative
        if not path.exists():
            raise FileNotFoundError(f"Missing script: {path}")

        print(f"→ {label} ({relative})")
        subprocess.run(
            [sys.executable, str(path)],
            cwd=REPO_ROOT,
            check=True,
        )
        print()

    print("All scripts completed successfully.")


if __name__ == "__main__":
    run_all()

# === FILE FOOTER ===
# End of file: run_all.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
