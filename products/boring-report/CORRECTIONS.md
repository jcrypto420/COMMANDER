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

## 2026-07-06 — fixes applied (Claude, pre-Josh-gate)

1. **USYC/BUIDL fix: DONE.** Added `NAV_ACCRUING_GECKO_IDS` classification in
   `generate_weekly.py` — tokenized cash-equivalent funds excluded from the
   peg-scored table, rendered in their own "not ranked" table instead.
   **Bonus catch during the fix:** USDY (Ondo US Dollar Yield) is the same
   asset class and was silently about to enter the rankings once it cracked
   top-10 supply — added proactively, not just the two originally flagged.
2. **`supply_stability_score`: REMOVED.** It was never in the documented
   methodology or the visible table — dropped from the generator entirely
   rather than retroactively justified. Methodology stays exactly §5.
3. **Repo-relative snapshot paths: DONE.** Embedded data block and source
   list now read `products/boring-report/snapshots/...`, no absolute paths.
4. **Structural fix beyond the three asks:** `generate_weekly.py` was
   discovered to only ever have CHECKED the report, never actually written
   it — the original W28.md was produced by some uncommitted process.
   Rewrote it to be the single authoritative generator; `verify.py` now
   imports its scoring logic directly instead of a separate copy, so the
   two can never silently diverge again.

Regenerated `weekly/2026-W28.md` in place. `verify.py` passes independently.
Ready for Josh's Gate Deck read.

## 2026-W28 (v1) — Josh Gate 1 verdict, 2026-07-08

**Verdict: CORRECTION — methodology revision ordered. Streak not started.**

1. **Coverage wrong-shaped:** top-10-by-supply alone hides the mechanically
   interesting set — "how is crvUSD or fxUSD not on that list?" Fix: add a
   curated mechanism-watch table below the top-10.
2. **Mechanism labels too crude:** DefiLlama's binary fiat-/crypto-backed
   tag scores a delta-neutral synthetic (USDe), a soft-liquidation CDP
   (crvUSD), and a leveraged-split design (fxUSD) identically. Fix:
   per-asset mechanism taxonomy with plain-language notes.
3. **Full-file transparency:** component scores lived only in the hidden
   data block; the rendered report must show the full breakdown.
4. **Scoring not trusted:** the fiat>crypto blanket in reserve/redemption
   is not a defensible methodology. Fix: published per-class score matrix
   (methodology v1.1), Josh gates the revision.

## 2026-07-08 — v1.1 fixes applied (Claude, back to Josh gate)

1. **Mechanism watch table added:** crvUSD, fxUSD, GHO, BOLD — curated
   criterion documented (structurally distinct solvency design, ≥$25M).
2. **Mechanism taxonomy:** 8 classes with plain-language explanations.
   Reclassifications with score impact: USDe → delta-neutral synthetic
   (79→73), USDD → issuer-managed crypto (77→64), DAI/USDS → hybrid
   CDP+RWA. crvUSD soft-liquidation vs GHO hard-liquidation distinguished.
3. **Full-file transparency:** component breakdown + both price sources now
   rendered in the report; per-asset "what would make this less boring"
   lines added (a PRD §5 requirement v0 had silently skipped).
4. **Published score matrix** per class replaces the fiat>crypto blanket;
   matrix changes now explicitly gated.
5. **Pipeline fixes found during the work:** new `snapshot_sources.py`
   (stdlib-only, Pi-ready — the 07-05 snapshots came from an uncommitted
   process); expanded CoinGecko id list so RLUSD/USDD/USDY no longer
   silently fall back to the DefiLlama price; BOLD's null DefiLlama price
   handled by an explicit never-silent n/a rule.
6. **verify.py upgraded to a total check:** rebuilds the entire report from
   the committed snapshots and diffs line-by-line (only the generated_at
   timestamp is exempt) instead of spot-checking numbers.

Regenerated `weekly/2026-W28.md` on fresh 2026-07-08 snapshots; verify
passes. Awaiting Josh's Gate 1 re-read of the v1.1 issue.
