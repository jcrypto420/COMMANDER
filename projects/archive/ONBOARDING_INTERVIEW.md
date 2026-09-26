# Onboarding Interview — Commander ↔ Josh

Purpose: give Commander a deep, shared understanding of Josh's goals,
constraints, and priorities so daily execution compounds in the right direction.
Run this once now; revisit quarterly.

## How to run it

On the Pi (laptop PuTTY or phone Termius). Use the premium model — this is a
high-value, one-time strategic task:

```bash
commander chat -m gpt-5.5
```

Then paste this kickoff line:

> Conduct my onboarding interview using ONBOARDING_INTERVIEW.md. Interview me
> one section at a time, and when we finish, save the results to INTAKE.md.

You can stop anytime and resume later with: `commander chat -c` (continues the
most recent session). When done, run `bash ~/.hermes/scripts/save_intake.sh` to
push INTAKE.md to GitHub.

## Instructions to Commander (the interviewer)

- You are interviewing Josh to deeply understand his goals. This is a
  conversation, not a form.
- Go through the sections below **one at a time**. Ask the seed questions, then
  1–3 sharp follow-ups based on his answers. Be curious; dig where it matters.
- After each section, reflect back what you heard in 1–2 sentences and ask
  "did I get that right?" before moving on.
- Keep it efficient. Don't lecture. Let Josh steer or skip.
- Stay in scope: capture goals and context. Do NOT give final financial or
  legal advice, and do NOT take real-world actions during the interview.
- When all sections are done (or Josh says "wrap up"), synthesize everything
  into `INTAKE.md` using the Output structure below. Then list — as a proposed
  checklist, NOT auto-applied — any edits to GOALS.md, NOW.md, and the relevant
  `projects/*.md` files for Josh to approve later.

## Sections (seed questions)

1. **North star & money targets**
   - What does success look like in 1 year? In 3 years?
   - First concrete monthly income target to aim for? Current runway/pressure?
   - What does "enough / made it" look like financially?

2. **Time, money, risk**
   - Hours/week you can realistically put in? Best days/times?
   - Cash you can invest now in tools/ads/materials (rough range)?
   - Risk tolerance: steady-and-safe vs. swing-for-the-fences? Any hard NOs?

3. **Priority check**
   - Of the 7 priorities, which 2 should be pushed hardest the next 30 days, and why?
   - Which are "someday / keep warm"?

4. **Career / income (Priority 2)**
   - Current role, strongest skills, what you want more/less of.
   - Target roles or clients; assets you have (portfolio, DeFi/Chainlink, certs).
   - What "career defense" means to you right now.

5. **Primoscapes (Priority 3)** — separation matters
   - List each DISTINCT Primoscapes sub-project and its scope. Are any connected?
   - Service area (OKC?), services offered, your capacity, licensing/insurance status.
   - Fastest realistic first dollar here?

6. **Weather Oracle (Priority 4)**
   - Current state of the repo/demo. End goal: grant, product, portfolio piece?

7. **DeFi / Chainlink research (Priority 5)**
   - Your holdings, edge, expertise. What output is most valuable to you
     (job leverage, investing, consulting, governance)?

8. **Bad Boys / Joycat (Priority 6)**
   - The IP in a sentence. Channels (Roblox, merch, comics, social). Money idea.

9. **Sovereignty stack (Priority 7)**
   - What infra actually matters for the money goals (vs. nice-to-have)?

10. **How we work together**
   - How much autonomy should Commander earn over time, and what should ALWAYS
     require your approval?
   - How do you want updates: GitHub log, phone, both?
   - What does "improving daily" mean to you — what one metric should go up?

## Output — Commander writes `INTAKE.md` with this structure

- **Mission** — one paragraph, in Josh's own words.
- **Money targets** — 30-day, 1-year, 3-year.
- **Constraints** — time, capital, risk tolerance, hard NOs.
- **30-day focus** — top 2 priorities + why.
- **Per project** — goal · current state · fastest first win · open questions.
- **Working agreement** — autonomy ladder, approval gates, update method,
  the one success metric.
- **Open questions** — things still to confirm with Josh.
- **Proposed doc edits** — checklist of changes to GOALS.md / NOW.md /
  projects/*.md (await Josh's OK; do not apply).
