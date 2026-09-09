# The Boring Report — Oracle Scorecard v0
## Outlook: evidence-limited

- **Version:** v0.1-evidence-baseline
- **Scope:** architecture evidence only. This is not historical incident telemetry, live deployment configuration, financial advice, or a protocol safety guarantee.
- **Rule:** an unknown control receives zero credit; zero incident-evidence points do **not** claim an incident occurred.
- **Truth harness:** `verify_scorecard.py` validates every quoted claim against a committed source snapshot and rebuilds this artifact exactly.

## Architecture-evidence scores

| Protocol | Fallback /30 | Liveness /25 | Concentration /25 | Incidents /20 | Total /100 |
|---|---:|---:|---:|---:|---:|
| Aave V3 | 30 | 0 | 10 | 0 | **40** |
| Morpho Blue | 0 | 0 | 0 | 0 | **0** |

## Reading this correctly

A higher number means more documented architecture controls in this deliberately narrow evidence pack—not a conclusion about security, solvency, historical performance, or current deployed configuration. The next increment must add deployment-specific feed maps, heartbeat/round observations, and a sourced incident ledger before any broader claims are made.

## Aave V3

**Boundary:** Oracle adapter architecture in aave-v3-core AaveOracle.sol; not deployment-specific feed configuration or historical telemetry.

### Fallback / redundancy — 30/30

The adapter names Chainlink Aggregators as its first source and forwards to a fallback oracle if the primary answer is non-positive or no asset source is configured.

**Evidence**
- `products/boring-report/scorecard/snapshots/2026-07-27/aave-oracle.sol` — “Use of Chainlink Aggregators as first source of price”
- `products/boring-report/scorecard/snapshots/2026-07-27/aave-oracle.sol` — “If the returned price by a Chainlink aggregator is <= 0, the call is forwarded to a fallback oracle”

### Liveness controls — 0/25

This adapter source uses latestAnswer but does not itself demonstrate a heartbeat, timestamp, or staleness check. No credit is inferred from missing evidence.

**Evidence**
- `products/boring-report/scorecard/snapshots/2026-07-27/aave-oracle.sol` — “int256 price = source.latestAnswer();”

### Source concentration — 10/25

The primary source family is explicit (Chainlink); a configurable fallback exists, but its live source diversity is not established by this architecture file. Partial credit only.

**Evidence**
- `products/boring-report/scorecard/snapshots/2026-07-27/aave-oracle.sol` — “Map of asset price sources (asset => priceSource)”
- `products/boring-report/scorecard/snapshots/2026-07-27/aave-oracle.sol` — “function setFallbackOracle(”

### Incident evidence — 0/20

No sourced incident ledger is in v0. Zero is an evidence-state score, not a claim that incidents occurred.

**Evidence**
- `products/boring-report/scorecard/snapshots/2026-07-27/aave-oracle.sol` — “contract AaveOracle is IAaveOracle”

## Morpho Blue

**Boundary:** Oracle interface architecture in morpho-blue IOracle.sol; not a rating of any individual Morpho market or its selected oracle.

### Fallback / redundancy — 0/30

The interface exposes one price() method and does not establish a fallback mechanism. No redundancy is inferred.

**Evidence**
- `products/boring-report/scorecard/snapshots/2026-07-27/morpho-i-oracle.sol` — “function price() external view returns (uint256);”

### Liveness controls — 0/25

The interface specifies price output but no freshness or heartbeat control. No credit is inferred from missing evidence.

**Evidence**
- `products/boring-report/scorecard/snapshots/2026-07-27/morpho-i-oracle.sol` — “Returns the price of 1 asset of collateral token”

### Source concentration — 0/25

Morpho explicitly places safe-oracle selection with the user; this generic interface does not establish protocol-wide source diversity.

**Evidence**
- `products/boring-report/scorecard/snapshots/2026-07-27/morpho-i-oracle.sol` — “It is the user's responsibility to select markets with safe oracles.”

### Incident evidence — 0/20

No sourced incident ledger is in v0. Zero is an evidence-state score, not a claim that incidents occurred.

**Evidence**
- `products/boring-report/scorecard/snapshots/2026-07-27/morpho-i-oracle.sol` — “interface IOracle”

## Source snapshots

- `products/boring-report/scorecard/snapshots/2026-07-27/manifest.json`
- `products/boring-report/scorecard/snapshots/2026-07-27/chainlink-feeds-mainnet.json` (inventory foundation for the next deployment-specific pass)
- `products/boring-report/scorecard/snapshots/2026-07-27/aave-oracle.sol`
- `products/boring-report/scorecard/snapshots/2026-07-27/morpho-i-oracle.sol`
