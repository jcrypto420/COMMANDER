# Market Activity daily snapshots — draft design

## Status
Draft-only support artifact for `MA-1`. Prepared 2026-09-26. Lane stays `todo` and parked behind the CI-1 week-smooth reopen condition. This note turns the vague "add daily snapshots" next action into a concrete, reviewable design so the lane is build-ready when reopened.

## Motivation
The current `dashboard/market_activity.json` is a single latest snapshot per run. It answers "what is the state right now?" but not "what changed since yesterday / this week?" Adding dated snapshots gives the dashboard a change-over-time dimension without adding keys, accounts, paid APIs, or trading behavior.

## What "daily snapshots" means concretely
- Each successful fetcher run appends a dated snapshot record to a history store.
- The dashboard can surface:
  - Today's snapshot (already available as `market_activity.json`).
  - Yesterday's snapshot for direct today-vs-yesterday comparison.
  - A 7-day window for trend context on prices, TVL, and repo activity.
- The feature is read-only, local, and derived from existing public sources only.

## Design options considered

### Option A — One growing JSON file with a `snapshots` array
A single file `dashboard/market_activity_history.json` holds:
```json
{
  "latest": { ... full current snapshot ... },
  "snapshots": [
    { "date": "2026-09-25", "snapshot": { ... } },
    { "date": "2026-09-24", "snapshot": { ... } }
  ]
}
```
- **Pros:** Single file, easy to back up, easy for the dashboard to read, atomic writes via write-to-temp-then-rename.
- **Cons:** File grows without bound unless capped; cap logic is required.

### Option B — One file per day in `dashboard/snapshots/`
Each run writes `dashboard/snapshots/2026-09-26.json`. The dashboard reads the directory listing.
- **Pros:** Naturally bounded (delete old files); each snapshot is independently addressable.
- **Cons:** Directory listing + mtime sorting adds a small runtime step; more files to manage.

### Recommendation: Option A with a 30-day cap
Option A is simpler for the dashboard and keeps the history in one atomic file. Cap the array at 30 snapshots; when the cap is reached, drop the oldest. The cap is generous enough for a week-smooth trend view and short enough that the file stays small and fast to read.

## Recommended schema

### History file: `dashboard/market_activity_history.json`
```json
{
  "version": 1,
  "generated_at": "2026-09-26T12:00:00.000000+00:00",
  "latest": {
    "generated_at": "2026-09-26T12:00:00.000000+00:00",
    "assets": [ ... ],
    "defi_protocols": [ ... ],
    "github_repos": [ ... ],
    "trending": [ ... ]
  },
  "snapshots": [
    {
      "date": "2026-09-25",
      "generated_at": "2026-09-25T23:02:52.432642+00:00",
      "asset_count": 7,
      "protocol_count": 8,
      "repo_count": 5,
      "snapshot": { ... full snapshot ... }
    }
  ]
}
```
- `date` is a `YYYY-MM-DD` string derived from `generated_at`, used as the stable day key.
- If two runs land on the same calendar day, the later run overwrites that day's entry (same-day refresh, not duplicate rows).
- The `snapshot` sub-object is the full current snapshot shape, so the dashboard can render historical entries identically to the latest.

## Fetcher changes (when lane reopens)

1. After writing `dashboard/market_activity.json` (the latest snapshot), load `dashboard/market_activity_history.json` if it exists.
2. Build the new entry: `date = generated_at.date().isoformat()`, `snapshot = full snapshot dict`.
3. If an entry for `date` already exists in `snapshots`, replace it; otherwise append.
4. Trim `snapshots` to the 30 most recent distinct dates (by `date` key).
5. Write `dashboard/market_activity_history.json` with the updated structure.
6. Keep both files in sync: `market_activity.json` is always the latest; `market_activity_history.json` always has `latest` matching `market_activity.json`.
7. Preserve all existing guardrails: no keys, no accounts, no trading, no advice, local-only.

## Dashboard changes (when lane reopens)

The `/market` route should add a small "change vs yesterday" panel when yesterday's snapshot exists:
- Asset price change vs yesterday's price for each watched asset (only when both snapshots exist).
- Protocol TVL change vs yesterday for each watched protocol.
- A 7-day trend note: which assets/protocols moved the most over the available window.
- Keep the existing latest-state panel intact; the history view is additive.

## Draft acceptance checks (rewrite when reopened)

- A fresh fetcher run writes both `dashboard/market_activity.json` and `dashboard/market_activity_history.json`.
- `market_activity_history.json` contains `latest` matching the current snapshot and a `snapshots` array with at least one dated entry.
- Same-day reruns replace the existing entry for that date rather than duplicating it.
- The 30-day cap is enforced: after 31 distinct dates, the array holds exactly 30 entries and the oldest is dropped.
- The `/market` route still renders without secrets and still shows the latest snapshot.
- A "change vs yesterday" panel appears when yesterday's snapshot exists; it is silent (no panel) when it does not.
- No API keys, accounts, paid endpoints, wallet code, or trading behavior are introduced.

## Explicit non-goals for this pass

- No public exposure of the history file; stays local/LAN until Josh approves.
- No aggregation across assets beyond per-asset and per-protocol comparison.
- No alerts, notifications, or Telegram delivery from the history feature.
- No RSS feed wiring (still deferred from the config-wiring pass).
- No new thresholds beyond what the config file already carries.

## Reopen condition
Stay parked until the CI-1 lane runs smoothly for a week. When reopened, implement the fetcher history-write step first (smallest safe slice), verify with a live run, then add the dashboard change-panel.

## Source alignment
- Config source of truth: `configs/market_watchlist.json`
- Fetcher: `scripts/fetch_market_activity.py`
- Current output: `dashboard/market_activity.json` (5,257 bytes, 2026-09-25 run)
- Project doc: `projects/market-activity-tracker.md`
- Config-wiring draft: `projects/market-activity-config-wiring-draft.md`
