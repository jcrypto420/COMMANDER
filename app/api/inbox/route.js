import fs from 'fs';
import path from 'path';
import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';

const ROOT = process.cwd();
const INBOX_MD = path.join(ROOT, 'COMMANDER_INBOX.md');
const INBOX_JSONL = path.join(ROOT, 'dashboard', 'commander_inbox.jsonl');
const MAX_MESSAGE = 1800;
const MAX_ENTRIES = 12;
const SECRET_PATTERNS = [
  /\b\d{8,10}:[A-Za-z0-9_-]{25,}\b/,
  /sk-[A-Za-z0-9_-]{20,}/i,
  /api[_-]?key\s*[:=]/i,
  /secret\s*[:=]/i,
  /password\s*[:=]/i,
  /seed phrase/i,
  /private key/i,
  /wallet seed/i,
];

function ensureInbox() {
  if (!fs.existsSync(INBOX_MD)) {
    fs.writeFileSync(INBOX_MD, '# Commander Inbox\n\nPhone/dashboard captures for Commander. Do not put secrets, passwords, API keys, seed phrases, private keys, or verification codes here.\n\n');
  }
  fs.mkdirSync(path.dirname(INBOX_JSONL), { recursive: true });
  if (!fs.existsSync(INBOX_JSONL)) fs.writeFileSync(INBOX_JSONL, '');
}

function cleanText(value) {
  return String(value || '').replace(/\r\n/g, '\n').trim().slice(0, MAX_MESSAGE);
}

function hasSecretLikeText(text) {
  return SECRET_PATTERNS.some((pattern) => pattern.test(text));
}

function readAllEntries() {
  ensureInbox();
  return fs.readFileSync(INBOX_JSONL, 'utf8').split('\n').filter(Boolean).map((line) => {
    try { return JSON.parse(line); } catch { return null; }
  }).filter(Boolean);
}

function writeAllEntries(entries) {
  ensureInbox();
  fs.writeFileSync(INBOX_JSONL, entries.map((entry) => JSON.stringify(entry)).join('\n') + (entries.length ? '\n' : ''));
}

function readEntries() {
  return readAllEntries().slice(-MAX_ENTRIES).reverse();
}

function appendInboxMarkdown(entry) {
  const actionLine = entry.action ? `\nTriage: ${entry.action}\n` : '';
  fs.appendFileSync(INBOX_MD, `\n## ${entry.created_at} — ${entry.lane}\n\nStatus: ${entry.status} / captured only. No action executed automatically.${actionLine}\n${entry.message}\n`);
}

export async function GET() {
  return NextResponse.json({ entries: readEntries() }, { headers: { 'Cache-Control': 'no-store' } });
}

export async function POST(request) {
  ensureInbox();
  let body;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: 'Invalid JSON body' }, { status: 400 });
  }

  const message = cleanText(body.message);
  const lane = cleanText(body.lane || 'capture').replace(/[^a-zA-Z0-9 _/-]/g, '').slice(0, 40) || 'capture';
  if (!message) return NextResponse.json({ error: 'Message is required' }, { status: 400 });
  if (hasSecretLikeText(message)) {
    return NextResponse.json({ error: 'Looks like a secret or credential. Do not submit that through Mission Control.' }, { status: 400 });
  }

  const entry = {
    id: `${Date.now()}-${Math.random().toString(16).slice(2, 8)}`,
    created_at: new Date().toISOString(),
    lane,
    message,
    status: 'new',
    note: 'Captured only. Commander has not executed this automatically.',
  };

  fs.appendFileSync(INBOX_JSONL, JSON.stringify(entry) + '\n');
  appendInboxMarkdown(entry);

  return NextResponse.json({ ok: true, entry, entries: readEntries() }, { status: 201 });
}

export async function PATCH(request) {
  ensureInbox();
  let body;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: 'Invalid JSON body' }, { status: 400 });
  }

  const id = cleanText(body.id);
  const action = cleanText(body.action).replace(/[^a-zA-Z0-9 _/-]/g, '').slice(0, 40);
  const allowedActions = new Set(['keep', 'park', 'make-task', 'ask-josh', 'trash-wank', 'done']);
  if (!id || !allowedActions.has(action)) {
    return NextResponse.json({ error: 'Valid id and action are required' }, { status: 400 });
  }

  const entries = readAllEntries();
  const index = entries.findIndex((entry) => entry.id === id);
  if (index < 0) return NextResponse.json({ error: 'Entry not found' }, { status: 404 });

  entries[index] = {
    ...entries[index],
    status: action,
    action,
    triaged_at: new Date().toISOString(),
    note: `Triaged as ${action}. No action executed automatically.`,
  };
  writeAllEntries(entries);
  fs.appendFileSync(INBOX_MD, `\n- ${entries[index].triaged_at}: triaged ${id} as ${action}. No action executed automatically.\n`);

  return NextResponse.json({ ok: true, entry: entries[index], entries: readEntries() });
}
