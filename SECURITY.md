<!--
=== FILE HEADER ===
Title: Security
Path: SECURITY.md
Created: 2026-07-14
Created by: docshamxo
Modified:
  - 2026-07-14 | docshamxo | Polish repository presentation and align documentation.
  - 2026-07-14 | docshamxo | Simplify setup and contributor docs.
=== END FILE HEADER ===
-->

# Security

Webhook URLs can post into Discord channels. Keep them private.

- Store them only in your local `.env`
- Use `python setup.py` to create `.env` from `.env.example`
- Never commit `.env`, paste webhooks into PRs, or share them in chat
- If a webhook leaks, regenerate it in Discord and update `.env`

<!--
=== FILE FOOTER ===
End of file: SECURITY.md
Maintained by: docshamxo
=== END FILE FOOTER ===
-->
