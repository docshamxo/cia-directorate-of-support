# === FILE HEADER ===
# Title: Reset Webhook State
# Path: tools/reset_webhook_state.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Empty-channel / mid-batch recovery helper for message ID state.
# === END FILE HEADER ===

"""Reset local webhook message ID state for empty-channel recovery.

Does not call Discord. Only edits gitignored ``.webhook_messages.json``.

Usage (from repository root):
    python tools/reset_webhook_state.py --list
    python tools/reset_webhook_state.py --key WEBHOOK_DS_PUBLIC_INFORMATION
    python tools/reset_webhook_state.py --all --yes
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common import cia_common as c  # noqa: E402
from common.exit_codes import CRITICAL, OK, WARNING  # noqa: E402


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reset .webhook_messages.json keys for empty-channel recovery."
    )
    parser.add_argument("--list", action="store_true", help="List tracked WEBHOOK_* keys.")
    parser.add_argument(
        "--key",
        action="append",
        default=[],
        metavar="WEBHOOK_*",
        help="Clear one webhook key (repeatable).",
    )
    parser.add_argument("--all", action="store_true", help="Clear entire local message ID state.")
    parser.add_argument("--yes", action="store_true", help="Required with --all to confirm wipe.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    if args.list:
        state = c.load_webhook_message_state()
        if not state:
            print("No tracked webhook message IDs.")
            return OK
        print(f"Tracked keys in {c.WEBHOOK_MESSAGES_PATH.name}:")
        for key in sorted(state):
            print(f"  {key}: {len(state[key])} id(s)")
        return OK

    if args.all:
        if not args.yes:
            print("Refusing --all without --yes (would wipe all tracked message IDs).")
            return WARNING
        removed = c.clear_webhook_message_state()
        print(f"Cleared all webhook message state ({removed} key(s)).")
        print("Next live send will post without deleting prior tracked messages.")
        return OK

    if not args.key:
        print("Specify --list, --key WEBHOOK_..., or --all --yes")
        return WARNING

    cleared = 0
    missing: list[str] = []
    for key in args.key:
        key = key.strip()
        if not key.startswith("WEBHOOK_"):
            print(f"Invalid key (expected WEBHOOK_*): {key}")
            return CRITICAL
        if c.clear_webhook_message_state(key):
            print(f"Cleared state for {key}")
            cleared += 1
        else:
            missing.append(key)

    if missing:
        print("Not present in state (already clear): " + ", ".join(missing))
    if cleared == 0 and missing:
        return WARNING
    print(
        "Empty-channel recovery: re-run the announcer once. "
        "Post-then-delete only removes IDs that were still tracked."
    )
    return OK


if __name__ == "__main__":
    raise SystemExit(main())

# === FILE FOOTER ===
# End of file: tools/reset_webhook_state.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
