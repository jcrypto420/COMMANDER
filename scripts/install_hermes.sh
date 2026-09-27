#!/usr/bin/env bash
# install_hermes.sh — CAUTIOUS helper to install Hermes Agent.
#
# This script does NOT install anything by default. It guards you.
# Run with:  CONFIRM=yes bash scripts/install_hermes.sh
# It will NOT install without CONFIRM=yes. Ask Josh first.
#
# Command verified 2026-06-27 from the official docs (see HERMES_SETUP.md).
# The installer bundles its own Python and does not require sudo.

set -euo pipefail

# Verified official installer for Linux/ARM64 (Raspberry Pi works):
INSTALL_CMD="curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash"

DOCS="https://hermes-agent.nousresearch.com/docs/  |  https://github.com/NousResearch/hermes-agent"

echo "Hermes install helper"
echo "Verify current install command first: $DOCS"
echo

if [ -z "$INSTALL_CMD" ]; then
  echo "STOP: INSTALL_CMD is empty."
  echo "Open the docs, confirm the official Linux/ARM64 install command,"
  echo "paste it into INSTALL_CMD in this script, then re-run with CONFIRM=yes."
  exit 1
fi

echo "Planned command:"
echo "  $INSTALL_CMD"
echo

if [ "${CONFIRM:-no}" != "yes" ]; then
  echo "Dry run only. Nothing executed."
  echo "To actually install, re-run:  CONFIRM=yes bash scripts/install_hermes.sh"
  exit 0
fi

echo "CONFIRM=yes set. Running install command in 5s (Ctrl-C to abort)..."
sleep 5
eval "$INSTALL_CMD"
echo
echo "Done. Now reload your shell:   source ~/.bashrc"
echo "Then continue with HERMES_SETUP.md:"
echo "  hermes setup --portal            # connect a model provider"
echo "  hermes profile create commander  # create the commander profile"
