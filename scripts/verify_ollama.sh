#!/usr/bin/env bash
# verify_ollama.sh — READ-ONLY check of Ollama + local models. Changes nothing.

set -u

echo "Ollama verification ($(date))"

if ! command -v ollama >/dev/null 2>&1; then
  echo "ollama: not installed (optional — see scripts/install_ollama_optional.sh)"
  exit 0
fi

echo "version: $(ollama --version 2>&1 | head -n1)"

echo
echo "Installed models:"
ollama list 2>/dev/null || echo "  (could not list — is the ollama service running?)"

echo
echo "API endpoint check (http://localhost:11434):"
if command -v curl >/dev/null 2>&1; then
  if curl -fsS http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "  reachable ✓ (OpenAI-compatible base: http://localhost:11434/v1)"
  else
    echo "  not reachable — start with: ollama serve"
  fi
else
  echo "  curl not available to test endpoint"
fi

echo "Done. Nothing was changed."
