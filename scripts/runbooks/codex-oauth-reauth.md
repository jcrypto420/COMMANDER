# Runbook: Codex OAuth token wiped after subscription cancel/renew

**Status:** partially documented — exact commands NOT yet captured. Whoever handles
the next occurrence MUST record the exact steps here (that's the point of this file).

## Symptom

Codex (Hermes provider on the Pi: "OpenAI Codex via ChatGPT OAuth", profile
`commander`, see NOW.md) stops authenticating after Josh cancels/renews his
ChatGPT subscription. The stored OAuth token is invalidated/wiped.

## History

- Occurrence 1: date unknown (referenced as prior art in occurrence 2's commit).
- Occurrence 2: 2026-07-06. Josh asked the identical question 3× across two
  sessions (01:41Z, 12:02Z, 12:05Z). Commit b2f9e4a claimed "now documented"
  but contained only Blender assets — the fix was never written down.

## What is known to work (verify, don't assume)

1. The fix is a re-authentication of the Codex provider for the Hermes
   `commander` profile — a fresh ChatGPT OAuth login flow, not an API key.
2. After re-auth, verify with a first safe read-only task (the NOW.md standard)
   before trusting the provider in loops.
3. Cost note: this provider is subscription-auth (no per-token cost) — do not
   "fix" it by swapping to a per-token key without Josh's explicit OK
   (CLAUDE.md: ask before spending).

## On next occurrence — capture these

- [ ] Exact command(s) run on the Pi, verbatim
- [ ] Where the token lives on disk (path), so wipes are diagnosable in seconds
- [ ] Time-to-fix, so the morning packet can say "known issue, 5 min"

## Prevention idea (queued, not built — leverage rules apply)

A daily loop pre-check: if provider auth fails, the morning packet says
"Codex token wiped again — run this runbook" instead of failing silently.
Build it only by replacing an existing check, not adding a new system.
