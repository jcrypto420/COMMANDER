'use client';

import { useEffect, useState } from 'react';

const lanes = ['capture', 'decision', 'idea', 'bug', 'approval', 'question'];

export default function CommanderInbox({ initialEntries = [] }) {
  const [message, setMessage] = useState('');
  const [lane, setLane] = useState('capture');
  const [entries, setEntries] = useState(initialEntries);
  const [status, setStatus] = useState('');
  const [busy, setBusy] = useState(false);

  async function refresh() {
    try {
      const res = await fetch('/api/inbox', { cache: 'no-store' });
      const data = await res.json();
      setEntries(data.entries || []);
    } catch {
      // Keep current entries.
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    setStatus('Capturing…');
    try {
      const res = await fetch('/api/inbox', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lane, message }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Capture failed');
      setEntries(data.entries || []);
      setMessage('');
      setStatus('Captured. No action executed automatically.');
    } catch (error) {
      setStatus(error.message || 'Capture failed');
    } finally {
      setBusy(false);
    }
  }

  async function triage(id, action) {
    setBusy(true);
    setStatus(`Marking ${action}…`);
    try {
      const res = await fetch('/api/inbox', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, action }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Triage failed');
      setEntries(data.entries || []);
      setStatus(`Marked ${action}. No action executed automatically.`);
    } catch (error) {
      setStatus(error.message || 'Triage failed');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="inbox-console">
      <form className="inbox-form" onSubmit={submit}>
        <div className="inbox-topline">
          <select value={lane} onChange={(event) => setLane(event.target.value)} aria-label="Inbox lane">
            {lanes.map((item) => <option value={item} key={item}>{item}</option>)}
          </select>
          <button className="open-button" type="submit" disabled={busy || !message.trim()}>{busy ? 'Saving…' : 'Send to Commander Inbox'}</button>
        </div>
        <textarea
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Capture an idea, decision, bug, approval note, or question. No secrets/passwords/API keys. This saves to COMMANDER_INBOX.md; Commander will act on it when running."
          rows={5}
          maxLength={1800}
        />
        <div className="inbox-meta"><span>{message.length}/1800</span><span>{status}</span></div>
      </form>
      <div className="inbox-list">
        {entries.length ? entries.slice(0, 5).map((entry) => (
          <div className="inbox-entry" key={entry.id}>
            <div><b>{entry.lane}</b><small>{entry.created_at?.replace('T', ' ').slice(0, 19)} UTC</small></div>
            <p>{entry.message}</p>
            <div className="inbox-entry-footer">
              <code>{entry.status || 'new'}</code>
              <span>
                {['keep', 'park', 'make-task', 'ask-josh', 'trash-wank'].map((action) => (
                  <button key={action} type="button" onClick={() => triage(entry.id, action)} disabled={busy}>{action}</button>
                ))}
              </span>
            </div>
          </div>
        )) : <p className="muted">No captured dashboard messages yet.</p>}
      </div>
    </div>
  );
}
