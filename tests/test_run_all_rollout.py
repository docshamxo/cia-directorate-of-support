# === FILE HEADER ===
# Title: Test Run All Rollout
# Path: tests/test_run_all_rollout.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Unit tests for --only / --stage selection.
# === END FILE HEADER ===

"""Unit tests for staged rollout and --only filtering."""

from __future__ import annotations

import pytest

from common.manifest import ANNOUNCERS, ROLLOUT_STAGES, announcers_for_office, resolve_rollout_stage
from common.rollout import selected_scripts


def test_resolve_rollout_stage_accepts_number_and_office() -> None:
    assert resolve_rollout_stage("1")[2] == "ds"
    assert resolve_rollout_stage("osec")[0] == "2"
    assert resolve_rollout_stage("4-grs")[2] == "grs"


def test_resolve_rollout_stage_rejects_unknown() -> None:
    with pytest.raises(ValueError, match="Unknown"):
        resolve_rollout_stage("nope")


def test_announcers_for_office_ds() -> None:
    ds = announcers_for_office("ds")
    assert len(ds) == 3
    assert all(path.startswith("ds/") for path, _label, _key in ds)


def test_selected_scripts_stage_intersects_only() -> None:
    selected = selected_scripts(only_arg="coc", stage_arg="grs")
    assert len(selected) == 1
    assert selected[0][0] == "grs/coc.py"


def test_selected_scripts_only_office() -> None:
    selected = selected_scripts(only_arg="esd", stage_arg="")
    assert len(selected) == 3
    assert all(path.startswith("esd/") for path, _label, _key in selected)


def test_selected_scripts_unknown_only_raises() -> None:
    with pytest.raises(ValueError, match="No announcers matched"):
        selected_scripts(only_arg="not-a-real-filter", stage_arg="")


def test_rollout_stages_cover_all_offices() -> None:
    offices = {office for _sid, _title, office in ROLLOUT_STAGES}
    assert offices == {"ds", "osec", "ote", "grs", "esd"}
    covered = sum(len(announcers_for_office(o)) for o in offices)
    assert covered == len(ANNOUNCERS)


# === FILE FOOTER ===
# End of file: tests/test_run_all_rollout.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
