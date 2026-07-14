"""
CIA GRS staff documents announcer.

Posts official Global Response Staff guides, training material, and
certification resources to a Discord webhook.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import cia_common as c

WEBHOOK_URL = c.require_webhook("WEBHOOK_GRS_STAFF_DOCUMENTS")

URL_BREACH_TRAINING_GUIDE = (
    "https://docs.google.com/document/d/1BopFMmd_0GC2q7k1gLssRJ_RJh6BMAFA3kObdlj407w/edit?usp=sharing"
)
URL_BREACHING_CERTIFICATE = (
    "https://docs.google.com/document/d/10VyRbeIE2IMP1qFt6wIZpzN50Iegwpzh0n3dnU_8--c/edit?usp=sharing"
)
URL_HANDBOOK = (
    "https://docs.google.com/document/d/1vCBNGn-Vv07FAqVUYle5AFGMy-5yXQJkRDGpYYhBsIU/edit?usp=sharing"
)
URL_TRYOUT_GUIDE = (
    "https://docs.google.com/document/d/1e199RDQlZ2sxU-qgAGB_jBM0ksPb-DVkNmXlburxNA0/edit?usp=sharing"
)


def _build_embeds() -> list[c.discord.Embed]:
    return [
        c.embed(
            title="STAFF DOCUMENTS",
            description=(
                "*Central Intelligence Agency · Global Response Staff*\n\n"
                f"{c.GRS_ABOUT}\n\n"
                "This channel serves as the official repository for authorized GRS "
                "staff documentation. The Global Response Staff is a sub-unit of the "
                "**Office of Security** under the **Directorate of Support**.\n\n"
                "Access is **strictly limited** to authorized personnel. Review, use, "
                "and handle all materials responsibly."
            ),
            color=c.COLOR_GRS,
            logo=c.LOGOS["grs"],
        ),
        c.embed(
            title="Training & Operational Guides",
            description="Official guides for GRS personnel, training, tryouts, and operations.",
            color=c.COLOR_GRS,
            fields=(
                c.link_field(
                    "Handbook",
                    "CIA GRS | Handbook",
                    URL_HANDBOOK,
                    "Primary reference for GRS policy and standards.",
                ),
                c.link_field(
                    "Breach Training",
                    "CIA GRS | Breach Training Guide",
                    URL_BREACH_TRAINING_GUIDE,
                    "Official breach training procedures and instruction.",
                ),
                c.link_field(
                    "Tryouts",
                    "CIA GRS | Tryout Guide",
                    URL_TRYOUT_GUIDE,
                    "Candidate tryout standards and evaluation guidance.",
                ),
            ),
        ),
        c.embed(
            title="Certifications",
            description="Official certification documentation for GRS personnel.",
            color=c.COLOR_GRS,
            fields=(
                c.link_field(
                    "Breaching Certification",
                    "CIA GRS | Breaching Certificate",
                    URL_BREACHING_CERTIFICATE,
                    "Qualification standards for breaching certification.",
                ),
            ),
        ),
        c.embed(
            title="Classification & Handling Notice",
            description=(
                "All documents listed in this channel are intended for **authorized GRS "
                "personnel only**.\n\n"
                "Unauthorized disclosure, redistribution, or leaking of any restricted "
                "material may result in a **BLACKLIST** from the **CIA Directorate of Support**.\n\n"
                "Handle all staff documents responsibly. Do not share materials outside "
                "authorized channels or personnel."
            ),
            color=c.COLOR_GRS,
        ),
        c.disclaimer_embed(classified=True),
    ]


def send_grs_staff_documents() -> None:
    c.send_webhook(
        WEBHOOK_URL,
        _build_embeds(),
        username=c.BOT_GRS,
        files=[c.logo_file(c.LOGOS["grs"])],
    )


if __name__ == "__main__":
    send_grs_staff_documents()
