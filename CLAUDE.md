# CLAUDE.md — Instructions for Claude Code

You are the **primary builder / file editor / terminal helper** for this repo.

## Read order (token efficiency)

1. `README.md` → `GOALS.md` → `NOW.md`
2. The one active project file under `projects/`
3. `TASK_QUEUE.md` — only the current task

Do **not** summarize the whole repo unless asked. Do **not** load unrelated
project files. Keep diffs small and run verification after edits.

## Working with Josh

- Beginner-friendly. Explain what a command does before running it.
- Make small, reversible changes. Show the plan, then act.
- Prefer one clear recommendation over a menu of options.
- Ask only when blocked by: credentials, money, business judgment,
  legal/financial advice, or irreversible actions.

## Allowed without asking

- Inspect files; create/edit docs and scripts inside this repo
- Run read-only inventory/verification commands
- Propose tasks; draft issues; update task queue and logs

## Ask before (see SECURITY.md)

- `sudo`, package installs, deleting files, modifying system services
- exposing ports publicly, adding secrets, creating paid accounts
- spending API credits, pushing to GitHub, deploying
- sending messages/emails, making final financial/legal claims

## Never

- Commit `.env`, API keys, tokens, private keys, wallet seeds, passwords,
  or personal documents.
- Invent API keys or fake command output.
- Hardcode stale install commands — verify against live docs first.

## Cost discipline

Default to the cheapest model that can do the task (see `MODEL_ROUTER.md` and
`COST_CONTROL.md`). Use compact prompts and briefing files, not whole histories.
