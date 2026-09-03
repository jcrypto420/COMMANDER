# Bad Boys / Joycat — Hermes idea-bank + MoA critics cron draft

## Status — 2026-07-09
- **State:** DRAFT ONLY — internal design packet for BB-26; no cron enabled, no outbound actions, no public posting
- **Purpose:** turn the existing Bad Boys constitution + pipeline into a cheap weekly idea-bank loop that pre-filters premises before Josh ever sees them
- **Source of truth:** `projects/badboys-cartoon-lab.md` is authoritative for style/constitution; this packet only packages the cron draft
- **Draft progress 2026-07-09:** added a concrete 10-premise seed set and a cheap implementation shape so the packet is closer to decision-ready
- **Draft progress 2026-07-10:** added a concrete weekly bank file shape and output schema so the packet now tells Josh exactly what the cron would write, where it would live, and what a weekly review would contain
- **Draft progress 2026-07-11:** added a first-run prompt skeleton and weekly review checklist so the cron proposal is now closer to a copy/paste implementation packet, not just a concept note
- **Draft progress 2026-07-12:** added a one-glance approval packet and explicit local-only storage path so Josh can make a ship/kill/tweak call without reading the full draft
- **Draft progress 2026-07-14:** added an explicit one-run smoke test shape: local-only runner, fallback model order, and exact weekly file checks so the packet can be exercised once before any schedule discussion
- **Draft progress 2026-07-14:** created a copy/paste weekly bank template at `assets/badboys/idea-bank/weekly-template.md` so the packet now has a concrete local-only output shape, not just a proposal
- **Draft progress 2026-07-24:** added a concrete local-only smoke-test checklist that ties the packet to the weekly template, fallback model order, and a simple file-shape verification pass before any cron talk
- **Next step:** if Josh approves, turn this into a real Hermes cron job and a stored weekly premise bank

## Recommendation

Use **one weekly Hermes cron** that does three things in sequence:

1. Generate **10 fresh premises** from the current Bad Boys constitution and active lane context.
2. Run a **MoA premise-critic** pass and keep only the strongest ideas.
3. Convert the survivors into **3–5 script-card drafts** and run the **MoA corny-detector** before banking them for Josh.

This keeps Josh out of the weeds, keeps the model spend cheap, and preserves the existing two-gate structure.

## Cheap implementation shape

- Read the current constitution plus the last weekly bank note.
- Generate exactly 10 short premises into one local weekly file.
- Score each premise against the constitution with a cheap MoA critic pass.
- Keep the top 5 only, with one-line keep/kill reasons.
- Convert only the survivors into script cards.
- Run a second corny-detector pass on those cards.
- Save 3–5 survivors and a one-paragraph summary for Josh.
- Keep everything local-only until Josh explicitly approves a public action.

## Seed premise bank v0

These are not final scripts — they are the first cheap prompt set for the weekly cron.

1. **wire status pending** — two banker Bad Boys stand in front of a giant monitor that never changes from `PENDING`; target: institutional finance bureaucracy; cast hint: pinstripe banker duo; loop note: coffee sip becomes the beat.
2. **content.** — a plain-face mascot holds a sign that says `content`; target: algorithm culture; cast hint: plain face, flat bg; loop note: end frame matches start frame.
3. **risk management.** — a cowboy-hat Bad Boy keeps adding hats while a chart falls off the wall; target: trader brain / fake prudence; cast hint: cowboy; loop note: silent escalation.
4. **day 1.** — a mascot lies on the floor while a narrator lists fake grind steps that do nothing; target: hustle culture; cast hint: plain face; loop note: opening line and closing line can mirror.
5. **compliance theater.** — a chef variant stamps empty forms at a blank desk; target: corporate absurdity; cast hint: chef; loop note: repeated stamp sound.
6. **quarterly alignment.** — five identical chairs sit in a meeting room with nobody in them; target: meeting culture / management jargon; cast hint: office variant; loop note: the slide deck pointer never moves.
7. **benchmark.** — a runner keeps jogging in place beside a printed chart that is already falling apart; target: performance theater; cast hint: athlete-ish or plain face; loop note: treadmill sound.
8. **growth.** — a sprout costume keeps getting watered with an empty cup; target: growth-at-all-costs rhetoric; cast hint: sprout; loop note: water never appears.
9. **synergy.** — two identical objects are pushed closer together until they still do nothing; target: collaboration buzzwords; cast hint: duo asset; loop note: one tiny push per beat.
10. **governance.** — a tiny voting booth sits under a giant corporate logo-shaped shadow that never resolves; target: institutional process; cast hint: plain face or banker; loop note: ballot box clicks once, then silence.

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

