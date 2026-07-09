# BAD BOYS CARTOON LAB — Studio Pipeline v1 (2026-07-03)

## Status — 2026-07-06
- **State:** ACTIVE — Josh greenlit crude/edgy cartoon shorts as the Bad Boys engine
- **Last advanced:** 2026-07-06 — Stage 4 (animation) + Stage 5 (cut/export) DONE for T+2 Ep.1. Final rendered+muxed short at `assets/badboys/cartoon-lab/t2-ep1/t2ep1_master.mp4` (18.0s, 1080x1920, VO+SFX muxed, caption burned in).
- **GATE 1 PASSED 2026-07-03 (evening):** Josh SHIPPED all four pilots via widget verdict. Production order: P4 "T+2" first, then P2 → P1 → P3.
- **Next action:** AWAITING JOSH GATE 2 on T+2 Ep.1 — ship/kill call on `t2ep1_master.mp4`. Several creative calls made where the storyboard was ambiguous (see BB-25 task note / Claude's Gate 2 message) — flagged, not silently improvised.
- **Waiting on:** Josh's Gate 2 verdict; BB-23 account creation (publishing cork, unblocked only after ship)
- **Stage 3 (T+2): VO COMPLETE** — Sarah stems at `assets/badboys/cartoon-lab/t2-ep1/vo/` (line1 + line2); SFX (coffee sip) at animatic timing
- **Stage 4 asset: banker costume/body REJECTED by Josh 2026-07-05** — reworked and approved 2026-07-06
- **Stage 4 (animation) + Stage 5 (cut/export): COMPLETE 2026-07-06** — banker costume rig puppeted via headless Blender scripts in `assets/badboys/cartoon-lab/t2-ep1/` (build_scene.py, animate_scene.py, render_silent.py, mux_audio.py, add_caption_and_export.py). Office-hum bed + optional terminal beep from the audio mix map were SKIPPED (no assets exist; generating them costs ElevenLabs credits, needs approval first) — VO + coffee sip sfx are muxed in. NOTE 2026-07-07: Josh rejected the animation quality at Gate 2 ("done trying to animate" in Blender) — motion-pipeline decision pending (see mirror/roadmap.md, local); stills remain approved.
- **BB-26 draft packet staged 2026-07-08** — weekly Hermes idea-bank + MoA critics cron draft written to `projects/badboys-idea-bank-cron-draft.md`; waiting on Josh approval before any cron implementation

Calibration (Josh, 2026-07-03): evergreen pipeline first (World Cup concept PARKED —
undeveloped, window closes Jul 19; revisit only if the pipeline is live before then).
Voice mode decided PER SHORT. Platforms: TikTok + YouTube Shorts to start. Budget
ceiling: ~$25/mo (voice/SFX/music credits; AI video assists deferred until signal).

---

## THE ART CONSTITUTION (strict — every critic enforces this)

1. **The face is law.** The canonical mark (`assets/badboys/FACE.jpg` /
   `INSIDEFACE NOBG.png`) is the source of truth: thick DOUBLE outline, two solid
   dot eyes (viewer-LEFT smaller & lower), ONE bold tapered wedge brow per eye
   (right larger), wide smirk sweeping UP hooking right. The character is ALWAYS
   rendered from canonical vectors — **never AI-generated. No exceptions.**
2. **Monoline minimalism.** Clean lines, flat colors. AI may assist motion,
   backgrounds, interstitials — only where it doesn't read as AI slop. In doubt:
   flat color background. The restraint IS the style.
3. **Real assets first** (refocus doc law): the costume variants (chef, DJ, cowboy,
   astronaut, sprout…) are the CAST. Squeeze them before inventing new characters.
4. **Deadpan > shock. Cold > corny.** No winking at camera, no "wait for it," no
   engagement-bait hooks, no fake slogans, no "AI-making-marketing" energy.
   Captions minimal lowercase (`testing this.` energy). Let the object carry it.
5. **Edge law (non-negotiable):** targets are hype media, crypto grift, hustle
   culture, algorithm brain, corporate absurdity — institutions and behaviors,
   NEVER protected groups, never individuals' appearance/identity. Crude ≠ cruel.
6. **Trademark law:** no real trade-dress parodies (the badbraums lesson). Fictional
   brands only. FIFA/league marks = risk zone.
7. **Voice mode per short** (silent / narrator / voiced) — script proposes it,
   corny-critic checks consistency. Early bias: silent or single deadpan narrator.
   **CAST (Josh, 2026-07-03): the narrator is "Sarah" (ElevenLabs premade,
   corporate-reassuring register) — settings: stability 0.95, style 0, speed
   0.93. She is the cartoon-lab default voice unless a script argues otherwise.**
8. **Format:** vertical 1080×1920, 8–30s, loop-ability preferred (last frame feeds
   first). Series > one-offs: recurring segments build a show, not clips.

## THE PIPELINE (stage → owner → critic → gate)

| # | Stage | Owner | Critic | Output |
|---|-------|-------|--------|--------|
| 0 | Idea bank (10 premises/wk) | Hermes weekly cron | **MoA premise-critic** (multi-model ensemble scores vs constitution; ≥7/10 survives) | 5 premises |
| 1 | Script cards (beats ≤6, VO/captions, cast, voice mode, ≤30s) | Hermes (cheap model, artifact-lab voice) | **MoA corny-detector** (kills try-hard/winking/hook-bait; trained on Josh's v1/v2 rejections) | 3–5 script cards |
| — | **JOSH GATE 1** | Josh, 8–9am window | — | ship / kill / one-liner per card (~60s total) |
| 2 | Storyboard + animatic | Claude (Mac) | on-model check vs Constitution §1–2 (face law, monoline purity) | timed panel sequence |
| 3 | Voice + audio | Claude via ElevenLabs (VO if narrator/voiced; SFX; music bed) | deadpan check — flat delivery, zero radio-DJ energy | audio stems |
| 4 | Animation | Claude Desktop + Blender MCP (rigged 2D puppet from canonical vectors) | slop check — no unintentional AI jank | rendered vertical master |
| 5 | Cut / captions / export | Claude (Mac) | platform-fit check (safe zones, loop test, caption timing) | final .mp4 + caption text |
| — | **JOSH GATE 2** | Josh | — | watch once: ship / kill |
| 6 | Publish TikTok + YT Shorts | **Josh** (credentials stay his) | schedule below | posted |
| 7 | Signal loop | Hermes morning loop + Monday review | — | format rankings → idea bank re-aim |

**Josh's total load: two gates + posting. ~5 min/day.** Everything else is agents.

## CADENCE & SCHEDULE

- **Phase 0 (this week):** rig the canonical puppet + take ONE pilot through all 7
  stages to calibrate quality/time. No cadence promises until the pilot ships.
- **Phase 1 (weeks 2–4):** 2 shorts/week. Post TikTok ~7–9pm CT (peak scroll);
  same file to YT Shorts next morning ~8am CT. 3 hashtags max, no spam.
- **Phase 2:** scale to 3–4/wk only on signal (a short >10k views or clear
  format winner). AI-video budget unlocks here, not before.
- Comment seeding pattern: pinned `keep or kill?` — comments are the taste lab.

## GROWTH MECHANICS (tactics, not vibes)

- **Series names make a show:** recurring segments (e.g., "PSA", "day 1", costume-cast
  bits) so viewers subscribe to a bit, not a clip. Winning format → weekly slot.
- Loop-ability farms rewatches (TikTok's strongest ranking signal).
- Reply-to-comment with video on the best comments (cheap episodes, huge favor
  from the algorithm).
- Sticker-pack drop (BB-24 artifact) announced only after a format proves itself —
  content builds the audience; the audience buys the object.
- Cross-platform lag (TT evening → YT morning) doubles surface per render, zero
  extra work.

## BUDGET MAP (~$25/mo ceiling)

ElevenLabs credits (short VO lines + SFX) ≈ $5–15 · music: compose_music sparingly
or CC0 beds ≈ $0–10 · Blender/rig/render: $0 · AI video assists: $0 until Phase 2
signal. Any new subscription = Josh approval per SECURITY.md.

---

## PILOT SCRIPT CARDS — GATE 1 PASSED: all four SHIPPED 2026-07-03; production order P4 → P2 → P1 → P3

### Pilot 1 — "PSA: content" · narrator mode · ~20s · cast: plain face
Beats: (1) Flat color bg. Mascot stands center, holding a small sign: `content`.
(2) Narrator, perfectly flat: "This is content. You are watching it." (3) Slow
zoom. Nothing happens. (4) Narrator: "Do not like it. Do not follow. It changes
nothing." (5) Mascot's smirk holds. Beat. (6) Narrator: "This has been content."
Caption: `content.` — Target: algorithm culture. Loop: end frame = start frame.

### Pilot 2 — "risk management" · silent mode · ~12s · cast: cowboy hat
Beats: (1) Mascot in cowboy hat stares at a wall chart, line going up. SFX: gentle
chime. (2) Line plummets off the chart, through the floor. SFX: none — silence.
(3) Mascot slowly places a SECOND cowboy hat on top of the first. (4) Holds stare.
Caption: `risk management.` — Target: crypto grift/trader brain. Loops clean.

### Pilot 4 — "BAD BOY BANKERS: T+2" · narrator mode · ~18s · cast: NEW pinstripe banker variant (Josh-ordered 2026-07-03)
SERIES PREMISE (Josh): Bad Boys in old-school pinstripe suits — recurring segment,
institutional-finance absurdity from lived settlement-ops experience. Ep 1 "T+2":
Beats: (1) Two banker Bad Boys stand before a giant monitor: `WIRE STATUS: PENDING`.
(2) Narrator, calm corporate: "Your funds are moving." (3) Nothing moves. One banker
sips coffee. (4) Narrator: "Your funds have always been moving." (5) Screen updates:
`PENDING`. (6) Smirks hold. Caption: `T+2.` — Target: institutional finance
bureaucracy. Loops clean. NOTE: banker costume is a new asset — build in the rig
session per Constitution §1 (canonical face, monoline suit, pinstripe line texture).

### Pilot 3 — "day 1" · narrator mode · ~25s · cast: plain face
Beats: (1) Mascot lies perfectly still on the floor, smirking, the entire short.
(2) Narrator, motivational-calm, escalating: "5am: rise. 5:01: grind. 5:02: cold
plunge. 5:03: gratitude. 5:04: dominate. 5:05: optimize the dominance. 5:06:
personal brand." (3) Nothing moves. (4) Narrator: "day one." Caption: `day 1.`
— Target: hustle culture. Loop: "5am: rise."

---

## PARKED

- **World Cup concept** — Josh has an undeveloped angle; tournament ends Jul 19.
  Revive only if the pipeline is shipping before ~Jul 12. Constitution §6 applies
  hard here (FIFA marks).
- Fully-voiced cast, Reels/X accounts, paid AI video — all Phase 2+, signal-gated.
