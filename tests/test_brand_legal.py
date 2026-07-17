# === FILE HEADER ===
# Title: Test Brand Legal
# Path: tests/test_brand_legal.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Brand/legal regression tests for bots, eyebrow, disclaimers.
# === END FILE HEADER ===

"""Brand / trademark / non-affiliation regressions."""

from __future__ import annotations

from pathlib import Path

from common import cia_common as c

ROOT = Path(__file__).resolve().parents[1]


def test_bot_names_include_community_or_rp_marker() -> None:
    for name in (c.BOT_DS, c.BOT_OSEC, c.BOT_OTE, c.BOT_GRS, c.BOT_ESD):
        assert "Community" in name or "(RP)" in name
        assert not name.strip().startswith("CIA |")
        assert len(name) <= 80


def test_agency_eyebrow_is_community_rp() -> None:
    text = c.agency_eyebrow("Office of Security")
    assert "community" in text.lower()
    assert "Central Intelligence Agency ·" not in text


def test_community_link_label() -> None:
    assert c.community_link_label("OSEC") == "DS Community | OSEC"


def test_disclaimer_title_and_affiliation() -> None:
    embed = c.disclaimer_embed(color=c.COLOR_DS)
    assert embed.title and "Unofficial" in embed.title
    assert "not affiliated" in (embed.description or "").lower()


def test_license_and_brand_docs_exist() -> None:
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    brand_text = (ROOT / "docs" / "BRAND.md").read_text(encoding="utf-8")
    assert "not affiliated" in license_text.lower()
    assert "Brand Use" in license_text or "brand use" in license_text.lower()
    assert "(RP)" in brand_text
    assert "Community" in brand_text


# === FILE FOOTER ===
# End of file: tests/test_brand_legal.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
