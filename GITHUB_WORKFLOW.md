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

## Never push secrets

- `.env`, keys, tokens, seeds, passwords, personal docs are git-ignored.
- Before any push: `git status` and confirm no secret/ignored file slipped in.

## Current remote

- `origin` → `https://github.com/jcrypto420/COMMANDER.git`
- This repo doubles as the `command-center`.
