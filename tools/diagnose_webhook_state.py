# === FILE HEADER ===
# Title: Diagnose Webhook State
# Path: tools/diagnose_webhook_state.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Diagnostic tool for webhook state, duplicates, and bot token.
# === END FILE HEADER ===

"""
Diagnose local webhook message state and .env webhook configuration.

Run from repository root:
    python tools/diagnose_webhook_state.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common import cia_common as c  # noqa: E402
from common.manifest import ANNOUNCERS  # noqa: E402


def _load_state() -> dict[str, list[int]]:
    path = c.WEBHOOK_MESSAGES_PATH
    if not path.is_file():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(raw, dict):
        return {}
    state: dict[str, list[int]] = {}
    for key, value in raw.items():
        if not isinstance(key, str):
            continue
        if isinstance(value, list):
            ids: list[int] = []
            for item in value:
                try:
                    ids.append(int(item))
                except (TypeError, ValueError):
                    continue
            state[key] = ids
        elif isinstance(value, (int, str)):
            try:
                state[key] = [int(value)]
            except (TypeError, ValueError):
                continue
    return state


def _mask_url(value: str) -> str:
    try:
        return c.mask_webhook_url(value)
    except Exception:
        return "(invalid URL)"


def main() -> int:
    load_dotenv(ROOT / ".env")
    env = dict(os.environ)
    state = _load_state()

    print(f"Diagnosing webhook state at {ROOT}\n")

    token = env.get(c.BOT_TOKEN_ENV, "").strip()
    if token:
        print(f"{c.BOT_TOKEN_ENV}: set (length {len(token)})")
    else:
        print(
            f"{c.BOT_TOKEN_ENV}: NOT SET - live runs will fail unless --allow-skip-reaction is used"
        )
    print()

    duplicates = c.find_duplicate_webhook_keys(env)
    if duplicates:
        print("Duplicate webhook URLs (same Discord webhook ID, multiple WEBHOOK_* keys):")
        for webhook_id, keys in sorted(duplicates.items()):
            print(f"  ID {webhook_id}:")
            for key in keys:
                url = env.get(key, "").strip()
                print(f"    {key} -> {_mask_url(url)}")
            sibling_note = "purge clears ALL sibling recorded IDs together"
            print(f"    ({sibling_note})")
        print()
    else:
        print("Duplicate webhook URLs: none detected among set WEBHOOK_* keys.\n")

    print("Announcer catalog vs .env:")
    for relative, label, webhook_key in ANNOUNCERS:
        url = env.get(webhook_key, "").strip()
        ids = state.get(webhook_key, [])
        status = "set" if url else "EMPTY"
        id_summary = f"{len(ids)} recorded ID(s)" if ids else "no recorded IDs"
        print(f"  {label}")
        print(f"    script: {relative}")
        print(f"    {webhook_key}: {status} ({id_summary})")
        if url:
            siblings = c.sibling_webhook_state_keys(url, webhook_key)
            if len(siblings) > 1:
                others = [k for k in siblings if k != webhook_key]
                print(f"    siblings: {', '.join(others)} (shared purge)")
            for sid in ids:
                print(f"      message ID: {sid}")
    print()

    orphan_keys = sorted(set(state) - {key for _, _, key in ANNOUNCERS})
    if orphan_keys:
        print("State keys not in announcer catalog (stale or manual):")
        for key in orphan_keys:
            ids = state.get(key, [])
            print(f"  {key}: {len(ids)} ID(s) -> {ids}")
        print()

    state_path = c.WEBHOOK_MESSAGES_PATH
    if state_path.is_file():
        print(f"State file: {state_path.name} ({state_path.stat().st_size} bytes)")
    else:
        print(f"State file: {state_path.name} (not present - first live send creates it)")
    print()

    print("Recovery hints:")
    print("  - Reset one channel: remove its WEBHOOK_* key from .webhook_messages.json")
    print("  - Reset all: delete .webhook_messages.json")
    print("  - Orphan channel messages: manual delete or run_all.py --bot-channel-purge")
    print("  - Do NOT use legacy Downloads\\DS scripts (no purge / no reactions)")
    print()
    print("See docs/OPS.md for the full runbook.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# === FILE FOOTER ===
# End of file: tools/diagnose_webhook_state.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
