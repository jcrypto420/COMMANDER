#!/usr/bin/env bash
# backup_command_center.sh — make a local, secret-free archive of this repo.
#
# Safe: only reads the repo and writes ONE archive to a backup dir.
# Excludes secrets, logs content, runtime state, and model files.
# Default backup dir: external storage if present, else $HOME/backups.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
NAME="command-center-$(date +%Y%m%d-%H%M%S).tar.gz"

# Prefer external 2TB storage if mounted; fall back to home.
BACKUP_DIR="${BACKUP_DIR:-}"
if [ -z "$BACKUP_DIR" ]; then
  for d in /mnt/* /media/*/* ; do
    if [ -d "$d" ] && [ -w "$d" ]; then BACKUP_DIR="$d/command-center-backups"; break; fi
  done
fi
[ -z "$BACKUP_DIR" ] && BACKUP_DIR="$HOME/backups"

mkdir -p "$BACKUP_DIR"

echo "Backing up: $REPO_DIR"
echo "Into:       $BACKUP_DIR/$NAME"
echo "Excluding secrets, .git, logs content, runtime state, models..."

tar \
  --exclude='.git' \
  --exclude='*.env' --exclude='.env' \
  --exclude='.hermes' --exclude='sessions' --exclude='memories' \
  --exclude='*.sqlite*' --exclude='*.db' \
  --exclude='logs/*.csv' --exclude='logs/*.md' \
  --exclude='*.gguf' --exclude='models' --exclude='.ollama' \
  --exclude='node_modules' --exclude='__pycache__' --exclude='.venv' --exclude='venv' \
  -czf "$BACKUP_DIR/$NAME" -C "$(dirname "$REPO_DIR")" "$(basename "$REPO_DIR")"

echo "Done: $BACKUP_DIR/$NAME"
echo "Tip: keep at least the last few backups; verify with: tar -tzf <file> | head"
