# TASK_QUEUE.md

Active task board only. Completed history lives in `TASK_ARCHIVE.md` and narrative progress lives in `logs/daily_progress.md`.

Status: `todo` / `doing` / `blocked` / `done`.
Approval = does this need Josh's OK before acting? (see `SECURITY.md`).

Operating rule: keep exactly one `doing` task when possible. Parked lanes should be `blocked` with a clear reopen condition, not half-active.

| ID | Project | Pri | Task | Status | Next action | Approval |
|----|---------|-----|------|--------|-------------|----------|
| CC-10 | Command Center | 1 | Private phone access (Tailscale-first) | todo | try Tailscale SSH / dashboard before any chat platform | **yes** |
| CC-13 | Command Center | 1 | Test model-specific worker pattern | todo | run one cheap read-only worker and log result | no |
| CI-1 | Career/Income | 1 | Daily job/application process | blocked | next lane after OPS-1 checkpoint; build draft-only tracker/checklist, no submissions/messages without Josh approval | **yes** |
| BB-17 | Bad Boys/Joycat | 2 | Week 1 manual posting packet | blocked | parked during systems reset; no public/account work unless Josh reopens Bad Boys | yes |
| BB-23 | Bad Boys/Joycat | 2 | TikTok account creation runbook | blocked | Josh must perform credentials/verification/2FA; Pi browser unavailable | **yes** |
| BB-24 | Bad Boys/Joycat | 2 | Refocus on real assets | blocked | parked while Josh shifts to market activity tracker; reopen only if approved | yes |
| WO-1 | Weather Oracle | 4 | Revenue-option scan before build | todo | identify profitable/grant/leverage angles | no |
| MA-1 | Market Activity | 2 | Personal/open-source market activity tracker | blocked | parked during systems reset; resume after loops/source-of-truth are clean | no |
| OPS-1 | Command Center | 1 | Anti-Slop Systems Reset | doing | clean NOW/TASK_QUEUE/report loops and define one trusted operating loop | no |

## Parking lot rules

- Do not add a new active row unless it has a concrete next action.
- If an idea is interesting but not today's lane, capture it in the relevant project doc or `logs/daily_progress.md`, not as `doing`.
- When a task finishes, move it to `TASK_ARCHIVE.md` during the next hygiene pass.
- If Josh says “keep going” during the Anti-Slop Systems Reset, continue queue/doc/report hygiene before reopening parked projects.
