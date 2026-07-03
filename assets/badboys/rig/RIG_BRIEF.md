# BADBOY PUPPET v1 — Blender Rig Brief (for the Claude Desktop + Blender MCP session)

Mission: build `BADBOY_PUPPET_v1.blend` in THIS folder — the reusable 2D-style
puppet for all Cartoon Lab shorts, plus the first costume: PINSTRIPE BANKER.

## Source of truth (Constitution §1 — the face is law)
- Canonical mark: `../INSIDEFACE NOBG.png` (trace THIS; `../FACE.jpg` = reference)
- EXACT features: thick DOUBLE outline; two solid dot eyes — viewer-LEFT smaller
  and lower; ONE bold tapered wedge brow per eye — right larger; wide smirk
  sweeping UP, hooking right. Never redraw from imagination. Never AI-generate.

## Build approach
1. Import canonical PNG as reference image; trace with Grease Pencil (or bezier
   curves → flat mesh). Flat emission shading only — no lights, no gradients,
   no depth. Monoline weight matched to source.
2. Keep proportions EXACT — verify by overlay toggle against the reference.

## Rig (minimal, cartoon-sufficient)
- Shape keys / bones for: brow raise + anger tilt, blink (eye scale-Y), smirk
  widen, subtle head bob, whole-body x/y bounce + squash-stretch (10% max).
- Costume system: separate collection per costume, swappable. Build TWO:
  (a) plain face (naked canonical), (b) PINSTRIPE BANKER — old-school double-
  breasted monoline suit, pinstripes as thin line texture, tiny tie. Suit follows
  body bounce. Same line weight as face.

## Camera / render
- Orthographic camera, portrait 1080×1920, EEVEE, 24 fps.
- Background: flat cream (#FFFFD6) or transparent — nothing else.

## Deliverables (save into this folder)
1. `BADBOY_PUPPET_v1.blend`
2. `tests/still_plain.png` + `tests/still_banker.png` (on-model check stills)
3. `tests/idle_loop.mp4` — 2s loop: blink + subtle bob, banker variant
Then commit/push via the COMMANDER repo (Claude Code session handles it if needed).

## On-model check (critic gate before anything ships)
Overlay test still vs `../INSIDEFACE NOBG.png`: outline doubled? eye asymmetry
correct (left smaller/lower)? brow wedges (right larger)? smirk hooks right-up?
Any NO = fix before rigging continues.
