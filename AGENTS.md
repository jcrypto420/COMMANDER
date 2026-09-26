# AGENTS.md — Roles

| Tool | Role |
|------|------|
| **ChatGPT** | Architect / strategist / project manager — ALSO runs a parallel job-search lane with Josh; its applications/searches MUST be recorded in `jobs/TRACKER.md` (dedupe: Chainlink was applied there while Hermes/Claude drafted for it) |
| **Claude Code** | Primary builder / file editor / terminal helper — runs on Josh's Mac (MOGDROP toolchain), local clone at `~/COMMANDER`; syncs with Hermes via this repo (pull before work, push after) |
| **Codex** | Second builder / reviewer / debugging assistant |
| **GitHub** | Source of truth and task history |
| **Raspberry Pi 4 (`commandcenter`)** | Always-on runtime |
| **Hermes Agent** | Autonomous execution operator |
| **Ollama** | Local model runtime (tiny on Pi; stronger later on better hardware) |
| **OpenRouter / Nous Portal / Venice / etc.** | Cheap or fallback hosted inference |

## Hermes profiles

- Start with **one** profile: `commander`.
- Do **not** create multiple sub-agents yet.
- `commander` reads this repo as its source of truth and runs the daily
  make-money loop (see `MONEY_OPS.md`).

## Future sub-agent structure (not yet)

When the base system is stable, profiles may specialize (e.g. `researcher`,
`builder`, `outreach`). Each Hermes profile gets its own config, `.env`,
`SOUL.md`, memories, sessions, skills, cron, and state DB. Keep tool surface
minimal until backups + approval rules are proven (see `MCP_PLAN.md`,
`SECURITY.md`).
