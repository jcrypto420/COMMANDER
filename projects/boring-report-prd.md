# PRD — "THE BORING REPORT" (working title, Josh names it at Gate N1)
## Institutional-deadpan risk ratings for onchain finance · v1.0 · 2026-07-05

## Status — 2026-07-07
- **State:** P0 + P1 SHIPPED (2026-07-05; W28 v0 generated, critic-fixed, verified — see `products/boring-report/`). P0.1 re-probe (2026-07-07, Mac) solved the one P0 blocker: Chainlink feed/PoR inventory is machine-readable via `reference-data-directory.vercel.app` JSON (315 mainnet feeds, 25 PoR) — see `products/boring-report/SOURCES.md`
- **Portfolio reset 2026-07-25:** The Boring Report is now the flagship compounding data/product build (see `projects/portfolio-reset-2026-07-25.md`). **P2 Oracle Scorecard v0 evidence baseline built 2026-07-27 and internally reviewed 2026-07-30:** two protocol fact files, three SHA-256-verified source snapshots, deterministic scoring, rendered Markdown/JSON/HTML, and a fail-closed verifier live under `products/boring-report/scorecard/`. The acceptance note is `products/boring-report/scorecard/internal-review-2026-07-30.md`. It is deliberately architecture-evidence-only; the next increment is one traceable Aave V3 deployment feed map, followed by heartbeat observations and a sourced incident ledger before broader score claims. W28 remains a useful internal reference, but no longer blocks the build behind repeated Gate Deck nagging.
- **Waiting on:** Josh's Gate 1 verdict; Josh's name verdict at Gate N1

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
- **Asset-class filter (added after W28 v0 critic review):** tokenized
  cash-equivalent / NAV-accruing funds (BUIDL, USYC, USDY — classified by
  known fund identity, not a price threshold, since accrual mechanics vary)
  are NOT scored on peg deviation. They render in a separate table with their
  own price only, pending a NAV-tracking benchmark.
- **v1.1 revision (2026-07-08, Josh Gate 1 correction):** solvency (25) and
  redemption (15) points come from a published per-mechanism-class matrix —
  fiat custodial 23/13 · hybrid CDP+RWA 20/12 · CDP immutable 20/12 ·
  CDP hard/soft liquidation 19/12 · delta-neutral synthetic 14/10 ·
  leveraged split 14/10 · issuer-managed crypto 10/8 · unclassified floor
  12/8 — never from DefiLlama's binary fiat/crypto tag. Coverage = top-10 by
  supply PLUS a curated mechanism-watch table (structurally distinct designs,
  ≥$25M circulating: crvUSD, fxUSD, GHO, BOLD). The rendered report must show
  the full component breakdown, both price sources (fallback never silent),
  and a per-asset "what would make this less boring" line. Matrix or class
  changes are methodology changes and require a Josh gate.
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

## 9. CRE onchain surface — "Boring Score feed" (Josh-directed, 2026-07-08)

**Product:** the v1.1 scoring pipeline re-implemented as a Chainlink CRE
workflow (TypeScript SDK, cron trigger): consensus-aggregated HTTP fetches of
the same $0 sources → deterministic v1.1 scoring → scores written onchain /
served per-request. The report becomes the free top-of-funnel; the feed is
the paid product. Revenue rails: **x402 pay-per-call** (apps/agents pay to
query scores via HTTP-triggered workflow) and **DataLink** (institutional
feed licensing across 40+ chains) — both live Chainlink offerings as of
2025-11 CRE GA. Buyers: protocol risk teams, DAO treasuries, structured
products, agent stacks needing a stablecoin/oracle-risk signal.

**Why us:** same unfair advantage as §1 (S&P oracle-risk methodology),
plus the truth harness — a ratings feed whose every number is reproducible
from committed snapshots is the institutional pitch.

**Milestones (each gated like §6):**
- **C0** — local proof, $0: port scoring to a CRE workflow, run in the free
  local simulator against live sources; simulator output committed as
  evidence. Needs Josh approval for: `cre` CLI + SDK install.
- **C1** — testnet: request CRE Early Access (Josh account gate), deploy,
  write weekly scores to a testnet contract.
- **C2** — demand check before any spend: 3–5 design-partner conversations
  + Chainlink grant/BUILD application (public-good angle). No mainnet
  until someone credible says they'd consume it.
- **C3** — mainnet + monetization (x402 first, DataLink conversation
  second). LINK/gas/credit spend = explicit Josh approval per SECURITY.md.

**Flags:** (a) known competitors in onchain risk signals: Chaos Labs risk
oracles, Credora/RedStone ratings, Bluechip, S&P's own stablecoin
assessments — differentiation is reproducibility + published methodology;
(b) a programmatically-consumed ratings feed raises the liability bar vs a
newsletter — legal framing is a Josh business-judgment item before C3;
(c) sequencing: methodology v1.1 needs Josh's Gate 1 blessing before it
ships onchain.
