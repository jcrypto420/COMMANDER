# HERMES_SETUP.md

How to install Hermes Agent and create the `commander` profile **safely**.

> ⚠️ **Do not hardcode stale install commands.** The commands below are marked
> **VERIFY** until checked against the live docs. Verify first, then fill in the
> exact command, then ask Josh before running anything that installs or uses
> `sudo`.

## Docs to verify (open these first)

- https://hermes-agent.nousresearch.com/docs/
- https://hermes-agent.nousresearch.com/docs/integrations/providers
- https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- https://github.com/NousResearch/hermes-agent
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/profiles.md

## Step 0 — Inventory (safe, no changes)

```bash
bash scripts/pi_inventory.sh
```

Confirm: arch (`aarch64`), RAM, disk, Docker, Python/Node versions. This tells
us which Hermes install method fits the Pi.

## Step 1 — Pick install method (VERIFY)

Check the docs for the supported install on Linux/ARM64. It is likely one of:

- a published package / installer script, or
- a Docker image, or
- a source/checkout install.

Record the **verified** command here:

```bash
# VERIFY: replace with the exact command from the docs
# e.g. (placeholder) curl -fsSL <official-url> | sh
```

Then run the cautious helper (it only prints/guards by default):

```bash
bash scripts/install_hermes.sh
```

> `install_hermes.sh` will NOT install until you set `CONFIRM=yes` and have
> pasted the verified command into it. See the script header.

## Step 2 — Create the `commander` profile (after approval)

Use the templates (copy, then fill secrets locally — never commit):

```bash
cp configs/hermes_config_template.yaml ~/.hermes/commander/config.yaml   # path VERIFY
cp configs/hermes_env_template.env      ~/.hermes/commander/.env          # path VERIFY
```

Edit `config.yaml` for the day-one provider (see `PROVIDERS.md`) and set the
model tiers from `MODEL_ROUTER.md`. Put the API key only in the local `.env`.

## Step 3 — Verify (safe)

```bash
bash scripts/verify_hermes.sh
```

Confirms the binary/container responds and the `commander` profile is detected.

## Step 4 — First safe Hermes task (read-only)

Give Hermes this task (no edits, no shell):

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
