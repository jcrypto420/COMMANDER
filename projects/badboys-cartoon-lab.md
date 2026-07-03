# BAD BOYS CARTOON LAB — Studio Pipeline v1 (2026-07-03)

## Status — 2026-07-03
- **State:** ACTIVE — Josh greenlit crude/edgy cartoon shorts as the Bad Boys engine
- **Last advanced:** 2026-07-03 — pipeline spec v1 + 3 pilot script cards banked
- **Next action:** Josh's script-gate verdict on the 3 pilots (8–9am window); Claude starts the Blender rig on the first approved script
- **Waiting on:** script verdicts; BB-23 account creation (still the cork for publishing)

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

## PILOT SCRIPT CARDS — for Josh Gate 1 (verdict: ship / kill / one-liner each)

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
