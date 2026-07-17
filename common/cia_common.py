# === FILE HEADER ===
# Title: CIA Common
# Path: common/cia_common.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Add CI, Dependabot, and repository validation tooling.
#   - 2026-07-14 | docshamxo | Move editable data out of hardcoded Python into YAML config.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
#   - 2026-07-14 | docshamxo | Fix misleading CI badge and harden README presentation. (#7)
#   - 2026-07-15 | docshamxo | Add Google Drive links to unit staff documents. (#10)
#   - 2026-07-15 | docshamxo | Delete prior webhook messages via local message ID state.
#   - 2026-07-17 | docshamxo | Put CoC usernames on their own line to avoid Discord wrap glitches.
#   - 2026-07-17 | docshamxo | Track all prior IDs on purge; auto-react ✅ via bot token.
#   - 2026-07-17 | docshamxo | Community markings, staff overlay, safer purge, logo confine, mentions off.
#   - 2026-07-17 | docshamxo | Sibling-key purge, louder checkmark failures, bot channel cleanup option.
#   - 2026-07-17 | docshamxo | Safe console print for Windows cp1252 dry-run paths.
#   - 2026-07-17 | docshamxo | Weave Inter Studios property notice into disclaimer closers and footers.
#   - 2026-07-17 | docshamxo | Accessibility helpers: markings, command bands, emoji-only guard.
#   - 2026-07-17 | docshamxo | Public webhook-state helpers for empty-channel / IR recovery.
#   - 2026-07-17 | docshamxo | Soften hero eyebrow; community link labels; stronger disclaimer title.
#   - 2026-07-17 | docshamxo | Privacy: applicant env URLs, holders overlay, retention notes.
# === END FILE HEADER ===

