# Bad Boys / Joycat — Hermes idea-bank + MoA critics cron draft

## Status — 2026-07-08
- **State:** DRAFT ONLY — internal design packet for BB-26; no cron enabled, no outbound actions, no public posting
- **Purpose:** turn the existing Bad Boys constitution + pipeline into a cheap weekly idea-bank loop that pre-filters premises before Josh ever sees them
- **Source of truth:** `projects/badboys-cartoon-lab.md` is authoritative for style/constitution; this packet only packages the cron draft
- **Next step:** if Josh approves, turn this into a real Hermes cron job and a stored weekly premise bank

## Recommendation

Use **one weekly Hermes cron** that does three things in sequence:

1. Generate **10 fresh premises** from the current Bad Boys constitution and active lane context.
2. Run a **MoA premise-critic** pass and keep only the strongest ideas.
3. Convert the survivors into **3–5 script-card drafts** and run the **MoA corny-detector** before banking them for Josh.

This keeps Josh out of the weeds, keeps the model spend cheap, and preserves the existing two-gate structure.

## Draft workflow

### Stage 0 — premise capture
- Input: current constitution, recent shipped pilots, parked ideas, and any new lane observations
- Output: 10 short premises, each written as a one-line show premise + target + cast hint
- Hard filter: no protected groups, no real-brand trade dress, no corny hook language, no motivational fluff

### Stage 1 — premise critic
- Run a MoA critic pass against the constitution
- Keep only ideas that score well on:
  - deadpan over corny
  - monoline / real-asset compatibility
  - loopability
  - target clarity
  - production feasibility
- Survivors: the top 5 ideas only

### Stage 2 — script-card draft
For each survivor, generate a tiny card with:
- title
- target
- beats (≤6)
- cast / asset variant
- voice mode
- loop note
- max length ≤30s

### Stage 3 — corny-detector
- Run the script cards through a second MoA critic pass
- Kill anything that feels like:
  - a “wait for it” setup
  - a fake lesson
  - a motivational turn
  - engagement bait
  - softened edge or over-explaining
- Save only the best 3–5 cards

### Stage 4 — bank for Josh
- Store the accepted cards in a weekly bank file
- Present Josh with a short decision packet:
  - what survived
  - why it survived
  - what asset/cast variant each idea wants
  - what the next production step would be

## Safety / scope gates

- No posting
- No emailing
- No account creation
- No spending
- No public upload
- No service changes
- No secret handling

## Suggested storage shape

- Weekly bank file: `projects/archive/badboys/` or a new internal bank path under `assets/badboys/idea-bank/`
- One weekly summary note with:
  - date
  - kept premises
  - killed premises
  - follow-up production recommendation

## Draft packet shape for Josh

Keep the approval packet tiny:

- **What it is:** weekly premise bank + script-card filter
- **Why it matters:** reduces time spent on weak ideas before they reach Josh
- **What it needs:** approval to implement the cron surface
- **What Josh decides:** ship / kill / tweak cadence

## Open questions for implementation later

- Should the cron live in Hermes cron or a repo-local timer wrapper?
- Should the weekly output file be appended to or one file per week?
- Should the premise critic include a short human-readable reason for each keep/kill?

## Next action

Wait for Josh approval, then implement the weekly cron and start the bank with 10 premises from the current cartoon-lab constitution.