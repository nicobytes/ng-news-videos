---
name: ng-news-guion
description: Write the Spanish script the host records on camera from the English NG News episode. Needs only videos/<slug>/assets/ng-news-<slug>-en.mp4 and outputs videos/<slug>/guion.md. First step of the workflow, before recording and before /ng-news-es. Use for "/ng-news-guion 26-18", "prepara el guion", "arma el guion del episodio".
---

# /ng-news-guion

> /ng-news-guion 26-18, lo graba Ricardo Chavarría

The first step of an episode: **EN video → `guion.md` → the host records it → `/ng-news-es` → `/ng-news-youtube`.**

## Pipeline

From the workspace root, `S=videos/<slug>`:

1. `pnpm new-ng <slug>`. Only the EN file is needed. Ask who records the episode if the user did not say (the hosts are Ricardo Chavarría and Nicolás Molina) and set `"host"` in `data/episode.json`.
2. `scripts/ng/fetch.sh $S`, then `scripts/ng/transcribe.sh $S`.
3. `uv run python scripts/ng/segment_en.py $S`.
4. `uv run python scripts/ng/guion.py prepare $S` → `data/en_script.md`, `data/review/en_captions.png`, `data/en.info.json`.
5. **Read the whole `en_script.md` and `en_captions.png`.** The burned-in captions are the EN script itself: use them for the exact wording and spelling of names. The transcript gets names wrong.
6. **Decide the interviews** (below) and write `data/interviews.json`, `[]` if there are none.
7. Write `guion.md` following the sections below.
8. `uv run python scripts/ng/guion.py check $S` fills in the estimated duration. Fix every `ERROR`.
9. Give the user the path, the duration and any interview or doubtful passage.

## Format of guion.md

```markdown
# Guion Ng-News en español 26/18

Duración estimada:

## Introducción

Hola, mi nombre es <host> y esto es NG News en español con las últimas novedades de la comunidad de Angular.

## Nombre de la noticia

Texto para leer, un párrafo por idea.

> ENTREVISTA 03:21-04:02: no se graba, queda el audio original con subtítulos.

## Cierre

Y eso es todo. Espero que tengas una excelente semana. Nos vemos en el próximo episodio. Hasta luego.
```

- `##` headings and `>` notes are not read aloud. Everything else is exactly what the host says.
- Nothing else in the file: no timestamps, no shot directions, no English. The host reads it to camera.
- Introducción and Cierre are fixed: always those exact words, with the name of who records it. The EN host's name never appears.

## How to write it

Calibrated on the recordings of 26-17 and 26/11. It is an adaptation for speaking, not a literal translation.

- **Same order and same facts as the EN.** Never add, drop or reinterpret a piece of news. Numbers, dates, versions and names stay exact.
- **Do not summarize.** Keep every detail, example and aside of the EN. The ES uses as many words as the EN or a few more (100-109 % measured) and runs about 92 % of its time, because Spanish is read faster. `check` measures it at 2.7 words per second and fails below 85 %: a short script forces the screen recordings to speed up.
- **Short sentences that sound natural aloud.** Split long EN sentences. Avoid structures that are hard to say in one breath.
- **Connectors between news:** "En otras noticias, ..." and, for the last one, "Para terminar, ...". Reactions: "Ante esto, ...".
- **Speak to the audience** in plural when the EN does: "Imaginen el caso habitual...".
- **Technical terms stay in English** (`glossary.json > keep_english`) and also: pull request, frontend, snapshot, resource, router, guard, builder, fork, issues, framework, open source. Use "librería", not "biblioteca".
- **Latin American neutral Spanish**, close and professional. No slang, no sensationalism.

Example:

- EN: "The reason is that the library has grown over time, which means if you do this as an open source, you have to spend much more time on it, and at some point, the income that they got from selling things around the library itself didn't cover the costs anymore."
- ES: "La razón es que la librería ha crecido con el tiempo, lo que exige dedicarle mucho más trabajo. Y en cierto punto, los ingresos generados por la venta de productos complementarios ya no cubrían los costos de desarrollo."

## Interviews

An interview is someone other than the host speaking in the video. **It is not translated into the script**: it stays with its original audio and Spanish captions.

- Candidates in `en_script.md`:
  - `[VOZ SIN TRANSCRIBIR] MM:SS-MM:SS`: Whisper often skips the second speaker and stretches the words around it, so **the interview may not be in the transcript at all**. Its span is only approximate.
  - `[OTRA VOZ]`: sentences in a voice different from the host.
- Read `en_captions.png` from start to end and compare it with the transcript: the burned-in captions always have the interview text. Any line missing from the transcript is a candidate, even if nothing is marked.
- Confirm each one in the video: `ffmpeg -ss <t> -t 20 -i assets/en/proxy.mp4 -vf "fps=1,scale=480:-1,tile=6x4" -frames:v 1 x.png`. The caption text gives the exact start and end, and the wording is usually first person after the host introduces the person.
- A guest's webcam or photo on screen is **not** an interview if the host is narrating over it. Those sentences go in the script.
- The host's introduction to the interview does go in the script.
- For each interview, add a `> ENTREVISTA MM:SS-MM:SS` note in its place, with the EN times, and an entry in `data/interviews.json`: `{"en_start": 201.0, "en_end": 242.5, "en": "...", "es": "..."}`. `en` is the exact text from the burned-in captions. `es` is the translation for the captions and is never read on camera.
- If you are not sure, keep the note and ask the user.
