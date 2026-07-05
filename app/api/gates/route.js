import fs from 'fs';
import path from 'path';
import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';

const ROOT = process.cwd();
const GATES_PATH = path.join(ROOT, 'gates', 'pending.json');
const INBOX_MD = path.join(ROOT, 'COMMANDER_INBOX.md');
const INBOX_JSONL = path.join(ROOT, 'dashboard', 'commander_inbox.jsonl');
const MAX_NOTE = 400;

function readGates() {
  try {
    return JSON.parse(fs.readFileSync(GATES_PATH, 'utf8'));
  } catch {
    return { updated_at: null, gates: [] };
  }
}

function writeGates(data) {
  data.updated_at = new Date().toISOString();
  fs.writeFileSync(GATES_PATH, JSON.stringify(data, null, 2) + '\n');
}

function cleanText(value, limit = MAX_NOTE) {
  return String(value || '').replace(/\r\n/g, '\n').trim().slice(0, limit);
}

export async function GET() {
  return NextResponse.json(readGates(), { headers: { 'Cache-Control': 'no-store' } });
}

export async function POST(request) {
  let body;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: 'Invalid JSON body' }, { status: 400 });
  }

  const id = cleanText(body.id, 80);
  const verdict = cleanText(body.verdict, 30).replace(/[^a-zA-Z0-9 _/-]/g, '');
  const note = cleanText(body.note);
  if (!id || !verdict) {
    return NextResponse.json({ error: 'id and verdict are required' }, { status: 400 });
  }

  const data = readGates();
  const gate = data.gates.find((entry) => entry.id === id);
  if (!gate) return NextResponse.json({ error: 'Gate not found' }, { status: 404 });
  if (gate.status !== 'pending') {
    return NextResponse.json({ error: 'Gate is not pending' }, { status: 409 });
  }
  if (!(gate.options || []).includes(verdict)) {
    return NextResponse.json({ error: 'Verdict not in gate options' }, { status: 400 });
  }

  gate.status = 'verdicted';
  gate.verdict = verdict;
  if (note) gate.note = note;
  gate.verdicted_at = new Date().toISOString();
  writeGates(data);

  const capture = {
    id: `${Date.now()}-${Math.random().toString(16).slice(2, 8)}`,
    created_at: gate.verdicted_at,
    lane: 'gate-verdict',
    message: `GATE VERDICT: ${verdict} — ${gate.title} (${gate.id})${note ? ` — note: ${note}` : ''}`,
    status: 'new',
    note: 'Captured only. Commander reads gate verdicts on its next loop; nothing executes automatically.',
  };
  fs.mkdirSync(path.dirname(INBOX_JSONL), { recursive: true });
  fs.appendFileSync(INBOX_JSONL, JSON.stringify(capture) + '\n');
  fs.appendFileSync(INBOX_MD, `\n## ${capture.created_at} — gate-verdict\n\nStatus: captured only. No action executed automatically.\n${capture.message}\n`);

  return NextResponse.json({ ok: true, gate, gates: readGates().gates }, { status: 201 });
}
