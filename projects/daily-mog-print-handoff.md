# THE DAILY MOG — print pipeline handoff (2026-07-06)

Context dump for a fresh chat continuing this task. Read this whole file first.

## What this is

A daily one-page print-out — **"THE DAILY MOG"** — auto-generated and printed
each morning on Josh's now-working home printer. Almanac-style: weather,
prices, news, a curated fact, a baby tip, a mascot one-liner, plus a trimmed
business core (Shipped count + the one live Decide). Replaces the old plain
"MORNING_REPORT.md" 5-line dispatch as the *physical* artifact — the phone
dashboard (Gate Deck / Library) stays the *digital* one.

## Standing rule — do not violate this

**Josh must approve a draft before anything gets sent to the physical
printer.** He was burned once by an unreviewed auto-print. This applies until
the format is explicitly locked, and arguably beyond (see memory file below).
Saved to persistent memory at
`~/.claude/projects/-Users-joshstokesberry-MOGDROP/memory/feedback-print-drafts-first.md`
— read it, it'll auto-load in the new chat too since it's in the memory index.

## Printer — already working, do not redo this

- Model: **HP Smart Tank 7602** (reports as "HP Smart Tank 7600 series" over
  mDNS), on home WiFi.
- Found via `avahi-browse -art` on the Pi once the printer was actually awake
  on WiFi — real IP **192.168.1.193**, hostname `HP38CA84F4A579.local`.
- CUPS + avahi-utils + hplip already installed on the Pi (`sudo apt-get
  install -y cups avahi-utils printer-driver-hpcups hplip`), `cups` service
  enabled, Josh added to the `lpadmin` group.
- Queue name: **`HP_SmartTank_7602`**, added as a driverless **IPP Everywhere**
  queue (NOT the HP-specific driver — first attempt used a `dnssd://` URI and
  negotiated as "Local Raw Printer" which printed a BLANK page; fixed by
  deleting and re-adding with a static URI:
  `sudo lpadmin -p HP_SmartTank_7602 -E -v "ipp://192.168.1.193:631/ipp/print" -m everywhere`).
  Confirmed working: `lpstat -p HP_SmartTank_7602 -l` should show real paper
  sizes/duplex/quality options, not "Local Raw Printer" — that string means
  it's broken again.
- Print command: `lp -d HP_SmartTank_7602 -o media=Letter <file>`. Verified
  working with real text and with the mockup PDF.

## Design direction — locked decisions

- **Title: "THE DAILY MOG"** (not "Commander"). Newspaper/almanac framing on
  purpose — the eclectic content (weather + prices + trivia + baby tip) is
  literally farmer's-almanac DNA, modernized.
- Two-column layout, ticker strip for prices, moon phase line, small mascot
  touch. Warm cream paper background (`#FBF6EC`), warm near-black ink
  (`#241F16`), 4 purposeful accent colors only: brand violet `#4B3F8F`
  (masthead/identity only), green `#1B7A4D` (price-up / shipped number), red
  `#A3402F` (price-down only), amber `#B8790A` + `#FBEBD2` bg (Decide box
  only). Color encodes meaning, never decoration — echoes the same restraint
  rule already used in Mission Control's dashboard CSS.
- **Cut the verbose lane-status dump** from the print version entirely — that
  project-management prose is what made v1 feel like a status memo instead of
  something pleasant to read. Phone dashboard already covers that job.
- Kept business core: **Shipped-this-week number** (small, not the hero
  anymore) + **one Decide box** (top pending Gate Deck item, amber accent).
- Sunrise/sunset: kept, liked.
- Mascot one-liner of the day: kept, but **broadened to the whole Bad Boys
  roster** (chef, DJ, cowboy, astronaut, plant sprout, banker, future
  costumes) — NOT banker-only jokes. Same deadpan/artifact-lab voice as
  `projects/badboys-cartoon-lab.md`'s Art Constitution. Should be a small
  curated pre-written bank (real, auditable, rotates) — not freshly
  improvised each morning, same pattern as the fact/baby-tip banks below.
- **Rejected/dropped:** "yesterday's win" callout and a sprint day-counter —
  Josh found both too ops/metric-flavored for a page meant to feel good, not
  track him. Don't resurrect these unless he asks.
- Undecided, Josh's call: "Vol. 1, No. N" issue-number flavor (offered as
  pure aesthetic/newspaper convention, distinct from the rejected day-counter
  — he hasn't ruled on it yet) and a "look up tonight" visible-planet line
  (no keyless source verified yet, unlike everything else below).

## Content lineup + verified data sources (all keyless, no signup)

