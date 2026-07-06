# PRD — "THE BORING REPORT" (working title, Josh names it at Gate N1)
## Institutional-deadpan risk ratings for onchain finance · v1.0 · 2026-07-05

## Status — 2026-07-05
- **State:** APPROVED for internal build (Josh, DeFi product lab session) — merges DF-1 concepts #1 Oracle Risk Scorecard + #3 Boring Report + #6 PoR Watch into one brand
- **Next action:** Hermes executes Milestone P0 (data-source probe + methodology skeleton)
- **Waiting on:** nothing for P0; Josh's name verdict at Gate N1

## 1. Product

A pseudonymous research product that rates the boringness of onchain financial
infrastructure — because in financial plumbing, boring = good. Three surfaces,
one methodology, one voice (institutional deadpan; "outlook: stable"):

1. **The Weekly** — one page, every week: stablecoin boring-scores, depeg watch,
   attestation gaps, one "least boring event of the week."
2. **The Scorecard** — living table rating oracle dependencies of top DeFi
   protocols: feed concentration, deviation history, fallback design, update
   liveness.
3. **PoR / Attestation Watch** — coverage table: which tokenized assets,
   stablecoins, and bridges have real proof-of-reserve or attestations, and
   which run on vibes.

**Why us (unfair advantage):** Josh co-authored S&P Global's published research
on blockchain oracle risk and interoperability/tokenization — this product is
that exact methodology, applied continuously, with an AI production line behind
it. Career flywheel: every issue is proof-of-work for the job lane.

**Explicitly NOT:** financial advice, token picks, price predictions, custody,
paid research services (killed 2026-07-02), or anything requiring API spend.

## 2. Users & revenue path

- **Phase A (internal):** Josh — quality gate + first reader.
- **Phase B (public, gated):** DeFi risk-curious users, protocol teams,
  crypto-native newsletters. Free.
- **Phase C (signal-gated):** paid tier / sponsorship / API only after
  free-tier traction (≥500 subs or clear pull). No monetization build before.

## 3. Constraints (hard)

- **$0 data budget.** Keyless public sources only (below). No new subscriptions.
- **Numbers are NEVER model-generated.** Every figure traces to a fetched
  source snapshot stored in the repo. A number without a source file = P0 bug.
- **Cheap models only** (gpt-5.4-mini pinned) for drafting; MoA critic pass for
  voice/claims before any Josh gate.
- **Runs on existing rails:** Pi crons + repo + Library/dashboard rendering.
  No new services until Phase B (which needs Josh's explicit approval —
  public exposure per SECURITY.md).
- **Voice constitution:** deadpan institutional, dry, zero hype, zero "🚀",
  ratings-agency cadence. Reuses the artifact-lab cold register. Never mean to
  individuals; institutions and mechanisms only (edge law applies here too).

## 4. Data sources (P0 must verify each is fetchable FROM THE PI)

| Source | Use | Access |
|---|---|---|
| DefiLlama API (llama.fi) | stablecoin supplies/prices, protocol TVL | public, keyless |
| CoinGecko free API | price/peg cross-check | public, rate-limited — cache aggressively |
| Chainlink docs feed pages + PoR feed list | oracle feed inventory, PoR coverage | public pages |
| Protocol docs/governance (per-protocol) | oracle configuration facts | public, manual-assisted |
| Attestation pages (issuer sites) | reserve attestation dates/auditors | public pages |

P0 records per source: reachable-from-Pi? rate limits? snapshot format.
(Lesson learned: the Pi got 403/999-blocked by S&P and LinkedIn before —
verify BEFORE building. Fallback: Claude/Mac fetches, commits snapshots.)

## 5. Methodology v1 (the IP — Josh + Claude own this file's soul)

**Boring Score, 0–100 (higher = more boring = better).** Draft rubric:
- **Stablecoins:** peg deviation (30d max + frequency) 30pts · reserve
  attestation recency/quality 25pts · redemption mechanics clarity 15pts ·
  concentration/custody structure 15pts · incident history 15pts.
- **Oracle dependencies (per protocol):** feed redundancy/fallback 30pts ·
  update liveness vs market moves 25pts · concentration (single-oracle risk)
  25pts · deviation incident history 20pts.
- **PoR/attestation coverage:** binary tiers — Live PoR feed / third-party
  attestation / self-reported / none ("vibes").
- Every score ships with a one-line "what would make this less boring" —
  the falsifiable statement that keeps us honest.
- Methodology page is public from day one (ratings credibility 101).

## 6. Milestones (Hermes-executable; ARTIFACT RULE applies to each)

| # | Deliverable | Acceptance (Claude critic-checks, Josh gates) |
|---|---|---|
| **P0** | `products/boring-report/SOURCES.md` — probe results for every source + snapshot samples committed | every source marked reachable/blocked with evidence; zero code yet |
| **P1** | Weekly generator v0: script pulls top-10 stablecoins → `products/boring-report/weekly/YYYY-WW.md` with scores + source snapshots | numbers match snapshots 100%; report renders in Library; voice passes MoA critic; **Josh internal read** |
| **P2** | Oracle Scorecard v0: structured `scorecard.json` + rendered table for top 10 protocols (research-assisted, fact-file per protocol) | every cell traceable to a fact file; on-methodology; **Josh gate** |
| **P3** | PoR/Attestation Watch v0 table, merged into weekly | coverage tiers evidenced; **Josh gate** |
| **P4** | Cron: weekly build Sunday 17:00 → MoA critic → Josh gate card on Gate Deck → archive | two consecutive FLAWLESS internal weeks (zero factual corrections from Josh) |
| **N1** | Naming/brand gate: Josh picks name + pseudonymous byline | name locked; simple wordmark (monoline, obviously) |
| **P5** | **PUBLIC LAUNCH GATE** — surface decision (Substack/Ghost/static) + first public issue | requires: P4 flawless streak + Josh explicit public-exposure approval per SECURITY.md |

Sequencing: P0 → P1 → (P2 ∥ P3) → P4 → N1 → P5. One milestone per draft-lane
pass; no milestone starts before the previous one's acceptance is logged.

## 7. QA + "flawless" monitoring (the part Josh asked for)

- **Truth harness:** every published number carries a source-snapshot path;
  `verify.py` re-checks report numbers against snapshots at build time —
  mismatch fails the build. Model-invented numbers are structurally impossible
  to ship.
- **Freshness guard:** any source snapshot >8 days old at build time → report
  marked STALE and blocked from the gate.
- **MoA critic pass** on every issue: voice (deadpan, no hype), claims
  (evidence-linked), edge law compliance.
- **Josh gate on every issue** during internal phase (Gate Deck card:
  ship/kill/one-liner). His factual corrections are logged in
  `products/boring-report/CORRECTIONS.md` — the flawless streak counter.
- **Failure alerts** ride the morning dispatch (source blocked, build failed,
  stale data) — never silent degradation.
- **Public phase adds:** corrections policy printed in every issue (ratings
  credibility = owning errors loudly).

## 8. Explicit non-goals v1

Token gating, tips/payments, custom domain, social automation, paid data,
historical backfills beyond 30d, covering >10 assets/protocols per surface.
Scope creep dies here. Expansion only on Phase C signal.
