# Empezar un video nuevo

Guía para arrancar un video desde cero. Léela cada vez que empieces uno.

## 0. Antes de empezar (una vez por máquina)

```bash
pnpm install
uv sync
pnpm exec playwright install chromium
```

Detalles en [SETUP.md](SETUP.md).

## 1. Crear el proyecto

Desde la raíz del workspace:

```bash
pnpm new-video <slug>
```

Si ya tienes el footage:

```bash
pnpm new-video <slug> --video /ruta/al/footage.mp4
```

Si ya sabes qué flujo lo construye, regístralo en `hyperframes.json` (ayuda al router a retomar el proyecto):

```bash
pnpm new-video <slug> --skill general-video
```

El `<slug>` usa solo minúsculas, dígitos, `-` o `_`. Crea `videos/<slug>/` con `index.html`, `hyperframes.json`, `meta.json` y `package.json`. No crea `BRIEF.md` ni `STORYBOARD.md`: los escribe `/hyperframes` (paso 4).

## 2. Skills

Las skills de HyperFrames se instalan una vez. El set trae el router `/hyperframes` y todos los flujos:

```bash
npx hyperframes skills                       # set completo
npx hyperframes skills update <workflow>     # instalar o refrescar un flujo concreto
```

Después **reinicia Claude Code** para que cargue las skills. Si el CLI no está disponible: `npx skills add heygen-com/hyperframes --all`.

Qué skill usar según el tipo de video:

| Si tu video es… | Skill |
| --- | --- |
| No sabes cuál es | `/hyperframes` (siempre; enruta y confirma el brief) |
| Promo o lanzamiento de un producto con URL | `/product-launch-video` |
| Explicativo desde texto, sin URL | `/faceless-explainer` |
| Motion graphic corto (< 10 s), sin narración | `/motion-graphics` |
| Talking-head con overlays gráficos | `/talking-head-recut` |
| Talking-head solo con subtítulos | `/embedded-captions` |
| Video sincronizado a una pista musical | `/music-to-video` |
| Cambios de un PR de GitHub | `/pr-to-video` |
| Presentación navegable (no MP4) | `/slideshow` |
| Cualquier otro (montaje, reel, tarjeta) | `/general-video` |
| Portar un proyecto de Remotion | `/remotion-to-hyperframes` |

Para tocar cómo se ve o se revela footage real (oscuro, retro, privado): `/media-use`. Para audio (mezcla, ducking, voz): `/hyperframes-audio`.

## 3. Abrir Claude Code en el video

```bash
cd videos/<slug>
claude --model claude-opus-5-5
```

Usa esfuerzo `xhigh` para una pieza nueva, `max` si los primeros 3 segundos tienen que enganchar, y uno medio para retoques (ver [SETUP.md](SETUP.md), sección 3b).

Trabaja siempre desde la carpeta del video, no desde la raíz.

## 4. El brief

`BRIEF.md` es lo que el router de HyperFrames lee para saber qué flujo correr. Hay dos caminos:

- **Recomendado:** deja que `/hyperframes` te entreviste (paso 5). Al final escribe `BRIEF.md` con frontmatter canónico (`workflow`, `flow`, `storyboard`, `message`, `destination`, `aspect`, `language`, `audience`, `length`, `angle`).
- **Atajo:** copia `templates/video/BRIEF.md` a `videos/<slug>/BRIEF.md` y llena **todas** las claves. El router se salta la entrevista.

Nunca dejes un `BRIEF.md` a medias: el router lo toma como confirmado y deja de preguntar.

Ten listo para la entrevista:

- **Logline**: qué debe sentir o entender el espectador.
- **Formato**: 16:9, 9:16, 1:1 o 4:5. Si son varios, reencuadra; no recortes.
- **Referencias**: qué tomar (ritmo, tipo, transiciones) y qué no (contenido, logos).
- **Pista musical**: si hay, mídela (paso 6).
- **Beats**: un cambio cada 2-4 segundos.
- **Entregables**: MP4 final, poster, contact sheet.

El estilo lo decides tú, por video. No hay un tema global.

## 5. Prompt de arranque

Pega esto en Claude Code, ajustando lo que va entre corchetes:

```
Usando /hyperframes, crea un video de [DURACIÓN] s en formato [FORMATO] sobre [TEMA].
Lee primero BRIEF.md y las reglas de CLAUDE.md del workspace.
Antes de escribir código: muéstrame el storyboard y espera mi OK.
Después de construirlo, corre el ciclo de crítica (CLAUDE.md, sección "Ciclo de crítica")
antes de renderizar el MP4 final.
```

Puertas en orden. No saltes ninguna:

