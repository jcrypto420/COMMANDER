# NOW.md

**Active focus:** Priority 1 — Command Center / Hermes setup.

**Today's desired outcome:** Repo scaffolding in place; Pi inventory run;
Hermes install path verified and ready for approval.

## Next 3 tasks

1. Run `scripts/pi_inventory.sh` on the Pi and paste results into a comment on
   `TASK_QUEUE.md` task CC-2.
2. Verify the current Hermes install command against the docs links in
   `HERMES_SETUP.md`; fill in the verified command.
3. Choose the day-one provider (Nous Portal or OpenRouter) and add the key to a
   local `.env` from `configs/hermes_env_template.env` (never commit it).

## Current blockers

- Network/Hermes-docs not reachable from the build environment — install
  commands in `HERMES_SETUP.md` are marked **VERIFY** until checked on the Pi.
- Need Josh's approval before any install / `sudo` / paid provider key.

_Update this file at the start and end of each working session._
