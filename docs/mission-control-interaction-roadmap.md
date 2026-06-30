# Mission Control Interaction Roadmap

Purpose: make the dashboard feel like a real command dapp without weakening safety.

## v0.1 — clickable repo artifacts

Status: implemented.

Mission Control can safely open whitelisted repo artifacts through `/files/...`, including:

- `assets/...` review galleries and images
- `projects/...` project briefs
- `docs/...` docs
- `MORNING_REPORT.md`
- `WEEKLY_MONEY_REVIEW.md`
- selected root status docs

Blocked by design:

- `.env`
- secrets / credentials / tokens
- wallet/seed/private-key filenames
- `node_modules`, `.git`, `.next`
- paths outside `/home/josh/COMMANDER`

## v0.2 — action cards

Status: implemented for first approval commands.

Mission Control now has a Decision Console:

1. Open the artifact.
2. Pick the command.
3. Copy it and paste into Telegram or the CLI chat.

Current command cards:

- Open real Bad Boys asset gallery + copy `APPROVE REAL ASSET ACCOUNT PREP`
- Open IN-1 paid-research backstop + copy `RUN IN-1 LEAD VERIFY`
- Open this roadmap + copy `PAUSE BAD BOYS — IMPROVE MISSION CONTROL`

Buttons still do not post, send, spend, trade, deploy, or change services.

## v0.3 — chat with Commander inside Mission Control

Recommended safe path:

1. Keep Telegram as the live Commander control channel for now.
2. Add a dashboard “Chat with Commander” panel that deep-links or gives a one-tap Telegram command first.
3. Later, add a local/private web chat endpoint only after auth/access control is designed.

Why not rush direct in-dashboard chat:

- A web chat endpoint is more powerful and riskier than read-only dashboard panels.
- It needs authentication, CSRF/rate limits, session routing, and clear approval behavior.
- Telegram is already Josh-only and proven.

Future implementation options:

- Local-only form that writes a queued prompt file for Commander to pick up.
- Webhook route into Hermes with allowlist/auth.
- Embedded gateway chat once Hermes dashboard/API auth is configured.
- Tailscale-only access plus a simple passphrase/OAuth layer.

Safety requirement:

Any in-dashboard chat must preserve the same approval gates: no spending, sending, posting, service changes, account actions, secrets, trades, or final financial/legal advice without Josh approval.
