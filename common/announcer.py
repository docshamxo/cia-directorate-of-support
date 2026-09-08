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
#   - 2026-07-17 | docshamxo | ASCII-safe staff warning; console_print for Windows dry-run.
#   - 2026-07-17 | docshamxo | Expand MIDCOM/LOWCOM labels for accessibility.
#   - 2026-07-17 | docshamxo | Alerting exit codes and structured IR event logs.
#   - 2026-07-17 | docshamxo | Default require_reaction; allow-skip and bot channel purge flags.
#   - 2026-08-04 | docshamxo | Frame GRS/ESD subunit CoC as PUBLIC channel content.
#   - 2026-08-04 | docshamxo | Omit Disclaimer embed from GRS/ESD subunit CoC.
#   - 2026-08-30 | docshamxo | Stamp effective-date footer on every announcer send.
#   - 2026-09-08 | docshamxo | Shared CoC hierarchy block builders; subunit CoC unit-only (no EL/DS/OSEC).
#   - 2026-09-08 | docshamxo | Shared staff-documents frame builders (hero/central/section/handling).
#   - 2026-09-08 | docshamxo | Shared information-channel frame builders (public + reference hubs).
#   - 2026-09-08 | docshamxo | GRS/ESD CoC: logo on hero embed only (not command block).
# === END FILE HEADER ===

"""Shared entry helpers for Discord announcer scripts.

Live sends go through ``cia_common.send_webhook``, which posts first, then
deletes previously recorded message IDs (including sibling keys that share a
webhook URL), and requires a checkmark via ``DISCORD_BOT_TOKEN``. Pass
``--allow-skip-reaction`` or set ``CIA_ALLOW_SKIP_REACTION=1`` to post without.
"""

from __future__ import annotations

import logging
import os
import sys
import time
from collections.abc import Callable, Sequence
from pathlib import Path

import discord

from common import cia_common as c
from common.exit_codes import ANNOUNCER_CONFIG, ANNOUNCER_SKIPPED
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


def allow_skip_reaction() -> bool:
    return env_flag("CIA_ALLOW_SKIP_REACTION") or _cli_flag("--allow-skip-reaction")


def bot_channel_purge_requested() -> bool:
    return env_flag(c.BOT_CHANNEL_PURGE_ENV) or _cli_flag("--bot-channel-purge")


def _cli_flag(name: str) -> bool:
    return name in sys.argv


def preview_embeds(
    embeds: Sequence[discord.Embed],
    *,
    webhook_key: str,
    username: str,
) -> None:
    c.validate_embed_limits(embeds)
    c.console_print(f"[dry-run] {webhook_key} as {username} - {len(embeds)} embed(s)")
    for index, embed in enumerate(embeds, start=1):
        title = embed.title or "(no title)"
        field_count = len(embed.fields)
        desc_len = len(embed.description or "")
        c.console_print(f"  {index}. {title}  fields={field_count}  description_chars={desc_len}")


def _warn_or_fail_staff_placeholders(
    webhook_key: str,
    embeds: Sequence[discord.Embed],
    *,
    dry_run: bool | None = None,
) -> None:
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
        "Copy config/links.staff.example.yaml -> config/links.staff.local.yaml "
        "and set real URLs before a live staff send."
    )
    if is_dry_run(dry_run=dry_run):
        c.console_print(f"Warning: {message}")
        logger.warning("%s", message)
        return
    print(message, file=sys.stderr)
    logger.error("event=staff_placeholder_block webhook_key=%s", webhook_key)
    raise SystemExit(ANNOUNCER_CONFIG)


