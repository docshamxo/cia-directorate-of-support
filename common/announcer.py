# === FILE HEADER ===
# Title: Announcer
# Path: common/announcer.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial creation
#   - 2026-07-15 | docshamxo | Pass webhook state key for prior-message cleanup.
#   - 2026-07-17 | docshamxo | Document purge-all IDs + ✅ reaction via shared send path.
#   - 2026-07-17 | docshamxo | Embed preflight, logging, staff fail-closed, slim subunit CoC.
# === END FILE HEADER ===

"""Shared entry helpers for Discord announcer scripts.

Live sends go through ``cia_common.send_webhook``, which posts first, then
deletes previously recorded message IDs, and adds ✅ when
``DISCORD_BOT_TOKEN`` is configured.
"""

from __future__ import annotations

import logging
import os
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

import discord

from common import cia_common as c
from common.manifest import STAFF_WEBHOOK_KEYS

EmbedBuilder = Callable[[], list[discord.Embed]]
FileBuilder = Callable[[], list[discord.File]]

logger = logging.getLogger("cia.announcer")


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


def _cli_flag(name: str) -> bool:
    return name in sys.argv


def preview_embeds(
    embeds: Sequence[discord.Embed],
    *,
    webhook_key: str,
    username: str,
) -> None:
    c.validate_embed_limits(embeds)
    print(f"[dry-run] {webhook_key} as {username} - {len(embeds)} embed(s)")
    for index, embed in enumerate(embeds, start=1):
        title = embed.title or "(no title)"
        field_count = len(embed.fields)
        desc_len = len(embed.description or "")
        print(f"  {index}. {title}  fields={field_count}  description_chars={desc_len}")


def _warn_or_fail_staff_placeholders(webhook_key: str, embeds: Sequence[discord.Embed]) -> None:
    if webhook_key not in STAFF_WEBHOOK_KEYS:
        return
    blob = "\n".join(
        [
            *(item.description or "" for item in embeds),
            *(field.value for item in embeds for field in item.fields),
        ]
    )
    if c.STAFF_PLACEHOLDER_MARKER not in blob and "example.invalid" not in blob:
        return
    message = (
        f"{webhook_key}: staff link placeholders still present. "
        "Copy config/links.staff.example.yaml → config/links.staff.local.yaml "
        "and set real URLs before a live staff send."
    )
    if is_dry_run():
        print(f"Warning: {message}")
        logger.warning("%s", message)
        return
    raise RuntimeError(message)


def run_announcer(
    *,
    webhook_key: str,
    username: str,
    build_embeds: EmbedBuilder,
    files: Sequence[discord.File] | FileBuilder | None = None,
    dry_run: bool | None = None,
) -> None:
    """Build embeds and either preview or send them to Discord."""
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    require_reaction = env_flag("CIA_REQUIRE_REACTION") or _cli_flag("--require-reaction")
    effective_date = env_flag("CIA_EFFECTIVE_DATE") or _cli_flag("--effective-date")

    logger.info("Building embeds for %s (%s)", webhook_key, username)
    embeds = build_embeds()
    c.validate_embed_limits(embeds)
    if effective_date:
        c.apply_effective_date_footer(embeds)
    _warn_or_fail_staff_placeholders(webhook_key, embeds)

    if is_dry_run(dry_run=dry_run):
        preview_embeds(embeds, webhook_key=webhook_key, username=username)
        return

    webhook_url = os.environ.get(webhook_key, "").strip()
    if not webhook_url:
        if allow_skip_empty_webhook():
            print(f"Skipping {webhook_key}: webhook URL not set")
            logger.info("Skipping %s: webhook URL not set", webhook_key)
            return
        raise RuntimeError(
            f"Missing {webhook_key}. Copy .env.example to .env and set your webhook URLs."
        )

    def file_factory() -> list[discord.File]:
        if files is None:
            return []
        if callable(files):
            return list(files())
        # Re-open from logo filenames so retries do not reuse spent file handles.
        reopened: list[discord.File] = []
        for item in files:
            filename = getattr(item, "filename", None) or Path(str(item)).name
            reopened.append(c.logo_file(c.confined_logo_path(filename)))
        return reopened

    logger.info("Sending %s via webhook (require_reaction=%s)", webhook_key, require_reaction)
    c.send_webhook(
        webhook_url,
        embeds,
        username=username,
        files=file_factory,
        state_key=webhook_key,
        require_reaction=require_reaction,
        effective_date=False,  # already applied above when requested
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
    """Shared GRS/ESD chain-of-command embed layout (need-to-know; no full DS ORBAT)."""
    return [
        c.chain_intro_embed(
            unit=unit_full,
            color=color,
            logo=logo,
            context=(
                f"The **{unit_full} ({unit_abbrev})** is a sub-unit of the **Office of Security** "
                "under the **Directorate of Support**. "
                f"{unit_abbrev} leadership reports through the OSEC and DS chains to Agency leadership. "
                "Full parent ORBAT is published in the DS / OSEC chain-of-command channels only."
            ),
        ),
        c.embed(
            title="Reporting Line",
            description=(
                f"{unit_abbrev} reports through **Office of Security** → **Directorate of Support**. "
                "Consult your immediate supervisor before escalating. "
                "Parent leadership names are intentionally omitted here (need-to-know)."
            ),
            color=color,
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
