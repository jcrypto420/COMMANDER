#!/usr/bin/env bash
# install_hermes.sh — CAUTIOUS helper to install Hermes Agent.
#
# This script does NOT install anything by default. It guards you.
# Steps:
#   1. Verify the current install command in the docs (see HERMES_SETUP.md).
#   2. Paste that exact command into INSTALL_CMD below.
#   3. Re-run with:  CONFIRM=yes bash scripts/install_hermes.sh
#
# It will NOT run sudo or installs without CONFIRM=yes. Ask Josh first.

set -euo pipefail

# >>> PASTE THE VERIFIED INSTALL COMMAND HERE (leave empty until verified) <<<
INSTALL_CMD=""

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
echo "Install command finished. Next: create the 'commander' profile (HERMES_SETUP.md step 2)."
