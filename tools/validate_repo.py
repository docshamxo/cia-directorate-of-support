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
# === END FILE HEADER ===

"""
Validate repository consistency for the CIA DS announcer suite.

Checks:
  - run_all.py catalog paths exist
  - every require_webhook(...) key is declared in .env.example
  - every WEBHOOK_* key in .env.example is used by a script
  - required logo assets exist
  - Python sources compile

Run from repository root:
    python tools/validate_repo.py
"""

from __future__ import annotations

import ast
import compileall
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_ALL = ROOT / "run_all.py"
ENV_EXAMPLE = ROOT / ".env.example"
COMMON = ROOT / "common" / "cia_common.py"

WEBHOOK_RE = re.compile(r'require_webhook\(\s*["\'](WEBHOOK_[A-Z0-9_]+)["\']\s*\)')
ENV_KEY_RE = re.compile(r"^(WEBHOOK_[A-Z0-9_]+)=", re.MULTILINE)
CATALOG_RE = re.compile(r'\(\s*"([^"]+\.py)"\s*,\s*"([^"]+)"\s*\)')

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
)

HEADER_MARKER = "=== FILE HEADER ==="
FOOTER_MARKER = "=== FILE FOOTER ==="
SKIP_BANNER_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pyc"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def catalog_entries() -> list[tuple[str, str]]:
    text = RUN_ALL.read_text(encoding="utf-8")
    entries = CATALOG_RE.findall(text)
    if len(entries) < 1:
        fail("No announcer catalog entries found in run_all.py")
    return entries


def webhook_keys_in_code() -> set[str]:
    keys: set[str] = set()
    for path in ROOT.rglob("*.py"):
        if ".venv" in path.parts or "venv" in path.parts:
            continue
        if path.parts[0] == "tools" and path.name == "validate_repo.py":
            # Allow self-reference pattern text without treating docs strings specially
            pass
        text = path.read_text(encoding="utf-8")
        keys.update(WEBHOOK_RE.findall(text))
    return keys


def webhook_keys_in_env_example() -> set[str]:
    text = ENV_EXAMPLE.read_text(encoding="utf-8")
    return set(ENV_KEY_RE.findall(text))


def validate_catalog() -> int:
    entries = catalog_entries()
    print(f"Catalog entries: {len(entries)}")
    for relative, label in entries:
        path = ROOT / relative
        if not path.is_file():
            fail(f"Catalog path missing for {label}: {relative}")
    return len(entries)


def validate_webhooks() -> None:
    used = webhook_keys_in_code()
    declared = webhook_keys_in_env_example()

    # Ignore any accidental matches from this validator file
    used.discard("WEBHOOK_PLACEHOLDER")

    missing_env = sorted(used - declared)
    unused_env = sorted(declared - used)

    if missing_env:
        fail(
            "Webhook keys used in code but missing from .env.example: "
            + ", ".join(missing_env)
        )
    if unused_env:
        fail(
            "Webhook keys in .env.example but unused in code: "
            + ", ".join(unused_env)
        )

    print(f"Webhook keys: {len(declared)} (code and .env.example match)")


def validate_logos() -> None:
    if not COMMON.is_file():
        fail(f"Missing shared module: {COMMON.relative_to(ROOT)}")

    for key, path in REQUIRED_LOGOS.items():
        if not path.is_file():
            fail(f"Missing logo for '{key}': {path.relative_to(ROOT)}")

    print(f"Logos: {len(REQUIRED_LOGOS)} present")


def validate_config() -> None:
    for path in REQUIRED_CONFIG:
        if not path.is_file():
            fail(f"Missing config file: {path.relative_to(ROOT)}")

    try:
        import yaml  # noqa: F401
    except ImportError as exc:
        fail(f"PyYAML is required: {exc}")

    # Importing loads and validates YAML shape used by announcers.
    import sys

    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from common import cia_common as c

    _ = c.DS_MOTTO, c.AGENCY_EXECUTIVE, c.LOGOS, c.url("community.discord_invite")
    print(f"Config: {len(REQUIRED_CONFIG)} YAML files load successfully")


def validate_banners() -> None:
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
    validate_config()
    validate_banners()
    validate_ast_parse()
    validate_compile()
    print("\nAll repository checks passed.")


if __name__ == "__main__":
    main()

# === FILE FOOTER ===
# End of file: tools/validate_repo.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
