'use client';

import { useEffect, useState } from 'react';

const VERDICT_COLORS = {
  SHIP: 'var(--green)',
  'THIS WEEKEND': 'var(--green)',
  'NEXT WEEK': 'var(--amber)',
  DEFER: 'var(--amber)',
  KILL: 'var(--red)',
};

export default function GateDeck() {
  const [gates, setGates] = useState([]);
  const [busy, setBusy] = useState('');
  const [notes, setNotes] = useState({});
  const [error, setError] = useState('');

  async function load() {
    try {
      const res = await fetch('/api/gates', { cache: 'no-store' });
      const data = await res.json();
      setGates(data.gates || []);
    } catch {
      setError('Could not load gates.');
    }
  }

  useEffect(() => { load(); }, []);

  async function verdict(id, choice) {
    setBusy(id);
    setError('');
    try {
      const res = await fetch('/api/gates', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, verdict: choice, note: notes[id] || '' }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Verdict failed');
      setGates(data.gates || []);
    } catch (err) {
      setError(String(err.message || err));
    } finally {
      setBusy('');
    }
  }

  const pending = gates.filter((gate) => gate.status === 'pending');
  const upcoming = gates.filter((gate) => gate.status === 'upcoming');
  const done = gates.filter((gate) => gate.status === 'verdicted');

  return (
    <main className="shell" style={{ maxWidth: 760 }}>
      <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', margin: '14px 0 18px' }}>
        <h1 style={{ fontSize: 26, margin: 0 }}>Gate deck</h1>
        <a href="/" style={{ color: 'var(--blue)', fontSize: 13, textDecoration: 'none' }}>← mission control</a>
      </div>
      <p style={{ color: 'var(--muted)', fontSize: 13, marginTop: -8 }}>
        Tap a verdict. It is captured for Commander&apos;s next loop — nothing executes automatically.
      </p>
      {error ? <p style={{ color: 'var(--red)', fontSize: 13 }}>{error}</p> : null}

      {pending.length === 0 && upcoming.length === 0 ? (
        <div className="panel" style={{ padding: '22px 24px', borderRadius: 16, marginTop: 14 }}>
          <p style={{ margin: 0, color: 'var(--soft)' }}>No pending decisions. The machine is working.</p>
        </div>
      ) : null}

      {pending.map((gate) => (
        <section key={gate.id} className="panel" style={{ padding: '18px 20px', borderRadius: 16, marginBottom: 14 }}>
          <div style={{ fontSize: 11, letterSpacing: '0.08em', textTransform: 'uppercase', color: 'var(--violet)', marginBottom: 6 }}>{gate.lane}</div>
          <h2 style={{ fontSize: 18, margin: '0 0 8px' }}>{gate.title}</h2>
          <p style={{ color: 'var(--soft)', fontSize: 14, lineHeight: 1.55, margin: '0 0 12px' }}>{gate.context}</p>
          <input
            value={notes[gate.id] || ''}
            onChange={(event) => setNotes({ ...notes, [gate.id]: event.target.value })}
            placeholder="optional one-liner (why / taste note)"
            style={{ width: '100%', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--line)', borderRadius: 10, padding: '9px 12px', color: 'var(--text)', fontSize: 13, marginBottom: 12 }}
          />
          <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
            {(gate.options || []).map((option) => (
              <button
                key={option}
                disabled={busy === gate.id}
                onClick={() => verdict(gate.id, option)}
                style={{
                  flex: 1,
                  minWidth: 110,
                  padding: '11px 14px',
                  borderRadius: 12,
                  border: `1px solid ${VERDICT_COLORS[option] || 'var(--line)'}`,
                  background: 'transparent',
                  color: VERDICT_COLORS[option] || 'var(--text)',
                  fontSize: 14,
                  fontWeight: 600,
                  cursor: 'pointer',
                  opacity: busy === gate.id ? 0.5 : 1,
                }}
              >
                {option}
              </button>
            ))}
          </div>
        </section>
      ))}

      {upcoming.map((gate) => (
        <section key={gate.id} className="panel" style={{ padding: '16px 20px', borderRadius: 16, marginBottom: 14, opacity: 0.55 }}>
          <div style={{ fontSize: 11, letterSpacing: '0.08em', textTransform: 'uppercase', color: 'var(--muted)', marginBottom: 6 }}>{gate.lane} · upcoming</div>
          <h2 style={{ fontSize: 16, margin: '0 0 6px' }}>{gate.title}</h2>
          <p style={{ color: 'var(--muted)', fontSize: 13, lineHeight: 1.5, margin: 0 }}>{gate.context}</p>
        </section>
      ))}

      {done.length ? (
        <div style={{ marginTop: 22 }}>
          <h3 style={{ fontSize: 13, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Recent verdicts</h3>
          {done.slice(-6).reverse().map((gate) => (
            <div key={gate.id} style={{ display: 'flex', justifyContent: 'space-between', gap: 12, padding: '9px 2px', borderBottom: '1px solid var(--line)', fontSize: 13 }}>
              <span style={{ color: 'var(--soft)' }}>{gate.title}</span>
              <span style={{ color: VERDICT_COLORS[gate.verdict] || 'var(--text)', fontWeight: 600, whiteSpace: 'nowrap' }}>{gate.verdict}</span>
            </div>
          ))}
        </div>
      ) : null}
    </main>
  );
}
