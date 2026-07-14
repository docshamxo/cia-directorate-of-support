# === FILE HEADER ===
# Title: Sync File Banners
# Path: tools/sync_file_banners.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
# === END FILE HEADER ===

"""
Apply or refresh the standard file header and footer on every text file.

Header includes: title, path, created date, created by, modification log.
Footer includes: end-of-file marker, path, maintained by.

Usage (from repository root):
    python tools/sync_file_banners.py
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CREATED_BY = "docshamxo"
MAINTAINED_BY = "docshamxo"

SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pyc"}
SKIP_DIR_PARTS = {".git", ".venv", "venv", "__pycache__", ".ruff_cache"}

HEADER_START = "=== FILE HEADER ==="
HEADER_END = "=== END FILE HEADER ==="
FOOTER_START = "=== FILE FOOTER ==="
FOOTER_END = "=== END FILE FOOTER ==="


def is_text_path(path: Path) -> bool:
    if path.suffix.lower() in SKIP_SUFFIXES:
        return False
    if any(part in SKIP_DIR_PARTS for part in path.parts):
        return False
    return True


def tracked_text_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    files: list[Path] = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        rel = raw.decode("utf-8")
        path = ROOT / rel
        if path.is_file() and is_text_path(path):
            files.append(path)
    return files


ACRONYMS = {
    "cia",
    "ds",
    "osec",
    "ote",
    "grs",
    "esd",
    "coc",
    "spp",
    "ci",
    "pr",
    "env",
}


def title_for(path: Path) -> str:
    stem = path.stem.replace("_", " ").replace("-", " ").strip()
    if path.name.upper() == "README.MD":
        parent = path.parent.name
        if parent in {".", ""} or path.parent == ROOT:
            return "README"
        parent_title = " ".join(
            part.upper() if part.lower() in ACRONYMS else part.capitalize()
            for part in parent.replace("_", " ").split()
        )
        return f"{parent_title} README"
    if path.name.upper() == "LICENSE":
        return "License"
    if path.name == ".env.example":
        return "Environment Example"
    if path.name == ".gitignore":
        return "Git Ignore"
    if path.name == ".editorconfig":
        return "Editor Config"
    words: list[str] = []
    for word in stem.split():
        lower = word.lower()
        if lower in ACRONYMS:
            words.append(lower.upper())
        elif word.isupper() and len(word) <= 6:
            words.append(word)
        else:
            words.append(word.capitalize())
    return " ".join(words)

def style_for(path: Path) -> str:
    suffix = path.suffix.lower()
    name = path.name.lower()
    if suffix == ".md":
        return "html"
    if suffix in {".py"}:
        return "hash"
    if suffix in {".yml", ".yaml", ".toml", ".txt", ".example"} or name in {
        ".gitignore",
        ".editorconfig",
        "ruff.toml",
        "requirements.txt",
        ".env.example",
    }:
        return "hash"
    if name.startswith(".") and suffix == "":
        return "hash"
    return "hash"


def git_created_date(rel: str) -> str:
    result = subprocess.run(
        ["git", "log", "--diff-filter=A", "--format=%ad", "--date=short", "--", rel],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if lines:
        return lines[-1]
    # Fall back to oldest commit touching the file.
    result = subprocess.run(
        ["git", "log", "--format=%ad", "--date=short", "--", rel],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return lines[-1] if lines else "2026-07-14"


def git_mod_log(rel: str) -> list[tuple[str, str]]:
    result = subprocess.run(
        ["git", "log", "--format=%ad|%s", "--date=short", "--", rel],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    entries: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for line in result.stdout.splitlines():
        if "|" not in line:
            continue
        date, message = line.split("|", 1)
        date = date.strip()
        message = message.strip()
        key = (date, message)
        if key in seen:
            continue
        seen.add(key)
        entries.append((date, message))
    entries.reverse()  # oldest first
    if not entries:
        entries.append((git_created_date(rel), "Initial creation"))
    return entries


def wrap_hash(lines: list[str]) -> str:
    return "\n".join(f"# {line}" if line else "#" for line in lines) + "\n"


def wrap_html(lines: list[str]) -> str:
    body = "\n".join(lines)
    return f"<!--\n{body}\n-->\n"


def build_header(rel: str, title: str, created: str, mod_log: list[tuple[str, str]]) -> list[str]:
    lines = [
        HEADER_START,
        f"Title: {title}",
        f"Path: {rel}",
        f"Created: {created}",
        f"Created by: {CREATED_BY}",
        "Modified:",
    ]
    for date, message in mod_log:
        lines.append(f"  - {date} | {CREATED_BY} | {message}")
    lines.append(HEADER_END)
    return lines


def build_footer(rel: str) -> list[str]:
    return [
        FOOTER_START,
        f"End of file: {rel}",
        f"Maintained by: {MAINTAINED_BY}",
        FOOTER_END,
    ]


def strip_existing(text: str, style: str) -> str:
    if style == "html":
        text = re.sub(
            r"<!--\s*" + re.escape(HEADER_START) + r".*?" + re.escape(HEADER_END) + r"\s*-->\s*",
            "",
            text,
            count=1,
            flags=re.S,
        )
        text = re.sub(
            r"\s*<!--\s*" + re.escape(FOOTER_START) + r".*?" + re.escape(FOOTER_END) + r"\s*-->\s*$",
            "\n",
            text,
            count=1,
            flags=re.S,
        )
        return text.lstrip("\n")

    # Hash comments
    text = re.sub(
        r"(?:^|\n)(?:#.*" + re.escape(HEADER_START) + r".*\n)(?:#.*\n)*?(?:#.*"
        + re.escape(HEADER_END)
        + r".*\n+)",
        "",
        text,
        count=1,
        flags=re.M,
    )
    text = re.sub(
        r"\n?(?:#.*" + re.escape(FOOTER_START) + r".*\n)(?:#.*\n)*?(?:#.*"
        + re.escape(FOOTER_END)
        + r".*\n*)\s*$",
        "\n",
        text,
        count=1,
        flags=re.M,
    )
    return text.lstrip("\n")


def apply_banners(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    style = style_for(path)
    original = path.read_text(encoding="utf-8-sig").replace("\ufeff", "")
    body = strip_existing(original, style).rstrip() + "\n"

    title = title_for(path)
    created = git_created_date(rel)
    mod_log = git_mod_log(rel)

    header_lines = build_header(rel, title, created, mod_log)
    footer_lines = build_footer(rel)

    if style == "html":
        header = wrap_html(header_lines)
        footer = wrap_html(footer_lines)
    else:
        header = wrap_hash(header_lines)
        footer = wrap_hash(footer_lines)

    # Keep a blank line between banner and body / footer.
    new_text = f"{header}\n{body.rstrip()}\n\n{footer}"
    if not new_text.endswith("\n"):
        new_text += "\n"

    if new_text == original:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    changed = 0
    for path in tracked_text_files():
        # Always include this script itself once tracked; while untracked, still ok.
        if apply_banners(path):
            print(f"updated {path.relative_to(ROOT).as_posix()}")
            changed += 1
    # Also apply to this tool if present on disk.
    self_path = Path(__file__).resolve()
    if self_path.is_file() and apply_banners(self_path):
        print(f"updated {self_path.relative_to(ROOT).as_posix()}")
        changed += 1
    print(f"Done. Updated {changed} file(s).")


if __name__ == "__main__":
    main()

# === FILE FOOTER ===
# End of file: tools/sync_file_banners.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
