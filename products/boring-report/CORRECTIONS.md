# Corrections & Review Ledger — the flawless-streak counter

Public phase requires 2 consecutive weeks with ZERO entries from Josh.
Claude critic findings (pre-Josh) don't break the streak — they exist so Josh never has to make them.

## 2026-W28 (v0) — Claude critic review, pre-Josh-gate

1. **METHODOLOGY (must fix): USYC misclassified.** Yield-bearing / NAV-accruing
   tokens (USYC, arguably BUIDL) are not $1-peg stablecoins — price >$1 is by
   design, not deviation. Fix: asset-class filter — exclude NAV-accruing tokens
   from the peg table (or give them their own "tokenized cash-equivalents" tier
   scored on NAV tracking, not $1 deviation). A ratings brand calling NAV accrual
   a depeg is a credibility wound.
2. **Methodology drift (fix or document):** `supply_stability_score` is computed
   and embedded but absent from PRD §5 and the visible table. Either add it to
   the methodology doc with weights, or remove it. No undocumented scoring.
3. **Hygiene:** snapshot paths in the embedded data block are absolute Pi paths
   (`/home/josh/...`) — use repo-relative paths for portability.

Verdict: v0 accepted as pipeline proof (truth harness independently verified on
a second machine). Issue itself: HOLD from Josh gate until fix 1 lands as W28-r2.