| Item | Source | Verified live? |
|---|---|---|
| Weather (OKC) + sunrise/sunset | Open-Meteo (open-meteo.com) | Not yet fetched live, just named as the plan — needs a real test call |
| BTC, ETH, LINK, CVX, AERO prices | CoinGecko free API (same as Boring Report already uses) | Same family already proven working all session |
| Silver (XAG), Oil (WTI) prices | Yahoo Finance keyless quote endpoint: `https://query1.finance.yahoo.com/v8/finance/chart/SI=F` and `.../CL=F` | **Confirmed live 2026-07-06** — both returned real JSON market data via curl |
| News — crypto/tech | CoinDesk RSS: `https://www.coindesk.com/arc/outboundfeeds/rss` | **Confirmed HTTP 200** (redirects from the `/rss/` trailing-slash version — use the no-trailing-slash URL directly) |
| News — general tech | TechCrunch RSS: `https://techcrunch.com/feed/` | **Confirmed HTTP 200** |
| News — OKC local | KFOR/News4 Oklahoma RSS: `https://kfor.com/feed/` | **Confirmed HTTP 200** on retry (first hit got a 429 rate-limit, not dead — just be gentle with request rate). KOCO (`https://www.koco.com/feed`, note no trailing slash after redirect) is a solid backup if KFOR ever goes quiet. The Oklahoman's guessed RSS path was a dead end (404) — don't reuse that URL. |
| Curated interesting fact | No API — small hand-written, verified bank (DeFi/oracle/Chainlink + native-plant/OKC trivia), rotates daily. Build once, keep real. |
| Baby tip | No API — small hand-written bank of general/safe newborn-care tips, framed as general info not medical advice. |
| Mascot one-liner | No API — curated bank in the deadpan Bad Boys voice, full costume roster, not banker-exclusive. |
| Calendar | **Explicitly parked** — Josh is setting this up directly in Hermes in parallel, don't touch it or duplicate the effort. |

## Files that exist right now

- `scripts/generate_dispatch.py` — the **v1** generator (old "COMMANDER"
  title, violet/green/amber only, no almanac content yet). Produces both
  `MORNING_REPORT.md` and `MORNING_REPORT.pdf` from one shared data-parse
  (deliberate — never let text/PDF formats diverge again, that's a lesson
  from an earlier tracker/gate desync bug this session). This is the
  previously-approved-so-far baseline, now superseded by the v2 direction —
  expect to replace or heavily rework it, not keep both long-term.
- `scripts/mockup_daily_mog_v2.py` → renders
  `MORNING_REPORT_v2_mockup.pdf` — the **new direction**, sample/placeholder
  data only, no live fetching wired up yet. This is the file mid-iteration
  when the chat ended.

## Exactly where this got interrupted

Just rendered the v2 mockup and did a self-critique before Josh replied.
**Two known bugs to fix first, before anything else:**
1. Ticker strip wraps unevenly — BTC/ETH/Silver/Oil break onto two lines,
   LINK/CVX/AERO don't, because the 7-column table (`colWidths=[0.98*inch]*7`)
   is too narrow for the longer price strings at 9pt Courier. Fix: either
   shrink font, widen the strip, cut it to fewer columns, or restructure so
   every item stacks the same way (symbol atop price+arrow) instead of
   accidentally wrapping only the long ones.
2. The 🌱 emoji in the Primoscapes weather-tie-in line rendered as a broken
   black square — reportlab's default Helvetica can't do emoji glyphs. Fix:
   remove emoji entirely, use a plain-text mark or a small reportlab-drawn
   dot/rule instead, anywhere in this doc.

Also flagged as genuinely good news: the mockup fills only about 60% of the
page — there's real headroom under the one-sheet constraint, not a squeeze.

**Josh's last message was just "What's your read?"-answering silence** — i.e.
the conversation moved to a new chat before he gave his verdict on the v2
mockup. **First thing to do in the new chat: show him the mockup again (or
regenerate it) and get his actual reaction and fixes-approval, then continue
iterating — do NOT skip ahead to wiring live data or automation until the
visual design is locked.**

## Requirements from Josh, not yet built (do these after design lock)

1. **Print automatically on Pi boot** — not a fixed clock time, tied to the
   boot event itself (he powers the Pi off nightly, so "on boot" = whenever
   he turns it on that morning). Likely a systemd oneshot service,
   `After=network-online.target` (needs WiFi for data fetches + the printer),
   triggered at boot. Do NOT wire this until format is locked AND until the
   draft-first rule is satisfied for the final format (get one explicit "yes,
   auto-print this" from Josh first).
2. **Hard one-page cap** — never let this bleed to page 2. Current mockup has
   headroom, but build in a defensive check (e.g., measure content height or
   just keep testing with realistic max-length news headlines/facts) before
   calling it safe.
3. **Freshest possible data** — every generation should hit live sources at
   run time, not cached/stale values. No source, no number — same truth-
   harness spirit as the Boring Report product already has.

## Other things left over from earlier in the session, lower priority

These were queued before the printer/report work took over and never got
finished — worth a mention to Josh but not blocking:
- A measurable numeric "goals ledger" companion to `GOALS.md` (Josh said
  "all" when asked what to build for goals/skills — this was one of three
  things, still outstanding).
- A `commander-primoscapes-ops` skill (mirroring the pattern of
  `commander-critic-passes` / `commander-goals-alignment`, which ARE already
  built and deployed on the Pi — see `configs/skills/` in the repo for both).
- Real efficiency lever already found and not yet acted on: `hermes
  prompt-size` showed tool schemas costing 49.4KB across 32 tools — more than
  2x everything else in the system prompt. Recommended tightening
  `enabled_toolsets` per cron job as the actual lever (not skill-pruning,
  which is already lean).

## Everything not mentioned here is unaffected

Jobs pipeline, Boring Report, Bad Boys cartoon lab (T+2 Episode 1 is fully
rendered but Josh said the cut is **trash, needs real rework** — do not
treat it as gate-ready), Gate Deck, Library — all continue exactly as they
were. This handoff is scoped to the print/dispatch redesign only.
