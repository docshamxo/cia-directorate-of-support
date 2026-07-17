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
#   - 2026-07-17 | docshamxo | Note purge-all recorded IDs and checkmark reactions on live runs.
#   - 2026-07-17 | docshamxo | Use common.manifest; add --only filter.
#   - 2026-07-17 | docshamxo | Add --stage / --list for safer staged office rollout.
#   - 2026-07-17 | docshamxo | Require bot token; allow-skip-reaction; bot channel purge; dup warn.
# === END FILE HEADER ===

"""
Run all CIA Directorate of Support Discord announcer scripts.

Usage (from the repository root):
    python run_all.py
    python run_all.py --dry-run
    python run_all.py --fail-fast
    python run_all.py --delay 1.5
    python run_all.py --only ds,osec
    python run_all.py --only WEBHOOK_GRS_COC,esd/coc.py
    python run_all.py --stage 1
    python run_all.py --stage osec --dry-run
    python run_all.py --list
    python run_all.py --list-stages
    python run_all.py --allow-skip-reaction
    python run_all.py --bot-channel-purge
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

from common import cia_common as c
from common.manifest import ANNOUNCERS, ROLLOUT_STAGES, announcers_for_office, resolve_rollout_stage
from common.rollout import selected_scripts

REPO_ROOT = Path(__file__).resolve().parent
SCRIPTS = ANNOUNCERS


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
    parser.add_argument(
        "--only",
        default="",
        help=(
            "Comma-separated filter: office folder (ds), script path (grs/coc.py), "
            "basename/stem (coc), label substring, or WEBHOOK_* key."
        ),
    )
    parser.add_argument(
        "--stage",
        default="",
        help=(
            "Run one staged office only (safer live rollout). "
            "Accepts stage number (1-5) or office (ds, osec, ote, grs, esd). "
            "See --list-stages. Prefer advancing stages one at a time after Discord verify."
        ),
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Print announcer catalog (respects --only / --stage) and exit.",
    )
    parser.add_argument(
        "--list-stages",
        action="store_true",
        help="Print recommended staged office rollout order and exit.",
    )
    parser.add_argument(
        "--allow-skip-reaction",
        action="store_true",
        help="Post without requiring DISCORD_BOT_TOKEN for checkmark reactions.",
    )
    parser.add_argument(
        "--bot-channel-purge",
        action="store_true",
        help="After each post, bot deletes other recent webhook messages in the channel.",
    )
    return parser.parse_args(argv)


def _selected_scripts(only_arg: str, stage_arg: str) -> list[tuple[str, str, str]]:
    try:
        return selected_scripts(only_arg=only_arg, stage_arg=stage_arg, catalog=SCRIPTS)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc


def _print_stages() -> None:
    print("Recommended staged office rollout (one stage per live pass):\n")
    for stage_id, title, office in ROLLOUT_STAGES:
        count = len(announcers_for_office(office))
        print(f"  Stage {stage_id}: {title} ({office}/) - {count} announcer(s)")
        print(f"    python run_all.py --stage {stage_id}")
        print(f"    python run_all.py --stage {office} --dry-run")
    print("\nAfter each live stage, verify Discord channels before advancing.")
    print("Full checklist: docs/RELEASE_CHECKLIST.md")


def _print_catalog(scripts: list[tuple[str, str, str]]) -> None:
    print(f"{len(scripts)} announcer(s):\n")
    for relative, label, webhook_key in scripts:
        print(f"  {relative}")
        print(f"    {label}  [{webhook_key}]")


def _warn_duplicate_webhooks(env: dict[str, str]) -> None:
    duplicates = c.find_duplicate_webhook_keys(env)
    if not duplicates:
        return
    print("Warning: multiple WEBHOOK_* keys share the same Discord webhook URL:")
    for webhook_id, keys in sorted(duplicates.items()):
        print(f"  webhook ID {webhook_id}: {', '.join(keys)}")
    print(
        "  Sibling keys purge together (see OPS.md). Prefer one webhook per channel when possible.\n"
    )


def _require_bot_token_for_live(*, allow_skip: bool) -> None:
    if allow_skip:
        return
    token = os.environ.get(c.BOT_TOKEN_ENV, "").strip()
    if token:
        return
    print(
        f"ERROR: {c.BOT_TOKEN_ENV} is not set. Live runs require a bot token for checkmark reactions.\n"
        "\n"
        "Setup:\n"
        "  1. Create a bot at https://discord.com/developers/applications\n"
        "  2. Invite it with Add Reactions + Read Message History (+ channel access)\n"
        f"  3. Paste the token into {c.BOT_TOKEN_ENV}= in .env\n"
        "  4. Re-run: python run_all.py\n"
        "\n"
        "To post without reactions (not recommended): python run_all.py --allow-skip-reaction\n"
        "\n"
        "Do not invent a bot token.\n"
    )
    raise SystemExit(1)


def run_all(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    load_dotenv(REPO_ROOT / ".env")
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    if args.list_stages:
        _print_stages()
        return 0

    scripts = _selected_scripts(args.only, args.stage)

    if args.list:
        if args.stage.strip():
            stage_id, title, office = resolve_rollout_stage(args.stage)
            print(f"Stage {stage_id}: {title} ({office}/)\n")
        _print_catalog(scripts)
        return 0

    env = os.environ.copy()
    pythonpath = str(REPO_ROOT)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = pythonpath if not existing else pythonpath + os.pathsep + existing
    if args.dry_run:
        env["CIA_DRY_RUN"] = "1"
    if not args.no_skip_empty:
        env["CIA_SKIP_EMPTY_WEBHOOKS"] = "1"
    if args.allow_skip_reaction:
        env["CIA_ALLOW_SKIP_REACTION"] = "1"
    if args.bot_channel_purge:
        env[c.BOT_CHANNEL_PURGE_ENV] = "1"
    env.setdefault("DISCORD_INVITE_URL", "https://example.invalid/discord-invite")
    env.setdefault(
        "DISCORD_OSEC_APPLICATION_RESULTS_URL",
        "https://example.invalid/application-results",
    )

    mode = "dry-run" if args.dry_run else "live"
    scope = f"{len(scripts)} announcer script(s)"
    if args.stage.strip():
        stage_id, title, office = resolve_rollout_stage(args.stage)
        scope = f"stage {stage_id} ({title} / {office}/) - {len(scripts)} script(s)"
    print(f"Running {scope} from {REPO_ROOT} ({mode})\n")
    print(
        "Note: use this repository only. Do NOT run legacy flat scripts under "
        "Downloads\\DS - they post without purge or checkmark reactions.\n"
    )
    print(
        "Note: live runs post first, then delete previously recorded webhook messages "
        "for each channel (see .webhook_messages.json), and require a checkmark reaction "
        f"via {c.BOT_TOKEN_ENV} unless --allow-skip-reaction is set.\n"
        "Messages posted before cleanup / outside local state are left alone.\n"
    )
    if not args.stage.strip() and not args.only.strip() and not args.dry_run:
        print(
            "Tip: for safer live rollout, prefer one office at a time:\n"
            "  python run_all.py --list-stages\n"
            "  python run_all.py --stage 1\n"
            "See docs/RELEASE_CHECKLIST.md\n"
        )

    _warn_duplicate_webhooks(env)

    if not args.dry_run:
        _require_bot_token_for_live(allow_skip=args.allow_skip_reaction)

    succeeded: list[str] = []
    skipped: list[str] = []
    failed: list[tuple[str, str]] = []

    for index, (relative, label, webhook_key) in enumerate(scripts):
        path = REPO_ROOT / relative
        if not path.exists():
            failed.append((label, f"Missing script: {path}"))
            if args.fail_fast:
                break
            continue

        webhook_value = env.get(webhook_key, "").strip()
        if not args.dry_run and not webhook_value and not args.no_skip_empty:
            print(f"skip {label} ({relative}) - empty {webhook_key}")
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

        if args.delay > 0 and index < len(scripts) - 1:
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
    if args.stage.strip() and not args.dry_run:
        stage_id, title, _office = resolve_rollout_stage(args.stage)
        print(f"Stage {stage_id} ({title}) complete - verify Discord, then advance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_all())

# === FILE FOOTER ===
# End of file: run_all.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
