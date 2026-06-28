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
| CC-8 | Command Center | 1 | Daily make-money loop as cron (draft-only) | doing | job created+tested; needs gateway service to auto-fire 7am | yes |
| CC-9 | Command Center | 1 | Install gateway service (auto-fire cron + messaging) | todo | `sudo hermes gateway install --system` (Josh) | **yes** |
| CC-10 | Command Center | 1 | Phone access via Telegram bot | todo | BotFather token + `commander gateway setup` | **yes** |
| IN-1 | Career/Income | 2 | First lead list + 1 outreach draft | todo | drafts only, no sending | no |

## Notes

- Keep this board short. Archive finished items to `logs/daily_progress.md`.
- One task "doing" at a time when possible.
