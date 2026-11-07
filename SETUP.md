# NG News Videos: setup rápido

```bash
pnpm install && uv sync
pnpm exec playwright install chromium
# Whisper en GPU (faster-whisper). El modelo se convierte UNA vez desde el HF cache (sin descargar de nuevo):
uv run ct2-transformers-converter --model openai/whisper-large-v3 \
  --output_dir ~/.cache/ng-news/whisper-large-v3-ct2 --copy_files tokenizer.json preprocessor_config.json --quantization float16
# (si openai/whisper-large-v3 no está en ~/.cache/huggingface, el primer comando lo descarga: ~3 GB)
```

Tiempos medidos en la RTX 3090: transcripción large-v3 ≈ 34 s por 5 min de audio.
`hyperframes transcribe` (whisper.cpp) corre en CPU aquí y no se usa en este workspace.

Uso: deja `ng-news-<slug>-en.mp4` y `ng-news-<slug>-es.mp4` en `videos/<slug>/assets/`, abre Claude Code en esta carpeta y pide `/ng-news-es Crea el episodio <slug>`.

---

# Setup del workspace

Cómo dejar el entorno listo para crear y renderizar videos de HyperFrames. Se hace una vez por máquina.

## 1. Requisitos del sistema

- **Node.js 22+**
- **pnpm** (el workspace usa `pnpm-workspace.yaml`)
- **ffmpeg** en el PATH (`ffmpeg -version`)
- **uv** para Python (`uv --version`)

## 2. Dependencias del root

```bash
pnpm install
```

Esto instala `hyperframes` (versión fijada en `package.json`) y `playwright`.

```bash
pnpm exec playwright install chromium
```

## 3. Dependencias de Python (audio)

```bash
uv sync
```

Crea `.venv/` (Python 3.11) con dos grupos de paquetes:

- **Base:** `numpy`, `librosa` y `soundfile`, para **analizar** audio: beats, golpes y BPM.
- **Grupo `musicgen`:** `torch` y `transformers`, para **generar** música en local. Se instala por defecto.

En Linux, el `torch` de PyPI ya trae CUDA: no hace falta conda ni instalar CUDA aparte. En WSL basta con el driver de NVIDIA de Windows. Para comprobar la GPU:

