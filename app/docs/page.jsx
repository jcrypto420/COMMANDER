import { LIBRARY, jobPacketDocs } from './library';

export const dynamic = 'force-dynamic';

export const metadata = { title: 'Library — Commander' };

export default function DocsIndex() {
  const entries = [
    ...LIBRARY.map((doc) => ({ ...doc, href: `/docs/${doc.slug}` })),
    ...jobPacketDocs(),
  ];
  const groups = [...new Set(entries.map((doc) => doc.group))];
  return (
    <main className="shell" style={{ maxWidth: 760 }}>
      <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', margin: '14px 0 6px' }}>
        <h1 style={{ fontSize: 26, margin: 0 }}>Library</h1>
        <a href="/" style={{ color: 'var(--blue)', fontSize: 13, textDecoration: 'none' }}>← mission control</a>
      </div>
      <p style={{ color: 'var(--muted)', fontSize: 13, marginTop: 0 }}>The documents that matter, one tap each. Active applications list themselves; applied and killed roles auto-archive out.</p>
      {groups.map((group) => (
        <section key={group} style={{ marginTop: 18 }}>
          <h2 style={{ fontSize: 12, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.1em', margin: '0 0 10px' }}>{group}</h2>
          <div style={{ display: 'grid', gap: 10 }}>
            {entries.filter((doc) => doc.group === group).map((doc) => (
              <a key={doc.href} href={doc.href} className="panel" style={{ display: 'block', padding: '14px 18px', borderRadius: 14, textDecoration: 'none', color: 'var(--text)' }}>
                <b style={{ fontSize: 15 }}>{doc.title}</b>
                <p style={{ margin: '4px 0 0', color: 'var(--muted)', fontSize: 13 }}>{doc.blurb}</p>
              </a>
            ))}
          </div>
        </section>
      ))}
    </main>
  );
}
