# === FILE HEADER ===
# Title: Validate Repo
# Path: tools/validate_repo.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Add CI, Dependabot, and repository validation tooling.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-17 | docshamxo | Manifest catalog; optional banners; env community URLs.
#   - 2026-07-17 | docshamxo | Secret-split, logo bare-name, mentions regression guards.
#   - 2026-07-17 | docshamxo | Validate Inter Studios property_notice is present in config.
#   - 2026-07-17 | docshamxo | Require accessibility helpers and docs.
#   - 2026-07-17 | docshamxo | Brand/legal checks: LICENSE, bot names, affiliation, eyebrow.
#   - 2026-07-17 | docshamxo | Announcers under units/; OPS.md under docs/.
# === END FILE HEADER ===

"""
Validate repository consistency for the CIA DS announcer suite.

Checks:
  - common.manifest catalog paths exist
  - every require_webhook(...) / webhook_key= is declared in .env.example
  - every WEBHOOK_* key in .env.example is used by a script
  - every c.url(...) key exists in config/links.yaml
  - required logo assets exist
  - secret-split: no webhook/bot secrets in tracked config; empty .env.example values
  - logo filenames in branding.yaml are bare names; mentions/logo helpers present
  - Python sources compile
  - optional file banners when CIA_REQUIRE_BANNERS=1
  - brand/legal: LICENSE, community bot names, affiliation copy, RP eyebrow

Run from repository root:
    python tools/validate_repo.py
"""

from __future__ import annotations

import ast
import compileall
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ENV_EXAMPLE = ROOT / ".env.example"
COMMON = ROOT / "common" / "cia_common.py"
LINKS_YAML = ROOT / "config" / "links.yaml"
MANIFEST = ROOT / "common" / "manifest.py"

WEBHOOK_RE = re.compile(
    r'(?:require_webhook|webhook_key)\s*(?:\(|\=)\s*["\'](WEBHOOK_[A-Z0-9_]+)["\']'
)
ENV_KEY_RE = re.compile(r"^(WEBHOOK_[A-Z0-9_]+)=", re.MULTILINE)
URL_CALL_RE = re.compile(r"""c\.url\(\s*['"]([^'"]+)['"]\s*\)""")

REQUIRED_LOGOS = {
    "ds": ROOT / "assets" / "logos" / "DS.png",
    "ote": ROOT / "assets" / "logos" / "OTE.png",
    "osec": ROOT / "assets" / "logos" / "OSEC.png",
    "grs": ROOT / "assets" / "logos" / "GRS.png",
    "esd": ROOT / "assets" / "logos" / "ESD.png",
}

REQUIRED_CONFIG = (
    ROOT / "config" / "branding.yaml",
    ROOT / "config" / "organization.yaml",
    ROOT / "config" / "personnel.yaml",
    ROOT / "config" / "links.yaml",
    ROOT / "config" / "regulations.yaml",
)

HEADER_MARKER = "=== FILE HEADER ==="
FOOTER_MARKER = "=== FILE FOOTER ==="
SKIP_BANNER_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pyc"}
SKIP_BANNER_NAMES = {"LICENSE"}
ANNOUNCER_DIRS = ("units/ds", "units/osec", "units/ote", "units/grs", "units/esd")
BOT_COMMUNITY_MARKER_RE = re.compile(r"Community|\(RP\)", re.IGNORECASE)
OFFICIAL_LOOKING_BOT_RE = re.compile(r"^CIA\s*\|")
BARE_CIA_EYEBROW_RE = re.compile(
    r"\*Central Intelligence Agency\s*·",
)

