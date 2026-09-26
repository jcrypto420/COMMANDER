# Dashboard Access Plan — easiest path for Josh

## Recommendation

Use the simple LAN path first:

```text
http://192.168.1.189:3011
```

Why this is the easiest now:

- Josh uses an HP laptop on the same home network.
- Tailscale CLI is not installed on this Pi right now, even though the Pi has a Tailscale-style `100.x` address from some interface state.
- Port `3010` is already occupied by an existing Sovereignty Stack dashboard/login service.
- Mission Control has already rendered successfully on port `3011`.
- No public internet exposure is needed.

## Temporary/manual run

From PuTTY:

```bash
cd /home/josh/COMMANDER
npm run dashboard:state
npm run dev:lan
```

Then open from the HP laptop:

```text
http://192.168.1.189:3011
```

Stop it with `Ctrl+C` in that terminal.

## Permanent path is now installed

Josh approved service setup. Mission Control now runs as a user-level service:

```text
commander-mission-control.service
```

It:

- runs `npm run dashboard:state` before start
- serves Mission Control on `0.0.0.0:3011`
- survives PuTTY disconnects
- stays on LAN only unless router/firewall rules expose it, which Commander must not do
- does not replace the existing `3010` Sovereignty Stack dashboard

See: `docs/mission-control-service.md`

## Later upgrade

If Josh wants secure away-from-home access, install/configure Tailscale deliberately and bind or firewall the dashboard for private-network access only. That is a separate approval-gated system change.

Suggested future phrase:

```text
APPROVE TAILSCALE DASHBOARD ACCESS SETUP
```

## Safety

- No public ports.
- No router changes.
- No secrets displayed.
- No service install until approved.
- Dashboard action buttons remain approval-gated.
