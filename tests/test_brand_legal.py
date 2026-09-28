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


def test_bot_names_follow_office_bot_pattern() -> None:
    expected = {
        c.BOT_DS: "CIA Directorate of Support Bot",
        c.BOT_OSEC: "CIA Office of Security Bot",
        c.BOT_OTE: "CIA Office of Training & Education Bot",
        c.BOT_GRS: "CIA Global Response Staff Bot",
        c.BOT_ESD: "CIA Executive Security Detail Bot",
    }
    for name, want in expected.items():
        assert name == want
        assert name.startswith("CIA ")
        assert name.endswith(" Bot")
        assert not name.strip().startswith("CIA |")
        assert len(name) <= 80


def test_agency_eyebrow_is_community_rp() -> None:
    text = c.agency_eyebrow("Office of Security")
    assert "community" in text.lower()
    assert "unofficial" not in text.lower()
    assert "Central Intelligence Agency ·" not in text


def test_community_link_label() -> None:
    assert c.community_link_label("OSEC") == "CIA DS | OSEC"


def test_disclaimer_title_and_affiliation() -> None:
    embed = c.disclaimer_embed(color=c.COLOR_DS)
    assert embed.title and "Disclaimer" in embed.title
    assert "unofficial" not in (embed.title or "").lower()
    assert "unofficial" not in (embed.description or "").lower()
    assert "not affiliated" in (embed.description or "").lower()


def test_disclaimer_only_on_rules_embeds() -> None:
    """Disclaimer closer is reserved for OTE/OSEC Rules posts."""
    for embeds in (
        c.server_regulations_embeds(),
        c.server_regulations_embeds(
            office="Office of Training & Education",
            motto=c.OTE_MOTTO,
            logo=c.LOGOS["ote"],
            color=c.COLOR_OTE,
        ),
    ):
        titles = [e.title or "" for e in embeds]
        assert titles.count("Disclaimer · Community") == 1

    hero = c.hero_embed(
        title="PUBLIC INFORMATION",
        unit="Office of Security",
        supporting="Reference hub.",
        color=c.COLOR_OSEC,
    )
    assert "Disclaimer" not in (hero.title or "")


def test_unofficial_roleplay_only_on_rules_heroes() -> None:
    """\"Unofficial … Roleplay\" appears once, and only on OTE/OSEC rules intros."""
    osec = c.server_regulations_embeds()
    ote = c.server_regulations_embeds(
        office="Office of Training & Education",
        motto=c.OTE_MOTTO,
        logo=c.LOGOS["ote"],
        color=c.COLOR_OTE,
    )
    for embeds in (osec, ote):
        blob = "\n".join([(e.title or "") + "\n" + (e.description or "") for e in embeds])
        assert blob.lower().count("unofficial") == 1
        assert "Unofficial Roblox Roleplay Community" in blob

    hero = c.hero_embed(
        title="PUBLIC INFORMATION",
        unit="Office of Security",
        supporting="Reference hub.",
        color=c.COLOR_OSEC,
    )
    assert "unofficial" not in (hero.description or "").lower()
    assert "**Office of Security**" in (hero.description or "")


def test_license_and_brand_docs_exist() -> None:
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    brand_text = (ROOT / "docs" / "BRAND.md").read_text(encoding="utf-8")
    assert "not affiliated" in license_text.lower()
    assert "Brand Use" in license_text or "brand use" in license_text.lower()
    assert "CIA Office of Security Bot" in brand_text or "CIA {Office}" in brand_text
    assert "Bot" in brand_text


# === FILE FOOTER ===
# End of file: tests/test_brand_legal.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
