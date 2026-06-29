import fs from 'fs';
import path from 'path';

const ROOT = process.cwd();
const STATE_PATH = path.join(ROOT, 'dashboard', 'state.json');
const WEEKLY_PATH = path.join(ROOT, 'WEEKLY_MONEY_REVIEW.md');
const MORNING_PATH = path.join(ROOT, 'MORNING_REPORT.md');

const fallback = {
  generated_at: new Date().toISOString(),
  host: { name: 'commandcenter', lan_ip: 'unknown', cwd: ROOT },
  goals: { sprint_target: '$6.9K in 69 days', passive_income_target: '$6.9K/month' },
  focus: {
    active: 'Command Center reliability + 69-day revenue sprint discovery',
    money_move: 'Build the mission-control dashboard into a decision system, not decoration.',
    review: ['Open: WEEKLY_MONEY_REVIEW.md', 'Decide: APPROVE REAL ASSET ACCOUNT PREP or RUN IN-1 LEAD VERIFY']
  },
  tasks: { doing: [], blocked: [], todo: [], approval: [], counts: { doing: 0, blocked: 0, todo: 0, done: 0 } },
  hermes: { provider: 'unknown', model: 'unknown', telegram: 'unknown', gateway: 'unknown' },
  cron: { daily_loop_active: false, next_run: 'unknown', deliver: 'unknown', last_run: 'unknown' },
  git: { branch: 'unknown', head: 'unknown', dirty_count: 0, changes: [] },
  sovereignty: { services: [], docker: { available: false, containers: [] } },
  learning: { today: 'Dashboards are decision systems.', qol: 'One screen, one move.', system_rule: 'Private/Tailscale first.' },
  safety: ['no public ports', 'no secrets displayed', 'approval-gated actions']
};

function readJson(filePath, defaultValue) {
  try { return JSON.parse(fs.readFileSync(filePath, 'utf8')); } catch { return defaultValue; }
}

function readText(filePath, limit = 1800) {
  try { return fs.readFileSync(filePath, 'utf8').slice(0, limit); } catch { return ''; }
}