```bash
uv run python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

En una máquina sin GPU, o para una instalación liviana (sin torch, que pesa unos 4 GB): `uv sync --no-group musicgen`.

Para que HyperFrames use este mismo Python en sus motores locales (el MusicGen de respaldo de `/media-use` y Kokoro), agrégalo a tu `~/.zshrc`:

```bash
export HYPERFRAMES_PYTHON="$HOME/Work/nicobytes/ng-news-videos/.venv/bin/python"
```

Para ejecutar un script:

```bash
uv run python scripts/mi_script.py
```

Medir el beat de una pista (para anclar cortes y sonidos):

```bash
uv run python scripts/beats.py videos/mi-video/assets/track.wav > videos/mi-video/assets/beats.json
```

Generar una cama musical con MusicGen en la GPU. La primera vez descarga el modelo, unos 7 GB, a `~/.cache/huggingface/`:

```bash
uv run python scripts/musicgen.py "warm minimal piano, light percussion, 100 BPM" -d 48 -o videos/mi-video/assets/music/track.wav --seeds 1,2,3
```

**Licencia:** los pesos de MusicGen son CC-BY-NC 4.0 (no comercial). Sirven para borradores y pistas temporales. Antes de publicar una pieza comercial con esa música, revisa la licencia o reemplázala por una pista con licencia.

### Transcripción (whisper.cpp)

`npx hyperframes transcribe` usa whisper.cpp. En Linux lo compila solo en el primer uso, pero necesita `cmake` y un compilador de C. Si tienes `build-essential` y te falta cmake, instálalo sin sudo:

```bash
uv tool install cmake
```

El binario queda en `~/.cache/hyperframes/whisper/whisper.cpp/build/bin/whisper-cli`. Los modelos se guardan en `~/.cache/hyperframes/whisper/models/`. Para español usa `-m large-v3`, que pesa 3,1 GB; el modelo por defecto, `small.en`, solo entiende inglés. `npx hyperframes doctor` muestra si whisper está listo.

## 3b. Modelo y esfuerzo de Claude Code

Para piezas nuevas conviene un modelo de la familia Opus 5.5 con esfuerzo alto (`xhigh`). Para retoques y re-renders basta un esfuerzo medio. Para el primer tercio de un video que tiene que enganchar desde el principio, `max`.

```bash
claude --model claude-opus-5-5
```

Dentro de la sesión, ajusta el esfuerzo con `/model`.

## 4. Skills de HyperFrames

Las skills viven en `.agents/skills/` y se registran en `skills-lock.json`.

```bash
npx hyperframes skills                            # instala el set completo publicado
npx hyperframes skills update                     # refresca las ya instaladas
npx hyperframes skills update <workflow>          # instala o refresca un workflow (p. ej. general-video)
npx hyperframes skills check                      # diagnostica skills viejas o faltantes
```

Si el CLI de HyperFrames no está disponible: `npx skills add heygen-com/hyperframes --all`.

Después de instalar o actualizar, **reinicia la sesión de Claude Code** para que carguen.

## 5. Plugin opcional: animación dibujada a mano

Es opcional. Úsalo solo si quieres el estilo de dibujo a mano (tinta, papel, acuarela) en un video. No es parte del flujo normal.

```bash
claude plugin marketplace add buildwithhanif/claude-animation-skill
claude plugin install claude-animation@claude-animation-skill
```

Requiere Node y ffmpeg, y su propio `npm install` dentro de la skill.

## 6. Crear un video nuevo

Desde la raíz:

```bash
pnpm new-video mi-video
```

Con footage:

```bash
pnpm new-video mi-video --video /ruta/al/footage.mp4
```

El comando hace esto:

- Crea `videos/mi-video/` con `hyperframes init` (ejemplo en blanco).
- Quita el `CLAUDE.md` y `AGENTS.md` que genera init: las reglas son las del root.
- Reescribe los scripts de `package.json` para usar la versión del root.
- **No** crea `BRIEF.md` ni `STORYBOARD.md`: los escribe el flujo de `/hyperframes`.

Después:

1. Pon footage y audio en `videos/mi-video/assets/`.
2. Abre Claude Code con `videos/mi-video/` como directorio de trabajo y usa `/hyperframes`. Su entrevista escribe `BRIEF.md`; el estilo se decide ahí, por video.
3. Si prefieres saltarte la entrevista, copia `templates/video/BRIEF.md` al video y llena **todas** las claves. Un brief a medias hace que el router deje de preguntar.

Guía paso a paso: [NUEVO_VIDEO.md](NUEVO_VIDEO.md).

## 7. Revisar, previsualizar y renderizar

Siempre desde dentro del video:

```bash
cd videos/mi-video
pnpm run check                             # lint, runtime, layout, motion, contraste
npx hyperframes preview --background       # preview persistente para revisar
npx hyperframes preview --status
npx hyperframes preview --stop             # cuando termines la revisión
pnpm run render                            # MP4 en renders/
```

`pnpm run dev` también sirve para previsualizar, pero bloquea la terminal. Desde un agente usa `--background`.

## 8. Publicar

```bash
cd videos/mi-video
pnpm run publish
```

## Versión de HyperFrames

Está fijada en un solo lugar: `devDependencies.hyperframes` del root. Para subirla:

```bash
pnpm add -D -w hyperframes@<versión>
pnpm exec hyperframes upgrade --check
```

Antes de cambiar la versión, revisa el `check` y el `render` de los videos que ya publicaste.

## Referencia de shared/

- `shared/brand/` — DESIGN.md y FRAME.md de referencia. Cada video puede seguirlos o no.
- `shared/blocks/` — bloques reutilizables. Cópialos a `compositions/` del video; no los enlaces.
- `shared/fonts/` — fuentes. Cópialas a `assets/` del video.
- `shared/recipes/` — recetas de media-use congeladas.
- `shared/CAPTIONS.md` — reglas de subtítulos: zona segura y estilo por defecto.

## Problemas comunes

- **`hyperframes is not installed`** en `new-video`: corre `pnpm install` en la raíz.
- **Una skill no aparece**: reinicia la sesión de Claude Code después de `npx skills add`.
- **`check` marca un warning en el ejemplo en blanco**: es esperado; el warning desaparece cuando la composición tiene contenido.
- **Render diferente entre dos videos**: revisa que ambos usen el CLI del root (`pnpm exec hyperframes --version`).
- **WSL: el render dice `browserGpuMode probe → software` (llvmpipe)**, aunque estés en el grupo `render`. Mesa no elige solo su driver D3D12, y Chrome termina dibujando por CPU. Fuérzalo en tu `~/.zshrc`:

  ```bash
  export GALLIUM_DRIVER=d3d12
  export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA
  ```

  Con eso el probe dice `hardware ... D3D12 (NVIDIA GeForce RTX 3090)`. No hace falta reiniciar el PC: basta con abrir una terminal nueva.
