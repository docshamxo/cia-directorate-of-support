"""
Shared configuration, organizational reference data, and Discord helpers
for CIA Directorate of Support announcer scripts.

Organizational descriptions are aligned with the YFPA CIA Organizational Bulletin.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import discord
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def require_webhook(env_key: str) -> str:
    """Load a Discord webhook URL from the environment / .env file."""
    value = os.environ.get(env_key, "").strip()
    if not value:
        raise RuntimeError(
            f"Missing {env_key}. Copy .env.example to .env and set your webhook URLs."
        )
    return value


# ── Paths & assets ────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = REPO_ROOT / "assets"
LOGOS_DIR = ASSETS_DIR / "logos"

LOGOS = {
    "ds": LOGOS_DIR / "DS.png",
    "ote": LOGOS_DIR / "OTE.png",
    "osec": LOGOS_DIR / "OSEC.png",
    "grs": LOGOS_DIR / "GRS.png",
    "esd": LOGOS_DIR / "ESD.png",
}

# ── Embed colors ──────────────────────────────────────────────────────────────

COLOR_DS = 0x1E3F78
COLOR_OSEC = 0x1E3F78
COLOR_OTE = 0x1E3F78
COLOR_GRS = 0xFFD700
COLOR_ESD = 0x9B111E

# ── Bot usernames ─────────────────────────────────────────────────────────────

BOT_DS = "CIA Directorate of Support Bot"
BOT_OSEC = "CIA | Office of Security"
BOT_OTE = "CIA | Office of Training & Education"
BOT_OTE_ALT = "CIA | Office of Training & Education Bot"
BOT_GRS = "CIA | Global Response Staff"
BOT_ESD = "CIA | Executive Security Detail"

# ── Community links ───────────────────────────────────────────────────────────

URL_ROBLOX_GROUP_DS = "https://www.roblox.com/share/g/945806945"
URL_ROBLOX_GROUP_OSEC = (
    "https://www.roblox.com/communities/288542436/CIA-Office-of-Security#!/about"
)
URL_ROBLOX_GROUP_GRS = "https://www.roblox.com/share/g/450710337"
URL_ROBLOX_GROUP_OTE = "https://www.roblox.com/share/g/1003614105"
URL_DISCORD_INVITE = "https://discord.gg/3S3vDK8nJY"

# ── Organizational reference (bulletin) ───────────────────────────────────────

DS_MOTTO = "WE GO AS ONE"
DS_CLASSIFICATION = "PUBLIC AFFAIRS"

DS_ABOUT = (
    "The **Directorate of Support (DS)** is the Agency's backbone — responsible for "
    "internal security, physical protection, and the readiness of every officer who serves. "
    "While other directorates operate at the sharp end of the mission, DS ensures the people, "
    "facilities, and operatives behind them remain protected and properly prepared.\n\n"
    "The Directorate is organized into subordinate offices, each safeguarding a distinct pillar "
    "of Agency operations: securing the institution from within, and forging the officers who "
    "carry the mission forward."
)

OSEC_MOTTO = "PROTECT · DETECT · RESPOND"

OSEC_ABOUT = (
    "The **Office of Security (OSEC)** is the Agency's internal law-enforcement and protective "
    "arm. Its officers serve as the Agency's guards and security force — safeguarding facilities, "
    "screening access, and enforcing internal security protocol across every CIA site.\n\n"
    "Two specialized sub-units operate beneath OSEC, handling escalated and high-priority "
    "protective taskings."
)

GRS_ABOUT = (
    "The Agency's operational-focused security element — rapid deployment, high-threat site "
    "security, and direct-action support for field operations worldwide."
)

ESD_ABOUT = (
    "A dedicated close-protection unit responsible for the personal security of High Value "
    "Targets (HVTs), senior leadership, and VIPs during travel and operations."
)

OTE_MOTTO = "SCIENTIA EST LUX LUCIS"

OTE_ABOUT = (
    "The **Office of Training & Education (OTE)** runs the Agency's **Officer Training Program** "
    "— recruiting, instructing, and certifying every new officer before they are cleared for "
    "active duty. OTE oversees tradecraft instruction, academy curriculum, and continuing "
    "professional development."
)

OTE_PILLARS = (
    (
        "Recruitment & Selection",
        "Screening and onboarding new applicants into the Agency's officer pipeline, ensuring "
        "every candidate meets the standard before training begins.",
    ),
    (
        "Tradecraft Instruction",
        "Core academy curriculum — fieldcraft, security protocol, and operational discipline "
        "taught to every officer prior to active deployment.",
    ),
    (
        "Continuing Development",
        "Ongoing professional education and re-certification keeping active officers current "
        "with Agency doctrine and standards.",
    ),
)

DS_OFFICES = (
    "Office of Training & Education (OTE)",
    "Office of Security (OSEC)",
)

OSEC_SUB_UNITS = (
    "Global Response Staff (GRS)",
    "Executive Security Detail (ESD)",
)

# ── Personnel data ────────────────────────────────────────────────────────────


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


AGENCY_EXECUTIVE = (
    Role("DIR", "Director of the Central Intelligence Agency", "YepaInvictus"),
    Role("DDIR", "Deputy Director of the Central Intelligence Agency", "laks_l"),
    Role("EDIR", "Executive Director of the Central Intelligence Agency", "ashlyn"),
    Role("CoS", "Chief of Staff", "Kaoetern1ty"),
    Role("IG", "Inspector General", "VACANT"),
)

DS_LEADERSHIP = (
    Role("CDSD", "Component Director, Directorate of Support", "ClassifiedDark24"),
    Role("DCDSD", "Deputy Component Director, Directorate of Support", "docshamxo"),
)

OTE_HIGH_COMMAND = (
    Role("DTE", "Director of Training and Education", "Shaikhuu"),
    Role("DDTE", "Deputy Director of Training and Education", "Railorbsj"),
    Role("ADTE", "Assistant Director of Training and Education", "AndyShotSecond"),
    Role("D", "Dean", "miqila0shu"),
)

OTE_STAFF_RANKS = (
    Rank("SP", "Senior Professor"),
    Rank("P", "Professor"),
    Rank("AP", "Associate Professor"),
)

OSEC_HIGH_COMMAND = (
    Role("DS", "Director of Security", "Dustykingeric"),
    Role("DDS", "Deputy Director of Security", "liveurlite"),
    Role("ADS", "Assistant Director of Security", "Rattler_289"),
    Role("Supt", "Superintendent", "Foxxy_Fan"),
)

OSEC_MAIN_CHIEF_MARSHALS = (
    Role("CM", "Chief Marshal", "Jamalclop"),
    Role("CM", "Chief Marshal", "Killjoy_74k"),
    Role("CM", "Chief Marshal", "Idk_Manti"),
    Role("CM", "Chief Marshal", "QueenIrealsub"),
)

GRS_COMMAND = (
    Role("CM", "Chief Marshal", "kkthegoaty2_0"),
    Role("DCM", "Deputy Chief Marshal", "MrPallen"),
)

ESD_COMMAND = (
    Role("CM", "Chief Marshal", "xBlq_h"),
    Role("DCM", "Deputy Chief Marshal", "Ghostfac32009"),
)

OSEC_MIDDLE_COMMAND = (
    Rank("CM", "Chief Marshal"),
    Rank("DCM", "Deputy Chief Marshal"),
    Rank("SI", "Security Inspector"),
    Rank("SC", "Security Captain"),
    Rank("SCL", "Security Chief Lieutenant"),
)

OSEC_LOW_COMMAND = (
    Rank("SL", "Security Lieutenant"),
    Rank("SCO", "Security Conduct Officer"),
    Rank("SS", "Security Supervisor"),
    Rank("TSA", "Tactical Security Agent"),
    Rank("SSA", "Senior Security Agent"),
    Rank("SA", "Security Agent"),
    Rank("JSA", "Junior Security Agent"),
    Rank("SP1/SP2", "Security Program Candidates"),
)

GRS_ESD_MIDDLE_COMMAND = OSEC_MIDDLE_COMMAND[2:]  # SI through SCL

GRS_ESD_LOW_COMMAND = (
    Rank("SL", "Security Lieutenant"),
    Rank("SCO", "Security Conduct Officer"),
    Rank("SS", "Security Supervisor"),
    Rank("TSA", "Tactical Security Agent"),
)

CHAIN_OF_COMMAND_INTRO = (
    "The Chain of Command is the structured hierarchy used to maintain order, "
    "accountability, and clear communication. All instructions, concerns, and "
    "requests should flow through your immediate supervisor before moving upward "
    "through leadership.\n\n"
    "Do not bypass ranks by directing issues to senior leadership when a "
    "lower-ranking supervisor is available and appropriate. Always consult the "
    "next rank above you rather than escalating to the highest authority."
)

DISCLAIMER_TEXT = "All text here is marked as **UNCLASSIFIED**."
DISCLAIMER_LINKS_TEXT = "All text and links listed here are marked as **UNCLASSIFIED**."
DISCLAIMER_CLASSIFIED_TEXT = (
    "Classification markings apply to linked documents as indicated above. "
    "All channel text is marked **UNCLASSIFIED** unless otherwise stated."
)

# ── Formatting helpers ────────────────────────────────────────────────────────


def roles_text(*roles: Role) -> str:
    return "\n".join(role.format() for role in roles)


def ranks_text(*ranks: Rank) -> str:
    return "\n".join(rank.format() for rank in ranks)


def bullets(*items: str) -> str:
    return "\n".join(f"**{item}**" for item in items)


def link(label: str, url: str) -> str:
    return f"[{label}]({url})"


def link_field(name: str, label: str, url: str, note: str | None = None) -> tuple[str, str]:
    value = link(label, url)
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
