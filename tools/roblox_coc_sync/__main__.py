# === FILE HEADER ===
# Title: Roblox CoC Sync CLI
# Path: tools/roblox_coc_sync/__main__.py
# Created: 2026-09-28
# Created by: docshamxo
# Modified:
#   - 2026-09-28 | docshamxo | CLI: once / loop / dry-run.
# === END FILE HEADER ===

"""python -m tools.roblox_coc_sync [--once] [--dry-run] [--loop]"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure repo root is on sys.path when invoked as a script.
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from dotenv import load_dotenv

from tools.roblox_coc_sync.sync import SyncSkip, configure_logging, run_loop, run_once


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Sync Roblox group ranks into the DS Chain of Command webhook message.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single sync and exit (default when --loop is not set).",
    )
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Run forever every interval_minutes (default 15).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Pull/map and preview embeds; do not edit Discord.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to roblox_coc_sync.yaml (default: config/ or example).",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    load_dotenv(_REPO_ROOT / ".env")
    configure_logging(verbose=args.verbose)

    once = args.once or not args.loop
    try:
        if once and not args.loop:
            run_once(config_path=args.config, dry_run=args.dry_run or None)
        else:
            run_loop(
                config_path=args.config,
                dry_run=args.dry_run or None,
                once=False,
            )
    except SyncSkip as exc:
        print(f"SKIP: {exc}", file=sys.stderr)
        return 10
    except FileNotFoundError as exc:
        print(f"CONFIG: {exc}", file=sys.stderr)
        return 20
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# === FILE FOOTER ===
# End of file: tools/roblox_coc_sync/__main__.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