function stripMd(text) {
  return text.replace(/^#+\s*/gm, '').replace(/\*\*/g, '').replace(/`/g, '').trim();
}

function statusClass(value) {
  const v = String(value || '').toLowerCase();
  if (v.includes('running') || v.includes('configured') || v.includes('active') || v === 'done') return 'good';
  if (v.includes('blocked') || v.includes('failed')) return 'bad';
  return 'warn';
}

function TaskCard({ task }) {
  return (
    <div className="task-card">
      <div className="task-id">{task.id}</div>
      <div className="task-main">
        <div className="task-title">{task.task}</div>
        <div className="task-sub">{task.project} · {task.next_action}</div>
      </div>
      <div className={`badge ${task.status}`}>{task.status}</div>
    </div>
  );
}

function MiniPanel({ label, value, tone = 'neutral' }) {
  return (
    <div className={`mini-panel ${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function BriefLine({ icon, title, children }) {
  return (
    <div className="brief-line">
      <div className="brief-icon">{icon}</div>
      <div>
        <b>{title}</b>
        <p>{children}</p>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const state = readJson(STATE_PATH, fallback);
  const weekly = stripMd(readText(WEEKLY_PATH));
  const morning = stripMd(readText(MORNING_PATH));
  const doing = state.tasks?.doing || [];
  const blocked = state.tasks?.blocked || [];
  const todos = state.tasks?.todo || [];
  const approvals = state.tasks?.approval || [];
  const primaryTasks = [...doing, ...blocked, ...todos].slice(0, 8);
  const services = state.sovereignty?.services || [];
  const containers = state.sovereignty?.docker?.containers || [];
  const review = state.focus?.review?.length ? state.focus.review : ['Open: WEEKLY_MONEY_REVIEW.md', 'Decide: choose one signal path'];
  const approvalPhrase = approvals[0]?.next_action || 'APPROVE REAL ASSET ACCOUNT PREP or RUN IN-1 LEAD VERIFY';

  return (
    <main className="shell">
      <section className="hero glass">
        <div className="brand-block">
          <div className="mark">C</div>
          <div>
            <div className="eyebrow">Commander / Mission Control</div>
            <h1>Daily tasks. Money moves. Infra health. One cockpit.</h1>
            <p className="hero-copy">Private, read-only-first dashboard for Josh’s 69-day revenue sprint and sovereignty stack. Buttons draft commands; risky actions stay approval-gated.</p>
          </div>
        </div>
        <div className="status-grid">
          <MiniPanel label="Telegram" value={state.hermes?.telegram || 'unknown'} tone={statusClass(state.hermes?.telegram)} />
          <MiniPanel label="Gateway" value={state.hermes?.gateway || 'unknown'} tone={statusClass(state.hermes?.gateway)} />
          <MiniPanel label="Cron" value={state.cron?.daily_loop_active ? '7am live' : 'check'} tone={state.cron?.daily_loop_active ? 'good' : 'warn'} />
          <MiniPanel label="LAN" value={state.host?.lan_ip || 'unknown'} tone="warn" />
        </div>
      </section>

      <section className="command-grid">
        <div className="panel money-panel">
          <div className="panel-label green">Today’s one move</div>
          <h2>{state.focus?.money_move}</h2>
          <p>{state.focus?.active}</p>
          <div className="metrics-row">
            <MiniPanel label="Sprint" value={state.goals?.sprint_target || '$6.9K'} tone="good" />
            <MiniPanel label="Passive target" value={state.goals?.passive_income_target || '$6.9K/mo'} />
            <MiniPanel label="Git changes" value={state.git?.dirty_count ?? 0} tone={(state.git?.dirty_count ?? 0) > 0 ? 'warn' : 'good'} />
          </div>
        </div>

        <div className="panel decision-panel">
          <div className="panel-label">60-second review</div>
          {review.slice(0, 4).map((item, index) => (
            <BriefLine key={item} icon={['🌅', '🎯', '🧠', '🛡️'][index] || '•'} title={index === 0 ? 'Open' : index === 1 ? 'Decide' : 'Context'}>{item}</BriefLine>
          ))}
          <div className="copy-card">
            <span>Next approval phrase</span>
            <code>{approvalPhrase}</code>
          </div>
        </div>
      </section>

      <section className="triple-grid">
        <div className="panel">
          <div className="panel-label">Task queue</div>
          <div className="task-stack">
            {primaryTasks.length ? primaryTasks.map((task) => <TaskCard key={task.id} task={task} />) : <p className="muted">No active tasks parsed.</p>}
          </div>
        </div>

        <div className="panel terminal-panel">
          <div className="panel-label">Commander runtime</div>
          <pre>{`provider: ${state.hermes?.provider}\nmodel: ${state.hermes?.model}\ngateway: ${state.hermes?.gateway}\ntelegram: ${state.hermes?.telegram}\ndelivery: ${state.cron?.deliver}\nnext cron: ${state.cron?.next_run}\nlast cron: ${state.cron?.last_run}\ngit: ${state.git?.branch} @ ${state.git?.head}\nhost: ${state.host?.name} / ${state.host?.lan_ip}`}</pre>
        </div>

        <div className="panel">
          <div className="panel-label">Sovereignty stack</div>
          <div className="service-grid">
            {services.slice(0, 8).map((service) => (
              <div className="service" key={service.name}>
                <span className={service.present ? 'service-dot on' : 'service-dot'} />
                <b>{service.name}</b>
                <small>{service.status}</small>
              </div>
            ))}
          </div>
          <div className="container-note">Docker containers detected: {containers.length}</div>
        </div>
      </section>

      <section className="command-grid lower">
        <div className="panel">
          <div className="panel-label">Interact with Commander</div>
          <div className="action-grid">
            <div className="action-card"><b>Telegram steering</b><p>Use Telegram for quick replies, approvals, and mid-day idea dumps.</p><code>gm / approve phrase / new idea</code></div>
            <div className="action-card"><b>Daily task mode</b><p>Open the dashboard, pick the one move, then use the optional 15/30/60-minute extensions.</p><code>read → decide → execute</code></div>
            <div className="action-card"><b>Future action layer</b><p>Buttons will generate approval packets first. No direct posting, spending, trading, or service changes.</p><code>approval-gated</code></div>
          </div>
        </div>

        <div className="panel report-panel">
          <div className="panel-label">Research / reports</div>
          <div className="report-columns">
            <div><h3>Weekly money review</h3><p>{weekly || 'WEEKLY_MONEY_REVIEW.md not found yet.'}</p></div>
            <div><h3>Morning brief</h3><p>{morning || 'MORNING_REPORT.md not found yet.'}</p></div>
          </div>
        </div>
      </section>

      <section className="panel footer-panel">
        <div>
          <div className="panel-label">Safety rail</div>
          <p>{(state.safety || []).join(' · ')}</p>
        </div>
        <div className="footer-meta">Generated {state.generated_at} · {state.host?.cwd}</div>
      </section>
    </main>
  );
}
