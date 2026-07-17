# === FILE HEADER ===
# Title: Test IR Reliability
# Path: tests/test_ir_reliability.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Exit codes, webhook state clear, run_all resume helpers.
# === END FILE HEADER ===

"""Unit tests for IR / SRE reliability helpers."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from common import cia_common as c
from common.batch import ScriptResult, apply_from_filter, classify_child_exit, resume_hint
from common.exit_codes import (
    ANNOUNCER_CONFIG,
    ANNOUNCER_SKIPPED,
    CRITICAL,
    OK,
    UNKNOWN,
    WARNING,
    classify_batch_exit,
)
from common.rollout import matches_only


def test_classify_batch_exit_ok_with_skips() -> None:
    assert classify_batch_exit(succeeded=3, skipped=2, failed=0) == OK


def test_classify_batch_exit_warning_all_skipped() -> None:
    assert classify_batch_exit(succeeded=0, skipped=5, failed=0) == WARNING


def test_classify_batch_exit_critical_on_failure() -> None:
    assert classify_batch_exit(succeeded=2, skipped=1, failed=1) == CRITICAL


def test_classify_batch_exit_strict_skips() -> None:
    assert classify_batch_exit(succeeded=2, skipped=1, failed=0, strict_skips=True) == WARNING


def test_classify_batch_exit_unknown_empty() -> None:
    assert classify_batch_exit(succeeded=0, skipped=0, failed=0) == UNKNOWN


def test_classify_child_exit_announcer_codes() -> None:
    assert classify_child_exit(0)[0] == "succeeded"
    assert classify_child_exit(ANNOUNCER_SKIPPED)[0] == "skipped"
    assert classify_child_exit(ANNOUNCER_CONFIG)[0] == "failed"
    assert classify_child_exit(1)[0] == "failed"


def test_apply_from_filter_resumes_inclusive() -> None:
    scripts = [
        ("ds/a.py", "A", "WEBHOOK_A"),
        ("osec/b.py", "B", "WEBHOOK_B"),
        ("ote/c.py", "C", "WEBHOOK_C"),
    ]
    selected = apply_from_filter(scripts, "osec/b.py")
    assert [item[0] for item in selected] == ["osec/b.py", "ote/c.py"]


def test_matches_only_webhook_key() -> None:
    assert matches_only("grs/coc.py", "GRS CoC", "WEBHOOK_GRS_COC", "WEBHOOK_GRS_COC")


def test_resume_hint_points_at_first_failure() -> None:
    results = [
        ScriptResult("ds/a.py", "A", "WA", "succeeded"),
        ScriptResult("osec/b.py", "B", "WB", "failed", reason="boom"),
        ScriptResult("ote/c.py", "C", "WC", "skipped"),
    ]
    assert resume_hint(results) == "python run_all.py --from osec/b.py"


def test_clear_webhook_message_state_one_key(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state_path = tmp_path / ".webhook_messages.json"
    lock_path = tmp_path / ".webhook_messages.lock"
    monkeypatch.setattr(c, "WEBHOOK_MESSAGES_PATH", state_path)
    monkeypatch.setattr(c, "WEBHOOK_MESSAGES_LOCK_PATH", lock_path)
    state_path.write_text(
        json.dumps({"WEBHOOK_A": [1], "WEBHOOK_B": [2, 3]}),
        encoding="utf-8",
    )
    assert c.clear_webhook_message_state("WEBHOOK_A") == 1
    saved = json.loads(state_path.read_text(encoding="utf-8"))
    assert "WEBHOOK_A" not in saved
    assert saved["WEBHOOK_B"] == [2, 3]
    assert c.clear_webhook_message_state("WEBHOOK_MISSING") == 0


def test_clear_webhook_message_state_all(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    state_path = tmp_path / ".webhook_messages.json"
    lock_path = tmp_path / ".webhook_messages.lock"
    monkeypatch.setattr(c, "WEBHOOK_MESSAGES_PATH", state_path)
    monkeypatch.setattr(c, "WEBHOOK_MESSAGES_LOCK_PATH", lock_path)
    state_path.write_text(json.dumps({"WEBHOOK_A": [1]}), encoding="utf-8")
    assert c.clear_webhook_message_state() == 1
    assert not state_path.exists()


# === FILE FOOTER ===
# End of file: tests/test_ir_reliability.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
