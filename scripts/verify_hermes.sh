#!/usr/bin/env bash
# verify_hermes.sh — READ-ONLY check that Hermes is installed and `commander` exists.
# Changes nothing.

set -u
have() { command -v "$1" >/dev/null 2>&1; }

echo "Hermes verification ($(date))"

if have hermes; then
  echo "hermes binary: found"
  hermes --version 2>/dev/null || echo "  (version flag may differ — VERIFY in docs)"
elif docker ps -a --format '{{.Names}} {{.Image}}' 2>/dev/null | grep -qi hermes; then
  echo "hermes: running/known as a Docker container"
  docker ps -a --format '  {{.Names}} ({{.Image}}) {{.Status}}' | grep -i hermes
else
  echo "hermes: NOT detected (binary or container). See HERMES_SETUP.md."
fi

echo
echo "Looking for the 'commander' profile (paths VERIFY against docs):"
for p in "$HOME/.hermes/commander" "$HOME/.config/hermes/commander" "./.hermes/commander"; do
  if [ -d "$p" ]; then echo "  found: $p"; fi
done

echo
echo "Reminder: a local .env with at least one provider key must exist (git-ignored)."
echo "Done. Nothing was changed."
