# AGENTS.md — Roles

| Tool | Role |
|------|------|
| **ChatGPT** | Architect / strategist / project manager |
| **Claude Code** | Primary builder / file editor / terminal helper |
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
