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
#   - 2026-07-17 | docshamxo | IR resilience: exit codes, --from, --retry, --report, resume hints.
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
    python run_all.py --from osec/staff_documents.py
    python run_all.py --retry 1 --report .run_report.json
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

from common import cia_common as c
from common.batch import (
    ScriptResult,
    apply_from_filter,
    classify_child_exit,
    resume_hint,
    stderr_tail,
)
from common.exit_codes import (
    CRITICAL,
    EXIT_CODE_HELP,
    OK,
    UNKNOWN,
    WARNING,
    classify_batch_exit,
)
from common.manifest import ANNOUNCERS, ROLLOUT_STAGES, announcers_for_office, resolve_rollout_stage
from common.rollout import selected_scripts

REPO_ROOT = Path(__file__).resolve().parent
SCRIPTS = ANNOUNCERS
logger = logging.getLogger("cia.run_all")


@dataclass
class BatchReport:
    started_at: str
    finished_at: str = ""
    mode: str = "live"
    exit_code: int = UNKNOWN
    exit_meaning: str = ""
    succeeded: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    failed: list[dict[str, str]] = field(default_factory=list)
    results: list[dict[str, object]] = field(default_factory=list)
    resume_hint: str = ""


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
        help="Print announcer catalog (respects --only / --stage / --from) and exit.",
    )
    parser.add_argument(
        "--list-stages",
        action="store_true",
        help="Print recommended staged office rollout order and exit.",
    )
    parser.add_argument(
        "--from",
        dest="from_token",
        default="",
        metavar="TOKEN",
        help=(
            "Resume mid-batch: skip catalog entries until this office/path/label/"
            "WEBHOOK_* matches (inclusive)."
        ),
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=0,
        metavar="N",
        help="After the main pass, retry failed scripts up to N extra times (default: 0).",
    )
    parser.add_argument(
        "--report",
        default="",
        metavar="PATH",
        help="Write a JSON batch report (timings, exit code, resume hint) to PATH.",
    )
    parser.add_argument(
        "--strict-skips",
        action="store_true",
        help="Exit WARNING (1) if any announcer was skipped while others succeeded.",
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
    parser.add_argument(
        "--require-reaction",
        action="store_true",
        help="Deprecated no-op: reactions are required by default (see --allow-skip-reaction).",
    )
    return parser.parse_args(argv)


def _selected_scripts(only_arg: str, stage_arg: str, from_token: str) -> list[tuple[str, str, str]]:
    try:
        scripts = selected_scripts(only_arg=only_arg, stage_arg=stage_arg, catalog=SCRIPTS)
        selected = apply_from_filter(scripts, from_token)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if from_token.strip() and selected and scripts and selected[0] != scripts[0]:
        relative, label, _webhook = selected[0]
        skipped = len(scripts) - len(selected)
        print(f"Resuming from {label} ({relative}) - skipped {skipped} earlier script(s)\n")
    return selected


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
    raise SystemExit(CRITICAL)


def _run_one(
    *,
    relative: str,
    label: str,
    webhook_key: str,
    env: dict[str, str],
    dry_run: bool,
    no_skip_empty: bool,
) -> ScriptResult:
    path = REPO_ROOT / relative
    if not path.exists():
        return ScriptResult(
            relative=relative,
            label=label,
            webhook_key=webhook_key,
            status="failed",
            reason=f"Missing script: {path}",
        )

    webhook_value = env.get(webhook_key, "").strip()
    if not dry_run and not webhook_value and not no_skip_empty:
        print(f"skip {label} ({relative}) - empty {webhook_key}")
        logger.info("event=batch_skip label=%s webhook_key=%s", label, webhook_key)
        return ScriptResult(
            relative=relative,
            label=label,
            webhook_key=webhook_key,
            status="skipped",
            reason=f"empty {webhook_key}",
        )

    print(f"-> {label} ({relative})")
    logger.info("event=batch_start label=%s path=%s", label, relative)
    started = time.monotonic()
    child_argv = [sys.executable, str(path)]
    if env.get("CIA_ALLOW_SKIP_REACTION") == "1":
        child_argv.append("--allow-skip-reaction")
    if env.get(c.BOT_CHANNEL_PURGE_ENV) == "1":
        child_argv.append("--bot-channel-purge")
    result = subprocess.run(
        child_argv,
        cwd=REPO_ROOT,
        env=env,
        check=False,
        stderr=subprocess.PIPE,
        text=True,
    )
    duration_ms = int((time.monotonic() - started) * 1000)
    tail = stderr_tail(result.stderr or "")
    if result.stderr:
        print(result.stderr, end="" if result.stderr.endswith("\n") else "\n", file=sys.stderr)

    status, reason = classify_child_exit(result.returncode)
    logger.info(
        "event=batch_finish label=%s status=%s exit_code=%s duration_ms=%s",
        label,
        status,
        result.returncode,
        duration_ms,
    )
    return ScriptResult(
        relative=relative,
        label=label,
        webhook_key=webhook_key,
        status=status,
        exit_code=result.returncode,
        reason=reason,
        duration_ms=duration_ms,
        stderr_tail=tail,
    )


def _write_report(path: Path, report: BatchReport) -> None:
    path.write_text(json.dumps(asdict(report), indent=2) + "\n", encoding="utf-8")
    print(f"Wrote batch report: {path}")


def run_all(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    load_dotenv(REPO_ROOT / ".env")
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    if args.list_stages:
        _print_stages()
        return OK

    try:
        scripts = _selected_scripts(args.only, args.stage, args.from_token)
    except SystemExit as exc:
        message = exc.code if isinstance(exc.code, str) else str(exc)
        print(message, file=sys.stderr)
        return WARNING

    if args.list:
        if args.stage.strip():
            stage_id, title, office = resolve_rollout_stage(args.stage)
            print(f"Stage {stage_id}: {title} ({office}/)\n")
        _print_catalog(scripts)
        return OK

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
    env.setdefault("OSEC_LOWCOM_APPLICATION_URL", "https://example.invalid/osec-lowcom-app")
    env.setdefault("OSEC_MIDCOM_APPLICATION_URL", "https://example.invalid/osec-midcom-app")
    env.setdefault("OTE_APPLICATION_URL", "https://example.invalid/ote-application")

    mode = "dry-run" if args.dry_run else "live"
    started_at = datetime.now(timezone.utc).isoformat()
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
    logger.info(
        "event=batch_run_start count=%s mode=%s fail_fast=%s retry=%s",
        len(scripts),
        mode,
        args.fail_fast,
        args.retry,
    )

    _warn_duplicate_webhooks(env)

    if not args.dry_run:
        _require_bot_token_for_live(allow_skip=args.allow_skip_reaction)

    results: list[ScriptResult] = []
    for index, (relative, label, webhook_key) in enumerate(scripts):
        result = _run_one(
            relative=relative,
            label=label,
            webhook_key=webhook_key,
            env=env,
            dry_run=args.dry_run,
            no_skip_empty=args.no_skip_empty,
        )
        results.append(result)
        if result.status == "failed" and args.fail_fast:
            break
        if args.delay > 0 and index < len(scripts) - 1:
            time.sleep(args.delay)
        print()

    retries_left = max(0, args.retry)
    while retries_left > 0:
        failed_entries = [item for item in results if item.status == "failed"]
        if not failed_entries:
            break
        retries_left -= 1
        print(f"-- Retry pass ({len(failed_entries)} failed; {retries_left} retry(s) left) --\n")
        for item in failed_entries:
            results = [
                r for r in results if not (r.relative == item.relative and r.status == "failed")
            ]
            retry_result = _run_one(
                relative=item.relative,
                label=item.label,
                webhook_key=item.webhook_key,
                env=env,
                dry_run=args.dry_run,
                no_skip_empty=args.no_skip_empty,
            )
            results.append(retry_result)
            if retry_result.status == "failed" and args.fail_fast:
                retries_left = 0
                break
            if args.delay > 0:
                time.sleep(args.delay)
            print()

    succeeded = [r for r in results if r.status == "succeeded"]
    skipped = [r for r in results if r.status == "skipped"]
    failed = [r for r in results if r.status == "failed"]

    exit_code = classify_batch_exit(
        succeeded=len(succeeded),
        skipped=len(skipped),
        failed=len(failed),
        strict_skips=args.strict_skips,
    )
    resume = resume_hint(results)

    print("-- Summary --")
    print(f"Succeeded: {len(succeeded)}")
    print(f"Skipped:   {len(skipped)}")
    print(f"Failed:    {len(failed)}")
    print(f"Exit:      {exit_code} ({EXIT_CODE_HELP.get(exit_code, 'unlisted')})")
    if skipped:
        print("Skipped scripts:")
        for item in skipped:
            print(f"  - {item.label}: {item.reason or 'skipped'}")
    if failed:
        print("Failed scripts:")
        for item in failed:
            print(f"  - {item.label}: {item.reason or 'failed'}")
            if item.stderr_tail:
                for line in item.stderr_tail.splitlines():
                    print(f"      stderr: {line}")
        if resume:
            print(f"\nMid-batch resume hint:\n  {resume}")
            if not args.dry_run:
                print(
                    "  See OPS.md -> Mid-batch failures. "
                    "State is per-channel; successful posts before the failure are already live."
                )

    if exit_code == OK:
        print("All runnable scripts completed successfully.")
        if args.stage.strip() and not args.dry_run:
            stage_id, title, _office = resolve_rollout_stage(args.stage)
            print(f"Stage {stage_id} ({title}) complete - verify Discord, then advance.")
    elif exit_code == WARNING:
        print("Batch finished with WARNING (degraded / skips).")
    elif exit_code == CRITICAL:
        print("Batch finished with CRITICAL failures.", file=sys.stderr)

    report = BatchReport(
        started_at=started_at,
        finished_at=datetime.now(timezone.utc).isoformat(),
        mode=mode,
        exit_code=exit_code,
        exit_meaning=EXIT_CODE_HELP.get(exit_code, ""),
        succeeded=[r.label for r in succeeded],
        skipped=[r.label for r in skipped],
        failed=[{"label": r.label, "reason": r.reason, "path": r.relative} for r in failed],
        results=[asdict(r) for r in results],
        resume_hint=resume,
    )
    if args.report:
        _write_report(Path(args.report), report)

    logger.info(
        "event=batch_run_finish exit_code=%s succeeded=%s skipped=%s failed=%s",
        exit_code,
        len(succeeded),
        len(skipped),
        len(failed),
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(run_all())

# === FILE FOOTER ===
# End of file: run_all.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
