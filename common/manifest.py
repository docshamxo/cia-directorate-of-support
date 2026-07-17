# === FILE HEADER ===
# Title: Manifest
# Path: common/manifest.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Single announcer catalog for run_all and validate_repo.
#   - 2026-07-17 | docshamxo | Staged office rollout order for safer live sends.
#   - 2026-07-17 | docshamxo | Announcer scripts live under units/<office>/.
# === END FILE HEADER ===

"""Announcer catalog — single source of truth for run_all and validate_repo."""

from __future__ import annotations

from pathlib import Path

# Office folder names (discoverable under units/).
OFFICES: tuple[str, ...] = ("ds", "osec", "ote", "grs", "esd")

# (relative script path, human label, WEBHOOK_* env key)
ANNOUNCERS: tuple[tuple[str, str, str], ...] = (
    ("units/ds/chain_of_command.py", "DS Chain of Command", "WEBHOOK_DS_CHAIN_OF_COMMAND"),
    ("units/ds/public_information.py", "DS Public Information", "WEBHOOK_DS_PUBLIC_INFORMATION"),
    ("units/ds/server_regulations.py", "Server Regulations", "WEBHOOK_DS_SERVER_REGULATIONS"),
    ("units/osec/information.py", "OSEC Information", "WEBHOOK_OSEC_INFORMATION"),
    ("units/osec/staff_documents.py", "OSEC Staff Documents", "WEBHOOK_OSEC_STAFF_DOCUMENTS"),
    (
        "units/osec/spp_information.py",
        "OSEC Security Phase Program",
        "WEBHOOK_OSEC_SPP_INFORMATION",
    ),
    ("units/osec/open_positions.py", "OSEC Open Positions", "WEBHOOK_OSEC_OPEN_POSITIONS"),
    ("units/ote/coc.py", "OTE Chain of Command", "WEBHOOK_OTE_COC"),
    ("units/ote/public_information.py", "OTE Public Information", "WEBHOOK_OTE_PUBLIC_INFORMATION"),
    ("units/ote/program_overview.py", "OTE Program Overview", "WEBHOOK_OTE_PROGRAM_OVERVIEW"),
    ("units/ote/staff_documents.py", "OTE Staff Documents", "WEBHOOK_OTE_STAFF_DOCUMENTS"),
    ("units/ote/open_positions.py", "OTE Open Positions", "WEBHOOK_OTE_OPEN_POSITIONS"),
    ("units/grs/coc.py", "GRS Chain of Command", "WEBHOOK_GRS_COC"),
    ("units/grs/information.py", "GRS Information", "WEBHOOK_GRS_INFORMATION"),
    ("units/grs/staff_documents.py", "GRS Staff Documents", "WEBHOOK_GRS_STAFF_DOCUMENTS"),
    ("units/esd/coc.py", "ESD Chain of Command", "WEBHOOK_ESD_COC"),
    ("units/esd/information.py", "ESD Information", "WEBHOOK_ESD_INFORMATION"),
    ("units/esd/staff_documents.py", "ESD Staff Documents", "WEBHOOK_ESD_STAFF_DOCUMENTS"),
)

# Safer live rollout: one office (stage) at a time. Operators advance explicitly.
# (stage id, human title, office folder)
ROLLOUT_STAGES: tuple[tuple[str, str, str], ...] = (
    ("1", "DS public core", "ds"),
    ("2", "OSEC", "osec"),
    ("3", "OTE", "ote"),
    ("4", "GRS", "grs"),
    ("5", "ESD", "esd"),
)

# Webhook keys whose embeds may reference STAFF_LOCAL_REQUIRED placeholders.
# Live sends warn/fail closed when unresolved; dry-run still builds embeds.
STAFF_WEBHOOK_KEYS: frozenset[str] = frozenset(
    {
        "WEBHOOK_OSEC_INFORMATION",
        "WEBHOOK_OSEC_STAFF_DOCUMENTS",
        "WEBHOOK_OSEC_SPP_INFORMATION",
        "WEBHOOK_OTE_STAFF_DOCUMENTS",
        "WEBHOOK_GRS_INFORMATION",
        "WEBHOOK_GRS_STAFF_DOCUMENTS",
        "WEBHOOK_ESD_STAFF_DOCUMENTS",
    }
)


def resolve_rollout_stage(token: str) -> tuple[str, str, str]:
    """Resolve ``--stage`` token to ``(id, title, office)``. Raises ValueError if unknown."""
    raw = token.strip().lower()
    if not raw:
        raise ValueError("empty stage token")
    for stage_id, title, office in ROLLOUT_STAGES:
        if raw in {stage_id, office, f"{stage_id}-{office}", title.lower()}:
            return stage_id, title, office
    known = ", ".join(f"{sid} ({office})" for sid, _title, office in ROLLOUT_STAGES)
    raise ValueError(f"Unknown rollout stage {token!r}. Expected one of: {known}")


def announcers_for_office(office: str) -> list[tuple[str, str, str]]:
    """Return catalog entries for ``office`` (e.g. ``ds`` → ``units/ds/...``)."""
    name = office.strip().lower().rstrip("/")
    if name.startswith("units/"):
        name = name[len("units/") :]
    return [entry for entry in ANNOUNCERS if name in Path(entry[0].replace("\\", "/")).parts]


# === FILE FOOTER ===
# End of file: common/manifest.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
