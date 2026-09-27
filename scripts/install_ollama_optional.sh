#!/usr/bin/env bash
# install_ollama_optional.sh — OPTIONAL local model runtime for the Pi.
#
# Ollama on the Pi 4 is for TINY models / low-stakes tasks only (see LOCAL_MODELS.md).
# Do NOT let this derail Hermes setup. Install only if Josh approves.
#
# Guarded: does nothing without CONFIRM=yes.
#   CONFIRM=yes bash scripts/install_ollama_optional.sh

set -euo pipefail

echo "Ollama (optional, Tier 0 local) install helper"
echo "Pi 4 = tiny models only. Heavy models belong on a Mac mini / custom PC later."
echo "Official install reference (VERIFY): https://ollama.com/download/linux"
echo

if command -v ollama >/dev/null 2>&1; then
  echo "ollama already installed: $(ollama --version 2>&1 | head -n1)"
  echo "Try a tiny model:  ollama pull qwen2.5:1.5b  &&  ollama run qwen2.5:1.5b"
  exit 0
fi

# The official one-liner uses sudo internally — requires explicit approval.
INSTALL_CMD="curl -fsSL https://ollama.com/install.sh | sh"   # VERIFY before trusting

echo "Planned command (uses sudo internally):"
echo "  $INSTALL_CMD"
echo

if [ "${CONFIRM:-no}" != "yes" ]; then
  echo "Dry run only. Nothing executed."
  echo "Verify the command above, get Josh's approval, then re-run:"
  echo "  CONFIRM=yes bash scripts/install_ollama_optional.sh"
  exit 0
fi

echo "CONFIRM=yes set. Installing in 5s (Ctrl-C to abort)..."
sleep 5
eval "$INSTALL_CMD"
echo
echo "Next (tiny model test):"
echo "  ollama pull qwen2.5:1.5b"
echo "  ollama run  qwen2.5:1.5b 'Summarize: hello world.'"
echo "Record speed/quality/RAM in LOCAL_MODELS.md."
