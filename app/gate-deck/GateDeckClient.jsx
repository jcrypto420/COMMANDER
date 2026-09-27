'use client';

import { useMemo, useState } from 'react';

const verdicts = [
  { key: 'keep', label: 'Keep' },
  { key: 'park', label: 'Park' },
  { key: 'make-task', label: 'Make task' },
  { key: 'ask-josh', label: 'Ask Josh' },
  { key: 'trash-wank', label: 'Trash wank' },
];

export default function GateDeckClient({ cards = [] }) {
  const [status, setStatus] = useState({});

  const counts = useMemo(() => ({
    cards: cards.length,
    approvals: cards.filter((card) => String(card.approval || '').toLowerCase().includes('yes')).length,
  }), [cards]);

  async function sendVerdict(card, verdict) {
    const key = `${card.id}:${verdict}`;
    setStatus((prev) => ({ ...prev, [key]: 'Posting verdict…' }));
    try {
      const message = [
        `GATE DECK VERDICT: ${verdict.toUpperCase()}`,
        `${card.id} · ${card.project}`,
        card.task,
        card.approval ? `Approval: ${card.approval}` : '',
        card.next_action ? `Next: ${card.next_action}` : '',
      ].filter(Boolean).join('\n');
      const res = await fetch('/api/inbox', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lane: 'approval', message }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to post verdict');
      setStatus((prev) => ({ ...prev, [key]: `Saved to inbox as ${data.entry?.id || 'entry'}.` }));
    } catch (error) {
      setStatus((prev) => ({ ...prev, [key]: error.message || 'Failed to post verdict' }));
    }
  }

  return (
    <div>
      <div className="status-grid" style={{ marginBottom: 12 }}>
        <div className="mini-panel good"><span>Pending decisions</span><strong>{counts.cards}</strong></div>
        <div className="mini-panel warn"><span>Approval-gated</span><strong>{counts.approvals}</strong></div>
      </div>
      <div className="gate-grid">
        {cards.length ? cards.map((card) => (
          <div className="gate-card" key={card.id}>
            <div className="gate-card-head">
              <b>{card.id} · {card.project}</b>
              <small>{card.status}</small>
            </div>
            <p>{card.task}</p>
            <code>{card.next_action}</code>
            <div className="gate-actions">
              {verdicts.map((verdict) => (
                <button key={verdict.key} type="button" onClick={() => sendVerdict(card, verdict.key)}>
                  {verdict.label}
                </button>
              ))}
            </div>
            <div className="gate-status">{verdicts.map((verdict) => status[`${card.id}:${verdict.key}`]).find(Boolean) || 'Verdict posts will land in COMMANDER_INBOX.md.'}</div>
          </div>
        )) : <p className="muted">No approval-gated tasks found.</p>}
      </div>
    </div>
  );
}
