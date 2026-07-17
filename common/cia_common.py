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
#   - 2026-07-17 | docshamxo | Safe console print for Windows cp1252 dry-run paths.
# === END FILE HEADER ===

"""
Shared Discord helpers and configuration loader for CIA DS announcers.

Editable data lives in config/*.yaml - not in this file:
  - config/branding.yaml      colors, bots, logos, community URLs
  - config/organization.yaml  mottos, about text, offices, disclaimers
  - config/personnel.yaml     chain-of-command names and ranks
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
STAFF_PLACEHOLDER_MARKER = "STAFF_LOCAL_REQUIRED"

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


def mask_webhook_url(webhook_url: str) -> str:
    """Return a log-safe webhook URL with the token redacted."""
    try:
        parsed = urlparse(webhook_url)
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) >= 3 and parts[0] == "api" and parts[1] == "webhooks":
            webhook_id = parts[2]
            return f"{parsed.scheme}://{parsed.netloc}/api/webhooks/{webhook_id}/***"
    except Exception:
        pass
    return "https://discord.com/api/webhooks/***"


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
    return _load_yaml("personnel.yaml")


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
    "This is an unofficial Roblox community — not affiliated with the US Government or CIA.",
)
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


def agency_eyebrow(unit: str) -> str:
    """Standard italic hero eyebrow: Central Intelligence Agency · {Unit}."""
    return f"*Central Intelligence Agency · {unit}*"


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
    embeds[-1].set_footer(text=f"Effective {stamp.isoformat()} (community roleplay)")


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
    """ALL CAPS hero title + italic CIA · Unit eyebrow + short supporting sentence."""
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
    return embed(title="Disclaimer", description=text, color=color)


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
    """Raise ValueError if embeds exceed Discord field limits."""
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
        try:
            webhook.delete_message(message_id)
            deleted += 1
        except HTTPException as exc:
            status = getattr(exc, "status", None)
            if status == 404:
                deleted += 1
                continue
            if status == 429:
                delay = _retry_after_seconds(exc, 1)
                logger.warning(
                    "Rate-limited deleting prior message %s for %s; sleeping %.1fs",
                    message_id,
                    state_key,
                    delay,
                )
                time.sleep(delay)
                try:
                    webhook.delete_message(message_id)
                    deleted += 1
                    continue
                except HTTPException as retry_exc:
                    if getattr(retry_exc, "status", None) == 404:
                        deleted += 1
                        continue
                    logger.warning(
                        "Could not delete prior message %s for %s (HTTP %s)",
                        message_id,
                        state_key,
                        getattr(retry_exc, "status", None),
                    )
                    remaining.append(message_id)
                    continue
            logger.warning(
                "Could not delete prior message %s for %s (HTTP %s)",
                message_id,
                state_key,
                status,
            )
            remaining.append(message_id)
        except (requests.Timeout, requests.ConnectionError) as exc:
            logger.warning(
                "Network error deleting prior message %s for %s: %s",
                message_id,
                state_key,
                exc,
            )
            remaining.append(message_id)

    remaining = _unique_message_ids(remaining)
    if deleted:
        console_print(f"Cleared {deleted} prior webhook message(s) for {state_key}")
        logger.info("Cleared %s prior webhook message(s) for %s", deleted, state_key)
    return remaining


def _add_checkmark_reaction(
    session: requests.Session,
    *,
    bot_token: str,
    channel_id: int,
    message_id: int,
) -> None:
    """PUT ✅ reaction as the bot user (webhooks cannot react by themselves)."""
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
            if response.status_code == 429 and attempt < MAX_SEND_ATTEMPTS:
                try:
                    payload = response.json()
                    delay = float(payload.get("retry_after", 1))
                except (ValueError, TypeError, json.JSONDecodeError):
                    delay = min(2**attempt, 30)
                logger.warning(
                    "Rate-limited adding ✅ to message %s; sleeping %.1fs",
                    message_id,
                    delay,
                )
                time.sleep(delay)
                continue
            raise RuntimeError(
                f"Failed to add ✅ reaction to message {message_id} (HTTP {response.status_code})"
            )
        except (requests.Timeout, requests.ConnectionError) as exc:
            last_error = exc
            if attempt < MAX_SEND_ATTEMPTS:
                delay = min(2**attempt, 30)
                logger.warning(
                    "Network error adding ✅ to message %s (attempt %s/%s); sleeping %.1fs",
                    message_id,
                    attempt,
                    MAX_SEND_ATTEMPTS,
                    delay,
                )
                time.sleep(delay)
                continue
            raise RuntimeError(
                f"Failed to add ✅ reaction to message {message_id}: network error"
            ) from exc
    raise RuntimeError(f"Failed to add ✅ reaction to message {message_id}") from last_error


def _react_to_messages(
    session: requests.Session,
    messages: list[Any],
    *,
    require_reaction: bool = False,
) -> None:
    """Best-effort ✅ on every message produced by this send cycle."""
    if not messages:
        return
    token = _bot_token()
    if not token:
        message = (
            f"{BOT_TOKEN_ENV} not set — skipped ✅ reactions. "
            "Add a bot token with Add Reactions + Read Message History in the target server."
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
                "Could not resolve channel_id for message %s; skipped ✅",
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
        console_print(f"Added ✅ to {reacted} webhook message(s)")
        logger.info("Added ✅ to %s webhook message(s)", reacted)
    if require_reaction and errors:
        raise RuntimeError("Required ✅ reactions failed: " + "; ".join(errors))


def send_webhook(
    webhook_url: str,
    embeds: list[discord.Embed],
    *,
    username: str,
    files: list[discord.File] | Callable[[], list[discord.File]] | None = None,
    state_key: str | None = None,
    require_reaction: bool = False,
    effective_date: bool = False,
) -> list[int]:
    """Send embeds via Discord webhook.

    When ``state_key`` is set, posts the new message first (``wait=True``), then
    deletes previously stored message IDs so a failed send does not empty the
    channel. Records all new IDs in ``.webhook_messages.json`` and adds ✅ when
    ``DISCORD_BOT_TOKEN`` is set. ``bot_token`` is never passed to
    ``SyncWebhook.from_url`` — reactions use a separate bot HTTP client.
    """
    from discord import SyncWebhook

    validate_webhook_url(webhook_url)
    if effective_date:
        apply_effective_date_footer(embeds)
    validate_embed_limits(embeds)

    masked = mask_webhook_url(webhook_url)
    session = _session_with_timeout()
    # Intentionally omit bot_token — keep reaction auth on the separate client path.
    webhook = SyncWebhook.from_url(webhook_url, session=session)

    prior_ids: list[int] = []
    if state_key:
        with _webhook_state_lock():
            prior_ids = list(_load_webhook_message_state().get(state_key, []))

    last_error: Exception | None = None
    for attempt in range(1, MAX_SEND_ATTEMPTS + 1):
        try:
            if files is None:
                attempt_files: list[discord.File] = []
            elif callable(files):
                attempt_files = list(files())
            else:
                # Re-open hazard: prefer callable factories from run_announcer.
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

            remaining_prior: list[int] = []
            if state_key and prior_ids:
                # Safer purge: only delete old messages after a successful post.
                remaining_prior = _delete_webhook_messages(
                    webhook,
                    state_key=state_key,
                    message_ids=prior_ids,
                )

            if state_key:
                combined = _unique_message_ids([*remaining_prior, *message_ids])
                with _webhook_state_lock():
                    state = _load_webhook_message_state()
                    if combined:
                        state[state_key] = combined
                    else:
                        state.pop(state_key, None)
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
