import fs from 'fs';
import path from 'path';

export const dynamic = 'force-dynamic';

const ROOT = process.cwd();
const MARKET_PATH = path.join(ROOT, 'dashboard', 'market_activity.json');

const fallback = {
  generated_at: new Date().toISOString(),
  disclaimer: 'Personal research dashboard only. Not financial advice.',
  sources: [],
  watchlist: { assets: [], defi_protocols: [], github_repos: [], trending: [] },
  signals: ['Run: npm run market:state'],
  warnings: ['No market snapshot found yet.'],
  next_build_step: 'Run the fetcher and refresh.',
};

function readJson(filePath, defaultValue) {
  try { return JSON.parse(fs.readFileSync(filePath, 'utf8')); } catch { return defaultValue; }
}

function money(value, digits = 2) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return '—';
  const n = Number(value);
  if (Math.abs(n) >= 1_000_000_000) return `$${(n / 1_000_000_000).toFixed(1)}B`;
  if (Math.abs(n) >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (Math.abs(n) >= 1_000) return `$${(n / 1_000).toFixed(1)}K`;
  return `$${n.toLocaleString(undefined, { maximumFractionDigits: digits })}`;
}

function pct(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return '—';
  const n = Number(value);
  return `${n >= 0 ? '+' : ''}${n.toFixed(2)}%`;
}

function tone(value) {
  const n = Number(value);
  if (Number.isNaN(n)) return 'neutral';
  if (n > 0) return 'good';
  if (n < 0) return 'bad';
  return 'neutral';
}

function Stat({ label, value, sub, toneName = 'neutral' }) {
  return (
    <div className={`market-stat ${toneName}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      {sub ? <small>{sub}</small> : null}
    </div>
  );
}

export default function MarketActivity() {
  const state = readJson(MARKET_PATH, fallback);
  const assets = state.watchlist?.assets || [];
  const protocols = state.watchlist?.defi_protocols || [];
  const repos = state.watchlist?.github_repos || [];
  const trending = state.watchlist?.trending || [];
  const link = assets.find((a) => a.symbol === 'LINK');
  const eth = assets.find((a) => a.symbol === 'ETH');
  const btc = assets.find((a) => a.symbol === 'BTC');

  return (
    <main className="shell market-shell">
      <section className="hero glass market-hero">
        <div className="brand-block">
          <div className="mark">M</div>
          <div>
            <div className="eyebrow">Market Activity / Personal Research</div>
            <h1>Watch the tape without becoming the trade.</h1>
            <p className="hero-copy">Open-source-friendly tracker for prices, DeFi TVL, GitHub activity, and narrative heat. Built for Josh’s personal market awareness — not recommendations.</p>
          </div>
        </div>
        <div className="status-grid">
          <Stat label="LINK" value={money(link?.price_usd)} sub={pct(link?.change_24h_pct)} toneName={tone(link?.change_24h_pct)} />
          <Stat label="ETH" value={money(eth?.price_usd)} sub={pct(eth?.change_24h_pct)} toneName={tone(eth?.change_24h_pct)} />
          <Stat label="BTC" value={money(btc?.price_usd)} sub={pct(btc?.change_24h_pct)} toneName={tone(btc?.change_24h_pct)} />
          <Stat label="Updated" value={String(state.generated_at || '').slice(0, 16).replace('T', ' ')} sub="UTC" toneName="neutral" />
        </div>
      </section>

      <section className="command-grid">
        <div className="panel market-panel">
          <div className="panel-label green">Signals, not advice</div>
          <div className="signal-stack">
            {(state.signals || []).map((signal) => <div className="signal-row" key={signal}>{signal}</div>)}
          </div>
          <p className="decision-note">{state.disclaimer}</p>
        </div>
        <div className="panel">
          <div className="panel-label">Next build step</div>
          <h2>{state.next_build_step}</h2>
          <p>Useful direction: configurable watchlists, daily snapshots, changelog alerts, RSS/governance tracking, and an open-source README so other crypto researchers can run it locally.</p>
        </div>
      </section>

      <section className="triple-grid">
        <div className="panel">
          <div className="panel-label">Asset watchlist</div>
          <div className="market-table">
            {assets.map((asset) => (
              <div className="market-row" key={asset.symbol}>
                <b>{asset.symbol}</b>
                <span>{money(asset.price_usd)}</span>
                <em className={tone(asset.change_24h_pct)}>{pct(asset.change_24h_pct)}</em>
              </div>
            ))}
          </div>
        </div>
        <div className="panel">
          <div className="panel-label">DeFi protocols</div>
          <div className="market-table">
            {protocols.map((proto) => (
              <a className="market-row link-row" href={proto.url} target="_blank" rel="noreferrer" key={proto.name}>
                <b>{proto.name}</b>
                <span>{money(proto.tvl_usd, 0)}</span>
                <em className={tone(proto.change_7d_pct)}>{pct(proto.change_7d_pct)} 7d</em>
              </a>
            ))}
          </div>
        </div>
        <div className="panel">
          <div className="panel-label">GitHub pulse</div>
          <div className="market-table">
            {repos.map((repo) => (
              <a className="repo-card" href={repo.url} target="_blank" rel="noreferrer" key={repo.repo}>
                <b>{repo.repo}</b>
                <span>{repo.stars?.toLocaleString?.() || repo.stars} stars · {repo.open_issues} issues</span>
                <small>pushed {repo.pushed_at}</small>
              </a>
            ))}
          </div>
        </div>
      </section>

      <section className="command-grid lower">
        <div className="panel">
          <div className="panel-label">Narrative heat</div>
          <div className="chip-grid">
            {trending.map((coin) => <div className="chip" key={`${coin.name}-${coin.score}`}>{coin.name} <small>{coin.symbol}</small></div>)}
          </div>
        </div>
        <div className="panel terminal-panel">
          <div className="panel-label">Sources / run command</div>
          <pre>{`sources: ${(state.sources || []).join(', ')}\nrefresh: npm run market:state\nfile: dashboard/market_activity.json\nwarnings: ${(state.warnings || []).length ? state.warnings.join(' | ') : 'none'}`}</pre>
        </div>
      </section>
    </main>
  );
}