### Concrete weekly file shape v1

- Suggested file name: `assets/badboys/idea-bank/weekly/YYYY-WW.md`
- Suggested sections:
  - `## Inputs`
  - `## 10 premises generated`
  - `## Keep/kill critic notes`
  - `## Top 5 survivors`
  - `## 3-5 script-card drafts`
  - `## Corny-detector notes`
  - `## Josh review summary`
- Suggested row fields for each premise:
  - premise
  - target
  - cast hint
  - critic score
  - keep/kill reason

### Weekly review packet v1

- 1 paragraph on why the week’s survivors were chosen
- a short list of the 3–5 best cards
- one line each on which asset variant each card wants next
- one explicit next production step for Josh if he wants to greenlight a short

## Draft packet shape for Josh

Keep the approval packet tiny:

- **What it is:** weekly premise bank + script-card filter
- **Why it matters:** reduces time spent on weak ideas before they reach Josh
- **What it needs:** approval to implement the cron surface
- **What Josh decides:** ship / kill / tweak cadence

### First-run prompt skeleton

Use this exact shape for the first weekly run once approved:

1. Load `projects/badboys-cartoon-lab.md` and the last weekly bank note.
2. Generate 10 short premises that obey the constitution and current lane context.
3. Run the MoA premise-critic and write keep/kill reasons in the weekly file.
4. Promote the top 5 to script-card drafts only if they pass the critic threshold.
5. Run the corny-detector on those cards and save the best 3–5.
6. Write one short Josh summary with the survivors and the next production step.

### Approval packet v2 — one-glance decision surface

If Josh wants the shortest possible verdict path, present the cron this way:

- **What it is:** a weekly Bad Boys premise-bank cron with two MoA filters
- **What it writes:** one weekly file at `assets/badboys/idea-bank/weekly/YYYY-WW.md` plus a short Josh summary
- **What it does not do:** posting, emailing, account creation, spending, public upload, or service changes
- **What Josh decides:** ship / kill / tweak cadence and storage path

This is the decision surface for approval, not the implementation itself.

### Draft v3 — one-run smoke test shape

If Josh wants a single safe preflight before any cron talk, run the proposal as a one-off local draft pass:

1. Read `projects/badboys-cartoon-lab.md` and the current BB-26 draft packet.
2. Generate 10 short premises into the weekly bank file path for the current ISO week.
3. If the default codex model is unavailable, fall back to the cheapest hosted draft model in the router; keep the run local-only either way.
4. Write keep/kill reasons for all 10 premises, then promote only the top 5.
5. Draft 3–5 script cards from the survivors and save a one-paragraph Josh summary.
6. Verify the file contains the required sections before calling the draft pass complete.

Smoke-test acceptance criteria:

- one weekly file written locally only
- 10 premises captured
- 5 or fewer survivors after critic pass
- 3–5 script-card drafts at the end
- no posting, sending, spending, or service changes

### Local-only smoke-test checklist v1

Use this as the exact preflight before any cron scheduling discussion:

1. Copy `assets/badboys/idea-bank/weekly-template.md` to the current ISO-week path under `assets/badboys/idea-bank/weekly/YYYY-WW.md`.
2. Fill `## Inputs` with the current date, ISO week, and lane context from `projects/badboys-cartoon-lab.md`.
3. Load the current constitution packet plus the weekly template, then draft 10 premises using the cheapest available local/default model first.
4. If `gpt-5.4-mini` via openai-codex is unavailable, fall back to `google/gemini-2.5-flash` via OpenRouter; keep the run local-only either way.
5. Verify the weekly file contains all required sections, 10 premise rows, and 3–5 survivor cards.
6. Stop and log the packet as draft-only if any step would require posting, sending, spending, account creation, or service changes.

### Weekly review checklist

- Did the weekly file include all 10 premises?
- Were keep/kill reasons written in plain English?
- Did the top 5 survivors stay compatible with the constitution?
- Did any card feel corny, winky, or over-explained?
- Is the Josh summary short enough to read in one glance?

## Open questions for implementation later

- Should the cron live in Hermes cron or a repo-local timer wrapper?
- Should the weekly output file be appended to or one file per week?
- Should the premise critic include a short human-readable reason for each keep/kill?

## Next action

Josh reviews the local-only weekly bank draft at `assets/badboys/idea-bank/weekly/2026-W30.md` and gives ship/kill/tweak on cadence + storage path.
