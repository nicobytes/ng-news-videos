# NG News Videos Workspace

Workspace HyperFrames para producir la **versión en español de NG News** (@ng-news → @ng-news-es). Un video por episodio en `videos/<slug>/`. Comando principal:

1. `/ng-news-guion 26-18`: con solo `videos/26-18/assets/ng-news-26-18-en.mp4`, escribe `guion.md`, el texto en español que se graba a cámara. Las entrevistas no se traducen.
2. Se graba y la grabación se copia en `videos/26-18/assets/ng-news-26-18-es.mp4`.
3. `/ng-news-es Crea el episodio 26-18`: edita, pasa la autocrítica, renderiza y genera la metadata.

Las skills se cargan al iniciar: usa una sesión nueva abierta en esta carpeta.

Para generar solo título, descripción y capítulos de un episodio ya editado:

> /ng-news-youtube 26-17

Muestra 3 títulos, descripción, capítulos y tags, pregunta qué título prefiere el usuario y sobrescribe `videos/<slug>/youtube.md`. `pnpm new-ng` rechaza un episodio ya compuesto: para repetirlo, corre los pasos desde `compose.mjs`. Instrucciones completas en `README.md`.

La skill `/ng-news-es` (`.agents/skills/ng-news-es/`) lleva el flujo completo: transcripción, segmentación, alineación, corrección de subtítulos, composición, **ciclo de autocrítica**, render 4K y metadata de YouTube con `/ng-news-youtube`. Geometría en `shared/brand/FRAME.md`. Aprendizajes del pipeline en `.agents/skills/ng-news-es/references/learnings.md`: léelos antes de cambiarlo.

Reglas fijas de NG News:
- El video EN es la capa base: marco, logo, panel derecho y pantallas son sus píxeles originales.
- **El panel derecho no se traduce**: título y viñetas quedan en inglés.
- Panel izquierdo `presenter` → presentador ES. Panel `screen` (grabación de pantalla, web, imagen, webcam de invitado) → se conserva.
- Subtítulos y audio van en español. Los subtítulos EN no deben verse nunca.
- El host nunca lee las entrevistas: conservan imagen y audio originales, con subtítulos en español del mismo estilo.
- Términos técnicos (Angular, signals, etc.) quedan en inglés según `glossary.json`.
- Nunca se renderiza el final sin pasar el ciclo de autocrítica (todas las puntuaciones ≥ 8).
- El presentador varía por episodio (Ricardo Chavarría o Nicolás Molina): `host` en `data/episode.json`.
- Los títulos de YouTube siempre empiezan con `Ng-News en español 26/xx: `.

---


Este repo es un **workspace multi-video**. La raíz no es una composición: cada video vive en `videos/<slug>/` y es un proyecto HyperFrames completo. Cada video define su propio estilo en su `BRIEF.md`; no hay un tema global que deban seguir todos.

Setup e instrucciones de arranque: [SETUP.md](SETUP.md). Para empezar un video nuevo, paso a paso (comando, skills, prompt y ciclo de crítica): [NUEVO_VIDEO.md](NUEVO_VIDEO.md).

## Skills — USA ESTOS PRIMERO

**Invoca la skill relevante antes de escribir o modificar una composición.** Las skills contienen patrones propios de HyperFrames (registro de `window.__timelines`, semántica de `data-*`, reglas de CSS compatibles con el render) que no están en la documentación web genérica. Saltártelas produce composiciones rotas.

**¿Algo con HyperFrames?** Empieza con `/hyperframes`: enruta cada pedido al flujo correcto y confirma el brief antes de empezar.

Flujos principales:

- `/product-launch-video` — URL de web o brief/guion → video de lanzamiento o promo.
- `/faceless-explainer` — texto libre (tema, artículo, notas), sin URL → explicativo de 60-90 s.
- `/embedded-captions` — video talking-head (MP4) → mismo footage con subtítulos.
- `/talking-head-recut` — talking-head / entrevista / podcast (MP4) → overlays gráficos sincronizados con el transcript.
- `/pr-to-video` — PR de GitHub → explicativo de cambios de código.
- `/motion-graphics` — motion graphic corto (< 10 s), sin narración.
- `/music-to-video` — pista musical → video sincronizado al beat.
- `/slideshow` — presentación o deck navegable (no es video renderizado).
- `/general-video` — cualquier otro video, incluido el modo companion.

**Portar una composición de Remotion:** `/remotion-to-hyperframes`.

Dominios: `/hyperframes-core`, `/hyperframes-animation`, `/hyperframes-keyframes`, `/hyperframes-creative`, `/hyperframes-cli`, `/media-use`, `/hyperframes-audio`, `/hyperframes-registry`, `/figma`.

**Cambiar cómo se ve o se revela footage o imágenes reales:** carga `/media-use` y lee `references/media-treatments.md` antes de editar. No improvises filtros CSS/SVG equivalentes.

> **Proyectos con Tailwind v4:** ver `/hyperframes-core` → `references/tailwind.md`.

