# === FILE HEADER ===
# Title: Exit Codes
# Path: common/exit_codes.py
# Created: 2026-07-17
# Created by: docshamxo
# Modified:
#   - 2026-07-17 | docshamxo | Nagios-style exit codes for announcer / run_all alerting.
# === END FILE HEADER ===

"""Alerting-style process exit codes (Nagios / Icinga compatible).

0 OK        - work completed as expected
1 WARNING   - degraded (e.g. nothing runnable / strict-skips tripped)
2 CRITICAL  - one or more hard failures
3 UNKNOWN   - unexpected runner/control-plane error
"""

from __future__ import annotations

OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

ANNOUNCER_OK = OK
ANNOUNCER_SKIPPED = 10
ANNOUNCER_CONFIG = 20

EXIT_CODE_HELP = {
    OK: "OK - all runnable announcers succeeded",
    WARNING: "WARNING - degraded (all skipped, or --strict-skips with skips)",
    CRITICAL: "CRITICAL - one or more announcer hard failures",
    UNKNOWN: "UNKNOWN - unexpected runner error",
    ANNOUNCER_SKIPPED: "announcer intentional skip (empty webhook)",
    ANNOUNCER_CONFIG: "announcer config / fail-closed error",
}


def classify_batch_exit(
    *,
    succeeded: int,
    skipped: int,
    failed: int,
    strict_skips: bool = False,
) -> int:
    """Map batch counters to an alerting exit code."""
    if failed > 0:
        return CRITICAL
    if succeeded == 0 and skipped == 0:
        return UNKNOWN
    if succeeded == 0 and skipped > 0:
        return WARNING
    if strict_skips and skipped > 0:
        return WARNING
    return OK


# === FILE FOOTER ===
# End of file: common/exit_codes.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