def run_announcer(
    *,
    webhook_key: str,
    username: str,
    build_embeds: EmbedBuilder,
    files: Sequence[discord.File] | FileBuilder | None = None,
    dry_run: bool | None = None,
) -> None:
    """Build embeds and either preview or send them to Discord.

    Exit conventions (when this process is the entry point):
      0  success / dry-run preview
      10 intentional skip (empty webhook with CIA_SKIP_EMPTY_WEBHOOKS)
      20 config / fail-closed (missing webhook, staff placeholders)
      other non-zero - unexpected send/runtime failure
    """
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    require_reaction = not allow_skip_reaction()
    # Stamp every post with today's date unless explicitly disabled.
    effective_date = not (
        env_flag("CIA_NO_EFFECTIVE_DATE") or _cli_flag("--no-effective-date")
    )
    bot_channel_purge = True if bot_channel_purge_requested() else None
    started = time.monotonic()

    logger.info(
        "event=build_start webhook_key=%s username=%s dry_run=%s",
        webhook_key,
        username,
        is_dry_run(dry_run=dry_run),
    )
    embeds = build_embeds()
    c.validate_embed_limits(embeds)
    if effective_date:
        c.apply_effective_date_footer(embeds)
    _warn_or_fail_staff_placeholders(webhook_key, embeds, dry_run=dry_run)

    if is_dry_run(dry_run=dry_run):
        preview_embeds(embeds, webhook_key=webhook_key, username=username)
        logger.info(
            "event=dry_run_ok webhook_key=%s embeds=%s duration_ms=%s",
            webhook_key,
            len(embeds),
            int((time.monotonic() - started) * 1000),
        )
        return

    webhook_url = os.environ.get(webhook_key, "").strip()
    if not webhook_url:
        if allow_skip_empty_webhook():
            c.console_print(f"Skipping {webhook_key}: webhook URL not set")
            logger.info("event=skip_empty webhook_key=%s", webhook_key)
            raise SystemExit(ANNOUNCER_SKIPPED)
        logger.error("event=missing_webhook webhook_key=%s", webhook_key)
        print(
            f"Missing {webhook_key}. Copy .env.example to .env and set your webhook URLs.",
            file=sys.stderr,
        )
        raise SystemExit(ANNOUNCER_CONFIG)

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

    logger.info(
        "event=send_start webhook_key=%s require_reaction=%s bot_channel_purge=%s",
        webhook_key,
        require_reaction,
        bot_channel_purge,
    )
    try:
        c.send_webhook(
            webhook_url,
            embeds,
            username=username,
            files=file_factory,
            state_key=webhook_key,
            require_reaction=require_reaction,
            effective_date=False,  # already applied above when requested
            bot_channel_purge=bot_channel_purge,
        )
    except Exception:
        logger.exception(
            "event=send_fail webhook_key=%s duration_ms=%s",
            webhook_key,
            int((time.monotonic() - started) * 1000),
        )
        raise
    logger.info(
        "event=send_ok webhook_key=%s embeds=%s duration_ms=%s",
        webhook_key,
        len(embeds),
        int((time.monotonic() - started) * 1000),
    )


def hierarchy_block_description(
    *,
    about: str,
    motto: str | None = None,
    classification: str | None = None,
) -> str:
    """Standard CoC block body: optional motto line, then about/context."""
    if motto:
        return f"{c.motto_line(motto, classification=classification)}\n\n{about}"
    return about


def agency_executive_embed(*, color: int = c.COLOR_DS) -> discord.Embed:
    """Agency EL hierarchy block (shared across CoC channels)."""
    return c.embed(
        title="Agency Executive Leadership",
        description=hierarchy_block_description(
            about=(
                "**Executive Chain of Command**\n\n"
                "Agency executive leadership sits above all Directorates. The "
                "**Directorate of Support (DS)** chain continues below."
            )
        ),
        color=color,
        fields=(("Executive Leadership", c.roles_text(*c.AGENCY_EXECUTIVE)),),
    )


def ds_leadership_embed(
    *,
    color: int = c.COLOR_DS,
    include_offices: bool = True,
    logo: Path | None = None,
) -> discord.Embed:
    """Directorate of Support leadership block (shared across CoC channels)."""
    fields: list[tuple[str, str]] = [("Leadership", c.roles_text(*c.DS_LEADERSHIP))]
    if include_offices:
        fields.append(("Offices", c.bullets(*c.DS_OFFICES)))
    return c.embed(
        title="Directorate of Support",
        description=hierarchy_block_description(
            motto=c.DS_MOTTO,
            classification=c.DS_CLASSIFICATION,
            about=c.DS_ABOUT,
        ),
        color=color,
        logo=logo,
        fields=tuple(fields),
    )


