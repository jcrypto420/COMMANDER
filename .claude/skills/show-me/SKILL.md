---
name: show-me
description: Put an artifact in front of Josh, reliably. Renders/exports the thing under discussion, copies it to exports/review/YYYY-MM-DD/, opens it, and states the full path. Use whenever Josh says "show me", "open it", "I can't see it", or whenever presenting any visual/PDF/audio/video artifact for review.
---

# Show Me

Josh reviewing his own work should cost zero navigation. Same place, every time.

## Steps

1. Identify the artifact under discussion. If ambiguous, pick the most recently
   modified candidate and say which you picked — don't ask.
2. Render/export its CURRENT state (fresh render, not a stale file). Before showing,
   self-check it zoomed-in first — see memory: render-before-showing-josh.
3. `mkdir -p exports/review/$(date +%Y-%m-%d)/` and copy the artifact there,
   named clearly (`what-it-is_vN.ext`), then `open` it.
4. Reply with: the full path, what changed since Josh last saw it, and the one
   question he should judge it on. Nothing else.

## Hard rules

- Never reply with a path alone and no opened file, and never "it should be there."
- If the render fails, say so plainly and show the error — don't present old output.
- Phone-access note: if Josh is away from the Mac, also state the dashboard route
  to the same file, if one exists — never invent one.
