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
```

## What it does

- Runs from `/home/josh/COMMANDER`.
- Runs `npm run dashboard:state` before startup.
- Serves Next.js Mission Control on `0.0.0.0:3011`.
- Does not touch existing port `3010` Sovereignty Stack dashboard.
- Survives PuTTY disconnects.

## Verification

Verified on 2026-06-29:

- `npm run build` passed with Next.js 16.2.9.
- `systemctl --user restart commander-mission-control.service` succeeded.
- service status showed `active (running)`.
- `curl http://127.0.0.1:3011/` returned rendered Next.js HTML.

## Safety

- No router/public exposure was configured.
- No secrets displayed.
- Dashboard action buttons remain approval-gated.
- Off-site access should be Tailscale/private-network only after approval.
