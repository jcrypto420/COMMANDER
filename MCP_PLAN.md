# MCP_PLAN.md

Hermes can load external tools via MCP. **Start minimal. Never expose too much
at once.** Verify MCP docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp

## Phase 1 — Minimal (start here)

- **Filesystem (read-only, scoped to this repo):** let Hermes read the truth
  files. No write/delete outside `command-center`.
- Built-in Hermes tools only beyond that.

## Phase 2 — After base system is stable + approvals proven

- **GitHub MCP:** read issues/PRs, draft issues. Writes/pushes require approval.
- **Filesystem (write, scoped):** edit repo files with small diffs.

## Phase 3 — Later, deliberately

- Browser stack (research/scraping) — sandboxed.
- Database (e.g. project tracker, plant/pricing DB for Primoscapes).
- Internal APIs (Weather Oracle, dashboards).

## Hard limits (see SECURITY.md)

- No broad/destructive tools yet.
- No financial-account, wallet/private-key, or autonomous-spending tools.
- No broad Gmail/calendar access.
- Each new tool added one at a time, with a clear scope and an approval rule.
