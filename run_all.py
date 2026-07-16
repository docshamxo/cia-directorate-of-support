# === FILE HEADER ===
# Title: Run All
# Path: run_all.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Note prior-message cleanup on live announcer runs.
# === END FILE HEADER ===

"""
Run all CIA Directorate of Support Discord announcer scripts.

Usage (from the repository root):
    python run_all.py
    python run_all.py --dry-run
    python run_all.py --fail-fast
    python run_all.py --delay 1.5
"""

from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent

SCRIPTS: tuple[tuple[str, str, str], ...] = (
    ("ds/chain_of_command.py", "DS Chain of Command", "WEBHOOK_DS_CHAIN_OF_COMMAND"),
    ("ds/public_information.py", "DS Public Information", "WEBHOOK_DS_PUBLIC_INFORMATION"),
    ("ds/server_regulations.py", "Server Regulations", "WEBHOOK_DS_SERVER_REGULATIONS"),
    ("osec/information.py", "OSEC Information", "WEBHOOK_OSEC_INFORMATION"),
    ("osec/staff_documents.py", "OSEC Staff Documents", "WEBHOOK_OSEC_STAFF_DOCUMENTS"),
    ("osec/spp_information.py", "OSEC Security Phase Program", "WEBHOOK_OSEC_SPP_INFORMATION"),
    ("osec/open_positions.py", "OSEC Open Positions", "WEBHOOK_OSEC_OPEN_POSITIONS"),
    ("ote/coc.py", "OTE Chain of Command", "WEBHOOK_OTE_COC"),
    ("ote/public_information.py", "OTE Public Information", "WEBHOOK_OTE_PUBLIC_INFORMATION"),
    ("ote/program_overview.py", "OTE Program Overview", "WEBHOOK_OTE_PROGRAM_OVERVIEW"),
    ("ote/staff_documents.py", "OTE Staff Documents", "WEBHOOK_OTE_STAFF_DOCUMENTS"),
    ("ote/open_positions.py", "OTE Open Positions", "WEBHOOK_OTE_OPEN_POSITIONS"),
    ("grs/coc.py", "GRS Chain of Command", "WEBHOOK_GRS_COC"),
    ("grs/information.py", "GRS Information", "WEBHOOK_GRS_INFORMATION"),
    ("grs/staff_documents.py", "GRS Staff Documents", "WEBHOOK_GRS_STAFF_DOCUMENTS"),
    ("esd/coc.py", "ESD Chain of Command", "WEBHOOK_ESD_COC"),
    ("esd/information.py", "ESD Information", "WEBHOOK_ESD_INFORMATION"),
    ("esd/staff_documents.py", "ESD Staff Documents", "WEBHOOK_ESD_STAFF_DOCUMENTS"),
)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run all CIA DS Discord announcers.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build embeds and print a preview without posting to Discord.",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop on the first script failure (default: continue and summarize).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Seconds to wait between scripts (default: 1.0). Use 0 to disable.",
    )
    parser.add_argument(
        "--no-skip-empty",
        action="store_true",
        help="Fail when a webhook env var is empty instead of skipping.",
    )
    return parser.parse_args(argv)


def run_all(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    load_dotenv(REPO_ROOT / ".env")
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    env = os.environ.copy()
    pythonpath = str(REPO_ROOT)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = pythonpath if not existing else pythonpath + os.pathsep + existing
    if args.dry_run:
        env["CIA_DRY_RUN"] = "1"
    if not args.no_skip_empty:
        env["CIA_SKIP_EMPTY_WEBHOOKS"] = "1"

    mode = "dry-run" if args.dry_run else "live"
    print(f"Running {len(SCRIPTS)} announcer scripts from {REPO_ROOT} ({mode})\n")
    print(
        "Note: live runs delete previously recorded webhook message(s) for each "
        "channel (see .webhook_messages.json), then post the new embed(s).\n"
        "Messages posted before this cleanup feature (or not recorded) are left alone.\n"
    )

    succeeded: list[str] = []
    skipped: list[str] = []
    failed: list[tuple[str, str]] = []

    for index, (relative, label, webhook_key) in enumerate(SCRIPTS):
        path = REPO_ROOT / relative
        if not path.exists():
            failed.append((label, f"Missing script: {path}"))
            if args.fail_fast:
                break
            continue

        webhook_value = env.get(webhook_key, "").strip()
        if not args.dry_run and not webhook_value and not args.no_skip_empty:
            print(f"skip {label} ({relative}) — empty {webhook_key}")
            skipped.append(label)
            continue

        print(f"-> {label} ({relative})")
        result = subprocess.run(
            [sys.executable, str(path)],
            cwd=REPO_ROOT,
            env=env,
            check=False,
        )
        if result.returncode == 0:
            succeeded.append(label)
        else:
            failed.append((label, f"exit code {result.returncode}"))
            if args.fail_fast:
                break

        if args.delay > 0 and index < len(SCRIPTS) - 1:
            time.sleep(args.delay)
        print()

    print("-- Summary --")
    print(f"Succeeded: {len(succeeded)}")
    print(f"Skipped:   {len(skipped)}")
    print(f"Failed:    {len(failed)}")
    if skipped:
        print("Skipped scripts:")
        for label in skipped:
            print(f"  - {label}")
    if failed:
        print("Failed scripts:")
        for label, reason in failed:
            print(f"  - {label}: {reason}")
        return 1

    print("All runnable scripts completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_all())

# === FILE FOOTER ===
# End of file: run_all.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
