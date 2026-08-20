# Job Application Tracker — SINGLE SOURCE OF TRUTH

**Rule for ALL agents (Claude, Hermes, ChatGPT via Josh):** check this table BEFORE
drafting, searching, or applying. Every application, draft, and verdict lands here
same-day. Duplicate work on an already-applied role = failed run.
Official-link column: always a full https:// markdown link — it renders tappable in the Library.

LIFECYCLE (Josh rule 2026-07-05): every application lives in its own folder under
`jobs/packets/active/<company-role>/`. **BOTH tables must be updated together on
apply/kill — Applications row removed, Archive row added, same commit. A stale
Applications row caused a wasted duplicate-draft cycle on 2026-07-06.** (packet.md + resume.docx + cover-letter.md).
The moment a role is APPLIED or KILLED, the folder moves to `jobs/packets/archive/`
and its row moves to the Archive table below — active views stay clean.
Josh checks this ONE file (or the dashboard Files tab → jobs/) for all job updates.

## Applications

| Date | Company | Role | Score | Status | Owner | Materials | Official link |
|---|---|---|---|---|---|---|---|
| — | Chainlink Labs | Sr. Solutions Engineer, Banking & Capital Markets (NY) | — | **CLOSED** — posting no longer live, verified 2026-07-06 (Ashby GraphQL returns null; not on the current board). Checked the apparent successor "Senior Solutions Architect, Banking and Capital Markets" — **REJECTED, poor fit**: role is hands-on pre-sales (PoC delivery, RFP/RFI/DDQ response, "evangelise with Sales and Marketing"), requires production coding (Solidity/Go/Rust/etc.) Josh doesn't have. Directly contradicts Josh's own taste profile ("why heavy-sales is a no-go" — career-income.md §7). Not applying. | — | [posting checked](https://jobs.ashbyhq.com/chainlink-labs/53348577-027a-4bad-bedd-2fb72d30a2d6) — verdict: skip |
| 2026-08-20 | Ripple | Treasury Manager, Global Treasury Ops (NY) | 8 | **DRAFTED — decision surface ready**; morning-sync refreshed 2026-08-20; New York posting verified 2026-08-14 and fresh 2026-08-20 18:01Z no-login recheck confirmed the page still live; NY annual base salary range $144K–$180K; packet/brief/form-prep note plus `source-recheck-note.md` and `next-scan-note.md` now ready for Josh’s hold/tweak/kill verdict | Josh | `jobs/packets/active/ripple-treasury-manager-global-treasury-ops/packet.md` + `decision-brief.md` + `form-prep-note.md` + `source-recheck-note.md` + `next-scan-note.md` | [Ripple careers](https://ripple.com/careers/all-jobs/job/7767531?gh_jid=7767531) |
|| — | BitGo | Financial Operations Manager (Palo Alto) | 4 | skip — location; keyword source only | — | — | [Greenhouse posting](https://job-boards.greenhouse.io/bitgo/jobs/8436572002) |
|| 2026-08-11 | Coinbase | Business Operations Senior Associate, Institutional | 8 | **PARKED — below current floor**; official Greenhouse feed confirms Remote — USA, job `7980600`, but disclosed base begins at $148,835 and misses Josh's $150K minimum | Josh | `jobs/packets/active/coinbase-institutional-business-ops/packet.md` + `decision-brief.md` | [official ATS](https://www.coinbase.com/careers/positions/7980600?gh_jid=7980600) |
| 2026-08-11 | Coinbase | Senior Manager, Product Operations, FCM Ops | 7 | **KILLED — Josh taste call:** no Coinbase Ops. Remote — USA; official feed disclosed $201,365–$236,900 base, but compensation does not override the role-fit verdict. | Josh | historical: `jobs/packets/active/coinbase-senior-manager-product-ops-fcm/decision-brief.md` | [official ATS](https://www.coinbase.com/careers/positions/8110496?gh_jid=8110496) |

## Archive (applied or killed — out of the active system)

| Date | Company | Role | Outcome | Materials |
|---|---|---|---|---|
| 2026-07-05 | Coinbase | Assoc. Manager, Billing Operations & Strategy | APPLIED ✅ — first full-pipeline case: gate verdict → resume+letter built → submitted same day | `jobs/packets/archive/coinbase-billing-ops/` (packet, Coinbase-OPs.pdf, docx, cover letter) |
| ~2026-07 | Chainlink Labs | Data Risk Operations Analyst | APPLIED ✅ (ChatGPT lane) — interview prep in archive folder | `jobs/packets/archive/chainlink-data-risk-ops/packet.md` |
| ~2026-07 | Kalshi | Finance Operations | APPLIED ✅ (ChatGPT lane, confirmed by Josh 2026-07-05) | resume: Josh's Desktop `kalshi.pdf` |
| ~2026-07 | Centrifuge | RWA/Investment Operations (role: Josh to confirm exact title) | APPLIED ✅ (ChatGPT lane, confirmed 2026-07-05) | resume: Josh's Desktop `Centrifuge.pdf` |
| ~2026-07 | Chainlink Labs | Strategy/Solutions (general — role: Josh to confirm) | APPLIED ✅ (ChatGPT lane, confirmed 2026-07-05) | resume: Josh's Desktop `CLL.pdf` |

## Daily quick-scan boards (Tier 1 — see SEARCH_PLAYBOOK.md)

Chainlink · Anchorage Digital · Kalshi · Crypto.com · Circle · Centrifuge · Paxos ·
Securitize · Ondo · Fireblocks · BitGo · Coinbase · Kraken · Alpaca

## Interview pipeline

| Company | Stage | Next step | Prep material |
|---|---|---|---|
| Chainlink Labs | applied, awaiting response (~2 wks post-close per posting) | if contacted: review packet fit case + talking points | `jobs/packets/chainlink-data-risk-ops.md` |

## Open items

- [x] Report 3 ruling: Josh CONFIRMED contribution (2026-07-03) — all three S&P reports usable with "contributor" phrasing everywhere.
- [x] Chainlink application date: not tracked (Josh: "move on") — row stands as applied, date unknown.
