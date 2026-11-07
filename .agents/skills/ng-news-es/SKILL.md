---
name: ng-news-es
description: Create the Spanish edition of an NG News episode from the two local high-quality files in videos/<slug>/assets (ng-news-<slug>-en.mp4 and ng-news-<slug>-es.mp4). Keeps the EN frame, right panel and screen recordings, swaps the host for the Spanish recording, replaces the captions with animated Spanish ones, runs the mandatory self-critique loop and renders the 4K MP4 for @ng-news-es, then generates its YouTube metadata. Use for "Crea la versión en español de 26-17" or /ng-news-es <slug>.
---

# /ng-news-es

> /ng-news-es Crea el episodio 26-17

Read first: `references/rules.md` (what changes and what never changes), `references/learnings.md` (what already failed), `shared/brand/FRAME.md` (geometry), workspace `CLAUDE.md`.

## Inputs

- `videos/<slug>/assets/ng-news-<slug>-en.mp4`: English episode, original quality.
- `videos/<slug>/assets/ng-news-<slug>-es.mp4`: Spanish host recording of `guion.md` (`/ng-news-guion`), may contain retakes and pauses.
- If the user gives other paths, pass them to `pnpm new-ng`. A YouTube URL is a last resort: it can lose quality.

## Pipeline

Run from the workspace root, `S=videos/<slug>`. Every step writes to `$S/data/`. No API key: you read the images and match meaning, the scripts do everything deterministic.

1. **Scaffold**: `pnpm new-ng <slug>` (add `--en <file> --es <file>` if they are not in `assets/` yet). Already done if `/ng-news-guion` ran.
2. **Prepare sources**: `scripts/ng/fetch.sh $S` → `assets/en/hq.mp4` (4K30 H.264 base layer), `assets/en/proxy.mp4` (1080p, analysis only).
3. **Transcribe**: `scripts/ng/transcribe.sh $S` → `data/transcript.{en,es}.json` (faster-whisper on the GPU, ~35 s per file, then `fix_terms.py`).
4. **Segment EN**: `uv run python scripts/ng/segment_en.py $S` → `data/blocks.json` + `data/review/segment_sheet.png`. **Look at the sheet**: each mid-frame must match its `presenter`/`screen` label. Fix `blocks.json` if wrong.
5. **Align**: `uv run python scripts/ng/align.py prepare $S`, read `data/alignment.todo.md`, write `data/alignment.json` by meaning (`{"blocks":[{"block":0,"es":[[a,b]]}]}`, inclusive ES sentence ids, monotonic, retakes left out). Then `align.py build $S` → `data/cutlist.json`. Confirm the dropped sentences are retakes or noise. `prepare` also cuts the interviews of `data/interviews.json` out of `blocks.json` (block ids change): they take no ES ranges.
6. **Proofread captions**: read the whole ES transcript against `alignment.todo.md`. For every proper name, read the EN burned-in caption: `ffmpeg -ss <t> -i assets/en/proxy.mp4 -frames:v 1 -vf crop=1560:300:90:700 name.png`. Write the fixes to `data/caption_fixes.json` (`[{"from":"Serge Chassanov","to":"Devin Chasanoff"}]`, exact word sequences). Add errors that will repeat to `glossary.json > asr_fixes`.
7. **CHECKPOINT**: print block / kind / EN time / ES text. Ask the user only about doubtful matches. Otherwise continue.
8. **Compose**: `node scripts/ng/compose.mjs $S` → `index.html`, `assets/es/presenter.mp4` (crop, tune `es_crop` in `data/episode.json`), `assets/es/voice.wav` (-16 LUFS), `data/timeline.json`. Use `--limit 30` for a short test.
9. **Check**: `cd $S && pnpm run check` — 0 errors. Style warnings are expected (see learnings).
10. **Critique loop** (below) — mandatory.
11. **Render**: `cd $S && HYPERFRAMES_EXTRACT_CACHE_DIR=$HOME/.cache/hf-extract pnpm exec hyperframes render -q delivery --resolution 4k -o renders/ng-news-<slug>-es.mp4` (~15 min per 5 min of video). Then run `scripts/ng/review.sh $S $S/renders/ng-news-<slug>-es.mp4` on the final file.
12. **YouTube metadata**: run `/ng-news-youtube <slug>` → `youtube.md` (3 titles, description, chapters, tags, links). Always the last step: it needs the timestamps of the final video.

## Critique loop (before the final render)

1. `scripts/ng/review.sh $S` renders a 1080p draft and builds the material in `renders/review/`. Confirm it is newer than `index.html` before looking at it.
2. **Automatic gates**, all must pass:
   - `checks.json`: duration equals expected (± 0.1 s), 0 black segments, `lufs` between -17 and -15.
   - `sync.json`: median offset ≤ 80 ms, ≥ 90 % of caption words heard.
   - Interviews: transcribe `assets/en/interview-N.wav` with `transcribe.py` and compare with `en` in `interviews.json`. It must contain only the guest: no words of the host at either end.
3. **Read every image**: `contact.png`, `phone.png`, `clips.png`, `captions.png` and every `strips/cut-NN.png`. Look for:
   - English caption remains or anything leaking around `#capbar`
   - a wrong shot flashing at a cut, EN host visible
   - right panel out of step with the block
   - caption overflow, 3 lines, words ending a line on "de", wrong names
   - host face badly cropped
4. **Score 1–10** with evidence for each: hook (first 2 s), mobile legibility (360 px), caption craft, motion, cut quality, EN-format fidelity, audio/caption sync (from `sync.json`), loudness. A score with no evidence does not count.
5. Fix the 3 worst problems (data JSON or `compose.mjs`), recompose, check, review again. Repeat until all are ≥ 8, max 5 iterations; if something stays below 8, report it instead of rendering silently.
6. Save the table in `renders/review/scorecard.md`. Only then render the final.
