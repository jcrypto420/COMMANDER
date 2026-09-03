#!/usr/bin/env bash
# THE DAILY MOG — boot runner: generate the live PDF, then print it.
#
# Triggered by the daily-mog.service systemd unit (After=network-online.target),
# so this fires once per boot — matching Josh powering the Pi off nightly and
# turning it on fresh each morning, not a fixed clock time.
#
# Wired for unattended auto-print per Josh's explicit approval (2026-07-06,
# see projects/daily-mog-print-handoff.md's standing draft-first rule — this
# is the one-time "yes" that rule requires before auto-print was allowed).
#
# If generation fails, we deliberately do NOT print — printing a stale PDF
# left over from a previous run would be a "no source, no number" violation
# dressed up as fresh data.
set -uo pipefail
cd "$(dirname "$0")/.."

LOG="logs/daily_mog_boot.log"
mkdir -p logs

echo "=== $(date '+%Y-%m-%d %H:%M:%S') boot run start ===" >> "$LOG"

if python3 scripts/generate_daily_mog.py >> "$LOG" 2>&1; then
    if lp -d HP_SmartTank_7602 -o media=Letter THE_DAILY_MOG.pdf >> "$LOG" 2>&1; then
        echo "printed OK" >> "$LOG"
    else
        echo "PRINT FAILED — see lp output above. PDF still generated at THE_DAILY_MOG.pdf." >> "$LOG"
    fi
else
    echo "GENERATE FAILED — nothing sent to printer, no stale PDF re-printed." >> "$LOG"
fi

echo "=== $(date '+%Y-%m-%d %H:%M:%S') boot run end ===" >> "$LOG"
