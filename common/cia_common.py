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
# === END FILE HEADER ===

"""
Shared Discord helpers and configuration loader for CIA DS announcers.

Editable data lives in config/*.yaml - not in this file:
  - config/branding.yaml      colors, bots, logos, community URLs
  - config/organization.yaml  mottos, about text, offices, disclaimers
  - config/personnel.yaml     chain-of-command names and ranks
  - config/links.yaml         document / form / channel URLs
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import discord
import yaml
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"
ASSETS_DIR = REPO_ROOT / "assets"
LOGOS_DIR = ASSETS_DIR / "logos"

load_dotenv(REPO_ROOT / ".env")


def require_webhook(env_key: str) -> str:
    """Load a Discord webhook URL from the environment / .env file."""
    value = os.environ.get(env_key, "").strip()
    if not value:
        raise RuntimeError(
            f"Missing {env_key}. Copy .env.example to .env and set your webhook URLs."
        )
    return value


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
    return _load_yaml("links.yaml")


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
    Look up a URL (or other string value) from config/links.yaml.

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
BOT_OTE_ALT = _bots["ote_alt"]
BOT_GRS = _bots["grs"]
BOT_ESD = _bots["esd"]

LOGOS = {key: LOGOS_DIR / filename for key, filename in _logo_files.items()}

URL_ROBLOX_GROUP_DS = url("community.roblox_group_ds")
URL_ROBLOX_GROUP_OSEC = url("community.roblox_group_osec")
URL_ROBLOX_GROUP_GRS = url("community.roblox_group_grs")
URL_ROBLOX_GROUP_OTE = url("community.roblox_group_ote")
URL_DISCORD_INVITE = url("community.discord_invite")

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
OTE_PILLARS = tuple(
    (item["title"], item["description"]) for item in _get_org("ote", "pillars")
)

GRS_ABOUT = _get_org("grs", "about")
ESD_ABOUT = _get_org("esd", "about")

_copy = _get_org("copy")
CHAIN_OF_COMMAND_INTRO = _copy["chain_of_command_intro"]
DISCLAIMER_TEXT = _copy["disclaimer"]
DISCLAIMER_LINKS_TEXT = _copy["disclaimer_links"]
DISCLAIMER_CLASSIFIED_TEXT = _copy["disclaimer_classified"]

# ── Personnel ─────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Role:
    """A single position in the chain of command."""

    abbrev: str
    title: str
    holder: str

    def format(self) -> str:
        return f"**[{self.abbrev}] {self.title}** - {self.holder}"


@dataclass(frozen=True, slots=True)
class Rank:
    """A rank title without an assigned holder."""

    abbrev: str
    title: str

    def format(self) -> str:
        return f"**[{self.abbrev}] {self.title}**"


def _roles(key: str) -> tuple[Role, ...]:
    return tuple(
        Role(item["abbrev"], item["title"], item["holder"]) for item in _personnel()[key]
    )


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
GRS_ESD_MIDDLE_COMMAND = OSEC_MIDDLE_COMMAND[2:]  # SI through SCL

# ── Formatting helpers ────────────────────────────────────────────────────────


def roles_text(*roles: Role) -> str:
    return "\n".join(role.format() for role in roles)


def ranks_text(*ranks: Rank) -> str:
    return "\n".join(rank.format() for rank in ranks)


def bullets(*items: str) -> str:
    return "\n".join(f"**{item}**" for item in items)


def link(label: str, url_value: str) -> str:
    return f"[{label}]({url_value})"


def link_field(
    name: str, label: str, url_value: str, note: str | None = None
) -> tuple[str, str]:
    value = link(label, url_value)
    if note:
        value += f"\n*{note}*"
    return (name, value)


def pillar_field(title: str, description: str) -> tuple[str, str]:
    return (title, f"**{title}**\n{description}")


# ── Embed helpers ─────────────────────────────────────────────────────────────


def logo_file(path: Path) -> discord.File:
    return discord.File(path, filename=path.name)


def set_logo(embed: discord.Embed, path: Path) -> None:
    embed.set_thumbnail(url=f"attachment://{path.name}")


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


def disclaimer_embed(*, classified: bool = False, links: bool = False) -> discord.Embed:
    if classified:
        text = DISCLAIMER_CLASSIFIED_TEXT
    elif links:
        text = DISCLAIMER_LINKS_TEXT
    else:
        text = DISCLAIMER_TEXT
    return embed(title="Disclaimer", description=text)


def chain_intro_embed(
    *,
    unit: str,
    color: int = COLOR_DS,
    context: str | None = None,
) -> discord.Embed:
    description = f"*Central Intelligence Agency · {unit}*\n\n"
    if context:
        description += f"{context}\n\n"
    description += CHAIN_OF_COMMAND_INTRO
    return embed(title="CHAIN OF COMMAND", description=description, color=color)


def important_notice_embed(
    *,
    unit: str,
    color: int = COLOR_DS,
    parent_units: tuple[str, ...] = (),
) -> discord.Embed:
    chain = "**, **".join(parent_units + (unit,))
    return embed(
        title="Important Notice",
        description=(
            f"All {unit} personnel and candidates must follow Agency regulations and the "
            f"**{chain}** chain of command.\n\n"
            "Unauthorized direct contact with command teams is **not permitted** "
            "for Agency personnel."
        ),
        color=color,
    )


def send_webhook(
    webhook_url: str,
    embeds: list[discord.Embed],
    *,
    username: str,
    files: list[discord.File] | None = None,
) -> None:
    from discord import SyncWebhook

    webhook = SyncWebhook.from_url(webhook_url)
    webhook.send(embeds=embeds, username=username, files=files or [])
    print("Sent successfully!")

# === FILE FOOTER ===
# End of file: common/cia_common.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
