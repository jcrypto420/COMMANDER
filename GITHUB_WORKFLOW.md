# GITHUB_WORKFLOW.md

GitHub is the source of truth and task history. Keep it clean and safe.

## Branch / commit / PR

- Work on a branch, not `main`, for anything non-trivial.
- Small, focused commits with clear messages.
- Open a PR for review (Codex/Claude can review). Merge after it looks good.
- **Pushing requires Josh's approval** (see `SECURITY.md`).

## Commit message style

```text
<area>: <what changed and why>

e.g.  scaffolding: add command-center truth files + scripts
      hermes: add verified install command to HERMES_SETUP.md
```

## Tasks ↔ GitHub

- `TASK_QUEUE.md` is the lightweight board; mirror big items as GitHub issues.
- Reference task IDs (e.g. `CC-3`) in commits and issues.

## Repo hygiene / anti-clutter rules

GitHub should stay a clean operating manual, not a junk drawer.

- Top-level files are only stable command-center artifacts: current reports, source-of-truth docs, and key plans.
- `projects/` should contain durable project briefs, approval packets, and reusable operating docs — not every scratch draft forever.
- `logs/daily_progress.md` is the timeline; do not create a new progress file for every small action.
- Generated/runtime files such as `dashboard/state.json` should stay local and out of GitHub history.
- Generated creative output should only be committed after curation. Keep scratch output ignored or archived.
- When a project lane gets noisy, consolidate older packets into one `archive/` or one summary doc, then update `NOW.md` / `TASK_QUEUE.md` to point only at the current next action.

Default commit rule: fewer, curated commits beat dumping everything. Commit what helps future Josh/Commander decide faster; leave local caches, scratch files, and secret helpers out.

## Never push secrets

- `.env`, keys, tokens, seeds, passwords, personal docs are git-ignored.
- Before any push: `git status` and confirm no secret/ignored file slipped in.

## Current remote

- `origin` → `https://github.com/jcrypto420/COMMANDER.git`
- This repo doubles as the `command-center`.