> **Skill faltante o desactualizada:** `npx hyperframes skills update <nombre>` (instala o refresca ese workflow o skill de dominio). Reinicia la sesión para que cargue.

## Versión del CLI

- **La versión de HyperFrames está fijada una sola vez, en la `devDependencies` del root (`package.json`).** Todos los videos la usan vía `pnpm exec hyperframes`. No pongas `npx hyperframes@X` en los scripts de un video: eso crea versiones distintas por video y cambia el render.
- Para subir de versión: cambia la versión en el root, corre `pnpm install`, y luego revisa las diferencias con `pnpm exec hyperframes upgrade --check`.
- Un video que ya renderiza bien no se reconstruye con otra versión sin verificar antes su `check` y su `render`.

## Comandos

Desde la raíz:

```bash
pnpm install                       # dependencias Node (incluye hyperframes y playwright)
uv sync                            # Python: numpy, librosa, soundfile + torch/transformers (MusicGen, CUDA)
pnpm new-video <slug>              # crear un video nuevo (BRIEF.md lo escribe /hyperframes)
pnpm new-video <slug> --video footage.mp4
```

Dentro de `videos/<slug>/` (siempre haz `cd` antes):

```bash
pnpm run check                     # lint + runtime + layout + motion + contraste
pnpm run dev                       # preview interactivo (bloquea la terminal)
npx hyperframes preview --background   # preview persistente para agentes
npx hyperframes preview --status
npx hyperframes preview --stop     # al terminar la revisión
pnpm run render                    # render a MP4
pnpm run publish                   # publicar y obtener enlace compartible
npx hyperframes lint --verbose     # incluye hallazgos info
npx hyperframes docs <tema>        # documentación en terminal
```

> **Los agentes usan `npx hyperframes preview --background` para entregar el Studio.** No envuelvas `npm run dev` en `run_in_background`: el proceso queda ligado a la sesión y el navegador se queda con `ERR_CONNECTION_TIMED_OUT`. Verifica con `--status` y cierra con `--stop`.

## Documentación

- Referencia local: `npx hyperframes docs <tema>` (temas: `data-attributes`, `gsap`, `compositions`, `rendering`, `examples`, `troubleshooting`).
- Documentación completa: `https://hyperframes.heygen.com/llms.txt`. Busca la página ahí; no adivines URLs.

## Estructura

```
ng-news-videos/
  CLAUDE.md             # reglas del workspace (esta fuente)
  SETUP.md              # cómo arrancar el setup y crear un video
  package.json          # hyperframes y playwright fijados; script new-video
  pyproject.toml        # dependencias Python (uv)
  scripts/new-video.mjs # scaffolding de videos (no escribe BRIEF.md ni STORYBOARD.md)
  scripts/beats.py      # grid de beats y golpes de una pista (uv run)
  scripts/musicgen.py   # cama musical generada en la GPU (uv run; pesos CC-BY-NC: borradores)
  scripts/sfx.mjs       # efectos de UI sintetizados (click, tick, pop, thump, chime, whoosh)
  templates/video/      # BRIEF.md canónico, para copiar y llenar completo si te saltas la entrevista
  shared/               # recursos compartidos (copiar, no enlazar)
    brand/              # DESIGN.md y FRAME.md de referencia
    blocks/             # bloques reutilizables
    fonts/
    recipes/            # recetas de media-use
    CAPTIONS.md         # reglas de subtítulos del workspace
  videos/<slug>/        # un proyecto HyperFrames por video
```

Archivos de un video:

- `index.html` — composición raíz.
- `compositions/` — subcomposiciones, referenciadas con `data-composition-src`.
- `BRIEF.md` — el brief confirmado, con frontmatter canónico (`workflow`, `flow`, `storyboard`, `message`…). El router de HyperFrames lo lee para saber qué flujo correr y no vuelve a preguntar: nunca lo dejes a medias.
- `STORYBOARD.md` — plan escena por escena. Nunca lo pongas en la raíz del workspace.
- `meta.json`, `hyperframes.json` — metadatos y registro de bloques.
- `assets/` — footage, audio e imágenes del video.
- `transcript.json` — transcript con timestamps, si existe.

**Reglas de estilo:** cada video decide su paleta, tipografía y tono en `BRIEF.md`. Si un video comparte algo con otro (un bloque, una fuente), cópialo desde `shared/` a su propio `assets/` o `compositions/`. Las rutas dentro de una composición son relativas al proyecto.

## Qué versionar

- **Sí:** `index.html`, `compositions/`, `BRIEF.md`, `STORYBOARD.md`, `meta.json`, `hyperframes.json`, `package.json`, `transcript.json`, fuentes en `assets/` que sean tuyas.
- **No:** `node_modules/`, `renders/`, MP4 generados, `frames*/`, `snapshots/`, `history/`, `backup*/`, `.thumbnails/`, `.waveform-cache/`, `.hyperframes/`, `vendor/`. El `.gitignore` ya los excluye.

