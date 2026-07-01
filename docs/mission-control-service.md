# Mission Control User Service

Mission Control is installed as a user-level systemd service so Josh can access the dashboard without keeping PuTTY open.

## Service

```text
commander-mission-control.service
```

Service file:

```text
/home/josh/.config/systemd/user/commander-mission-control.service
```

## URL

Home WiFi / LAN:

```text
http://192.168.1.189:3011
```

Phone access:

- Works from phone if the phone is on the same home WiFi/LAN and the router allows device-to-device traffic.
- Does not work from cellular/off-site yet.
- For safe away-from-home access, set up Tailscale later with explicit approval.

## Useful commands

```bash
systemctl --user status commander-mission-control.service --no-pager
systemctl --user restart commander-mission-control.service
journalctl --user -u commander-mission-control.service -n 80 --no-pager
systemctl --user status commander-mission-control-refresh.timer --no-pager
journalctl --user -u commander-mission-control-refresh.service -n 40 --no-pager
```

## What it does

- Runs from `/home/josh/COMMANDER`.
- Runs `npm run dashboard:state` before startup.
- Serves Next.js Mission Control on `0.0.0.0:3011`.
- Does not touch existing port `3010` Sovereignty Stack dashboard.
- Survives PuTTY disconnects.

## Auto-refresh

Approved and installed on 2026-06-30:

- `commander-mission-control-refresh.timer` runs every 2 minutes.
- It triggers `commander-mission-control-refresh.service`.
- The refresh service runs `npm run dashboard:state` from `/home/josh/COMMANDER`.
- The browser page includes a 120-second refresh so phone Mission Control catches new state without manual reloads.
- This is read-only dashboard state generation; it does not post, send, spend, create accounts, expose ports, or touch secrets.

## Verification

Verified on 2026-06-29:

- `npm run build` passed with Next.js 16.2.9.
- `systemctl --user restart commander-mission-control.service` succeeded.
- service status showed `active (running)`.
- `curl http://127.0.0.1:3011/` returned rendered Next.js HTML.
- `commander-mission-control-refresh.timer` is enabled/active and refresh service completed successfully.

## Safety

- No router/public exposure was configured.
- No secrets displayed.
- Dashboard action buttons remain approval-gated.
- Commander Inbox is capture/triage only: it writes to `COMMANDER_INBOX.md` and local ignored `dashboard/commander_inbox.jsonl`; it does not execute commands, post, send, spend, or touch secrets.
- Off-site access should be Tailscale/private-network only after approval.
