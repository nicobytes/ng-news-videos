# Captions — safe zone & no-overlap rule

Workspace-wide, brand-agnostic. Applies to **every** video project under `videos/<slug>/`, regardless of which `shared/brand/*` (or no brand) that project uses — this is a technical/layout law, not an aesthetic choice. Written after the same overlap bug recurred across projects; see `videos/cloudflare-latency-motion-en/` for the worked example this doc was extracted from.

## The rule

1. **Captions always live in the same safe zone, every scene, every card, every frame of the video.** Never move the caption position per-scene to "make it fit" — that's the bug, not the fix.
2. **No animation, card, label, or on-screen graphic may ever extend into that zone.** If a scene's content would reach it, the content is what moves or shrinks — not the caption.
3. Corollary: when you build ANY new scene/card for a video that carries captions, treat the caption safe zone as a hard **content ceiling** and design the scene to stay above it from the start, instead of discovering the overlap after the fact.

## The safe zone (1080×1920 reference, 9:16)

Derived from Instagram Reels' own reserved UI (profile/follow chip at top; username, caption duplicate, audio track, and the right-side like/comment/share icon column at bottom):

| Edge | Reserved | Why |
| --- | --- | --- |
| Bottom | **340px** | Reels' own username/caption/music bar + engagement icons live under here. Caption pill's bottom edge sits at `bottom: 340px` from the frame, never lower. |
| Left / right | **110px** each | Clears the right-side action-icon column and gives symmetric margin. |
| Top | ~250px | Profile/follow chip. Rarely a caption concern (captions sit low), but scene titles/kickers should also start below this. |

**Content ceiling:** every scene/card's own content (stat cards, logo grids, diagrams, end-card copy) must end by **y ≈ 1460** at the latest, leaving ~460px of clear air above the caption zone. This is *not* the same number as the caption's own top edge — it's a buffer so the two never touch even with 2-line captions.

If a scene's content naturally wants to run past y=1460 (a tall diagram, a 4-item grid, an end-card with bars): shrink it, move its `top` up, or drop a redundant trailing line (a "foot" caption line duplicating what the VO already says is the easiest thing to cut — the spoken captions already carry that text, so a matching on-screen footnote is often pure redundancy, not lost information).

## The two bugs that caused this, twice

Both found and fixed in `videos/cloudflare-latency-motion-en/`. Watch for them in every new project:

1. **An `!important` shorthand silently beats a later non-important longhand.** `inset: auto !important;` followed by `bottom: 340px;` (no `!important`) does **not** apply the bottom value — the shorthand's implicit `bottom: auto !important` already won. Every longhand (`top`, `left`, `right`, `bottom`, `width`, `height`) needs its **own** `!important` when overriding the shared `.clip` class's `inset: 0`. This is why an earlier version of the caption CSS in this project rendered pinned to the top instead of the Reels-safe bottom.
2. **A `data-composition-src` sub-composition is never auto-hidden by the host outside its own `data-start`/`data-duration` window** — only plain `<video>`/`<audio>` and plain non-composition-src `<div class="clip">` clips get that automatic show/hide. If a caption or overlay is mounted as a composition-src sub-comp with a window shorter than the full video, it must self-blank (listen for the global `hf-seek` event, compare against its own start/duration, toggle its own opacity) — see `card-clouds.html` etc. in the same project for the pattern. Easiest fix: make the caption sub-composition span the **entire video** (`data-start="0"`, `data-duration="<full length>"`) and manage per-phrase visibility internally with its own GSAP timeline, the way `videos/cloudflare-latency-motion-en/compositions/captions.html` does — then this bug never applies to it at all.

## Default caption visual style — karaoke word-highlight

Unless a project's brief calls for something else, this is the default caption treatment (proven across `videos/gem_latest/` and `videos/cloudflare-latency-motion-en/`):

- One dark pill per phrase (`background: #18181b`, `border-radius: 20px`, drop shadow), whole phrase visible at once — not a one-word-reveal.
- Words inside the pill sweep color as they're spoken: **`#a1a1aa`** (upcoming, gray) → **`#06b6d4`** (active, cyan, with a `scale: 1.05` pop) → **`#fafafa`** (already spoken, near-white).
- Font: `Inter` weight 700–800 (use whichever weight the project's font files actually ship — `cloudflare-latency-motion-en` only has 800, not 700, and substituted it), auto-shrunk per phrase via a canvas `measureText` fit-to-width loop so long lines don't overflow the pill.
- `power2.out` easing on both the entrance pop and the per-word color/scale transitions; a quick `power2.in` fade-out between phrases sized to the natural SRT gap.
- Reference implementations: `videos/cloudflare-latency-motion-en/compositions/captions.html` (clean, parametrized by a `CUES` array of `{start, end, text}` — start here for a new project) and `videos/gem_latest/compositions/caption-gradient-fill.html` (word-level timing instead of phrase-level, gradient-clip text instead of solid color).

## Building captions for a new project — checklist

1. Get word or phrase-level timing (SRT, or a word-level transcript) and build a `CUES` array of `{start, end, text}`.
2. Merge/clean the raw ASR output: fix obvious mis-transcriptions (brand/tech names especially), fold stray sub-1-second fragments into a neighbor, cap phrases at a readable word count (~12 words).
3. Build ONE sub-composition spanning the full video (`data-start="0"`, `data-duration="<video length>"`) using the karaoke pattern above — don't emit one `<div>` per phrase on the master timeline; that's harder to keep positioned consistently and doesn't self-manage visibility.
4. Position it with the safe-zone numbers above, every `top`/`left`/`right`/`bottom`/`width`/`height` longhand carrying its own `!important` if it's overriding `.clip`.
5. **Before wiring in any other scene/card**, check its content against the y≈1460 ceiling. Fix the ceiling violation in the scene, not by moving the caption.
6. Verify with `npx hyperframes snapshot --at <a timestamp per scene/card>` and actually look at the frame — the gap between content and caption should be visually obvious, not just numerically non-negative.
