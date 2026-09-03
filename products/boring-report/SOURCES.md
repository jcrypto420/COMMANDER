# The Boring Report — P0 Source Probe

**Date:** 2026-07-05T19:30:43-05:00
**Host:** Pi (`/home/josh/COMMANDER`)
**Method:** raw HTTP fetches from the Pi only; no API keys, no login, no code generation, no JS automation.

## P0 verdict

| Source category | Probed URL(s) | Reachable from Pi? | Rate limit / block? | Snapshot format | Evidence |
|---|---|---:|---|---|---|
| DefiLlama API | `https://api.llama.fi/protocols` ; `https://stablecoins.llama.fi/stablecoins?includePrices=true` | Yes | No block hit | JSON | `200 OK`; body starts with `[{"id":"2269","name":"Binance CEX"...` and `{"peggedAssets":[{"id":"1","name":"Tether"...` |
| CoinGecko free API | `https://api.coingecko.com/api/v3/ping` ; `https://api.coingecko.com/api/v3/simple/price?ids=usd-coin,tether,ethereum,bitcoin&vs_currencies=usd` | Yes | No block hit on small sample | JSON | `200 OK`; ping returned `{"gecko_says":"(V3) To the Moon!"}`; price call returned BTC/ETH/USDT/USDC USD values |
| Chainlink docs feed pages + PoR feed list | `https://docs.chain.link/data-feeds` ; `https://data.chain.link/` | Mixed | Docs reachable; PoR/feed-list blocked with 429 | HTML | Docs page `200 OK` with title `Chainlink Data Feeds | Chainlink Documentation`; `data.chain.link` returned `429 Too Many Requests` / Vercel security checkpoint |
| Protocol docs / governance (per-protocol) | `https://aave.com/docs` ; `https://governance.aave.com/` | Yes | No block hit | HTML | `200 OK`; titles `Aave Protocol Overview` and `Aave - Governance Forum` |
| Attestation pages (issuer sites) | `https://www.circle.com/transparency` | Yes | No block hit | HTML | `200 OK`; title `Transparency & Stability | Circle` |

## Snapshot samples

### 1) DefiLlama API — protocol TVL

**Probe:** `https://api.llama.fi/protocols`

**Result:** `200 OK`, `application/json`

**Sample:**
```json
[{"id":"2269","name":"Binance CEX","address":null,"symbol":"BNB","url":"https://www.binance.com","description":"Binance is a cryptocurrency exchange which is the largest exchange in the world in terms of daily trading volume of cryptocurrencies",...
```

### 2) DefiLlama stablecoins — supply + prices

**Probe:** `https://stablecoins.llama.fi/stablecoins?includePrices=true`

**Result:** `200 OK`, `application/json`

**Sample:**
```json
{"peggedAssets":[{"id":"1","name":"Tether","symbol":"USDT","gecko_id":"tether","pegType":"peggedUSD","priceSource":"defillama","pegMechanism":"fiat-backed","circulating":{"peggedUSD":184187935618.49506},...
```

### 3) CoinGecko free API — ping + peg cross-check

**Probes:**
- `https://api.coingecko.com/api/v3/ping`
- `https://api.coingecko.com/api/v3/simple/price?ids=usd-coin,tether,ethereum,bitcoin&vs_currencies=usd`

**Result:** both `200 OK`, JSON

**Samples:**
```json
{"gecko_says":"(V3) To the Moon!"}
```

```json
{"bitcoin":{"usd":63421},"ethereum":{"usd":1779.39},"tether":{"usd":0.999113},"usd-coin":{"usd":0.999815}}
```

### 4) Chainlink docs feed pages

**Probe:** `https://docs.chain.link/data-feeds`

**Result:** `200 OK`, `text/html`

**Sample:**
```html
<title>Chainlink Data Feeds | Chainlink Documentation</title>
```

### 5) Chainlink PoR / feed list

**Probe:** `https://data.chain.link/`

**Result:** `429 Too Many Requests` from a Vercel security checkpoint

**Sample:**
```html
<title>Vercel Security Checkpoint</title>
```

### 6) Protocol docs / governance

**Probes:**
- `https://aave.com/docs`
- `https://governance.aave.com/`

**Result:** both `200 OK`, HTML

**Samples:**
```html
<title>Aave Protocol Overview</title>
```