def office_command_embed(
    *,
    title: str,
    about: str,
    roles: tuple[c.Role, ...],
    color: int,
    motto: str | None = None,
    classification: str | None = None,
    logo: Path | None = None,
    roles_field: str = "High Command",
    extra_fields: tuple[tuple[str, str], ...] = (),
) -> discord.Embed:
    """Office or sub-unit command block with standardized title / body / role field."""
    return c.embed(
        title=title,
        description=hierarchy_block_description(
            motto=motto,
            classification=classification,
            about=about,
        ),
        color=color,
        logo=logo,
        fields=((roles_field, c.roles_text(*roles)),) + extra_fields,
    )


def subunit_command_about(about: str) -> str:
    """Parent framing + unit about for GRS/ESD command blocks."""
    return (
        "A sub-unit of the **Office of Security** under the **Directorate of Support**.\n\n"
        f"{about}"
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
    """Shared GRS/ESD public CoC layout (unit command only; no parent EL/DS/OSEC blocks)."""
    return [
        c.chain_intro_embed(
            unit=unit_full,
            color=color,
            logo=logo,
            context=(
                f"The **{unit_full} ({unit_abbrev})** is a sub-unit of the **Office of Security** "
                "under the **Directorate of Support**. "
                f"{unit_abbrev} reports through OSEC and DS to Agency leadership. "
                "Parent DS / OSEC Order of Battle is published in those chain-of-command channels."
            ),
        ),
        office_command_embed(
            title=unit_full,
            about=subunit_command_about(about),
            roles=command_roles,
            color=color,
            roles_field="Command Team",
        ),
        c.embed(
            title=f"{unit_abbrev} MIDCOM",
            description="Mid-level supervision and operational oversight.",
            color=color,
            fields=(
                (
                    c.command_band_label("MIDCOM") + " ranks",
                    c.ranks_text(*c.GRS_ESD_MIDDLE_COMMAND),
                ),
            ),
        ),
        c.embed(
            title=f"{unit_abbrev} LOWCOM",
            description=f"Field and operational ranks within {unit_full}.",
            color=color,
            fields=(
                (c.command_band_label("LOWCOM") + " ranks", c.ranks_text(*c.GRS_ESD_LOW_COMMAND)),
            ),
        ),
        c.important_notice_embed(
            unit=unit_abbrev,
            color=color,
            parent_units=("Directorate of Support", "Office of Security"),
        ),
    ]


def staff_docs_hero_embed(
    *,
    unit_full: str,
    unit_abbrev: str,
    color: int,
    logo: Path | None = None,
) -> discord.Embed:
    """Standard STAFF DOCUMENTS hero for office and sub-unit channels."""
    return c.hero_embed(
        title="STAFF DOCUMENTS",
        unit=unit_full,
        supporting=(
            f"Authorized {unit_abbrev} staff documentation index. Need-to-know access only."
        ),
        color=color,
        logo=logo,
    )


def staff_docs_central_embed(
    *,
    unit_abbrev: str,
    drive_url_key: str,
    drive_link_name: str,
    color: int,
    extra_fields: tuple[tuple[str, str], ...] = (),
) -> discord.Embed:
    """Central Repository block with Drive root and optional extras."""
    fields = (
        c.link_field(
            "Google Drive",
            c.community_link_label(drive_link_name),
            c.url(drive_url_key),
            c.marking_note("STAFF"),
        ),
    ) + extra_fields
    return c.embed(
        title="Central Repository",
        description=(
            f"Primary Google Drive folder for {unit_abbrev} handbooks, guides, forms, and "
            "internal files. Use Drive for materials not listed below."
        ),
        color=color,
        fields=fields,
    )


def staff_docs_section_embed(
    *,
    title: str,
    description: str,
    fields: tuple[tuple[str, str], ...],
    color: int,
) -> discord.Embed:
    """Category section for staff document links."""
    return c.embed(
        title=title,
        description=description,
        color=color,
        fields=fields,
    )


def staff_docs_handling_embed(*, unit_full: str, color: int) -> discord.Embed:
    """Restricted Classification & Handling closer for staff-docs channels."""
    return c.classification_handling_embed(
        unit=unit_full,
        authority=f"CIA {unit_full}",
        color=color,
        restricted=True,
    )


def staff_docs_link(
    name: str,
    link_name: str,
    url_key: str,
) -> tuple[str, str]:
    """STAFF-marked link field with standard CIA DS | label."""
    return c.link_field(
        name,
        c.community_link_label(link_name),
        c.url(url_key),
        c.marking_note("STAFF"),
    )


def info_hero_embed(
    *,
    unit_full: str,
    unit_abbrev: str,
    color: int,
    logo: Path | None = None,
    public: bool = True,
    supporting: str | None = None,
) -> discord.Embed:
    """Standard INFORMATION / PUBLIC INFORMATION hero."""
    if supporting is None:
        supporting = (
            f"Public overview of {unit_abbrev}, its mission, and official community resources."
            if public
            else f"Reference hub for {unit_abbrev} records and authorized documentation."
        )
    return c.hero_embed(
        title="PUBLIC INFORMATION" if public else "INFORMATION",
        unit=unit_full,
        supporting=supporting,
        color=color,
        logo=logo,
    )


def info_about_embed(
    *,
    unit_full: str,
    unit_abbrev: str,
    about: str,
    color: int,
    motto: str | None = None,
    classification: str | None = None,
    fields: tuple[tuple[str, str], ...] = (),
    subunit_parent: str | None = None,
) -> discord.Embed:
    """About block: offices use 'About the Office'; sub-units use 'About {ABBREV}'."""
    if subunit_parent:
        title = f"About {unit_abbrev}"
        framing = (
            f"The **{unit_full}** is a sub-unit of the **{subunit_parent}**, "
            "operating under the **Directorate of Support**.\n\n"
        )
        body = framing + about
    else:
        title = "About the Office"
        body = hierarchy_block_description(
            motto=motto,
            classification=classification,
            about=about,
        )
    return c.embed(
        title=title,
        description=body,
        color=color,
        fields=fields,
    )


def info_community_links_embed(
    *,
    unit_abbrev: str,
    fields: tuple[tuple[str, str], ...],
    color: int,
    description: str | None = None,
) -> discord.Embed:
    """Community Links block with full-sentence description."""
    return c.embed(
        title="Community Links",
        description=(
            description
            or (
                f"Official Roblox groups and community resources for {unit_abbrev} "
                "and its parent organizations."
            )
        ),
        color=color,
        fields=fields,
    )


def info_tryout_requirements_embed(
    *,
    unit_abbrev: str,
    combat_requirement: str,
    color: int,
) -> discord.Embed:
    """Shared GRS/ESD tryout eligibility block."""
    return c.embed(
        title="Tryout Requirements",
        description=(
            f"Minimum eligibility for {unit_abbrev} tryouts and applications:\n"
            f"{c.tryout_requirements_text(combat_requirement=combat_requirement)}"
        ),
        color=color,
    )


def info_reference_documents_embed(
    *,
    unit_full: str,
    fields: tuple[tuple[str, str], ...],
    color: int,
) -> discord.Embed:
    """Reference Documents block for mixed-clearance information hubs."""
    return c.embed(
        title="Reference Documents",
        description=(
            f"Agency-wide and {unit_full} reference material. Observe each "
            "document's clearance marking."
        ),
        color=color,
        fields=fields,
    )


def info_public_link(
    name: str,
    link_name: str,
    url_value: str,
) -> tuple[str, str]:
    """PUBLIC-marked document link with CIA DS | label."""
    return c.link_field(
        name,
        c.community_link_label(link_name),
        url_value,
        c.marking_note("PUBLIC"),
    )


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
