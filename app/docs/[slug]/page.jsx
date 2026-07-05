import fs from 'fs';
import { marked } from 'marked';
import { resolveDoc, linkifyRepoPaths } from '../library';

export const dynamic = 'force-dynamic';

export default async function DocView({ params }) {
  const { slug } = await params;
  const doc = resolveDoc(slug);
  let html = '';
  let missing = false;
  if (doc) {
    try {
      const raw = fs.readFileSync(doc.absPath, 'utf8');
      html = linkifyRepoPaths(marked.parse(raw, { gfm: true, breaks: false }));
    } catch {
      missing = true;
    }
  }

  return (
    <main className="shell" style={{ maxWidth: 760 }}>
      <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', margin: '14px 0 10px', gap: 12 }}>
        <h1 style={{ fontSize: 20, margin: 0 }}>{doc ? doc.title : 'Not found'}</h1>
        <a href="/docs" style={{ color: 'var(--blue)', fontSize: 13, textDecoration: 'none', whiteSpace: 'nowrap' }}>← library</a>
      </div>
      {!doc ? (
        <p style={{ color: 'var(--muted)' }}>That document is not in the library.</p>
      ) : missing ? (
        <p style={{ color: 'var(--muted)' }}>{doc.file} does not exist yet — it will appear here the moment an agent creates it.</p>
      ) : (
        <article className="panel doc-prose" style={{ padding: '20px 22px', borderRadius: 16 }} dangerouslySetInnerHTML={{ __html: html }} />
      )}
    </main>
  );
}