1. Brief completo (`BRIEF.md`).
2. Storyboard aprobado (`STORYBOARD.md`).
3. Construcción con `pnpm run check` sin errores.
4. Ciclo de crítica con puntuación de 8 o más.
5. Render final.
6. Publicar, si hace falta.

## 6. Música o pista de audio (si la hay)

Mide el beat antes de animar:

```bash
uv run python scripts/beats.py assets/track.wav > assets/beats.json
```

Ancla los cambios de escena a `beats` y los sonidos a `hits`.

Sin pista hay tres caminos:

- **Catálogo de HeyGen:** con `/media-use`, si iniciaste sesión con `npx hyperframes auth login`.
- **Generarla en tu GPU con MusicGen:** varias semillas para elegir; `--section` cambia el ánimo en un segundo dado.
- **Instagram:** agregar la música de su librería al publicar.

```bash
uv run python ../../scripts/musicgen.py "<estilo en inglés, BPM>" -d <segundos> -o assets/music/track.wav --seeds 1,2,3
uv run python ../../scripts/musicgen.py "<tenso>" --section "15=<cálido>" -d 48 -o assets/music/track.wav
```

La licencia de MusicGen es no comercial (CC-BY-NC 4.0). Úsala para borradores y verifica la licencia antes de publicar.

Voz en off grabada por ti: transcríbela con timestamps por palabra. En español no uses el modelo por defecto (`small.en` solo entiende inglés):

```bash
npx hyperframes transcribe assets/vo/voice.wav -l es -m large-v3
```

Efectos de UI (click, tick, pop, thump, chime, whoosh) sintetizados en código, sin licencias:

```bash
node ../../scripts/sfx.mjs --kit assets/sfx                     # un WAV por sonido
node ../../scripts/sfx.mjs assets/sfx/cues.json assets/sfx/mix.wav  # una pista desde una lista de cues
```

## 7. Ciclo de crítica

**Se activa pidiéndolo.** Claude Code lee `CLAUDE.md` pero no lo ejecuta solo; incluye la instrucción en el prompt (paso 5) o pídela después de construir.

Desde `videos/<slug>/`:

```bash
# Hoja de contacto de la composición (genera PNG en .hyperframes/artifacts/snapshots/)
npx hyperframes snapshot --frames 30

# Render final (sale en renders/<slug>.mp4)
pnpm run render
```

Con el MP4 final, las revisiones de tira, teléfono y loop están en `CLAUDE.md`:

```bash
mkdir -p renders/review
ffmpeg -y -ss 4.1 -i renders/<slug>.mp4 -vf "scale=320:-1,tile=12x1" -frames:v 1 renders/review/strip.png
ffmpeg -y -i renders/<slug>.mp4 -vf "fps=1,scale=360:-1,tile=5x3" -frames:v 1 renders/review/phone.png
ffmpeg -y -stream_loop 1 -i renders/<slug>.mp4 -c copy renders/review/loop_check.mp4
```

Prompt para pedir la revisión (puedes pegarlo tal cual):

```
Ciclo de crítica. Abre las imágenes de la hoja de contacto, la tira y la prueba de teléfono y míralas de verdad.
Puntúa de 1 a 10: gancho en 2 s, legibilidad en móvil, calidad de movimiento, variedad,
composición, precisión de marca, sincronía con el sonido.
Lista los 3 peores problemas con su tiempo. Corrígelos, vuelve a revisar solo esos segundos
y repite hasta que cada puntuación sea 8 o más. Después dame el nuevo render.
```

Los problemas que más hay que buscar: texto superpuesto en transiciones, cosas que se deslizan en vez de ajustarse con easing, texto escalado borroso, momentos muertos, y saltos en la costura del loop.

## 8. Entregar

```bash
pnpm run check      # sin errores
pnpm run render     # renders/<slug>.mp4
pnpm run publish    # enlace compartible (opcional)
```

Antes de dar el video por terminado: `check` limpio, ciclo de crítica en 8 o más, y el MP4 revisado a 360 px.

## Problemas comunes

- **La skill no aparece**: reinicia Claude Code después de instalarla.
- **El router no pregunta nada y hace algo raro**: revisa si hay un `BRIEF.md` a medias en el video.
- **`check` marca un warning en el ejemplo en blanco**: es esperado hasta que la composición tenga contenido.
- **Claude empieza a escribir un motor de render propio**: recuérdale que use HyperFrames (ver `CLAUDE.md`, sección "Motor de render").
- **Preview bloqueado**: en agentes usa `npx hyperframes preview --background`, no `pnpm run dev`. Ciérralo con `--stop`.
