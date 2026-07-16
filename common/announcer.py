# === FILE HEADER ===
# Title: Announcer
# Path: common/announcer.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial creation
# === END FILE HEADER ===

"""Shared entry helpers for Discord announcer scripts."""

from __future__ import annotations

import os
from collections.abc import Callable, Sequence
from pathlib import Path

import discord

from common import cia_common as c

EmbedBuilder = Callable[[], list[discord.Embed]]
FileBuilder = Callable[[], list[discord.File]]


def env_flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def is_dry_run(*, dry_run: bool | None = None) -> bool:
    if env_flag("CIA_DRY_RUN"):
        return True
    if dry_run is True:
        return True
    return False


def allow_skip_empty_webhook() -> bool:
    return env_flag("CIA_SKIP_EMPTY_WEBHOOKS")


def preview_embeds(
    embeds: Sequence[discord.Embed],
    *,
    webhook_key: str,
    username: str,
) -> None:
    print(f"[dry-run] {webhook_key} as {username} - {len(embeds)} embed(s)")
    for index, embed in enumerate(embeds, start=1):
        title = embed.title or "(no title)"
        field_count = len(embed.fields)
        desc_len = len(embed.description or "")
        print(f"  {index}. {title}  fields={field_count}  description_chars={desc_len}")
    if len(embeds) > 10:
        raise ValueError(f"Discord allows at most 10 embeds per message; got {len(embeds)}")


def run_announcer(
    *,
    webhook_key: str,
    username: str,
    build_embeds: EmbedBuilder,
    files: Sequence[discord.File] | FileBuilder | None = None,
    dry_run: bool | None = None,
) -> None:
    """Build embeds and either preview or send them to Discord."""
    embeds = build_embeds()
    if len(embeds) > 10:
        raise ValueError(f"Discord allows at most 10 embeds per message; got {len(embeds)}")

    if is_dry_run(dry_run=dry_run):
        preview_embeds(embeds, webhook_key=webhook_key, username=username)
        return

    webhook_url = os.environ.get(webhook_key, "").strip()
    if not webhook_url:
        if allow_skip_empty_webhook():
            print(f"Skipping {webhook_key}: webhook URL not set")
            return
        raise RuntimeError(
            f"Missing {webhook_key}. Copy .env.example to .env and set your webhook URLs."
        )

    resolved_files: list[discord.File] | None
    if files is None:
        resolved_files = None
    elif callable(files):
        resolved_files = list(files())
    else:
        resolved_files = list(files)

    c.send_webhook(
        webhook_url,
        embeds,
        username=username,
        files=resolved_files,
    )


def subunit_coc_embeds(
    *,
    unit_full: str,
    unit_abbrev: str,
    color: int,
    about: str,
    command_roles: tuple[c.Role, ...],
    logo: Path | None = None,
) -> list[discord.Embed]:
    """Shared GRS/ESD chain-of-command embed layout."""
    return [
        c.chain_intro_embed(
            unit=unit_full,
            color=color,
            logo=logo,
            context=(
                f"The **{unit_full} ({unit_abbrev})** is a sub-unit of the **Office of Security** "
                "under the **Directorate of Support**. "
                f"{unit_abbrev} leadership reports through the OSEC and DS chains to Agency leadership."
            ),
        ),
        c.embed(
            title="Directorate of Support",
            description=(
                f"{unit_abbrev} reports through the Directorate of Support chain of command."
            ),
            color=color,
            fields=(("Leadership", c.roles_text(*c.DS_LEADERSHIP)),),
        ),
        c.embed(
            title=f"{unit_abbrev} Command",
            description=(
                f"Senior leadership responsible for {unit_abbrev} operations and policy.\n\n{about}"
            ),
            color=color,
            fields=(("Command Team", c.roles_text(*command_roles)),),
        ),
        c.embed(
            title=f"{unit_abbrev} MIDCOM",
            description="Mid-level leadership responsible for supervision and operational oversight.",
            color=color,
            fields=(("MIDCOM Ranks", c.ranks_text(*c.GRS_ESD_MIDDLE_COMMAND)),),
        ),
        c.embed(
            title=f"{unit_abbrev} LOWCOM",
            description=f"Field and operational ranks within the {unit_full}.",
            color=color,
            fields=(("LOWCOM Ranks", c.ranks_text(*c.GRS_ESD_LOW_COMMAND)),),
        ),
        c.important_notice_embed(
            unit=unit_abbrev,
            color=color,
            parent_units=("Directorate of Support", "Office of Security"),
        ),
        c.disclaimer_embed(color=color),
    ]


def logo_files(*keys: str) -> list[discord.File]:
    return [c.logo_file(c.LOGOS[key]) for key in keys]


def ensure_logo_exists(key: str) -> Path:
    path = c.LOGOS[key]
    if not path.is_file():
        raise FileNotFoundError(f"Missing logo for '{key}': {path}")
    return path


# === FILE FOOTER ===
# End of file: common/announcer.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
