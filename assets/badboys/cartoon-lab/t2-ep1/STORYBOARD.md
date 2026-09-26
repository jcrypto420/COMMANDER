# BAD BOY BANKERS — Ep. 1 "T+2" · Storyboard + Animatic Spec v1

Stage 2 artifact · 2026-07-05 · runs ~18.0s · vertical 1080×1920 · 24fps · loops clean
VO: Sarah stems in `vo/` — line1 = 1.28s, line2 = 1.93s (timings below use actuals)

## Scene

One locked orthographic shot, no cuts. Flat cream background (#FFFFD6). A giant
wall monitor occupies the top third — dark slate rectangle, monoline border,
oversized system text. Two banker Bad Boys stand lower-center facing the
monitor, backs 3/4 to camera so both smirks stay readable in profile-ish
turn (face law: features always fully visible — cheat the heads toward camera).
BANKER A (left, taller placement) holds a tiny coffee cup. BANKER B (right).

Screen text style: monospace, pale green on slate, terminal-flavored.

## Panels

| # | Time | Action | Audio | Screen |
|---|------|--------|-------|--------|
| 1 | 0.0–2.5 | Hold. Both bankers perfectly still, staring up at monitor. Idle-loop micro-bob only (2% amplitude). | Room tone (low office hum, barely audible) | `WIRE STATUS: PENDING` + blinking cursor |
| 2 | 2.5–3.8 | Nothing changes. | **VO line 1** (2.5–3.78): "Your funds are moving." | unchanged |
| 3 | 3.8–7.5 | Dead hold. BANKER B blinks once at 5.5 (single blink, slow: 6 frames). | Silence (hum only) | cursor keeps blinking |
| 4 | 7.5–9.5 | BANKER A raises the tiny cup, one sip: 12-frame raise, hold at lips 18 frames, 12-frame lower. Head tilt ≤4°. | Coffee sip SFX at 8.0 (`sfx/coffee-sip.mp3`) | unchanged |
| 5 | 9.5–11.5 | Return to exact hold. | **VO line 2** (9.6–11.53): "Your funds have always been moving." | unchanged |
| 6 | 11.5–13.5 | Screen "refreshes": text wipes for 6 frames, re-renders. | Soft terminal beep (optional, ≤ -18db) | wipes → `WIRE STATUS: PENDING` (identical) |
| 7 | 13.5–16.0 | Both smirks widen 15% via shape key over 24 frames — the ONLY facial acting in the short. Hold. | Hum only | cursor blinks |
| 8 | 16.0–18.0 | Caption fades in bottom-center at 16.2, holds. Frame at 18.0 is IDENTICAL to frame 1 (caption excepted) → loop. | Hum fades to loop point | `T+2.` caption, lowercase, cream-on-nothing |

## Caption

`T+2.` — bottom center, safe-zone clear of TikTok UI (bottom 320px and right
140px kept empty). Font: heavy monoline sans, small. Nothing else on screen ever.

## Comedy physics (why each hold is that long)

The joke is institutional stillness. Every beat that feels one second too long
is one second right. Do not add motion to "help" a hold. The screen refresh
that changes nothing (panel 6) is the thesis of the entire series.

## Blender notes (Stage 4, when reworked banker lands)

- Two instances of the banker costume collection; BANKER A scaled 1.03 for
  depth cheat. Rig actions needed: idle micro-bob (loop), single blink (B),
  cup raise/sip/lower (A — requires a cup prop bone), smirk-widen shape key.
- Monitor is a flat plane + text objects; cursor blink = 12-frame visibility
  cycle; refresh wipe = 6-frame scale-Y collapse/restore of the text block.
- Camera: ortho, static, portrait. Render EEVEE, cream world, no lights
  (emission shading per constitution §2).

## Audio mix map

| Track | Content | Level |
|---|---|---|
| A1 | Sarah VO (line1 @2.5, line2 @9.6) | full, -3db |
| A2 | office hum loop 0–18s | -30db, fade at loop seam |
| A3 | coffee sip @8.0 | -12db |
| A4 | terminal beep @11.5 (optional — cut if it reads cute) | -18db |

## Gate 2 checklist (what Josh judges on the final cut)

1. Does the stillness read as deadpan or as broken video? (Former = ship)
2. Smirk-widen at 13.5 — earned or corny?
3. Loop seam invisible?
4. Banker costume on-model per the reworked rig.
