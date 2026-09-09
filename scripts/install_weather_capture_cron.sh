#!/bin/sh
# Idempotently install the nightly weather-oracle capture cron (Pi).
# Target: 20:30 America/Chicago. Debian cron has no CRON_TZ, so translate
# if the Pi clock is UTC. Re-running replaces the old line, never duplicates.
set -e

REPO="/home/josh/COMMANDER"
TZ_NAME=$(cat /etc/timezone 2>/dev/null || echo unknown)
case "$TZ_NAME" in
  America/Chicago) SCHED="30 20 * * *" ;;
  UTC|Etc/UTC)     SCHED="30 1 * * *" ;;  # 20:30 CDT
  *) echo "unexpected Pi timezone '$TZ_NAME' — install manually"; exit 1 ;;
esac

LINE="$SCHED cd $REPO && python3 products/weather-oracle/capture_daily.py >> logs/weather_capture.log 2>&1"
( crontab -l 2>/dev/null | grep -v 'weather-oracle/capture_daily' ; echo "$LINE" ) | crontab -
echo "installed ($TZ_NAME): $(crontab -l | grep 'weather-oracle/capture_daily')"
