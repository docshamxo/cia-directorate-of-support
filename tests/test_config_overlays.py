# === FILE HEADER ===
# Title: Test Config Overlays
# Path: tests/test_config_overlays.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Deep-merge + staff local overlay + fail-closed URLs.
# === END FILE HEADER ===

"""Regression tests for YAML config loading and staff link overlays."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from common import cia_common as c


def test_deep_merge_nested_dicts() -> None:
    base = {"a": {"x": 1, "y": 2}, "b": 3}
    overlay = {"a": {"y": 99, "z": 4}, "c": 5}
    merged = c._deep_merge(base, overlay)
    assert merged == {"a": {"x": 1, "y": 99, "z": 4}, "b": 3, "c": 5}
    # Base must not be mutated.
    assert base["a"]["y"] == 2


def test_deep_merge_replaces_non_dict_leaf() -> None:
    merged = c._deep_merge({"a": {"x": 1}}, {"a": "replaced"})
    assert merged["a"] == "replaced"


def test_is_staff_placeholder_markers() -> None:
    assert c.is_staff_placeholder("https://x/STAFF_LOCAL_REQUIRED")
    assert c.is_staff_placeholder("https://example.invalid/path")
    assert not c.is_staff_placeholder("https://docs.google.com/document/d/abc")


def test_url_known_public_link() -> None:
    value = c.url("community.roblox_group_ds")
    assert value.startswith("http")
    assert not c.is_staff_placeholder(value)


def test_url_unknown_path_raises() -> None:
    with pytest.raises(KeyError, match="Unknown links"):
        c.url("does.not.exist")


def test_require_resolved_url_fails_on_placeholder(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        c,
        "url",
        lambda path: "https://example.invalid/STAFF_LOCAL_REQUIRED",
    )
    with pytest.raises(RuntimeError, match="unresolved"):
        c.require_resolved_url("osec.staff_documents.google_drive")


def test_staff_local_overlay_deep_merges(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "links.yaml").write_text(
        yaml.safe_dump(
            {
                "community": {"roblox_group_ds": "https://public.example/ds"},
                "osec": {
                    "staff_documents": {
                        "google_drive": "https://example.invalid/STAFF_LOCAL_REQUIRED",
                        "tryout_guide": "https://example.invalid/STAFF_LOCAL_REQUIRED",
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    (config_dir / "links.staff.local.yaml").write_text(
        yaml.safe_dump(
            {
                "osec": {
                    "staff_documents": {
                        "google_drive": "https://drive.google.com/drive/folders/REAL",
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(c, "CONFIG_DIR", config_dir)
    c._links.cache_clear()
    try:
        data = c._links()
        assert data["community"]["roblox_group_ds"] == "https://public.example/ds"
        assert data["osec"]["staff_documents"]["google_drive"].endswith("/REAL")
        assert "STAFF_LOCAL_REQUIRED" in data["osec"]["staff_documents"]["tryout_guide"]
        assert c.url("osec.staff_documents.google_drive").endswith("/REAL")
        # Unresolved sibling still fails closed.
        with pytest.raises(RuntimeError, match="unresolved"):
            c.require_resolved_url("osec.staff_documents.tryout_guide")
    finally:
        c._links.cache_clear()


def test_staff_overlay_ignored_when_not_mapping(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "links.yaml").write_text(
        yaml.safe_dump({"community": {"roblox_group_ds": "https://public.example/ds"}}),
        encoding="utf-8",
    )
    (config_dir / "links.staff.local.yaml").write_text("- not a mapping\n", encoding="utf-8")

    monkeypatch.setattr(c, "CONFIG_DIR", config_dir)
    c._links.cache_clear()
    try:
        assert c._links()["community"]["roblox_group_ds"] == "https://public.example/ds"
    finally:
        c._links.cache_clear()


def test_validate_webhook_url_accepts_discord_shapes() -> None:
    c.validate_webhook_url("https://discord.com/api/webhooks/1/abc-def")
    c.validate_webhook_url("https://canary.discord.com/api/webhooks/1/abc")
    with pytest.raises(ValueError, match="Invalid Discord webhook"):
        c.validate_webhook_url("https://evil.example/api/webhooks/1/abc")


def test_mask_webhook_url_canary() -> None:
    masked = c.mask_webhook_url("https://canary.discord.com/api/webhooks/99/sekrit")
    assert "99" in masked
    assert "sekrit" not in masked


# === FILE FOOTER ===
# End of file: tests/test_config_overlays.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
