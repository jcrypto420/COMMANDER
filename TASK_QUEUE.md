# TASK_QUEUE.md

Simple task board. Status: `todo` / `doing` / `blocked` / `done`.
Approval = does this need Josh's OK before acting? (see `SECURITY.md`)

| ID | Project | Pri | Task | Status | Next action | Approval |
|----|---------|-----|------|--------|-------------|----------|
| CC-1 | Command Center | 1 | Create repo scaffolding | done | — | no |
| CC-2 | Command Center | 1 | Inventory the Pi | done | aarch64, Debian 12, 31G free | no |
| CC-3 | Command Center | 1 | Verify Hermes install command vs live docs | done | verified 2026-06-27 | no |
| CC-4 | Command Center | 1 | Install Hermes on Pi | done | v0.17.0 in ~/.local/bin | yes |
| CC-5 | Command Center | 1 | Create `commander` profile + provider | done | Codex/ChatGPT OAuth | yes |
| CC-6 | Command Center | 1 | Run first safe Hermes task (read-only) | done | summary passed | no |
| CC-7 | Command Center | 1 | Add OpenRouter as cheap fallback tier | done | fallback: codex → gemini-2.5-flash → llama-3.1-8b | yes |
| CC-8 | Command Center | 1 | Daily make-money loop as cron (draft-only) | done | live; fires 7am daily; test run produced correct draft | yes |
| CC-9 | Command Center | 1 | Gateway service (cron scheduler) | done | user-level (non-root), linger on, NO listening ports | yes |
| CC-10 | Command Center | 1 | Private phone access (Tailscale-first) | todo | try Tailscale SSH / dashboard before any chat platform | **yes** |
| CC-11 | Command Center | 1 | Apply approved onboarding intake doc updates | done | GOALS/NOW/project files updated from INTAKE.md | no |
| REV-1 | Revenue Sprint | 1 | Choose first 69-day revenue sprint experiment | todo | compare speed to revenue, cost, risk, Josh time | no |
| IN-1 | Career/Income | 2 | First lead list + 1 outreach draft | todo | drafts only, no sending | no |
| BB-1 | Bad Boys/Joycat | 2 | Public Joycat/Mog/Mogcoin research + asset inventory | todo | research CT context; ask Josh for Bad Boys files | no |
| BB-2 | Bad Boys/Joycat | 2 | First audience/sales launch loop draft | todo | draft content cadence + offer; no posting | no |
| WO-1 | Weather Oracle | 4 | Revenue-option scan before build | todo | identify profitable/grant/leverage angles | no |

## Notes

- Keep this board short. Archive finished items to `logs/daily_progress.md`.
- One task "doing" at a time when possible.
