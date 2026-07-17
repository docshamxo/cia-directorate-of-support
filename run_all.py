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
#   - 2026-07-17 | docshamxo | Note purge-all recorded IDs and ✅ reactions on live runs.
#   - 2026-07-17 | docshamxo | Use common.manifest; add --only filter.
#   - 2026-07-17 | docshamxo | Add --stage / --list for safer staged office rollout.
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
        "Note: live runs post first, then delete previously recorded webhook messages "
        "for each channel (see .webhook_messages.json), and add a checkmark reaction when "
        "DISCORD_BOT_TOKEN is set.\n"
        "Messages posted before cleanup / outside local state are left alone.\n"
    )
    if not args.stage.strip() and not args.only.strip() and not args.dry_run:
        print(
            "Tip: for safer live rollout, prefer one office at a time:\n"
            "  python run_all.py --list-stages\n"
            "  python run_all.py --stage 1\n"
            "See docs/RELEASE_CHECKLIST.md\n"
        )

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
