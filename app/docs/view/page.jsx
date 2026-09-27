import fs from 'fs';
import { marked } from 'marked';
import { safeMdPath, linkifyRepoPaths } from '../library';

export const dynamic = 'force-dynamic';

export default async function DocFreeView({ searchParams }) {
  const { f } = await searchParams;
  const doc = safeMdPath(f);
  let html = '';
  if (doc) {
    const raw = fs.readFileSync(doc.abs, 'utf8');
    html = linkifyRepoPaths(marked.parse(raw, { gfm: true, breaks: false }));
  }

  return (
    <main className="shell" style={{ maxWidth: 760 }}>
      <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', margin: '14px 0 10px', gap: 12 }}>
        <h1 style={{ fontSize: 18, margin: 0, wordBreak: 'break-all' }}>{doc ? doc.rel : 'Not available'}</h1>
        <a href="/docs" style={{ color: 'var(--blue)', fontSize: 13, textDecoration: 'none', whiteSpace: 'nowrap' }}>← library</a>
      </div>
      {!doc ? (
        <p style={{ color: 'var(--muted)' }}>That file is not viewable here.</p>
      ) : (
        <article className="panel doc-prose" style={{ padding: '20px 22px', borderRadius: 16 }} dangerouslySetInnerHTML={{ __html: html }} />
      )}
    </main>
  );
}
