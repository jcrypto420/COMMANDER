# TASK_QUEUE.md

Simple task board. Status: `todo` / `doing` / `blocked` / `done`.
Approval = does this need Josh's OK before acting? (see `SECURITY.md`)

| ID | Project | Pri | Task | Status | Next action | Approval |
|----|---------|-----|------|--------|-------------|----------|
| CC-1 | Command Center | 1 | Create repo scaffolding | done | Review files | no |
| CC-2 | Command Center | 1 | Run `pi_inventory.sh` on Pi | todo | `bash scripts/pi_inventory.sh` | no |
| CC-3 | Command Center | 1 | Verify Hermes install command vs live docs | todo | Check docs links in HERMES_SETUP.md | no |
| CC-4 | Command Center | 1 | Install Hermes on Pi | blocked | Wait for CC-3 + Josh approval | **yes** |
| CC-5 | Command Center | 1 | Create `commander` profile + 1 provider | blocked | After CC-4 | **yes** |
| CC-6 | Command Center | 1 | Run first safe Hermes task (read-only summary) | blocked | After CC-5 | no |

## Notes

- Keep this board short. Archive finished items to `logs/daily_progress.md`.
- One task "doing" at a time when possible.
