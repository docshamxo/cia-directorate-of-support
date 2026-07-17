# === FILE HEADER ===
# Title: Batch
# Path: common/batch.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Shared run_all selection / exit classification helpers.
# === END FILE HEADER ===

"""Pure helpers for batch announcer runs (importable without executing run_all)."""

from __future__ import annotations

from dataclasses import dataclass

from common.exit_codes import ANNOUNCER_CONFIG, ANNOUNCER_SKIPPED
from common.rollout import matches_only


@dataclass
class ScriptResult:
    relative: str
    label: str
    webhook_key: str
    status: str  # succeeded | skipped | failed
    exit_code: int | None = None
    reason: str = ""
    duration_ms: int = 0
    stderr_tail: str = ""


def apply_from_filter(
    scripts: list[tuple[str, str, str]], from_token: str
) -> list[tuple[str, str, str]]:
    token = from_token.strip()
    if not token:
        return scripts
    for index, (relative, label, webhook_key) in enumerate(scripts):
        if matches_only(relative, label, webhook_key, token):
            return scripts[index:]
    raise ValueError(f"No announcers matched --from {from_token!r}")


def classify_child_exit(returncode: int) -> tuple[str, str]:
    """Return (status, reason) for a child announcer exit code."""
    if returncode == 0:
        return "succeeded", ""
    if returncode == ANNOUNCER_SKIPPED:
        return "skipped", f"announcer skip exit {ANNOUNCER_SKIPPED}"
    if returncode == ANNOUNCER_CONFIG:
        return "failed", f"config/fail-closed exit {ANNOUNCER_CONFIG}"
    return "failed", f"exit code {returncode}"


def resume_hint(results: list[ScriptResult]) -> str:
    """Suggest --from for the first failed script."""
    for item in results:
        if item.status == "failed":
            return f"python run_all.py --from {item.relative}"
    return ""


def stderr_tail(text: str, *, max_lines: int = 12) -> str:
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    return "\n".join(lines[-max_lines:])


# === FILE FOOTER ===
# End of file: common/batch.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
