# === FILE HEADER ===
# Title: Server Regulations
# Path: ds/server_regulations.py
# Created: 2026-07-14
# Created by: docshamxo
# Modified:
#   - 2026-07-14 | docshamxo | Initial CIA Directorate of Support announcer repo.
#   - 2026-07-14 | docshamxo | Add required file headers and footers across the repository.
#   - 2026-07-14 | docshamxo | Refresh file header modification logs after banner rollout.
# === END FILE HEADER ===

"""
CIA DS server regulations announcer.

Posts the Directorate of Support communications server regulations
to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_DS_SERVER_REGULATIONS")


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.embed(
            title="SERVER REGULATIONS",
            description=(
                f"*{c.DS_MOTTO} · Classification: {c.DS_CLASSIFICATION}*\n\n"
                "Welcome to the Roblox Central Intelligence Agency Directorate of Support "
                "Office of Security Communications Server. All personnel and visitors are "
                "expected to maintain professionalism, discipline, and operational integrity "
                "at all times. Failure to comply with the following regulations may result in "
                "administrative action, removal from the server, or further disciplinary measures."
            ),
        ),
        c.embed(
            description=(
                "**PROFESSIONAL CONDUCT**\n"
                "All members shall conduct themselves in a respectful and professional manner "
                "regardless of rank, position, or affiliation. Disrespectful, disruptive, or "
                "hostile behavior is prohibited.\n\n"
                "**DISCRIMINATION AND HARASSMENT**\n"
                "Harassment, discrimination, hate speech, threats, or targeted abuse based on "
                "race, religion, nationality, gender, or any protected characteristic will not "
                "be tolerated under any circumstances.\n\n"
                "**COMPLIANCE WITH DISCORD POLICIES**\n"
                "All members must comply with Discord's Terms of Service and Community "
                "Guidelines at all times. Violations of Discord policy are also considered "
                "violations of server regulations.\n\n"
                "**SPAM AND UNAUTHORIZED PROMOTION**\n"
                "Spamming, flooding channels, mass messaging, excessive pinging, or advertising "
                "external communities, products, or services without authorization from Office "
                "of Security leadership is prohibited."
            ),
        ),
        c.embed(
            description=(
                "**APPROPRIATE CONTENT STANDARDS**\n"
                "All communications, media, usernames, and profile content must remain "
                "appropriate for a professional operational environment. NSFW, explicit, "
                "graphic, or otherwise inappropriate material is strictly prohibited.\n\n"
                "**CHAIN OF COMMAND**\n"
                "Personnel are required to respect and follow the established chain of command. "
                "Orders and directives issued by authorized supervisory personnel are expected "
                "to be followed unless they violate server policy or administration directives.\n\n"
                "**PROPER CHANNEL USAGE**\n"
                "Members must use channels for their designated purpose. Off-topic discussions "
                "should remain within approved discussion channels."
            ),
        ),
        c.embed(
            description=(
                "**TROLLING AND DISRUPTIVE BEHAVIOR**\n"
                "Trolling, baiting, flaming, provoking arguments, or intentionally disrupting "
                "operations or conversations is prohibited.\n\n"
                "**IMPERSONATION**\n"
                "Impersonating Office of Security personnel, staff members, leadership, or other "
                "community members is strictly forbidden.\n\n"
                "**REPORTING PROCEDURES**\n"
                "Operational concerns, misconduct, or rule violations should be reported through "
                "designated reporting procedures or directly to authorized staff members.\n\n"
                "**UNAUTHORIZED ADVERTISING**\n"
                "Advertising other Roblox groups, Discord servers, organizations, websites, or "
                "social platforms without prior authorization is prohibited."
            ),
        ),
        c.embed(
            description=(
                "**COMPLIANCE WITH STAFF DIRECTIVES**\n"
                "Instructions issued by Office of Security staff, moderators, or administrative "
                "personnel must be followed. Administrative decisions regarding server operations "
                "and moderation are final unless overturned by higher authority.\n\n"
                "**PRIVACY AND SECURITY**\n"
                "Sharing personal information, leaking confidential material, doxxing, or "
                "engaging in activities that compromise operational security or member privacy "
                "is strictly prohibited.\n\n"
                "**BOT USAGE**\n"
                "Bots and automated systems must be used responsibly and only within designated "
                "channels and approved purposes.\n\n"
                "**POLITICAL AND CONTROVERSIAL TOPICS**\n"
                "Political debates, extremist content, election discussions, political harassment, "
                "or inflammatory discussions regarding governments, political parties, or current "
                "geopolitical conflicts are prohibited to maintain operational professionalism."
            ),
        ),
        c.embed(
            description=(
                "**ENFORCEMENT ACTIONS**\n"
                "Violations of server regulations may result in warnings, communication "
                "restrictions, suspension, removal from Office of Security operations, or "
                "permanent removal from the community depending on severity and frequency of "
                "violations.\n\n"
                "----------\n\n"
                "Failure to understand these regulations does not exempt personnel from "
                "enforcement actions. Presence within this server constitutes acknowledgment "
                "and acceptance of all established regulations and administrative policies."
            ),
        ),
        c.disclaimer_embed(),
    ]


def send_server_regulations() -> None:
    c.send_webhook(WEBHOOK_URL, _build_embeds(), username=c.BOT_DS)


if __name__ == "__main__":
    send_server_regulations()

# === FILE FOOTER ===
# End of file: ds/server_regulations.py
# Maintained by: docshamxo
# === END FILE FOOTER ===
