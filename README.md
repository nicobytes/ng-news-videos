# NG News ES

Versión en español de [@ng-news](https://www.youtube.com/@ng-news) para [@ng-news-es](https://www.youtube.com/@ng-news-es).

## Instalación

Se hace una vez por máquina. Detalle y solución de problemas en [SETUP.md](SETUP.md).

**Requisitos:** Node.js 22+, pnpm, ffmpeg, [uv](https://docs.astral.sh/uv/) y [Claude Code](https://claude.com/claude-code). Para transcribir en local hace falta una GPU NVIDIA (en WSL basta el driver de Windows).

```bash
git clone git@github.com:nicobytes/ng-news-videos.git
cd ng-news-videos
pnpm install                          # hyperframes y playwright, con la versión fijada
pnpm exec playwright install chromium
uv sync                               # Python 3.11: yt-dlp, faster-whisper, librosa, torch
```

Convierte el modelo de Whisper una sola vez (descarga unos 3 GB la primera vez):

```bash
uv run ct2-transformers-converter --model openai/whisper-large-v3 \
  --output_dir ~/.cache/ng-news/whisper-large-v3-ct2 \
  --copy_files tokenizer.json preprocessor_config.json --quantization float16
```

Las skills ya vienen en `.agents/skills/`. Abre la sesión de Claude Code en esta carpeta para que carguen (si falta alguna, `npx hyperframes skills`).

> Los videos, audios y renders **no se versionan** (`.gitignore`): en un clon nuevo hay que volver a poner los MP4 en `videos/<slug>/assets/`.

## Uso

Las skills se cargan al iniciar la sesión: abre siempre una sesión nueva en esta carpeta, en la app de Claude o desde la terminal:

```bash
cd ~/Work/nicobytes/ng-news-videos && claude
```

### Flujo de un episodio

`/ng-news-guion` → grabar a cámara → `/ng-news-es` → `/ng-news-youtube` (este último corre solo al final de `/ng-news-es`).

**1. Preparar el guion.** Copia el video EN en alta calidad con este nombre:

```text
videos/26-18/assets/ng-news-26-18-en.mp4
```

En la sesión, pide:

```text
/ng-news-guion 26-18, lo graba Ricardo Chavarría
```

Deja en `videos/26-18/guion.md` el texto para leer a cámara, en unos 5 min. El host no lee las entrevistas: aparecen como una nota `> ENTREVISTA` y no se graban. En la edición conservan su audio original con subtítulos en español.

**2. Grabar** el guion y copiar la grabación aquí:

```text
videos/26-18/assets/ng-news-26-18-es.mp4
```

**3. Editar.** En la sesión, pide:

```text
/ng-news-es Crea el episodio 26-18
```

La skill (`.agents/skills/ng-news-es/SKILL.md`) transcribe EN/ES en la GPU, segmenta bloques presenter/screen, alinea la grabación ES con la línea de tiempo EN, corrige los subtítulos, compone con HyperFrames, pasa el **ciclo de autocrítica**, renderiza en 4K y corre `/ng-news-youtube`.

Solo se detiene si tiene dudas sobre la alineación y al final para elegir el título. Con un episodio de 5 min, cuenta con unos 30 min entre borrador y render 4K, y más si la autocrítica pide otra vuelta.

El resultado queda en `videos/26-18/renders/ng-news-26-18-es.mp4` y `videos/26-18/youtube.md`.

El panel derecho se queda en inglés, igual que el original. Solo cambian el presentador, el audio y los subtítulos.

### Generar solo título, descripción y capítulos

Con un episodio ya editado, por ejemplo el 26-17:

```text
/ng-news-youtube 26-17
```

Muestra 3 títulos, la descripción, los capítulos y los tags, y pregunta cuál título prefieres. Sobrescribe `videos/26-17/youtube.md`.

### Limitaciones

- `pnpm new-ng` rechaza un episodio ya compuesto, como el 26-17. Para repetirlo, corre los pasos a mano desde `compose.mjs`.

## Pasos a mano (por episodio `videos/<slug>/`)

```bash
pnpm new-ng 26-17
scripts/ng/fetch.sh videos/26-17
scripts/ng/transcribe.sh videos/26-17
uv run python scripts/ng/segment_en.py videos/26-17       # revisar data/review/segment_sheet.png
uv run python scripts/ng/align.py prepare videos/26-17    # escribir data/alignment.json
uv run python scripts/ng/align.py build videos/26-17
node scripts/ng/compose.mjs videos/26-17                  # --limit 30 para una prueba corta
scripts/ng/review.sh videos/26-17                         # material de autocrítica
```

Con el video ya editado, `/ng-news-youtube 26-17` genera la metadata de YouTube:

```bash
uv run python scripts/ng/youtube_meta.py prepare videos/26-17   # transcripción final y links del EN
uv run python scripts/ng/youtube_meta.py build videos/26-17     # valida data/youtube.json, escribe youtube.md
```

Geometría del cuadro: `shared/brand/FRAME.md`. Reglas: `.agents/skills/ng-news-es/references/rules.md`. Aprendizajes: `.agents/skills/ng-news-es/references/learnings.md`.