```html
<title>Aave - Governance Forum</title>
```

### 7) Issuer attestation page

**Probe:** `https://www.circle.com/transparency`

**Result:** `200 OK`, HTML

**Sample:**
```html
<title>Transparency &amp; Stability | Circle</title>
```

## Notes

- The Pi can fetch the key public sources needed for P1/P2 work.
- The only blocked category in this P0 pass was the Chainlink PoR/feed-list portal at `data.chain.link`.
- All numbers and snippets above are direct fetch outputs from the Pi; nothing here is model-generated.
- Next step is still zero-code methodology work: keep source snapshots in-repo and use them as the only basis for future Boring Report numbers.

---

# P0.1 re-probe — 2026-07-07 (Mac)

**Date:** 2026-07-07 ~15:00-05:00
**Host:** Mac (`/Users/joshstokesberry/COMMANDER`) — Claude Code session. **Pi reachability of the new endpoints below is NOT yet verified**; per the P0 lesson, Hermes must re-run these two fetches from the Pi before any cron depends on them.
**Evidence:** headers + trimmed body samples in `snapshots/probe-2026-07-07/`.

## What changed since 2026-07-05

| Finding | Detail | Evidence |
|---|---|---|
| **PoR feed-list block is SOLVED** | The docs addresses pages serve their feed tables from a public static JSON directory: `https://reference-data-directory.vercel.app/feeds-mainnet.json` → `200 OK`, `application/json`, ~418 KB. **315 Ethereum-mainnet feeds, 25 flagged Proof of Reserve** (`docs.productType == "Proof of Reserve"`). Each feed carries `proxyAddress`, `heartbeat`, `threshold` (deviation %), `feedCategory`, `feedType` — the exact fields the P2 Scorecard rubric (update liveness, deviation config) and P3 PoR Watch need. No more scraping `data.chain.link`. | `chainlink_rdd_mainnet.headers`, `chainlink_rdd_mainnet.sample.json` |
| Per-network directory enumerated | 63 distinct `reference-data-directory.vercel.app/*.json` files (Arbitrum, Base, Avalanche, BSC, etc.) extracted from the docs page — multichain coverage is one URL swap away. | `chainlink_rdd_urls.txt` |
| PoR docs page moved | `docs.chain.link/data-feeds/proof-of-reserve/addresses` is now a meta-refresh redirect to `/data-feeds/smartdata/addresses` (PoR folded into "SmartData"). Both return `200`; pages are ~16.8 MB JS-heavy HTML — use the RDD JSON instead. | `chainlink_por_page.html` (91-byte redirect stub), `chainlink_smartdata_page.headers` |
| DefiLlama still clean | `stablecoins.llama.fi/stablecoins?includePrices=true` → `200`, 511 KB JSON. `api.llama.fi/tvl/aave` → `200`, bare number (`13216560270.05` = Aave TVL USD). No rate-limit headers exposed. | `defillama_stablecoins.*`, `defillama_protocol_aave.*` |
| CoinGecko still clean | `simple/price` for 5 stablecoins → `200`, JSON with `last_updated_at`; response cached 30–60 s (`cache-control: max-age=30, s-maxage=60`). Keep the aggressive-cache rule. | `coingecko_simple_price.*` |
| Issuer pages: Circle OK, Tether JS-rendered | Circle transparency HTML contains attestation content in the raw fetch (20 keyword hits). **Tether's page is a JS shell** (1 hit) — reserve figures load client-side, so P3 needs either Tether's published attestation PDFs or a browser-assisted fetch. Aave governance forum still `200`. | `circle_transparency.sample.html`, `tether_transparency.sample.html`, `aave_governance.*` |

## P2/P3 implications

- **P2 (Oracle Scorecard) is unblocked:** feed inventory, heartbeats, and deviation thresholds are machine-readable via RDD JSON. Remaining P2 research (fallback design, incident history) stays manual-assisted per the PRD.
- **P3 (PoR Watch) has its coverage list:** the 25 mainnet PoR feeds enumerate "who has a live PoR feed" directly; attestation-tier evidence still comes from issuer pages, with the Tether caveat above.
- **Action before P2 cron work:** verify `reference-data-directory.vercel.app` is fetchable from the Pi (it is a Vercel host, and `data.chain.link`'s block was a Vercel checkpoint — do not assume).
