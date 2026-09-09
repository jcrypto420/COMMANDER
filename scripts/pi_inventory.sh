#!/usr/bin/env bash
# pi_inventory.sh — READ-ONLY inventory of the Raspberry Pi.
# Changes nothing. Safe to run anytime. (See HERMES_SETUP.md step 0.)

set -u

line() { printf '\n--- %s ---\n' "$1"; }
have() { command -v "$1" >/dev/null 2>&1; }

echo "Command Center — Pi Inventory ($(date))"

line "Identity"
echo "hostname: $(hostname 2>/dev/null)"
echo "user:     $(whoami 2>/dev/null)"
echo "pwd:      $(pwd)"

line "OS / Arch"
if [ -r /etc/os-release ]; then . /etc/os-release; echo "os: ${PRETTY_NAME:-unknown}"; fi
echo "kernel: $(uname -srm 2>/dev/null)"
echo "arch:   $(uname -m 2>/dev/null)"

line "Memory"
if have free; then free -h; else echo "free not available"; fi

line "Disk"
df -h 2>/dev/null | grep -Ev 'tmpfs|udev' || df -h

line "External storage mounts"
# Common external mount roots; harmless if empty.
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT 2>/dev/null || echo "lsblk not available"
echo "(also check /media and /mnt)"
ls -1 /media 2>/dev/null; ls -1 /mnt 2>/dev/null

line "Docker"
if have docker; then docker --version; docker ps --format '  {{.Names}} ({{.Image}})' 2>/dev/null || echo "  (cannot list containers — may need permissions)"; else echo "docker not installed"; fi

line "CasaOS / Dockge (detection only)"
if have casaos || [ -d /etc/casaos ] || systemctl list-units 2>/dev/null | grep -qi casaos; then echo "CasaOS: likely present"; else echo "CasaOS: not detected"; fi
if docker ps --format '{{.Names}}' 2>/dev/null | grep -qi dockge; then echo "Dockge: container detected"; else echo "Dockge: not detected"; fi

line "Tailscale"
if have tailscale; then tailscale status 2>/dev/null | head -n 5 || echo "tailscale installed (status needs permission)"; else echo "tailscale not installed"; fi

line "Toolchain versions"
have git    && echo "git:    $(git --version)"            || echo "git: not installed"
have python3&& echo "python: $(python3 --version 2>&1)"    || echo "python3: not installed"
have node   && echo "node:   $(node --version)"            || echo "node: not installed"
have npm    && echo "npm:    $(npm --version)"             || echo "npm: not installed"
have ollama && echo "ollama: $(ollama --version 2>&1 | head -n1)" || echo "ollama: not installed"

line "Done"
echo "Nothing was changed. Paste this output into TASK_QUEUE.md task CC-2."
