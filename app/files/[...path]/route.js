import fs from 'fs';
import path from 'path';
import { NextResponse } from 'next/server';

const ROOT = process.cwd();
const ALLOWED_PREFIXES = [
  'assets/',
  'projects/',
  'docs/',
  'dashboard/',
  'prototypes/'
];
const ALLOWED_ROOT_FILES = new Set([
  'MORNING_REPORT.md',
  'WEEKLY_MONEY_REVIEW.md',
  'COMMANDER_OPERATING_RHYTHM_V1.md',
  'TASK_QUEUE.md',
  'NOW.md',
  'GOALS.md'
]);
const BLOCKED_PATTERNS = [
  /(^|\/)\.env/i,
  /secret/i,
  /credential/i,
  /token/i,
  /wallet/i,
  /seed/i,
  /private[_-]?key/i,
  /\.pem$/i,
  /\.key$/i,
  /node_modules\//i,
  /\.git\//i,
  /\.next\//i
];

function contentType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return {
    '.html': 'text/html; charset=utf-8',
    '.htm': 'text/html; charset=utf-8',
    '.md': 'text/plain; charset=utf-8',
    '.txt': 'text/plain; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.css': 'text/css; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8'
  }[ext] || 'application/octet-stream';
}

function isAllowed(relPath) {
  if (!relPath || relPath.includes('..') || path.isAbsolute(relPath)) return false;
  if (BLOCKED_PATTERNS.some((pattern) => pattern.test(relPath))) return false;
  if (ALLOWED_ROOT_FILES.has(relPath)) return true;
  return ALLOWED_PREFIXES.some((prefix) => relPath.startsWith(prefix));
}

export async function GET(_request, { params }) {
  const routeParams = await params;
  const relPath = decodeURIComponent((routeParams.path || []).join('/'));
  if (!isAllowed(relPath)) {
    return NextResponse.json({ error: 'File path is not allowed' }, { status: 403 });
  }

  const fullPath = path.resolve(ROOT, relPath);
  if (!fullPath.startsWith(ROOT + path.sep)) {
    return NextResponse.json({ error: 'File path escaped repo root' }, { status: 403 });
  }

  try {
    const stat = fs.statSync(fullPath);
    if (!stat.isFile()) {
      return NextResponse.json({ error: 'Not a file' }, { status: 404 });
    }
    const body = fs.readFileSync(fullPath);
    return new NextResponse(body, {
      headers: {
        'Content-Type': contentType(fullPath),
        'Cache-Control': 'no-store',
        'X-Content-Type-Options': 'nosniff'
      }
    });
  } catch {
    return NextResponse.json({ error: 'File not found' }, { status: 404 });
  }
}
