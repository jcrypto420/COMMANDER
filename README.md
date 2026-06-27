# Command Center

Josh's AI command center. A compact, shared source of truth for **Claude Code**,
**Codex**, **GitHub**, the **terminal**, and **Hermes Agent** so they all work
from the same project truth.

**Mission:** Run Hermes as a safe, increasingly autonomous operator that helps
Josh make money as passively/automatically as possible, while keeping token/API
costs low and avoiding context drift.

First runtime: **Raspberry Pi 4 (`commandcenter`)** — always-on lightweight
orchestrator, *not* the heavy local-LLM box.

## How agents should use this repo

Read in this order (and stop — don't load the whole repo):

1. `README.md` (this file)
2. `GOALS.md`
3. `NOW.md`
4. The one active project file under `projects/`
5. `TASK_QUEUE.md` — only the current task

Then follow `CLAUDE.md` (Claude Code rules), `AGENTS.md` (who does what), and
`SECURITY.md` (what needs approval).

## First commands

On the Raspberry Pi, after cloning this repo:

```bash
# 1. Read-only inventory of the Pi (changes nothing)
bash scripts/pi_inventory.sh

# 2. Read the Hermes setup plan, then verify install commands against live docs
less HERMES_SETUP.md
```

Hermes install and the `commander` profile are **not** run automatically — they
require Josh's approval (see `HERMES_SETUP.md` and `SECURITY.md`).

## Layout

| Path | Purpose |
|------|---------|
| `GOALS.md` / `NOW.md` | Mission + current focus |
| `PROJECTS.md` / `projects/` | Money-making projects (kept separate) |
| `TASK_QUEUE.md` | Simple task board |
| `HERMES_SETUP.md` | Verified Hermes install + `commander` profile |
| `MODEL_ROUTER.md` / `PROVIDERS.md` / `LOCAL_MODELS.md` | Cheap-first model routing |
| `COST_CONTROL.md` | Token/spend discipline |
| `SECURITY.md` | Approval + safety rules |
| `MONEY_OPS.md` | Daily make-money loop |
| `MCP_PLAN.md` | Minimal-first MCP tool surface |
| `GITHUB_WORKFLOW.md` | Branch/commit/PR conventions |
| `configs/` | Hermes/MCP/router templates (no secrets) |
| `scripts/` | Cautious, read-only-first helper scripts |
| `logs/` | Usage + daily progress logs |

**Never commit secrets.** See `SECURITY.md` and `.gitignore`.
