# Security

## Discord webhooks

Webhook URLs grant permission to post into Discord channels. Treat them as secrets.

| Do | Do not |
|----|--------|
| Store URLs in a local `.env` file | Commit `.env` or paste webhooks into issues/PRs |
| Copy from `.env.example` | Hard-code URLs in Python modules |
| Rotate a webhook if it was shared | Reuse the same webhook across unrelated channels unless intentional |

Staff-document and chain-of-command announcers may target restricted channels. Prefer least privilege: one webhook per channel.

## Reporting

If a webhook or other secret is exposed, regenerate it in Discord channel settings and update your local `.env` immediately.
