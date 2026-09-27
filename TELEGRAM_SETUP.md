# Telegram Setup Checklist

Purpose: connect Commander to Josh's phone for summaries, blockers, and approval
requests while keeping risky actions gated.

## Current status

- Hermes gateway is running manually on the Pi.
- The `hermes` launcher is available at `/home/josh/.local/bin/hermes`; it may
  not be on PATH in every non-interactive shell.
- Telegram is the recommended first phone channel, but setup requires a bot
  token/secret from Josh. Do not store the token in git.

## Josh steps

1. Open Telegram.
2. Message `@BotFather`.
3. Create a bot with `/newbot`.
4. Copy the bot token.
5. Do **not** paste the token into GitHub or any repo file.
6. Provide the token only through the local Hermes setup prompt or another safe
   secret-entry path.

## Commander steps after Josh has the token ready

Run from the Pi / local shell:

```bash
/home/josh/.local/bin/hermes gateway setup
```

Then:

```bash
/home/josh/.local/bin/hermes gateway restart
/home/josh/.local/bin/hermes gateway status
```

If the gateway needs to persist through logout, install/run it as a user service
only after Josh approves any service changes:

```bash
/home/josh/.local/bin/hermes gateway install
/home/josh/.local/bin/hermes gateway start
```

## Safety settings

Initial Telegram scope should be:

- Daily summary delivery.
- Blocker notifications.
- Approval requests.
- Short user commands like "run today's loop" or "focus Bad Boys today".

Still requires approval:

- Posting/sending public content.
- Spending/API credits.
- Adding secrets.
- Deployments/services/ports.
- GitHub pushes unless separately approved.
- DeFi/financial actions.

## First harmless test

After setup, send a harmless status check to the Telegram chat or use the Hermes
platform test flow if offered by `gateway setup`.

Expected first message style:

```text
Commander phone channel connected.
Mode: summaries/blockers/approvals only.
No spending, posting, sending, deployments, or secrets without Josh approval.
```
