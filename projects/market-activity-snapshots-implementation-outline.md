# Market Activity daily snapshots — implementation outline

**Status:** Draft-only support artifact for `MA-1`. Prepared 2026-09-27. Lane stays `todo` and parked behind the CI-1 week-smooth reopen condition. This outline converts the approved design note (`projects/market-activity-snapshots-draft.md`) into exact, build-ready code changes so the lane is implementation-ready when the reopen condition clears. **No code is changed in this pass.**

**Prerequisite for this outline to be actionable:** the CI-1 lane must run smoothly for a week (the parked lane's reopen condition). Until then, this file is reference material only.

---

## What "done" looks like for this lane

- A fresh fetcher run writes both `dashboard/market_activity.json` (latest) and `dashboard/market_activity_history.json` (latest + capped `snapshots[]` array).
- `market_activity_history.json` contains `latest` matching the current snapshot and a `snapshots` array with at least one dated entry.
- Same-day reruns replace the existing entry for that date rather than duplicating it.
- The 30-day cap is enforced: after 31 distinct dates, the array holds exactly 30 entries and the oldest is dropped.
- The `/market` route shows a small "change vs yesterday" panel when yesterday's snapshot exists; it is silent when it does not.
- No API keys, accounts, paid endpoints, wallet code, or trading behavior are introduced.

---

## File map (all paths relative to `/home/josh/COMMANDER`)

| Role | Path | Current state |
|------|------|---------------|
| Fetcher | `scripts/fetch_market_activity.py` | Implemented + smoke-tested; writes `dashboard/market_activity.json` only |
| Config | `configs/market_watchlist.json` | Implemented; repo-stored watchlist source |
| Latest output | `dashboard/market_activity.json` | Written per run by the fetcher |
| History output (new) | `dashboard/market_activity_history.json` | Does not exist yet |
| Dashboard route | `app/market/page.jsx` | Reads `dashboard/market_activity.json`; shows latest state only |
| Design note | `projects/market-activity-snapshots-draft.md` | Complete; this outline is the companion build spec |
| Project status | `projects/market-activity-tracker.md` | Parked; `Status: PARKED` |

---

## Change 1 — Fetcher history-write step

**File:** `scripts/fetch_market_activity.py`  
**Where:** at the end of `main()`, after the existing `OUT.write_text(...)` line (line ~369), before the final `print(...)` line.  
**New constant (top of file, alongside `OUT` and `CONFIG`):**

```python
HISTORY = ROOT / "dashboard" / "market_activity_history.json"
HISTORY_CAP = 30
```

**New helper (add near the other helpers, before `main()`):**

```python
def update_history(latest_snapshot: dict, history_path: Path, cap: int) -> None:
    """Append or replace a dated snapshot in the history file; cap at `cap` entries.

    Same-calendar-day reruns replace the existing entry for that date (same-day
    refresh, not duplicate rows). When the cap is exceeded, the oldest distinct
    date is dropped.
    """
    generated_at = latest_snapshot.get("generated_at") or datetime.now(timezone.utc).isoformat()
    date_key = datetime.fromisoformat(generated_at).date().isoformat()

    if history_path.exists():
        try:
            payload = json.loads(history_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            payload = {}
    else:
        payload = {}

    if not isinstance(payload, dict):
        payload = {}

    snapshots = payload.get("snapshots")
    if not isinstance(snapshots, list):
        snapshots = []

    # Replace same-date entry if present, else append.
    replaced = False
    for i, entry in enumerate(snapshots):
        if isinstance(entry, dict) and entry.get("date") == date_key:
            snapshots[i] = {
                "date": date_key,
                "generated_at": generated_at,
                "asset_count": len(latest_snapshot.get("watchlist", {}).get("assets", [])),
                "protocol_count": len(latest_snapshot.get("watchlist", {}).get("defi_protocols", [])),
                "repo_count": len(latest_snapshot.get("watchlist", {}).get("github_repos", [])),
                "snapshot": latest_snapshot,
            }
            replaced = True
            break
    if not replaced:
        snapshots.append({
            "date": date_key,
            "generated_at": generated_at,
            "asset_count": len(latest_snapshot.get("watchlist", {}).get("assets", [])),
            "protocol_count": len(latest_snapshot.get("watchlist", {}).get("defi_protocols", [])),
            "repo_count": len(latest_snapshot.get("watchlist", {}).get("github_repos", [])),
            "snapshot": latest_snapshot,
        })

    # Stable sort by date descending, then trim to cap.
    snapshots.sort(key=lambda e: e.get("date", ""), reverse=True)
    if len(snapshots) > cap:
        snapshots = snapshots[:cap]

    payload = {
        "version": 1,
        "generated_at": generated_at,
        "latest": latest_snapshot,
        "snapshots": snapshots,
    }

    tmp = history_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    tmp.replace(history_path)
```

**Call (in `main()`, right after the existing `OUT.write_text(...)` line):**

```python
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, warnings={len(warnings)})")

    # --- NEW: daily snapshot history (MA-1 reopen) ---
    update_history(state, HISTORY, HISTORY_CAP)
    print(f"wrote {HISTORY} ({HISTORY.stat().st_size} bytes)")
```

**Guardrails preserved:** no new imports beyond `datetime` (already imported); no network calls; no keys/secrets/accounts; same atomic write-to-tmp-then-replace pattern as the existing output.

---

## Change 2 — `/market` "change vs yesterday" panel

**File:** `app/market/page.jsx`  
**Where:** add a new panel inside the existing `command-grid lower` section (after the "Sources / run command" panel, before the closing `</section>` at line ~150), or in a new `<section>` of its own. The least invasive insertion point is a new panel in the `command-grid lower` section.

**New helper functions (add near the existing `money`/`pct`/`tone` helpers):**

```jsx
function readHistory() {
  try {
    const raw = fs.readFileSync(path.join(ROOT, 'dashboard', 'market_activity_history.json'), 'utf8');
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function snapshotForDate(history, targetDate) {
  if (!history || !Array.isArray(history.snapshots)) return null;
  return history.snapshots.find(e => e.date === targetDate)?.snapshot || null;
}

function changeRow(label, today, yesterday) {
  if (today === undefined || today === null || yesterday === undefined || yesterday === null) {
    return null;
  }
  const diff = today - yesterday;
  const cls = diff === 0 ? 'neutral' : diff > 0 ? 'good' : 'bad';
  const sign = diff >= 0 ? '+' : '';
  return { label, value: `${sign}${diff.toFixed(2)}%`, sub: `vs ${yesterday.toFixed(2)}%`, toneName: cls };
}
```

**Date helpers (use UTC so the panel is deterministic regardless of server timezone):**

```jsx
const today iso = (() => {
  const g = state.generated_at ? new Date(state.generated_at) : new Date();
  return g.toISOString().slice(0, 10);
})();
const yesterday_iso = (() => {
  const d = new Date();
  d.setUTCDate(d.getUTCDate() - 1);
  return d.toISOString().slice(0, 10);
})();
```

**New panel JSX (insert in the `command-grid lower` section):**

```jsx
<div className="panel">
  <div className="panel-label">Change vs yesterday</div>
  {history && yesterdaySnapshot ? (
    <div className="market-table">
      {assets.map(a => {
        const todayP = a.change_24h_pct;            // today's 24h change from live snapshot
        const yRow = yesterdaySnapshot.watchlist?.assets?.find(y => y.symbol === a.symbol);
        const yP = yRow?.change_24h_pct;
        const row = changeRow(a.symbol, todayP, yP);
        return row ? <div className="market-row" key={a.symbol}><b>{row.label}</b><span>{row.value}</span><em className={row.toneName}>{row.sub}</em></div> : null;
      })}
      {protocols.map(p => {
        const yRow = yesterdaySnapshot?.watchlist?.defi_protocols?.find(y => y.name === p.name);
        const row = changeRow(p.name, p.change_7d_pct, yRow?.change_7d_pct);
        return row ? <a className="market-row link-row" href={p.url} target="_blank" rel="noreferrer" key={p.name}><b>{row.label}</b><span>{row.value}</span><em className={row.toneName}>{row.sub}</em></a> : null;
      })}
    </div>
  ) : (
    <div className="muted">No yesterday snapshot yet — history panel appears after the first daily-snapshot run.</div>
  )}
</div>
```

**Wire the new panel's data at the top of `MarketActivity()`:**

```jsx
export default function MarketActivity() {
  const state = readJson(MARKET_PATH, fallback);
  const history = readHistory();
  const yesterdaySnapshot = history ? snapshotForDate(history, yesterday_iso) : null;
  // ... existing body ...
}
```

**Panel placement note:** keep the existing hero stat row (LINK / ETH / BTC / Updated) untouched; the change-vs-yesterday panel is additive and appears only when `history` and `yesterdaySnapshot` are both present. When they are absent (first run, or history file missing), the panel shows the muted placeholder text above.

---

## Acceptance checks (run when lane reopens)

1. Run `python3 scripts/fetch_market_activity.py` from repo root. Confirm:
   - `dashboard/market_activity.json` is written (as before).
   - `dashboard/market_activity_history.json` is written with `version: 1`, a `latest` object matching the current snapshot, and a `snapshots` array with at least one entry whose `date` matches today's date.
2. Run the fetcher a second time on the same day. Confirm:
   - `market_activity_history.json` still has exactly one entry for today's date (same-day overwrite, no duplicate).
   - The `snapshots` array length did not grow.
3. Simulate a multi-day history: seed `market_activity_history.json` with 31 distinct date entries, then run the fetcher. Confirm:
   - The file holds exactly 30 snapshot entries after the run.
   - The oldest date is dropped; today's entry is present.
4. Run `npm run build` then serve the `/market` route. Confirm:
   - The page renders the latest snapshot as before (LINK / ETH / BTC / assets / protocols / repos / trending all present).
   - When `market_activity_history.json` has a yesterday entry, a "change vs yesterday" panel appears.
   - When `market_activity_history.json` is absent or has no yesterday entry, the panel shows the muted placeholder and the rest of the page is unaffected.
5. Secret scan: confirm no `.env`, API keys, tokens, seeds, or wallet material is introduced in the two changed files. Confirm `dashboard/market_activity_history.json` contains no secrets (it is derived purely from public API responses).

---

## Explicit non-goals for this pass (carried from the design note)

- No public exposure of the history file; stays local/LAN until Josh approves.
- No aggregation beyond per-asset and per-protocol comparison.
- No alerts, notifications, or Telegram delivery from the history feature.
- No RSS feed wiring (still deferred).
- No new thresholds beyond what `configs/market_watchlist.json` already carries.
- No wallet code, signing, trading, or advice.

---

## Reopen condition

Stay parked until the CI-1 lane runs smoothly for a week. When reopened, implement Change 1 (fetcher history-write step) first as the smallest safe slice, verify with a live run using the acceptance checks above, then implement Change 2 (the `/market` change-vs-yesterday panel) and verify with `npm run build`.

---

## Source alignment

- Design authority: `projects/market-activity-snapshots-draft.md`
- Project status: `projects/market-activity-tracker.md` (Status: PARKED)
- Config source of truth: `configs/market_watchlist.json`
- Fetcher: `scripts/fetch_market_activity.py`
- Dashboard route: `app/market/page.jsx`
- Queue row: `TASK_QUEUE.md` row `MA-1`
