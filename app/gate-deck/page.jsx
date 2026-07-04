import fs from 'fs';
import path from 'path';
import GateDeckClient from './GateDeckClient';

export const dynamic = 'force-dynamic';

const ROOT = process.cwd();
const TASKS_PATH = path.join(ROOT, 'TASK_QUEUE.md');

function parseTasks(md) {
  const rows = [];
  for (const line of String(md || '').split('\n')) {
    if (!line.startsWith('|') || line.includes('|----') || line.includes('| ID ') || line.includes('|----')) continue;
    const cells = line.trim().slice(1, -1).split('|').map((cell) => cell.trim().replace(/`/g, ''));
    if (cells.length < 7) continue;
    const [id, project, pri, task, status, next_action, approval] = cells;
    if (!/^[A-Z]+-\d+/.test(id)) continue;
    if (!String(approval).toLowerCase().includes('yes') || status === 'done') continue;
    rows.push({ id, project, pri, task, status, next_action, approval });
  }
  return rows;
}

export default function GateDeckPage() {
  let tasks = [];
  try {
    tasks = parseTasks(fs.readFileSync(TASKS_PATH, 'utf8'));
  } catch {
    tasks = [];
  }

  return (
    <main className="shell gate-shell">
      <section className="hero glass">
        <div className="brand-block">
          <div className="mark">G</div>
          <div>
            <div className="eyebrow">Gate Deck / capture only</div>
            <h1>Tap a verdict card, save it to the inbox, and let the next loop read it.</h1>
            <p className="hero-copy">This page does not execute actions. It only posts verdicts into the existing Commander inbox API so the next safe run can pick them up.</p>
          </div>
        </div>
      </section>

      <section className="panel" style={{ marginTop: 14 }}>
        <div className="panel-label green">Pending decisions from TASK_QUEUE.md</div>
        <GateDeckClient cards={tasks} />
      </section>

      <section className="panel" style={{ marginTop: 14, display: 'flex', justifyContent: 'space-between', gap: 12, alignItems: 'center' }}>
        <div>
          <div className="panel-label">Capture-only rule</div>
          <p className="decision-note">No shell execution, no sending, no spending, no service changes. Verdicts land in <code>COMMANDER_INBOX.md</code> and get read on the next Commander run.</p>
        </div>
        <a className="open-button" href="/">Back to Mission Control</a>
      </section>
    </main>
  );
}