## Motor de render

Usa HyperFrames para renderizar. No escribas un motor de render propio (un `seek(t)` con Playwright y ffmpeg a mano) salvo que el usuario lo pida explícitamente: los agentes tienden a elegirlo por defecto, y se pierde la sincronía con las skills y el `check`.

## Brief de director

Antes del storyboard, `BRIEF.md` debe fijar: logline (qué debe sentir el espectador), referencias (qué tomar y qué no), formatos de salida, pista de audio y deliverables. Si el brief no tiene estas partes, pregúntalas antes de escribir código.

- Las referencias dan la **gramática** (ritmo, tipo, transiciones), nunca el contenido ni logos ajenos.
- Si hay una pista de audio, mídela con `uv run python scripts/beats.py assets/track.wav > assets/beats.json` y ancla los cambios de escena a `beats` y los golpes a `hits`.
- Sin pista, ofrece el catálogo de HeyGen (`/media-use`) o `scripts/musicgen.py` con varias semillas para que el usuario elija de oído. Anota en `BRIEF.md` el modelo, el prompt y la semilla. Los pesos de MusicGen son CC-BY-NC 4.0: en una pieza comercial, avisa antes de publicar.

## Calidad por defecto

Estos valores aplican a todo video salvo que su `BRIEF.md` los anule explícitamente:

- Evitar: título centrado sobre degradado, todo con fade-in, etiquetas en las esquinas o bordes de cuadro, brillo en elementos de interfaz, partículas genéricas.
- Algo nuevo cada 2-4 segundos.
- Una fuente de display y una de interfaz; un color de acento salvo que el brief diga otra cosa.
- Revisar la legibilidad a 360 px de ancho.

## Ciclo de crítica (antes del render final)

1. Renderiza una vista previa de cada escena o beat, y revísala visualmente. Guarda las revisiones en `renders/review/`, que ya está en `.gitignore`.
2. Puntúa de 1 a 10: gancho en los primeros 2 s, legibilidad en móvil, calidad de movimiento, variedad, composición, precisión de marca y sincronía con el sonido.
3. Corrige los 3 peores problemas y repite hasta que cada puntuación sea 8 o más.
4. Solo entonces renderiza el MP4 final.

Comandos de revisión (desde dentro del video, sobre un MP4 renderizado):

```bash
mkdir -p renders/review
# Contact sheet: 2 fotogramas por segundo, 6 por fila
ffmpeg -y -i renders/final.mp4 -vf "fps=2,scale=270:-1,tile=6x5" -frames:v 1 renders/review/contact.png
# Tira de 12 fotogramas alrededor de una acción rápida (en el segundo 4.1)
ffmpeg -y -ss 4.1 -i renders/final.mp4 -vf "scale=320:-1,tile=12x1" -frames:v 1 renders/review/strip.png
# Prueba de teléfono: cómo se lee a 360 px
ffmpeg -y -i renders/final.mp4 -vf "fps=1,scale=360:-1,tile=5x3" -frames:v 1 renders/review/phone.png
# Prueba de loop: reproduce dos veces seguidas y revisa la costura
ffmpeg -y -stream_loop 1 -i renders/final.mp4 -c copy renders/review/loop_check.mp4
```

Los revisores (tú o un agente) deben mirar las imágenes de verdad y buscar: texto superpuesto durante transiciones, cosas que se deslizan en lugar de ajustarse con easing, texto escalado borroso, momentos muertos sin movimiento, y saltos en la costura del loop.

## Lint — SIEMPRE tras un cambio

Después de crear o editar cualquier `.html` de composición, corre `pnpm run check` dentro del video. Corrige todos los errores antes de dar el trabajo por terminado. Revisa los warnings antes de renderizar.

## Reglas clave

1. Cada elemento con tiempo necesita `data-start` y duración. `data-start` es lo que lo marca como temporizado; `data-track-index` solo sirve para la pista visual del Studio y el render no lo lee.
2. Dale `class="clip"` a los elementos visuales con tiempo. El framework controla la visibilidad con `data-start`, pero el CSS de `.clip` es lo que da a la escena su caja de cuadro completo; `lint` avisa si falta.
3. Registra **un** timeline raíz pausado por composición en `window.__timelines`:
   ```js
   window.__timelines = window.__timelines || {};
   window.__timelines["composition-id"] = gsap.timeline({ paused: true });
   ```
   Los timelines de escena que agregues a ese raíz **no** deben estar pausados: un hijo pausado no avanza cuando se hace seek al raíz. El runtime activa los hermanos registrados, no cualquier timeline anidado.
4. Los videos usan `muted` con un `<audio>` separado para la pista de audio.
5. Las subcomposiciones se referencian con `data-composition-src="compositions/archivo.html"`.
6. Solo lógica determinista: nada de `Date.now()`, `Math.random()` ni fetch de red dentro de la composición.
7. Antes de cambiar el estilo de footage o imágenes reales, aplica las reglas de `/media-use` (ver arriba).
