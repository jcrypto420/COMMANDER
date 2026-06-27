# HERMES_SETUP.md

How to install Hermes Agent and create the `commander` profile **safely**.

> **Verified 2026-06-27** against the official docs + GitHub README.
> Hermes supports Linux **ARM64**, so the Raspberry Pi 4 (`aarch64`) works.
> The installer bundles its own Python 3.11+. Run all of this **on the Pi**
> (over SSH), not on the Windows laptop.

## Docs (source of these commands)

- https://hermes-agent.nousresearch.com/docs/
- https://github.com/NousResearch/hermes-agent
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/profiles.md
- https://hermes-agent.nousresearch.com/docs/integrations/providers
- https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models

## Step 0 — Inventory (safe, no changes)

```bash
bash scripts/pi_inventory.sh
```

Confirm: arch is `aarch64`, plus RAM/disk. (Python/Node are NOT required — the
installer bundles Python.)

## Step 1 — Install Hermes (needs Josh's approval)

The official installer (it sets up its own Python; does not need sudo):

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.bashrc          # reload shell so the `hermes` command is found
```

Cautious wrapper (same command, but guarded — won't run until you opt in):

```bash
CONFIRM=yes bash scripts/install_hermes.sh
```

## Step 2 — Connect a model provider (easiest first)

```bash
hermes setup --portal
```

This does one OAuth login to **Nous Portal** and gives you a model plus tool
features (web search, image gen, TTS, browser) — the fastest path to a working
agent on day one. (Alternative: `hermes setup` for manual provider/key entry;
`hermes model` to switch providers/models later — OpenRouter, Anthropic, OpenAI,
Ollama/your own endpoint, etc. See `PROVIDERS.md` / `MODEL_ROUTER.md`.)

## Step 3 — Create the `commander` profile

```bash
hermes profile create commander      # makes ~/.hermes/profiles/commander/
hermes profile use commander         # make it the default (optional)
```

Each profile has its own `config.yaml`, `.env`, `SOUL.md`, memories, sessions,
skills, cron, and state DB in `~/.hermes/profiles/commander/`.

Optionally seed it from our templates (then edit; **never commit secrets**):

```bash
cp configs/hermes_config_template.yaml ~/.hermes/profiles/commander/config.yaml
cp configs/hermes_env_template.env      ~/.hermes/profiles/commander/.env
```

Put API keys only in that local `.env`.

## Step 4 — Verify (safe)

```bash
bash scripts/verify_hermes.sh
hermes profile use commander && hermes --version   # confirm profile + binary
```

## Step 5 — First safe Hermes task (read-only)

Start the agent on the profile, pointed at this repo:

```bash
cd ~/COMMANDER         # wherever you cloned command-center
commander chat         # or: hermes -p commander chat
```

Then give it this task (no edits, no shell):

```text
Read README.md, GOALS.md, NOW.md, PROJECTS.md, TASK_QUEUE.md,
MODEL_ROUTER.md, and SECURITY.md. Summarize:
1) the current mission, 2) the top three tasks,
3) the cheapest model/provider strategy, 4) any blockers.
Do not edit files. Do not run shell commands.
```

## Day-one success

Hermes runs · `commander` profile exists · one provider works · one safe task
completes · cost strategy documented · no secrets committed.
