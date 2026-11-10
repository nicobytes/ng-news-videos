# NG News ES — rules

Why these exist and what was tried: `learnings.md`.

## What changes vs the EN episode

| Element | ES version |
|---|---|
| Frame, NEWS logo | EN original pixels |
| Right panel (title + bullets) | **EN original pixels, stays in English. Never translate it.** |
| Left panel, `screen` block | EN original pixels (screen recording, web, image, guest webcam) |
| Left panel, `presenter` block | ES host, 16:9 face crop |
| Caption bar | EN captions hidden by `#capbar`, ES captions on top |
| Audio | ES narration, -16 LUFS. Interviews keep their original audio, also at -16 LUFS |

## Left panel

- `presenter` = the EN host's webcam. `screen` = everything else. A guest's webcam is `screen`: it stays.
- An interview is someone other than the host speaking. The host never reads it: it is not in `guion.md`, and it keeps the EN picture and audio with Spanish captions (`data/interviews.json`).
- First shot of a new section is never zoomed.

## Captions (bottom bar)

Follows the rail contract of `/embedded-captions` (`references/rail.md`). The matte pipeline does not apply: the bar has no person behind it.

- Source: `transcript.es.json` + `data/caption_fixes.json`.
- One phrase on screen, at most 2 balanced lines, cut at clause boundaries, never ending on "de", "la"...
- Word fill: each word goes dim to white as spoken, with a magenta edge and a small lift (technique of `shared/blocks/caption-gradient-fill.html`).
- Interview captions look the same: same font and word fill, spread over each line because a translation has no word timing.
- Emphasis: numbers and glossary terms (except Angular) stay pink.
- Font: Montserrat 700, 48 px, the same face as the titles and bullets of the EN right panel (user rule since 26-18: titles and captions share one typography). Do not change it per episode; `caption_font` in `data/episode.json` (files in `templates/ng-news/fonts/`) exists only for an explicit user request.

## Text

- The ES hosts are Ricardo Chavarría and Nicolás Molina: it varies per episode, see `host` in `data/episode.json`.
- Proper names: the EN burned-in caption wins over any transcript. Crop it at the moment of the name.
- Captions are verbatim except for ASR errors and stutters. Do not rewrite what the host said.
- Terms in `glossary.json > keep_english` stay in English with that exact casing.

## Timing

- ES audio drives the timeline; silences over 0.6 s between sentences are cut.
- Block boundaries snap to the ES sentence that introduces the new content.

## Alignment

- Match by meaning, monotonic. Retakes and false starts are simply left out of `alignment.json`.
- Confirm with the user only what is really doubtful: a block whose ES text does not cover the EN meaning.
