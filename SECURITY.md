# SECURITY.md

Safety + approval rules for Hermes and Claude Code. When in doubt, ask Josh.

## Allowed without asking

- Inspect files
- Create project docs and scripts (inside `command-center`)
- Run read-only system inventory commands
- Propose tasks; draft issues
- Create local files inside this repo
- Run non-destructive verification commands

## Ask before

- `sudo` commands
- package installs
- deleting files
- modifying system services
- exposing ports publicly
- adding secrets
- creating paid accounts
- spending API credits
- pushing to GitHub
- deploying anything
- sending messages/emails
- making financial/legal claims as final advice

## Never commit

`.env` files, API keys, tokens, private keys, wallet seeds, passwords, or
personal documents. These are git-ignored — keep it that way.

## Secrets handling

- Templates live in `configs/*_template.env` with **placeholder** values only.
- Real keys go in local `.env` files outside version control.
- If a secret is ever committed, rotate it immediately and scrub history.

## Tool surface

Start Hermes with a **minimal** tool surface (see `MCP_PLAN.md`). Do not grant
broad or destructive tools until repo + backups + approval rules are proven.
