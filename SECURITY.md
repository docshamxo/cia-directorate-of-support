# Security

Webhook URLs can post into Discord channels. Keep them private.

- Store them only in your local `.env`
- Use `python setup.py` to create `.env` from `.env.example`
- Never commit `.env`, paste webhooks into PRs, or share them in chat
- If a webhook leaks, regenerate it in Discord and update `.env`
