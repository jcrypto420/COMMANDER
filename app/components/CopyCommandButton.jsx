'use client';

import { useState } from 'react';

export default function CopyCommandButton({ command, label = 'Copy' }) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    try {
      await navigator.clipboard.writeText(command);
      setCopied(true);
      setTimeout(() => setCopied(false), 1400);
    } catch {
      setCopied(false);
    }
  }

  return (
    <button className="copy-button" type="button" onClick={copy}>
      {copied ? 'Copied' : label}
    </button>
  );
}
