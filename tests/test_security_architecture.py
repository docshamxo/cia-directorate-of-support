# === FILE HEADER ===
# Title: Test Security Architecture
# Path: tests/test_security_architecture.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Validator coverage for secret-split and logo/mentions guards.
# === END FILE HEADER ===

"""Regression tests for security-architecture validators (no live Discord)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_validate_repo():
    path = ROOT / "tools" / "validate_repo.py"
    spec = importlib.util.spec_from_file_location("validate_repo", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_validate_secret_split_passes_on_clean_tree() -> None:
    vr = _load_validate_repo()
    vr.validate_secret_split()


def test_validate_mentions_and_logo_guards_passes() -> None:
    vr = _load_validate_repo()
    vr.validate_mentions_and_logo_guards()


def test_validate_logos_bare_filenames() -> None:
    vr = _load_validate_repo()
    vr.validate_logos()


def test_webhook_leak_regex_detects_discord_url() -> None:
    vr = _load_validate_repo()
    assert vr.WEBHOOK_URL_LEAK_RE.search(
        "see https://discord.com/api/webhooks/123456789012345678/AbCdEfGhIjKlMnOp"
    )
    assert not vr.WEBHOOK_URL_LEAK_RE.search("https://example.invalid/not-a-webhook")


# === FILE FOOTER ===
# End of file: tests/test_security_architecture.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
