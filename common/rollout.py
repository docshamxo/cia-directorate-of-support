# === FILE HEADER ===
# Title: Rollout
# Path: common/rollout.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Shared --only / --stage selection for run_all.
# === END FILE HEADER ===

"""Shared announcer selection for staged office rollout and --only filters."""

from __future__ import annotations

from pathlib import Path

from common.manifest import ANNOUNCERS, announcers_for_office, resolve_rollout_stage


def matches_only(relative: str, label: str, webhook_key: str, only: str) -> bool:
    token = only.strip().lower()
    if not token:
        return True
    rel = relative.lower().replace("\\", "/")
    base = Path(rel).name
    stem = Path(rel).stem
    return (
        token == webhook_key.lower()
        or token == rel
        or token == base
        or token == stem
        or token in label.lower()
        or rel.startswith(token.rstrip("/") + "/")
        or rel.split("/", 1)[0] == token
    )


def filter_only(scripts: list[tuple[str, str, str]], only_arg: str) -> list[tuple[str, str, str]]:
    raw = [part.strip() for part in only_arg.split(",") if part.strip()]
    if not raw:
        return list(scripts)
    selected: list[tuple[str, str, str]] = []
    for entry in scripts:
        relative, label, webhook_key = entry
        if any(matches_only(relative, label, webhook_key, token) for token in raw):
            selected.append(entry)
    if not selected:
        raise ValueError(f"No announcers matched --only {only_arg!r}")
    return selected


def selected_scripts(
    only_arg: str = "",
    stage_arg: str = "",
    catalog: tuple[tuple[str, str, str], ...] | None = None,
) -> list[tuple[str, str, str]]:
    """Apply optional ``--stage`` then ``--only``. Raises ValueError on bad filters."""
    scripts: list[tuple[str, str, str]] = list(catalog if catalog is not None else ANNOUNCERS)
    if stage_arg.strip():
        _stage_id, _title, office = resolve_rollout_stage(stage_arg)
        scripts = announcers_for_office(office)
        if not scripts:
            raise ValueError(f"No announcers found for office {office!r}")
    return filter_only(scripts, only_arg)


# === FILE FOOTER ===
# End of file: common/rollout.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