# Discord webhook URL in tracked tree = secret split regression.
WEBHOOK_URL_LEAK_RE = re.compile(
    r"https://(?:canary\.|ptb\.)?(?:discord|discordapp)\.com/api/webhooks/\d+/",
    re.IGNORECASE,
)
# Discord bot token shape (rough; catches accidental pastes into YAML/docs).
BOT_TOKEN_LEAK_RE = re.compile(r"\b[MN][A-Za-z0-9_-]{23,}\.[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]{27,}\b")
BARE_LOGO_NAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")
SECRET_ENV_VALUE_RE = re.compile(
    r"^(DISCORD_BOT_TOKEN|DISCORD_INVITE_URL|DISCORD_OSEC_APPLICATION_RESULTS_URL|"
    r"WEBHOOK_[A-Z0-9_]+)=(.*)$",
    re.MULTILINE,
)
SCAN_SECRET_GLOBS = (
    "config/*.yaml",
    "README.md",
    "SECURITY.md",
    "docs/**/*.md",
    ".env.example",
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def env_flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def catalog_entries() -> list[tuple[str, str, str]]:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from common.manifest import ANNOUNCERS

    if len(ANNOUNCERS) < 1:
        fail("No announcer catalog entries found in common/manifest.py")
    return list(ANNOUNCERS)


def webhook_keys_in_code() -> set[str]:
    keys: set[str] = set()
    for path in ROOT.rglob("*.py"):
        if any(part in {".venv", "venv", ".git", "__pycache__", "tests"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        keys.update(WEBHOOK_RE.findall(text))
    return keys


def webhook_keys_in_env_example() -> set[str]:
    text = ENV_EXAMPLE.read_text(encoding="utf-8")
    return set(ENV_KEY_RE.findall(text))


def validate_catalog() -> int:
    entries = catalog_entries()
    print(f"Catalog entries: {len(entries)} (from common/manifest.py)")
    for relative, label, webhook_key in entries:
        path = ROOT / relative
        if not path.is_file():
            fail(f"Catalog path missing for {label}: {relative}")
        if not webhook_key.startswith("WEBHOOK_"):
            fail(f"Catalog webhook key invalid for {label}: {webhook_key}")
    if not MANIFEST.is_file():
        fail("Missing common/manifest.py")
    return len(entries)


def validate_webhooks() -> None:
    used = webhook_keys_in_code()
    declared = webhook_keys_in_env_example()

    used.discard("WEBHOOK_PLACEHOLDER")

    missing_env = sorted(used - declared)
    unused_env = sorted(declared - used)

    if missing_env:
        fail("Webhook keys used in code but missing from .env.example: " + ", ".join(missing_env))
    if unused_env:
        fail("Webhook keys in .env.example but unused in code: " + ", ".join(unused_env))

    print(f"Webhook keys: {len(declared)} (code and .env.example match)")


def validate_logos() -> None:
    if not COMMON.is_file():
        fail(f"Missing shared module: {COMMON.relative_to(ROOT)}")

    for key, path in REQUIRED_LOGOS.items():
        if not path.is_file():
            fail(f"Missing logo for '{key}': {path.relative_to(ROOT)}")

    branding_path = ROOT / "config" / "branding.yaml"
    branding_text = branding_path.read_text(encoding="utf-8")
    # Lightweight parse: logos: block keys → bare filenames only.
    in_logos = False
    for line in branding_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("logos:"):
            in_logos = True
            continue
        if in_logos:
            if not line[:1].isspace() and stripped and not stripped.startswith("#"):
                break
            if ":" not in stripped or stripped.startswith("#"):
                continue
            _key, _, value = stripped.partition(":")
            filename = value.strip().strip("'\"")
            if not filename:
                continue
            if not BARE_LOGO_NAME_RE.match(filename) or "/" in filename or "\\" in filename:
                fail(f"config/branding.yaml logos must be bare filenames, got: {filename!r}")

    print(f"Logos: {len(REQUIRED_LOGOS)} present (bare filenames ok)")


def validate_secret_split() -> None:
    """Fail closed if webhook/bot secrets leak into tracked public files."""
    issues: list[str] = []

    env_text = ENV_EXAMPLE.read_text(encoding="utf-8")
    for match in SECRET_ENV_VALUE_RE.finditer(env_text):
        key, value = match.group(1), match.group(2).strip()
        if value:
            issues.append(f".env.example: {key} must be empty (got non-empty value)")

    for pattern in SCAN_SECRET_GLOBS:
        for path in ROOT.glob(pattern):
            if not path.is_file():
                continue
            # Staff local overlays are gitignored; skip if present on disk.
            if "staff.local" in path.name:
                continue
            text = path.read_text(encoding="utf-8")
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            if WEBHOOK_URL_LEAK_RE.search(text):
                issues.append(f"{rel}: Discord webhook URL must not appear in tracked files")
            if BOT_TOKEN_LEAK_RE.search(text):
                issues.append(
                    f"{rel}: Discord bot-token-shaped string must not appear in tracked files"
                )

    if issues:
        fail("Secret-split checks failed:\n  - " + "\n  - ".join(issues))
    print("Secret split: tracked files clean; .env.example values empty")


def validate_mentions_and_logo_guards() -> None:
    """Regression guards for AllowedMentions.none() and logo confinement helpers."""
    common_text = COMMON.read_text(encoding="utf-8")
    issues: list[str] = []

    if "AllowedMentions.none()" not in common_text:
        issues.append("common/cia_common.py: missing AllowedMentions.none() on webhook send")
    if "allowed_mentions=discord.AllowedMentions.none()" not in common_text:
        issues.append(
            "common/cia_common.py: webhook.send must pass "
            "allowed_mentions=discord.AllowedMentions.none()"
        )
    if "def confined_logo_path" not in common_text:
        issues.append("common/cia_common.py: missing confined_logo_path()")
    if "def logo_file" not in common_text:
        issues.append("common/cia_common.py: missing logo_file()")
    if re.search(r"SyncWebhook\.from_url\([^)]*bot_token\s*=", common_text):
        issues.append(
            "common/cia_common.py: do not pass bot_token into SyncWebhook.from_url "
            "(keep reaction auth on the separate bot client)"
        )

    for folder in ANNOUNCER_DIRS:
        for path in (ROOT / folder).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            if "discord.File(" in text and "logo_file(" not in text:
                issues.append(
                    f"{rel}: attach logos via c.logo_file(...), not raw discord.File(...)"
                )

    if issues:
        fail("Mentions/logo regression guards failed:\n  - " + "\n  - ".join(issues))
    print("Mentions/logo guards: AllowedMentions.none + confined logos ok")


def _flatten_link_paths(node: Any, prefix: str = "") -> set[str]:
    paths: set[str] = set()
    if isinstance(node, dict):
        for key, value in node.items():
            if str(key).startswith("#"):
                continue
            path = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(value, dict):
                paths.update(_flatten_link_paths(value, path))
            elif isinstance(value, str):
                paths.add(path)
    return paths


def url_keys_in_code() -> set[str]:
    keys: set[str] = set()
    for folder in ANNOUNCER_DIRS:
        for path in (ROOT / folder).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            keys.update(URL_CALL_RE.findall(text))
    common_text = COMMON.read_text(encoding="utf-8")
    keys.update(re.findall(r"""url\(\s*['"]([^'"]+)['"]\s*\)""", common_text))
    return keys


def validate_url_keys() -> None:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    import yaml

    links = yaml.safe_load(LINKS_YAML.read_text(encoding="utf-8"))
    if not isinstance(links, dict):
        fail("config/links.yaml must contain a mapping")

    available = _flatten_link_paths(links)
    used = url_keys_in_code()
    missing = sorted(used - available)
    if missing:
        fail("c.url() / url() keys missing from config/links.yaml: " + ", ".join(missing))
    print(f"Link keys: {len(used)} referenced paths resolve in links.yaml")


def validate_config() -> None:
    for path in REQUIRED_CONFIG:
        if not path.is_file():
            fail(f"Missing config file: {path.relative_to(ROOT)}")

    try:
        import yaml  # noqa: F401
    except ImportError as exc:
        fail(f"PyYAML is required: {exc}")

    os.environ.setdefault("DISCORD_INVITE_URL", "https://example.invalid/discord-invite")
    os.environ.setdefault(
        "DISCORD_OSEC_APPLICATION_RESULTS_URL",
        "https://example.invalid/application-results",
    )
    os.environ.setdefault("OSEC_LOWCOM_APPLICATION_URL", "https://example.invalid/osec-lowcom-app")
    os.environ.setdefault("OSEC_MIDCOM_APPLICATION_URL", "https://example.invalid/osec-midcom-app")
    os.environ.setdefault("OTE_APPLICATION_URL", "https://example.invalid/ote-application")

    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from common import cia_common as c

    _ = (
        c.DS_MOTTO,
        c.AGENCY_EXECUTIVE,
        c.LOGOS,
        c.GRS_ESD_MIDDLE_COMMAND,
        c.discord_invite_url(),
        c.osec_application_results_url(),
        c.osec_lowcom_application_url(),
        c.ote_application_url(),
        c.server_regulations_embeds(),
    )
    if len(c.GRS_ESD_MIDDLE_COMMAND) < 1:
        fail("grs_esd_middle_command must contain at least one rank")
    if "PUBLIC" not in c.DISCLAIMER_TEXT and "PUBLIC" not in c.DISCLAIMER_LINKS_TEXT:
        fail("disclaimer copy should use community PUBLIC marking")
    if "Inter Studios" not in c.PROPERTY_NOTICE:
        fail("property_notice should name Inter Studios")
    if "not affiliated" not in c.AFFILIATION_NOTICE.lower():
        fail("affiliation_notice must state non-affiliation")
    if "not affiliated" not in c.DISCLAIMER_TEXT.lower():
        fail("disclaimer must state non-affiliation")
    eyebrow = c.agency_eyebrow("Office of Security")
    if "community" not in eyebrow.lower() and "rp" not in eyebrow.lower():
        fail("agency_eyebrow must frame units as community/RP (not bare USG banner)")
    if BARE_CIA_EYEBROW_RE.search(eyebrow):
        fail("agency_eyebrow must not use a bare Central Intelligence Agency banner")
    if "PUBLIC" not in c.MARKING_PUBLIC or "STAFF" not in c.MARKING_STAFF:
        fail("marking_public / marking_staff copy should use community markings")
    public_disc = c.disclaimer_embed(color=c.COLOR_DS).description or ""
    if "not affiliated" not in public_disc.lower():
        fail("disclaimer_embed must state non-affiliation")
    if "Inter Studios" not in public_disc:
        fail("disclaimer_embed should append property_notice")
    print(f"Config: {len(REQUIRED_CONFIG)} YAML files load successfully")


def validate_brand_legal() -> None:
    """LICENSE, bot naming, and documentation non-affiliation banners."""
    license_path = ROOT / "LICENSE"
    brand_path = ROOT / "docs" / "BRAND.md"
    if not license_path.is_file():
        fail("LICENSE is required (MIT + brand use / trademark notice)")
    license_text = license_path.read_text(encoding="utf-8")
    for needle in ("not affiliated", "Brand Use", "trademark", "roleplay"):
        if needle.lower() not in license_text.lower():
            fail(f"LICENSE must include brand-use language mentioning '{needle}'")
    if not brand_path.is_file():
        fail("docs/BRAND.md is required (bot naming / non-affiliation guidance)")
    brand_text = brand_path.read_text(encoding="utf-8")
    if "Community" not in brand_text or "(RP)" not in brand_text:
        fail("docs/BRAND.md must document Community / (RP) bot naming markers")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "not affiliated" not in readme.lower():
        fail("README.md must include a non-affiliation banner")

    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from common import cia_common as c

    for key, name in {
        "ds": c.BOT_DS,
        "osec": c.BOT_OSEC,
        "ote": c.BOT_OTE,
        "grs": c.BOT_GRS,
        "esd": c.BOT_ESD,
    }.items():
        if not BOT_COMMUNITY_MARKER_RE.search(name):
            fail(
                f"config/branding.yaml bots.{key}={name!r} must include "
                "'Community' or '(RP)' (see docs/BRAND.md)"
            )
        if OFFICIAL_LOOKING_BOT_RE.match(name.strip()):
            fail(
                f"config/branding.yaml bots.{key}={name!r} looks like an official "
                "CIA | … account; use a community/RP display name"
            )
        if len(name) > 80:
            fail(f"config/branding.yaml bots.{key} exceeds Discord's 80-char username limit")

    print("Brand/legal: LICENSE, docs/BRAND.md, affiliation banners, bot names ok")


def validate_banners() -> None:
    if not env_flag("CIA_REQUIRE_BANNERS"):
        print("File banners: skipped (set CIA_REQUIRE_BANNERS=1 to enforce)")
        return
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    missing: list[str] = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        rel = raw.decode("utf-8")
        path = ROOT / rel
        if not path.is_file() or path.suffix.lower() in SKIP_BANNER_SUFFIXES:
            continue
        if path.name in SKIP_BANNER_NAMES:
            continue
        if any(part in {".git", ".venv", "venv", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        if HEADER_MARKER not in text or FOOTER_MARKER not in text:
            missing.append(rel)
    if missing:
        fail(
            "Missing file header/footer banners in: "
            + ", ".join(missing)
            + ". Run: python tools/sync_file_banners.py"
        )
    print("File banners: header and footer present on tracked text files")


def validate_compile() -> None:
    ok = compileall.compile_dir(
        str(ROOT),
        quiet=1,
        force=True,
        rx=re.compile(r"([\\/]\.venv|[\\/]venv|[\\/]\.git)"),
    )
    if not ok:
        fail("Python compilation failed")
    print("compileall: ok")


DISCLAIMER_CALL_RE = re.compile(r"disclaimer_embed\((.*?)\)", re.DOTALL)
FORBIDDEN_SPELLING_RE = re.compile(r"\b[Yy][Ff][Pp][Aa]\b|YFPA")
USG_MARKING_RE = re.compile(
    r"\bUNCLASSIFIED\b|\bCONFIDENTIAL\b|\bSECRET\b|CONTROLLED UNCLASSIFIED|\bCUI\b"
)
HERO_TITLE_RE = re.compile(
    r'title\s*=\s*"(PUBLIC INFORMATION|INFORMATION|STAFF DOCUMENTS|OPEN POSITIONS|'
    r'SECURITY PHASE PROGRAM|OFFICER TRAINING PROGRAM|CHAIN OF COMMAND|SERVER REGULATIONS)"'
)


def validate_style_guide() -> None:
    """Heuristic checks aligned with the Discord Embed Style Guide."""
    issues: list[str] = []

    for folder in ANNOUNCER_DIRS:
        for path in (ROOT / folder).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            rel = str(path.relative_to(ROOT)).replace("\\", "/")

            if FORBIDDEN_SPELLING_RE.search(text):
                issues.append(f"{rel}: forbidden spelling YFPA/Yfpa (use Yepa if needed)")
            if "BOT_OTE_ALT" in text:
                issues.append(f"{rel}: use BOT_OTE instead of BOT_OTE_ALT")
            if USG_MARKING_RE.search(text):
                issues.append(
                    f"{rel}: USG-style marking vocabulary found; use PUBLIC/STAFF/CANDIDATE"
                )

            for match in DISCLAIMER_CALL_RE.finditer(text):
                args = match.group(1)
                if "color=" not in args:
                    issues.append(f"{rel}: disclaimer_embed(...) must pass color=")

            if (
                HERO_TITLE_RE.search(text)
                and "hero_embed(" not in text
                and "chain_intro_embed(" not in text
            ):
                if path.name != "server_regulations.py":
                    issues.append(
                        f"{rel}: hero channel titles should use hero_embed(...) "
                        "(or chain_intro_embed for CoC)"
                    )

    common_text = COMMON.read_text(encoding="utf-8")
    if "def hero_embed" not in common_text or "def agency_eyebrow" not in common_text:
        issues.append("common/cia_common.py: missing hero_embed / agency_eyebrow helpers")
    if "def marking_note" not in common_text or "def command_band_label" not in common_text:
        issues.append(
            "common/cia_common.py: missing accessibility helpers (marking_note / command_band_label)"
        )
    if "def validate_embed_accessibility" not in common_text:
        issues.append("common/cia_common.py: missing validate_embed_accessibility")
    if not (ROOT / "docs" / "ACCESSIBILITY.md").is_file():
        issues.append("docs/ACCESSIBILITY.md: missing accessibility guidance for channel content")
    if "BOT_OTE_ALT" in common_text:
        issues.append("common/cia_common.py: remove BOT_OTE_ALT")
    if "allowed_mentions" not in common_text:
        issues.append("common/cia_common.py: webhook sends must set allowed_mentions=none()")

    branding = (ROOT / "config" / "branding.yaml").read_text(encoding="utf-8")
    if "ote_alt" in branding:
        issues.append("config/branding.yaml: remove ote_alt (use single OTE bot name)")

    common_eyebrow = COMMON.read_text(encoding="utf-8")
    if 'f"*Central Intelligence Agency · {unit}*"' in common_eyebrow:
        issues.append("common/cia_common.py: agency_eyebrow must not use bare CIA USG banner text")

    if issues:
        fail("Style-guide heuristics failed:\n  - " + "\n  - ".join(issues))
    print("Style guide: announcer heuristics passed")


def validate_ast_parse() -> int:
    count = 0
    for path in ROOT.rglob("*.py"):
        if any(part in {".venv", "venv", ".git", "__pycache__"} for part in path.parts):
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            fail(f"Syntax error in {path.relative_to(ROOT)}: {exc}")
        count += 1
    print(f"AST parse: {count} files ok")
    return count


def main() -> None:
    print(f"Validating repository at {ROOT}\n")
    validate_catalog()
    validate_webhooks()
    validate_logos()
    validate_secret_split()
    validate_mentions_and_logo_guards()
    validate_config()
    validate_url_keys()
    validate_brand_legal()
    validate_banners()
    validate_style_guide()
    validate_ast_parse()
    validate_compile()
    print("\nAll repository checks passed.")


if __name__ == "__main__":
    main()

# === FILE FOOTER ===
# End of file: tools/validate_repo.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
