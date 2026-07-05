import path from 'path';

const ROOT = process.cwd();

export const LIBRARY = [
  { slug: 'jobs-tracker', file: 'jobs/TRACKER.md', title: 'Job tracker', blurb: 'Every application, status, and link. The single source of truth.', group: 'Jobs' },
  { slug: 'jobs-playbook', file: 'jobs/SEARCH_PLAYBOOK.md', title: 'Search playbook', blurb: 'How roles get found, verified, scored, and tailored.', group: 'Jobs' },
  { slug: 'packet-chainlink', file: 'jobs/packets/chainlink-data-risk-ops.md', title: 'Chainlink packet', blurb: 'Applied — now interview prep.', group: 'Jobs' },
  { slug: 'packet-coinbase', file: 'jobs/packets/coinbase-billing-ops.md', title: 'Coinbase packet', blurb: 'Send-ready. Verdict pending on the Gate Deck.', group: 'Jobs' },
  { slug: 'cartoon-lab', file: 'projects/badboys-cartoon-lab.md', title: 'Cartoon lab', blurb: 'Pipeline, art constitution, pilot scripts, production status.', group: 'Bad Boys' },
  { slug: 'storyboard-t2', file: 'assets/badboys/cartoon-lab/t2-ep1/STORYBOARD.md', title: 'T+2 storyboard', blurb: 'Episode one, panel by panel.', group: 'Bad Boys' },
  { slug: 'now', file: 'NOW.md', title: 'NOW', blurb: 'Active focus, next tasks, blockers.', group: 'Command center' },
  { slug: 'task-queue', file: 'TASK_QUEUE.md', title: 'Task queue', blurb: 'The live board across every lane.', group: 'Command center' },
  { slug: 'morning-report', file: 'MORNING_REPORT.md', title: 'Morning report', blurb: 'Latest daily dispatch from the 07:30 loop.', group: 'Command center' },
  { slug: 'weekly-review', file: 'WEEKLY_MONEY_REVIEW.md', title: 'Weekly money review', blurb: 'Monday scoreboard — leads with the shipped count.', group: 'Command center' },
];

export function resolveDoc(slug) {
  const doc = LIBRARY.find((entry) => entry.slug === slug);
  if (!doc) return null;
  return { ...doc, absPath: path.join(ROOT, doc.file) };
}

import fs from 'fs';

const BLOCKED = [/(^|\/)\./, /secret/i, /credential/i, /token/i, /wallet/i, /seed/i, /node_modules\//];

export function safeMdPath(rel) {
  const clean = String(rel || '').trim();
  if (!clean || clean.includes('..') || path.isAbsolute(clean)) return null;
  if (!clean.endsWith('.md')) return null;
  if (BLOCKED.some((pattern) => pattern.test(clean))) return null;
  const abs = path.resolve(ROOT, clean);
  if (!abs.startsWith(ROOT + path.sep)) return null;
  if (!fs.existsSync(abs)) return null;
  return { rel: clean, abs };
}

function hrefFor(rel) {
  const inLibrary = LIBRARY.find((entry) => entry.file === rel);
  if (inLibrary) return `/docs/${inLibrary.slug}`;
  if (rel.endsWith('.md')) return `/docs/view?f=${encodeURIComponent(rel)}`;
  return '/files/' + rel.split('/').map(encodeURIComponent).join('/');
}

export function linkifyRepoPaths(html) {
  const pathPattern = /<code>([A-Za-z0-9][\w./ -]*\.(?:md|pdf|png|jpe?g|gif|svg|mp3|mp4|html|json|csv))<\/code>/g;
  let out = html.replace(pathPattern, (match, rel) => {
    if (!fs.existsSync(path.join(ROOT, rel)) || BLOCKED.some((pattern) => pattern.test(rel))) return match;
    return `<a href="${hrefFor(rel)}"><code>${rel}</code></a>`;
  });
  out = out.replace(/href="((?!https?:|\/|#)[\w./ -]+\.md)"/g, (match, rel) => {
    if (!fs.existsSync(path.join(ROOT, rel))) return match;
    return `href="${hrefFor(rel)}"`;
  });
  return out;
}
