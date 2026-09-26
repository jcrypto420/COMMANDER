---
name: commander-critic-passes
description: "Use when a cartoon-lab script/premise or a Boring Report issue needs a second opinion before Josh's gate. Runs a structured /moa critique against the relevant rubric, applies a pass/fail threshold, and logs the verdict."
version: 1.0.0
author: Commander
license: private
metadata:
  hermes:
    tags: [commander, moa, critic, cartoon-lab, boring-report, quality-gate]
    related_skills: [commander-command-center-ops, commander-goals-alignment]
---

# Commander Critic Passes

Every artifact that reaches Josh's Gate Deck has already survived one automated
critique. This skill is that critique. It exists because self-review by the
same model that wrote the draft catches almost nothing — a second pass, even
from the same underlying model at a different sampling temperature, catches
real defects (see: the W28 USYC misclassification, the corny v1/v2 TikTok
scripts). MoA is configured and active at $0 cost (`hermes moa list` to confirm).

## When to use

- A cartoon-lab premise or script card is about to be banked for Josh's Gate 1
  (`projects/badboys-cartoon-lab.md`).
- A Boring Report issue is about to be marked ready for Josh's Gate Deck
  (`products/boring-report/`).
- Any other artifact where the constitution/methodology it must obey lives in
  a specific repo file and a fresh pair of eyes should check compliance before
  a human wastes a gate-read on something that fails an obvious rule.
- **Don't use for:** routine draft-lane work with no constitution to check
  against, or anything already past a Josh gate (his verdict outranks this).

## Procedure

1. **Identify the rubric.** Do not invent one. Pull the actual constitution:
   - Cartoon lab → `projects/badboys-cartoon-lab.md` §"THE ART CONSTITUTION"
     (face law, monoline purity, deadpan-over-corny, edge law, trademark law).
   - Boring Report → the PRD §3 constraints + §5 methodology + §7 QA
     (`projects/boring-report-prd.md`), plus whatever's already logged in
     `products/boring-report/CORRECTIONS.md` so a fixed defect never recurs.
2. **Invoke `/moa` with a self-contained prompt.** Include the rubric items
   verbatim and the artifact text/data being judged — the aggregator has no
   memory of this conversation. Ask for a 1-10 score per rubric item plus one
   concrete failure/pass reason each. Example shape:
   ```
   /moa Score this against these rules, 1-10 each, one line why:
   1. Deadpan, not corny — no winking at camera, no hook-bait.
   2. Edge aims at institutions/behaviors, never protected groups.
   3. [artifact-specific rubric item]
   Artifact: <paste the script card / report section>
   ```
3. **Apply the threshold.** ≥7/10 on every item survives to Josh's gate.
   Below 7 on ANY item: revise and re-run this skill, or kill the artifact —
   never bank a sub-7 item hoping Josh won't notice; that wastes his 60 seconds.
4. **Log the verdict**, win or lose, in the artifact's home file:
   - Cartoon lab: append under the relevant pilot card in
     `projects/badboys-cartoon-lab.md`.
   - Boring Report: append to `products/boring-report/CORRECTIONS.md` under
     that week's dated section — this file is the flawless-streak counter,
     so a caught-and-fixed defect here does NOT count against the streak;
     only a defect Josh catches after the gate does.
5. **Completion criterion:** every rubric item has a logged score AND either
   (a) the artifact is banked for Josh's gate with all scores ≥7, or (b) the
   artifact is revised/killed with the specific failing item named. "I ran
   /moa" without a logged score against a named rubric item is not done.

## Cost discipline

The active MoA preset is two `gpt-5.4-mini` reference passes plus a
`gpt-5.4-mini` aggregator — genuinely free on Codex OAuth. Do not switch the
preset to a paid provider/model without Josh's explicit approval; the whole
point of this skill is a free safety net, not a quota risk. If judgment
quality on a specific rubric feels weak, say so in the verdict log rather than
silently escalating models.