"""
Shared Discord helpers and configuration loader for CIA DS announcers.

Editable data lives in config/*.yaml - not in this file:
  - config/branding.yaml      colors, bots, logos, community URLs
  - config/organization.yaml  mottos, about text, offices, disclaimers
  - config/personnel.yaml     chain-of-command names and ranks
  - config/personnel.holders.local.yaml  optional mid-tier roster overlay (gitignored)
  - config/links.yaml         public document / form / channel URLs
  - config/links.staff.local.yaml  optional staff Drive overlay (gitignored)
  - config/regulations.yaml   server regulations prose
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
import time
from collections.abc import Callable, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlparse

import discord
import requests
import yaml
from discord.errors import HTTPException
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"
ASSETS_DIR = REPO_ROOT / "assets"
LOGOS_DIR = ASSETS_DIR / "logos"
# Local-only message IDs for purge-before-repost (never commit; no webhook URLs stored).
# Retention: Discord snowflakes only — dispose by deleting this file when rotating
# webhooks, leaving the project, or clearing channel state. Not a durable audit log.
WEBHOOK_MESSAGES_PATH = REPO_ROOT / ".webhook_messages.json"
WEBHOOK_MESSAGES_LOCK_PATH = REPO_ROOT / ".webhook_messages.lock"

load_dotenv(REPO_ROOT / ".env")

logger = logging.getLogger("cia.common")

WEBHOOK_URL_RE = re.compile(
    r"^https://(?:canary\.|ptb\.)?(?:discord|discordapp)\.com/api/webhooks/\d+/[\w-]+/?$",
    re.IGNORECASE,
)
DEFAULT_HTTP_TIMEOUT = 30.0
MAX_SEND_ATTEMPTS = 5
DISCORD_API_BASE = "https://discord.com/api/v10"
# U+2705 WHITE HEAVY CHECK MARK — applied to every successful webhook post.
CHECKMARK_REACTION = "\u2705"
BOT_TOKEN_ENV = "DISCORD_BOT_TOKEN"
DISCORD_INVITE_ENV = "DISCORD_INVITE_URL"
OSEC_RESULTS_ENV = "DISCORD_OSEC_APPLICATION_RESULTS_URL"
OSEC_LOWCOM_APP_ENV = "OSEC_LOWCOM_APPLICATION_URL"
OSEC_MIDCOM_APP_ENV = "OSEC_MIDCOM_APPLICATION_URL"
OTE_APPLICATION_ENV = "OTE_APPLICATION_URL"
OTE_APPLICATION_TRACKER_ENV = "OTE_APPLICATION_TRACKER_URL"
STAFF_PLACEHOLDER_MARKER = "STAFF_LOCAL_REQUIRED"

# Optional: after post, bot deletes other recent webhook messages in the channel
# (requires Manage Messages + Read Message History). Set CIA_BOT_CHANNEL_PURGE=1.
BOT_CHANNEL_PURGE_ENV = "CIA_BOT_CHANNEL_PURGE"
BOT_CHANNEL_PURGE_LIMIT = 50
MAX_DELETE_ATTEMPTS = 5

# Discord embed limits (preflight).
EMBED_TITLE_LIMIT = 256
EMBED_DESCRIPTION_LIMIT = 4096
EMBED_FIELD_NAME_LIMIT = 256
EMBED_FIELD_VALUE_LIMIT = 1024
EMBED_FOOTER_LIMIT = 2048
EMBEDS_PER_MESSAGE_LIMIT = 10


def console_print(message: str) -> None:
    """Print to stdout without crashing on narrow Windows console encodings."""
    try:
        print(message)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", None) or "ascii"
        print(message.encode(encoding, errors="replace").decode(encoding, errors="replace"))


def require_webhook(env_key: str) -> str:
    """Load a Discord webhook URL from the environment / .env file."""
    value = os.environ.get(env_key, "").strip()
    if not value:
        raise RuntimeError(
            f"Missing {env_key}. Copy .env.example to .env and set your webhook URLs."
        )
    validate_webhook_url(value)
    return value


def validate_webhook_url(webhook_url: str) -> None:
    """Reject non-Discord webhook URLs without echoing the secret token."""
    if not WEBHOOK_URL_RE.match(webhook_url.strip()):
        raise ValueError(
            "Invalid Discord webhook URL shape "
            "(expected https://discord.com/api/webhooks/<id>/<token>)"
        )


def webhook_application_id(webhook_url: str) -> str:
    """Extract the webhook snowflake ID from a Discord webhook URL."""
    parsed = urlparse(webhook_url.strip())
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) >= 3 and parts[0] == "api" and parts[1] == "webhooks":
        return parts[2]
    raise ValueError("Cannot extract webhook ID from URL")


def mask_webhook_url(webhook_url: str) -> str:
    """Return a log-safe webhook URL with the token redacted."""
    try:
        webhook_id = webhook_application_id(webhook_url)
        parsed = urlparse(webhook_url.strip())
        return f"{parsed.scheme}://{parsed.netloc}/api/webhooks/{webhook_id}/***"
    except Exception:
        pass
    return "https://discord.com/api/webhooks/***"


def sibling_webhook_state_keys(webhook_url: str, primary_key: str) -> list[str]:
    """Return all WEBHOOK_* env keys that currently point at the same webhook ID.

    Two announcers sharing one Discord webhook (same URL / ID) must purge each
    other's recorded message IDs — otherwise prior posts accumulate in-channel.
    """
    try:
        target_id = webhook_application_id(webhook_url)
    except ValueError:
        return [primary_key]

    keys = [primary_key]
    seen = {primary_key}
    for key, value in os.environ.items():
        if not key.startswith("WEBHOOK_") or key in seen:
            continue
        candidate = (value or "").strip()
        if not candidate:
            continue
        try:
            if webhook_application_id(candidate) == target_id:
                keys.append(key)
                seen.add(key)
        except ValueError:
            continue
    return keys


def collect_prior_message_ids(
    state: dict[str, list[int]],
    state_keys: Sequence[str],
) -> list[int]:
    """Merge recorded message IDs across related state keys (order-preserving)."""
    merged: list[int] = []
    for key in state_keys:
        merged.extend(state.get(key, []))
    return _unique_message_ids(merged)


def find_duplicate_webhook_keys(
    env: dict[str, str] | None = None,
) -> dict[str, list[str]]:
    """Map webhook application ID to WEBHOOK_* keys that share that ID."""
    source = env if env is not None else dict(os.environ)
    by_id: dict[str, list[str]] = {}
    for key, value in sorted(source.items()):
        if not key.startswith("WEBHOOK_"):
            continue
        candidate = (value or "").strip()
        if not candidate:
            continue
        try:
            wid = webhook_application_id(candidate)
        except ValueError:
            continue
        by_id.setdefault(wid, []).append(key)
    return {wid: keys for wid, keys in by_id.items() if len(keys) > 1}


def is_staff_placeholder(value: str) -> bool:
    return STAFF_PLACEHOLDER_MARKER in value or "example.invalid" in value


def _deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = dict(base)
    for key, value in overlay.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _load_yaml(name: str) -> dict[str, Any]:
    path = CONFIG_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"Missing config file: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Config file must contain a mapping: {path}")
    return data


@lru_cache(maxsize=1)
def _branding() -> dict[str, Any]:
    return _load_yaml("branding.yaml")


@lru_cache(maxsize=1)
def _organization() -> dict[str, Any]:
    return _load_yaml("organization.yaml")


@lru_cache(maxsize=1)
def _personnel() -> dict[str, Any]:
    data = _load_yaml("personnel.yaml")
    local_path = CONFIG_DIR / "personnel.holders.local.yaml"
    if local_path.is_file():
        overlay = yaml.safe_load(local_path.read_text(encoding="utf-8"))
        if isinstance(overlay, dict):
            for key, value in overlay.items():
                data[key] = value
            logger.debug("Merged personnel holders overlay from %s", local_path.name)
        else:
            logger.warning("%s is not a mapping; ignoring", local_path.name)
    return data


@lru_cache(maxsize=1)
def _links() -> dict[str, Any]:
    data = _load_yaml("links.yaml")
    local_path = CONFIG_DIR / "links.staff.local.yaml"
    if local_path.is_file():
        overlay = yaml.safe_load(local_path.read_text(encoding="utf-8"))
        if isinstance(overlay, dict):
            data = _deep_merge(data, overlay)
            logger.debug("Merged staff link overlay from %s", local_path.name)
        else:
            logger.warning("%s is not a mapping; ignoring", local_path.name)
    return data


@lru_cache(maxsize=1)
def _regulations() -> dict[str, Any]:
    return _load_yaml("regulations.yaml")


def _parse_color(value: str | int) -> int:
    if isinstance(value, int):
        return value
    text = str(value).strip()
    if text.lower().startswith("0x"):
        return int(text, 16)
    if text.startswith("#"):
        return int(text[1:], 16)
    return int(text)


def url(path: str) -> str:
    """
    Look up a URL (or other string value) from config/links.yaml (+ staff overlay).

    Example: url(\"osec.information.handbook\")
    """
    node: Any = _links()
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            raise KeyError(f"Unknown links config path: {path}")
        node = node[part]
    if not isinstance(node, str) or not node.strip():
        raise ValueError(f"links.{path} must be a non-empty string")
    return node.strip()


def require_resolved_url(path: str) -> str:
    """Like url(), but fails closed when the value is still a staff placeholder."""
    value = url(path)
    if is_staff_placeholder(value):
        raise RuntimeError(
            f"Staff link '{path}' is unresolved (still a placeholder). "
            "Copy config/links.staff.example.yaml to config/links.staff.local.yaml "
            "and set real Drive/document URLs."
        )
    return value


def env_url(env_key: str, *, required: bool = True) -> str:
    """Load a URL from the environment (Discord invite, channel links, etc.)."""
    value = os.environ.get(env_key, "").strip()
    if not value:
        if required:
            raise RuntimeError(f"Missing {env_key}. Copy .env.example to .env and set the value.")
        return ""
    return value


def _get_org(*parts: str) -> Any:
    node: Any = _organization()
    for part in parts:
        node = node[part]
    return node


# ── Branding ──────────────────────────────────────────────────────────────────

_b = _branding()
_colors = _b["colors"]
_bots = _b["bots"]
_logo_files = _b["logos"]

COLOR_DS = _parse_color(_colors["ds"])
COLOR_OSEC = _parse_color(_colors["osec"])
COLOR_OTE = _parse_color(_colors["ote"])
COLOR_GRS = _parse_color(_colors["grs"])
COLOR_ESD = _parse_color(_colors["esd"])

BOT_DS = _bots["ds"]
BOT_OSEC = _bots["osec"]
BOT_OTE = _bots["ote"]
BOT_GRS = _bots["grs"]
BOT_ESD = _bots["esd"]


def confined_logo_path(filename: str | Path) -> Path:
    """Resolve a logo filename strictly under assets/logos (reject .. / absolutes)."""
    text = str(filename)
    if "/" in text or "\\" in text or text.startswith("~"):
        raise ValueError(f"Logo path must be a bare filename under assets/logos, got: {filename!r}")
    raw = Path(text)
    if raw.is_absolute() or len(raw.parts) != 1 or raw.parts[0] in {".", ".."}:
        raise ValueError(f"Logo path must be a filename under assets/logos, got: {filename!r}")
    logos_root = LOGOS_DIR.resolve()
    candidate = (LOGOS_DIR / raw.name).resolve()
    try:
        candidate.relative_to(logos_root)
    except ValueError as exc:
        raise ValueError(f"Logo path escapes assets/logos: {filename!r}") from exc
    return candidate


LOGOS = {key: confined_logo_path(filename) for key, filename in _logo_files.items()}

URL_ROBLOX_GROUP_DS = url("community.roblox_group_ds")
URL_ROBLOX_GROUP_OSEC = url("community.roblox_group_osec")
URL_ROBLOX_GROUP_GRS = url("community.roblox_group_grs")
URL_ROBLOX_GROUP_OTE = url("community.roblox_group_ote")


def discord_invite_url() -> str:
    """Community Discord invite from env (not committed in public YAML)."""
    return env_url(DISCORD_INVITE_ENV, required=True)


def osec_application_results_url() -> str:
    """OSEC application-results channel URL from env."""
    return env_url(OSEC_RESULTS_ENV, required=True)


def osec_lowcom_application_url() -> str:
    """OSEC LOWCOM Google Form URL from env (applicant intake)."""
    return env_url(OSEC_LOWCOM_APP_ENV, required=True)


def osec_midcom_application_url() -> str:
    """OSEC MIDCOM Google Form URL from env (applicant intake)."""
    return env_url(OSEC_MIDCOM_APP_ENV, required=True)


def ote_application_url() -> str:
    """OTE Professor application form URL from env (applicant intake)."""
    return env_url(OTE_APPLICATION_ENV, required=True)


def ote_application_tracker_url(*, required: bool = False) -> str:
    """OTE applicant tracker spreadsheet URL from env (staff/ops only).

    Do not embed this in public open-positions posts — tracker sheets hold
    applicant status and other PII-adjacent fields.
    """
    return env_url(OTE_APPLICATION_TRACKER_ENV, required=required)


# ── Organization copy ─────────────────────────────────────────────────────────

DS_MOTTO = _get_org("ds", "motto")
DS_CLASSIFICATION = _get_org("ds", "classification")
DS_ABOUT = _get_org("ds", "about")
DS_OFFICES = tuple(_get_org("ds", "offices"))

OSEC_MOTTO = _get_org("osec", "motto")
OSEC_ABOUT = _get_org("osec", "about")
OSEC_SUB_UNITS = tuple(_get_org("osec", "sub_units"))

OTE_MOTTO = _get_org("ote", "motto")
OTE_ABOUT = _get_org("ote", "about")
OTE_PILLARS = tuple((item["title"], item["description"]) for item in _get_org("ote", "pillars"))

GRS_ABOUT = _get_org("grs", "about")
ESD_ABOUT = _get_org("esd", "about")

_copy = _get_org("copy")
CHAIN_OF_COMMAND_INTRO = _copy["chain_of_command_intro"]
AFFILIATION_NOTICE = _copy.get(
    "affiliation_notice",
    (
        "**Unofficial community roleplay.** Not affiliated with the United States Government "
        "or the Central Intelligence Agency."
    ),
)
PROPERTY_NOTICE = str(
    _copy.get(
        "property_notice",
        "Property of the Central Intelligence Agency (ROBLOX), Inter Studios",
    )
).strip()
DISCLAIMER_TEXT = _copy["disclaimer"]
DISCLAIMER_LINKS_TEXT = _copy["disclaimer_links"]
DISCLAIMER_STAFF_TEXT = _copy.get("disclaimer_staff") or _copy.get(
    "disclaimer_classified", DISCLAIMER_TEXT
)
IMPORTANT_NOTICE_TEMPLATE = _copy["important_notice"]
STAFF_HANDLING_NOTICE = _copy["staff_handling_notice"]
STAFF_HANDLING_NOTICE_RESTRICTED = _copy.get("staff_handling_notice_restricted") or _copy.get(
    "staff_handling_notice_secret", STAFF_HANDLING_NOTICE
)
MARKING_PUBLIC = _copy.get("marking_public", "Marking: PUBLIC.")
MARKING_STAFF = _copy.get("marking_staff", "Marking: STAFF.")
MARKING_CANDIDATE = _copy.get("marking_candidate", "Marking: CANDIDATE.")

# ── Personnel ─────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Role:
    """A single position in the chain of command."""

    abbrev: str
    title: str
    holder: str

    def format(self) -> str:
        # Username on its own line so Discord embed wrapping does not split
        # "Title - username" awkwardly across lines for long role titles.
        return f"**[{self.abbrev}] {self.title}**\n→ {self.holder}"


@dataclass(frozen=True, slots=True)
class Rank:
    """A rank title without an assigned holder."""

    abbrev: str
    title: str

    def format(self) -> str:
        return f"**[{self.abbrev}] {self.title}**"


def _roles(key: str) -> tuple[Role, ...]:
    return tuple(Role(item["abbrev"], item["title"], item["holder"]) for item in _personnel()[key])


def _ranks(key: str) -> tuple[Rank, ...]:
    return tuple(Rank(item["abbrev"], item["title"]) for item in _personnel()[key])


AGENCY_EXECUTIVE = _roles("agency_executive")
DS_LEADERSHIP = _roles("ds_leadership")
OTE_HIGH_COMMAND = _roles("ote_high_command")
OTE_STAFF_RANKS = _ranks("ote_staff_ranks")
OSEC_HIGH_COMMAND = _roles("osec_high_command")
OSEC_MAIN_CHIEF_MARSHALS = _roles("osec_main_chief_marshals")
GRS_COMMAND = _roles("grs_command")
ESD_COMMAND = _roles("esd_command")
OSEC_MIDDLE_COMMAND = _ranks("osec_middle_command")
OSEC_LOW_COMMAND = _ranks("osec_low_command")
GRS_ESD_LOW_COMMAND = _ranks("grs_esd_low_command")
GRS_ESD_MIDDLE_COMMAND = _ranks("grs_esd_middle_command")

# ── Formatting helpers ────────────────────────────────────────────────────────


def roles_text(*roles: Role) -> str:
    return "\n".join(role.format() for role in roles)


def ranks_text(*ranks: Rank) -> str:
    return "\n".join(rank.format() for rank in ranks)


def bullets(*items: str) -> str:
    return "\n".join(f"**{item}**" for item in items)


def link(label: str, url_value: str) -> str:
    return f"[{label}]({url_value})"


def link_field(name: str, label: str, url_value: str, note: str | None = None) -> tuple[str, str]:
    value = link(label, url_value)
    if note:
        value += f"\n*{note}*"
    return (name, value)


def pillar_field(title: str, description: str) -> tuple[str, str]:
    return (title, description)


# ── Accessibility / inclusive design ──────────────────────────────────────────

# Discord embed sidebar color is decorative only (not announced by screen readers).
# Always pair unit color with explicit unit / marking / status text.
COMMAND_BAND_LABELS: dict[str, str] = {
    "LOWCOM": "Lower Command (LOWCOM)",
    "MIDCOM": "Middle Command (MIDCOM)",
    "HIGHCOM": "High Command (HIGHCOM)",
}

# Strip common emoji / symbol ranges when checking for a text signal.
_EMOJI_SYMBOL_RE = re.compile(
    "["
    "\U0001f300-\U0001faff"  # Misc. pictographs, symbols, extended
    "\U00002700-\U000027bf"  # Dingbats
    "\U00002600-\U000026ff"  # Misc. symbols
    "\U0000fe00-\U0000fe0f"  # Variation selectors
    "\U0000200d"  # ZWJ
    "\U0000200b-\U0000200f"  # Zero-width / direction marks
    "]+",
    flags=re.UNICODE,
)
_TEXT_SIGNAL_RE = re.compile(r"[A-Za-z0-9]")


def command_band_label(band: str) -> str:
    """Expand LOWCOM/MIDCOM/HIGHCOM so abbreviations are not the only signal."""
    key = band.strip().upper()
    return COMMAND_BAND_LABELS.get(key, band.strip())


def marking_note(marking: str, extra: str | None = None) -> str:
    """Community marking as readable text (never color-only sensitivity)."""
    text = f"Marking: {marking.strip().upper()}."
    if extra:
        text = f"{text} {extra.strip()}"
    return text


def has_text_signal(value: str) -> bool:
    """True when value still has letters/digits after removing emoji/symbols."""
    if not value or not value.strip():
        return False
    cleaned = _EMOJI_SYMBOL_RE.sub("", value)
    return bool(_TEXT_SIGNAL_RE.search(cleaned))


def validate_embed_accessibility(embeds: Sequence[discord.Embed]) -> None:
    """Reject emoji-only titles/field names that hide meaning from screen readers."""
    issues: list[str] = []
    for index, item in enumerate(embeds, start=1):
        title = item.title or ""
        if title and not has_text_signal(title):
            issues.append(f"embed {index} title is emoji/symbol-only (no text alternative)")
        for field_index, field in enumerate(item.fields, start=1):
            if field.name and not has_text_signal(field.name):
                issues.append(
                    f"embed {index} field {field_index} name is emoji/symbol-only "
                    "(critical info needs words, not emoji alone)"
                )
            if field.value and not has_text_signal(field.value):
                issues.append(
                    f"embed {index} field {field_index} value is emoji/symbol-only "
                    "(provide a text alternative)"
                )
    if issues:
        raise ValueError("Discord embed accessibility check failed:\n  - " + "\n  - ".join(issues))


def agency_eyebrow(unit: str) -> str:
    """Italic hero eyebrow: community RP framing + unit (not an official USG banner)."""
    return f"*Unofficial community RP · {unit}*"


def community_link_label(name: str) -> str:
    """Discord link text that stays RP-clear without looking like an official agency hyperlink."""
    return f"DS Community | {name}"


def motto_line(motto: str, *, classification: str | None = None) -> str:
    """Italic motto line, optionally with community marking."""
    if classification:
        return f"*{motto} · Marking: {classification}*"
    return f"*{motto}*"


def pending_group_field(name: str, label: str) -> tuple[str, str]:
    """Community link placeholder when a Roblox group is not yet available."""
    return (name, f"*{label} — coming soon.*")


# ── Embed helpers ─────────────────────────────────────────────────────────────


def logo_file(path: Path) -> discord.File:
    confined = confined_logo_path(path.name if path.parent == LOGOS_DIR else path)
    if path.resolve() != confined and path.name:
        # Allow pre-resolved LOGOS entries; still confine by filename.
        confined = confined_logo_path(path.name)
    if not confined.is_file():
        raise FileNotFoundError(f"Missing logo file: {confined}")
    return discord.File(confined, filename=confined.name)


def set_logo(embed: discord.Embed, path: Path) -> None:
    embed.set_thumbnail(url=f"attachment://{path.name}")


def apply_effective_date_footer(
    embeds: Sequence[discord.Embed], *, when: date | None = None
) -> None:
    """Stamp an effective-date footer on the last embed (mutates in place)."""
    if not embeds:
        return
    stamp = when or date.today()
    footer = f"Effective {stamp.isoformat()} (community roleplay)"
    if PROPERTY_NOTICE:
        footer = f"{footer} · {PROPERTY_NOTICE}"
    embeds[-1].set_footer(text=footer)


def embed(
    *,
    description: str,
    title: str | None = None,
    color: int = COLOR_DS,
    logo: Path | None = None,
    fields: tuple[tuple[str, str], ...] = (),
) -> discord.Embed:
    result = discord.Embed(description=description, color=color)
    if title:
        result.title = title
    if logo:
        set_logo(result, logo)
    for name, value in fields:
        result.add_field(name=name, value=value, inline=False)
    return result


def hero_embed(
    *,
    title: str,
    unit: str,
    supporting: str,
    color: int = COLOR_DS,
    logo: Path | None = None,
) -> discord.Embed:
    """ALL CAPS hero title + italic community-RP eyebrow + short supporting sentence."""
    return embed(
        title=title,
        description=f"{agency_eyebrow(unit)}\n\n{supporting}",
        color=color,
        logo=logo,
    )


def disclaimer_embed(
    *,
    classified: bool = False,
    staff: bool = False,
    links: bool = False,
    color: int = COLOR_DS,
) -> discord.Embed:
    if classified or staff:
        text = DISCLAIMER_STAFF_TEXT
    elif links:
        text = DISCLAIMER_LINKS_TEXT
    else:
        text = DISCLAIMER_TEXT
    if "not affiliated" not in text.lower():
        text = f"{AFFILIATION_NOTICE}\n\n{text}"
    if PROPERTY_NOTICE and PROPERTY_NOTICE not in text:
        text = f"{text.rstrip()}\n\n**{PROPERTY_NOTICE}**"
    return embed(title="Disclaimer · Unofficial Community", description=text, color=color)


def chain_intro_embed(
    *,
    unit: str,
    color: int = COLOR_DS,
    context: str | None = None,
    logo: Path | None = None,
) -> discord.Embed:
    description = f"{agency_eyebrow(unit)}\n\n"
    if context:
        description += f"{context}\n\n"
    description += CHAIN_OF_COMMAND_INTRO
    return embed(title="CHAIN OF COMMAND", description=description, color=color, logo=logo)


def important_notice_embed(
    *,
    unit: str,
    color: int = COLOR_DS,
    parent_units: tuple[str, ...] = (),
) -> discord.Embed:
    chain = "**, **".join(parent_units + (unit,))
    description = IMPORTANT_NOTICE_TEMPLATE.format(unit=unit, chain=chain)
    return embed(
        title="Important Notice",
        description=description,
        color=color,
    )


def classification_handling_embed(
    *,
    unit: str,
    authority: str = "CIA Directorate of Support",
    color: int = COLOR_DS,
    secret: bool = False,
    restricted: bool = False,
) -> discord.Embed:
    use_restricted = restricted or secret
    template = STAFF_HANDLING_NOTICE_RESTRICTED if use_restricted else STAFF_HANDLING_NOTICE
    return embed(
        title="Classification & Handling Notice",
        description=template.format(unit=unit, authority=authority),
        color=color,
    )


def server_regulations_embeds() -> list[discord.Embed]:
    """Build DS server regulations embeds from config/regulations.yaml."""
    data = _regulations()
    intro = str(data["intro"]).format(
        eyebrow=agency_eyebrow("Directorate of Support"),
        motto=DS_MOTTO,
        classification=DS_CLASSIFICATION,
    )
    embeds = [
        embed(
            title=str(data.get("title", "SERVER REGULATIONS")),
            description=intro,
            logo=LOGOS["ds"],
        )
    ]
    for section in data.get("sections", []):
        title = section.get("title")
        embeds.append(
            embed(
                title=str(title) if title else None,
                description=str(section["body"]),
            )
        )
    embeds.append(disclaimer_embed(color=COLOR_DS))
    return embeds


def validate_embed_limits(embeds: Sequence[discord.Embed]) -> None:
    """Raise ValueError if embeds exceed Discord field limits or a11y basics."""
    if len(embeds) > EMBEDS_PER_MESSAGE_LIMIT:
        raise ValueError(
            f"Discord allows at most {EMBEDS_PER_MESSAGE_LIMIT} embeds per message; "
            f"got {len(embeds)}"
        )
    issues: list[str] = []
    for index, item in enumerate(embeds, start=1):
        title = item.title or ""
        if len(title) > EMBED_TITLE_LIMIT:
            issues.append(f"embed {index} title length {len(title)} > {EMBED_TITLE_LIMIT}")
        description = item.description or ""
        if len(description) > EMBED_DESCRIPTION_LIMIT:
            issues.append(
                f"embed {index} description length {len(description)} > {EMBED_DESCRIPTION_LIMIT}"
            )
        footer = item.footer.text if item.footer else ""
        if footer and len(footer) > EMBED_FOOTER_LIMIT:
            issues.append(f"embed {index} footer length {len(footer)} > {EMBED_FOOTER_LIMIT}")
        for field_index, field in enumerate(item.fields, start=1):
            if len(field.name) > EMBED_FIELD_NAME_LIMIT:
                issues.append(
                    f"embed {index} field {field_index} name length "
                    f"{len(field.name)} > {EMBED_FIELD_NAME_LIMIT}"
                )
            if len(field.value) > EMBED_FIELD_VALUE_LIMIT:
                issues.append(
                    f"embed {index} field {field_index} value length "
                    f"{len(field.value)} > {EMBED_FIELD_VALUE_LIMIT}"
                )
    if issues:
        raise ValueError("Discord embed limit check failed:\n  - " + "\n  - ".join(issues))
    validate_embed_accessibility(embeds)


def _session_with_timeout(timeout: float = DEFAULT_HTTP_TIMEOUT) -> requests.Session:
    session = requests.Session()
    original_request = session.request

    def request_with_timeout(method: str, url: str, **kwargs: Any) -> requests.Response:
        kwargs.setdefault("timeout", timeout)
        return original_request(method, url, **kwargs)

    session.request = request_with_timeout  # type: ignore[method-assign]
    return session


def _retry_after_seconds(exc: HTTPException, attempt: int) -> float:
    retry_after = getattr(exc, "retry_after", None)
    if isinstance(retry_after, int | float) and retry_after > 0:
        return float(retry_after)
    response = getattr(exc, "response", None)
    if response is not None:
        header = response.headers.get("Retry-After")
        if header:
            try:
                return float(header)
            except ValueError:
                pass
    return min(2**attempt, 30)


@contextmanager
def _webhook_state_lock(timeout: float = 30.0):
    """Best-effort exclusive lock around .webhook_messages.json read/write."""
    lock_path = WEBHOOK_MESSAGES_LOCK_PATH
    deadline = time.time() + timeout
    fd: int | None = None
    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode("ascii", errors="ignore"))
            break
        except FileExistsError:
            if time.time() >= deadline:
                raise TimeoutError(f"Timed out waiting for {lock_path.name}") from None
            # Stale lock recovery: if older than 2 minutes, remove and retry.
            try:
                age = time.time() - lock_path.stat().st_mtime
                if age > 120:
                    lock_path.unlink(missing_ok=True)
                    continue
            except OSError:
                pass
            time.sleep(0.05)
    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
        try:
            lock_path.unlink(missing_ok=True)
        except OSError:
            pass


def _load_webhook_message_state() -> dict[str, list[int]]:
    """Load local webhook message ID state (message IDs only; never URLs)."""
    path = WEBHOOK_MESSAGES_PATH
    if not path.is_file():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("Could not read %s (%s); starting with empty state", path.name, exc)
        return {}
    if not isinstance(raw, dict):
        logger.warning("%s is not a JSON object; starting with empty state", path.name)
        return {}

    state: dict[str, list[int]] = {}
    for key, value in raw.items():
        if not isinstance(key, str):
            continue
        if isinstance(value, list):
            ids: list[int] = []
            for item in value:
                try:
                    ids.append(int(item))
                except (TypeError, ValueError):
                    continue
            state[key] = ids
        elif isinstance(value, (int, str)):
            try:
                state[key] = [int(value)]
            except (TypeError, ValueError):
                continue
    return state


def _save_webhook_message_state(state: dict[str, list[int]]) -> None:
    """Persist message IDs atomically. Does not store webhook URLs or tokens."""
    path = WEBHOOK_MESSAGES_PATH
    payload = {key: [int(mid) for mid in ids] for key, ids in sorted(state.items()) if ids}
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(text, encoding="utf-8")
    tmp_path.replace(path)


def load_webhook_message_state() -> dict[str, list[int]]:
    """Public read of local message ID state (locked). Never includes webhook URLs."""
    with _webhook_state_lock():
        return _load_webhook_message_state()


def clear_webhook_message_state(state_key: str | None = None) -> int:
    """Clear one key or the entire local message ID file.

    Returns the number of keys removed. Does not call Discord.
    """
    with _webhook_state_lock():
        state = _load_webhook_message_state()
        if state_key is None:
            removed = len(state)
            if WEBHOOK_MESSAGES_PATH.is_file():
                WEBHOOK_MESSAGES_PATH.unlink()
                logger.info("Removed webhook message state file (%s key(s))", removed)
            return removed
        if state_key not in state:
            return 0
        state.pop(state_key, None)
        if state:
            _save_webhook_message_state(state)
        elif WEBHOOK_MESSAGES_PATH.is_file():
            WEBHOOK_MESSAGES_PATH.unlink()
        logger.info("Cleared webhook message state for %s", state_key)
        return 1


def _unique_message_ids(ids: list[int]) -> list[int]:
    """Preserve order while dropping duplicate message IDs."""
    seen: set[int] = set()
    ordered: list[int] = []
    for message_id in ids:
        if message_id in seen:
            continue
        seen.add(message_id)
        ordered.append(message_id)
    return ordered


def _bot_token() -> str:
    return os.environ.get(BOT_TOKEN_ENV, "").strip()


def _message_channel_id(message: Any) -> int | None:
    """Extract channel snowflake from a webhook wait=True message object."""
    channel_id = getattr(message, "channel_id", None)
    if channel_id is not None:
        try:
            return int(channel_id)
        except (TypeError, ValueError):
            pass
    channel = getattr(message, "channel", None)
    if channel is not None:
        raw = getattr(channel, "id", channel)
        try:
            return int(raw)
        except (TypeError, ValueError):
            return None
    return None


def _delete_webhook_messages(
    webhook: Any,
    *,
    state_key: str,
    message_ids: list[int],
) -> list[int]:
    """Best-effort delete of the given message IDs. Returns IDs that remain."""
    prior_ids = _unique_message_ids(list(message_ids))
    if not prior_ids:
        return []

    deleted = 0
    remaining: list[int] = []
    for message_id in prior_ids:
        deleted_ok = False
        last_status: int | None = None
        for attempt in range(1, MAX_DELETE_ATTEMPTS + 1):
            try:
                webhook.delete_message(message_id)
                deleted_ok = True
                break
            except HTTPException as exc:
                status = getattr(exc, "status", None)
                last_status = status if isinstance(status, int) else None
                if status == 404:
                    deleted_ok = True
                    break
                if status == 429 and attempt < MAX_DELETE_ATTEMPTS:
                    delay = _retry_after_seconds(exc, attempt)
                    logger.warning(
                        "Rate-limited deleting prior message %s for %s "
                        "(attempt %s/%s); sleeping %.1fs",
                        message_id,
                        state_key,
                        attempt,
                        MAX_DELETE_ATTEMPTS,
                        delay,
                    )
                    time.sleep(delay)
                    continue
                if isinstance(status, int) and status >= 500 and attempt < MAX_DELETE_ATTEMPTS:
                    delay = min(2**attempt, 30)
                    logger.warning(
                        "Server error deleting prior message %s for %s "
                        "(HTTP %s, attempt %s/%s); sleeping %.1fs",
                        message_id,
                        state_key,
                        status,
                        attempt,
                        MAX_DELETE_ATTEMPTS,
                        delay,
                    )
                    time.sleep(delay)
                    continue
                break
            except (requests.Timeout, requests.ConnectionError) as exc:
                if attempt < MAX_DELETE_ATTEMPTS:
                    delay = min(2**attempt, 30)
                    logger.warning(
                        "Network error deleting prior message %s for %s "
                        "(attempt %s/%s): %s; sleeping %.1fs",
                        message_id,
                        state_key,
                        attempt,
                        MAX_DELETE_ATTEMPTS,
                        exc,
                        delay,
                    )
                    time.sleep(delay)
                    continue
                logger.warning(
                    "Network error deleting prior message %s for %s: %s",
                    message_id,
                    state_key,
                    exc,
                )
                break

        if deleted_ok:
            deleted += 1
        else:
            logger.warning(
                "Could not delete prior message %s for %s (HTTP %s)",
                message_id,
                state_key,
                last_status,
            )
            remaining.append(message_id)

    remaining = _unique_message_ids(remaining)
    if deleted:
        console_print(f"Cleared {deleted} prior webhook message(s) for {state_key}")
        logger.info("Cleared %s prior webhook message(s) for %s", deleted, state_key)
    if remaining:
        print(
            f"Warning: {len(remaining)} prior message(s) for {state_key} could not be "
            "deleted (wrong webhook, missing Manage Messages, or already gone). "
            "See OPS.md / tools/diagnose_webhook_state.py."
        )
    return remaining


def _bot_channel_purge_enabled() -> bool:
    return os.environ.get(BOT_CHANNEL_PURGE_ENV, "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _bot_cleanup_channel_webhook_messages(
    session: requests.Session,
    *,
    bot_token: str,
    channel_id: int,
    keep_message_ids: set[int],
    state_key: str,
    limit: int = BOT_CHANNEL_PURGE_LIMIT,
) -> int:
    """Delete recent webhook-authored messages in a channel except keep IDs.

    Requires Manage Messages and Read Message History. Only webhook messages.
    """
    headers = {"Authorization": f"Bot {bot_token}"}
    list_url = f"{DISCORD_API_BASE}/channels/{channel_id}/messages?limit={min(max(limit, 1), 100)}"
    try:
        response = session.get(list_url, headers=headers)
    except (requests.Timeout, requests.ConnectionError) as exc:
        logger.warning("Bot channel cleanup skipped for %s (list failed): %s", state_key, exc)
        return 0

    if response.status_code == 403:
        print(
            f"Warning: bot cannot list/delete messages in channel {channel_id} "
            f"for {state_key} - grant Manage Messages + Read Message History, "
            f"or unset {BOT_CHANNEL_PURGE_ENV}."
        )
        logger.warning("Bot channel cleanup forbidden for channel %s (%s)", channel_id, state_key)
        return 0
    if response.status_code not in {200, 204}:
        logger.warning(
            "Bot channel cleanup list failed for %s (HTTP %s)",
            state_key,
            response.status_code,
        )
        return 0

    try:
        messages = response.json()
    except (ValueError, TypeError, json.JSONDecodeError):
        logger.warning("Bot channel cleanup: invalid JSON for %s", state_key)
        return 0
    if not isinstance(messages, list):
        return 0

    deleted = 0
    for item in messages:
        if not isinstance(item, dict):
            continue
        if not item.get("webhook_id"):
            continue
        try:
            message_id = int(item["id"])
        except (KeyError, TypeError, ValueError):
            continue
        if message_id in keep_message_ids:
            continue
        delete_url = f"{DISCORD_API_BASE}/channels/{channel_id}/messages/{message_id}"
        for attempt in range(1, MAX_DELETE_ATTEMPTS + 1):
            try:
                del_resp = session.delete(delete_url, headers=headers)
            except (requests.Timeout, requests.ConnectionError) as exc:
                if attempt < MAX_DELETE_ATTEMPTS:
                    time.sleep(min(2**attempt, 30))
                    continue
                logger.warning(
                    "Bot cleanup network error on message %s for %s: %s",
                    message_id,
                    state_key,
                    exc,
                )
                break
            if del_resp.status_code in {200, 204, 404}:
                deleted += 1
                break
            if del_resp.status_code == 429 and attempt < MAX_DELETE_ATTEMPTS:
                try:
                    delay = float(del_resp.json().get("retry_after", 1))
                except (ValueError, TypeError, json.JSONDecodeError, AttributeError):
                    delay = min(2**attempt, 30)
                time.sleep(delay)
                continue
            logger.warning(
                "Bot cleanup could not delete message %s for %s (HTTP %s)",
                message_id,
                state_key,
                del_resp.status_code,
            )
            break

    if deleted:
        print(f"Bot channel cleanup removed {deleted} extra webhook message(s) for {state_key}")
        logger.info(
            "Bot channel cleanup removed %s extra webhook message(s) for %s",
            deleted,
            state_key,
        )
    return deleted


def _add_checkmark_reaction(
    session: requests.Session,
    *,
    bot_token: str,
    channel_id: int,
    message_id: int,
) -> None:
    """PUT checkmark reaction as the bot user (webhooks cannot react by themselves)."""
    emoji = quote(CHECKMARK_REACTION, safe="")
    api_url = (
        f"{DISCORD_API_BASE}/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
    )
    headers = {"Authorization": f"Bot {bot_token}"}
    last_error: Exception | None = None
    for attempt in range(1, MAX_SEND_ATTEMPTS + 1):
        try:
            response = session.put(api_url, headers=headers)
            if response.status_code in {200, 204}:
                return
            if response.status_code == 403:
                raise RuntimeError(
                    f"Failed to add checkmark reaction to message {message_id} (HTTP 403). "
                    "Bot needs Add Reactions + Read Message History and channel access."
                )
            if response.status_code == 429 and attempt < MAX_SEND_ATTEMPTS:
                try:
                    payload = response.json()
                    delay = float(payload.get("retry_after", 1))
                except (ValueError, TypeError, json.JSONDecodeError):
                    delay = min(2**attempt, 30)
                logger.warning(
                    "Rate-limited adding checkmark to message %s; sleeping %.1fs",
                    message_id,
                    delay,
                )
                time.sleep(delay)
                continue
            raise RuntimeError(
                f"Failed to add checkmark reaction to message {message_id} "
                f"(HTTP {response.status_code})"
            )
        except (requests.Timeout, requests.ConnectionError) as exc:
            last_error = exc
            if attempt < MAX_SEND_ATTEMPTS:
                delay = min(2**attempt, 30)
                logger.warning(
                    "Network error adding checkmark to message %s (attempt %s/%s); sleeping %.1fs",
                    message_id,
                    attempt,
                    MAX_SEND_ATTEMPTS,
                    delay,
                )
                time.sleep(delay)
                continue
            raise RuntimeError(
                f"Failed to add checkmark reaction to message {message_id}: network error"
            ) from exc
    raise RuntimeError(f"Failed to add checkmark reaction to message {message_id}") from last_error


def _react_to_messages(
    session: requests.Session,
    messages: list[Any],
    *,
    require_reaction: bool = True,
) -> None:
    """Apply checkmark on every message produced by this send cycle."""
    if not messages:
        return
    token = _bot_token()
    if not token:
        message = (
            f"{BOT_TOKEN_ENV} not set - cannot add checkmark reactions. "
            "Create a bot at https://discord.com/developers/applications , invite it "
            "with Add Reactions + Read Message History (and channel access), then set "
            f"{BOT_TOKEN_ENV} in .env. Use --allow-skip-reaction only if you intentionally "
            "want to post without reactions."
        )
        if require_reaction:
            raise RuntimeError(message)
        console_print(f"Warning: {message}")
        logger.warning("%s", message)
        return

    reacted = 0
    errors: list[str] = []
    for message in messages:
        message_id = int(message.id)
        channel_id = _message_channel_id(message)
        if channel_id is None:
            logger.warning(
                "Could not resolve channel_id for message %s; skipped checkmark",
                message_id,
            )
            errors.append(f"missing channel_id for {message_id}")
            continue
        try:
            _add_checkmark_reaction(
                session,
                bot_token=token,
                channel_id=channel_id,
                message_id=message_id,
            )
            reacted += 1
        except RuntimeError as exc:
            logger.warning("%s", exc)
            console_print(f"Warning: {exc}")
            errors.append(str(exc))
    if reacted:
        console_print(f"Added checkmark to {reacted} webhook message(s)")
        logger.info("Added checkmark to %s webhook message(s)", reacted)
    if require_reaction and errors:
        raise RuntimeError("Required checkmark reactions failed: " + "; ".join(errors))
    if require_reaction and reacted == 0 and messages:
        raise RuntimeError("Required checkmark reactions failed: no messages reacted")


def send_webhook(
    webhook_url: str,
    embeds: list[discord.Embed],
    *,
    username: str,
    files: list[discord.File] | Callable[[], list[discord.File]] | None = None,
    state_key: str | None = None,
    require_reaction: bool = True,
    effective_date: bool = False,
    bot_channel_purge: bool | None = None,
) -> list[int]:
    """Send embeds via Discord webhook with sibling-key purge and checkmark reactions."""
    from discord import SyncWebhook

    validate_webhook_url(webhook_url)
    if effective_date:
        apply_effective_date_footer(embeds)
    validate_embed_limits(embeds)

    masked = mask_webhook_url(webhook_url)
    session = _session_with_timeout()
    webhook = SyncWebhook.from_url(webhook_url, session=session)

    state_keys = sibling_webhook_state_keys(webhook_url, state_key) if state_key else []
    if state_key and len(state_keys) > 1:
        print(
            f"Note: {state_key} shares a webhook URL with "
            + ", ".join(k for k in state_keys if k != state_key)
            + " - purge will clear all sibling recorded IDs."
        )
        logger.info(
            "Shared webhook for %s; sibling state keys: %s",
            state_key,
            ", ".join(state_keys),
        )

    prior_ids: list[int] = []
    if state_key:
        with _webhook_state_lock():
            state = _load_webhook_message_state()
            prior_ids = collect_prior_message_ids(state, state_keys)

    do_bot_purge = _bot_channel_purge_enabled() if bot_channel_purge is None else bot_channel_purge

    last_error: Exception | None = None
    for attempt in range(1, MAX_SEND_ATTEMPTS + 1):
        try:
            if files is None:
                attempt_files: list[discord.File] = []
            elif callable(files):
                attempt_files = list(files())
            else:
                attempt_files = list(files)

            logger.info(
                "Sending webhook %s as %s (attempt %s/%s, embeds=%s, files=%s)",
                masked,
                username,
                attempt,
                MAX_SEND_ATTEMPTS,
                len(embeds),
                len(attempt_files),
            )
            posted_messages: list[Any] = []
            message = webhook.send(
                embeds=embeds,
                username=username,
                files=attempt_files,
                wait=True,
                allowed_mentions=discord.AllowedMentions.none(),
            )
            if message is not None:
                posted_messages.append(message)

            message_ids = [int(msg.id) for msg in posted_messages]
            if state_key and message_ids:
                with _webhook_state_lock():
                    state = _load_webhook_message_state()
                    existing = collect_prior_message_ids(state, state_keys)
                    state[state_key] = _unique_message_ids([*existing, *message_ids])
                    for sibling in state_keys:
                        if sibling != state_key:
                            state.pop(sibling, None)
                    _save_webhook_message_state(state)

            remaining_prior: list[int] = []
            if state_key and prior_ids:
                remaining_prior = _delete_webhook_messages(
                    webhook,
                    state_key=state_key,
                    message_ids=prior_ids,
                )

            if do_bot_purge and posted_messages:
                token = _bot_token()
                channel_id = _message_channel_id(posted_messages[0])
                if token and channel_id is not None:
                    _bot_cleanup_channel_webhook_messages(
                        session,
                        bot_token=token,
                        channel_id=channel_id,
                        keep_message_ids=set(message_ids),
                        state_key=state_key or "webhook",
                    )
                elif do_bot_purge and not token:
                    print(
                        f"Warning: {BOT_CHANNEL_PURGE_ENV} set but {BOT_TOKEN_ENV} "
                        "missing - skipped bot channel cleanup."
                    )

            if state_key:
                combined = _unique_message_ids([*remaining_prior, *message_ids])
                with _webhook_state_lock():
                    state = _load_webhook_message_state()
                    if combined:
                        state[state_key] = combined
                    else:
                        state.pop(state_key, None)
                    for sibling in state_keys:
                        if sibling != state_key:
                            state.pop(sibling, None)
                    _save_webhook_message_state(state)

            _react_to_messages(session, posted_messages, require_reaction=require_reaction)
            logger.info("Webhook send succeeded (%s) as %s", masked, username)
            console_print("Sent successfully!")
            return message_ids
        except HTTPException as exc:
            last_error = exc
            status = getattr(exc, "status", None)
            if status == 429 and attempt < MAX_SEND_ATTEMPTS:
                delay = _retry_after_seconds(exc, attempt)
                logger.warning(
                    "Discord rate-limited webhook %s (attempt %s/%s); sleeping %.1fs",
                    masked,
                    attempt,
                    MAX_SEND_ATTEMPTS,
                    delay,
                )
                time.sleep(delay)
                continue
            if isinstance(status, int) and status >= 500 and attempt < MAX_SEND_ATTEMPTS:
                delay = min(2**attempt, 30)
                logger.warning(
                    "Discord server error %s for webhook %s (attempt %s/%s); sleeping %.1fs",
                    status,
                    masked,
                    attempt,
                    MAX_SEND_ATTEMPTS,
                    delay,
                )
                time.sleep(delay)
                continue
            raise RuntimeError(
                f"Discord webhook send failed (HTTP {status}) for {masked}"
            ) from None
        except (requests.Timeout, requests.ConnectionError) as exc:
            last_error = exc
            if attempt < MAX_SEND_ATTEMPTS:
                delay = min(2**attempt, 30)
                logger.warning(
                    "Network error sending webhook %s (attempt %s/%s); sleeping %.1fs",
                    masked,
                    attempt,
                    MAX_SEND_ATTEMPTS,
                    delay,
                )
                time.sleep(delay)
                continue
            raise RuntimeError(f"Discord webhook send failed for {masked}: network error") from None

    raise RuntimeError(f"Discord webhook send failed for {masked}") from last_error


# === FILE FOOTER ===
# End of file: common/cia_common.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
