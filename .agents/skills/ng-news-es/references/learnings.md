# Aprendizajes del pipeline NG News ES

Lo que se aprendió produciendo el episodio 26-17. Léelo antes de cambiar el pipeline: cada punto costó tiempo o calidad.

## Decisiones del formato

- **El panel derecho NO se traduce.** Título y viñetas se quedan en inglés, igual que el original. Solo cambian el presentador, el audio y los subtítulos.
- **El EN es la capa base.** Marco, logo, panel derecho y grabaciones de pantalla son píxeles originales. Encima solo van `#capbar` (tapa los subtítulos EN), el presentador ES y los subtítulos ES. Reconstruir el marco en HTML era más código y peor resultado.
- **Fuente de video: archivos locales, no YouTube.** Los originales van en `videos/<slug>/assets/ng-news-<slug>-{en,es}.mp4`. Descargar de YouTube puede bajar calidad; la URL queda como último recurso.
- **Salida en 4K** (`--resolution 4k -q delivery`). El panel izquierdo usa `presenter.mp4` a 1500×844, que es exactamente 2× el panel.

## Transcripción

- **Usa faster-whisper (CTranslate2) en la GPU.** 34 s por 5 min de audio.
- `hyperframes transcribe` (whisper.cpp) corre en CPU en esta máquina: más de 10 min por archivo.
- El pipeline de `transformers` con `return_timestamps="word"` es inservible en audio largo: con `batch_size=8` llena los 24 GB de VRAM y con batch 2 tampoco terminó en 10 min. Su prueba de 60 s engañó (0.7× tiempo real).
- **No uses `hotwords` ni `initial_prompt`.** Probado: arreglan algunos nombres pero inventan otros errores ("junio de 1926", "el plugin sabe", "este port") y borraron una frase entera. Mejor transcripción neutra + corrección.
- **Modelo sin descargar:** la red va a ~0,4 MB/s. `ct2-transformers-converter` convierte el `openai/whisper-large-v3` de la caché de HF en segundos (ver `SETUP.md`). Si `transcribe.py` parece colgado con CPU y GPU casi quietas, está descargando.
- Requiere `nvidia-cublas-cu12` y `nvidia-cudnn-cu12`, y que `LD_LIBRARY_PATH` esté puesto antes de arrancar el proceso (`transcribe.py` se re-ejecuta a sí mismo).

## Corrección de texto

- **Whisper se equivoca sobre todo en nombres propios y términos técnicos**, en ambos idiomas: "Engie News", "Serge Chassanov", "router result", "Sbuild".
- **El subtítulo quemado del EN es la fuente fiable de grafías** (Devin Chasanoff, PrimeTek). El transcript EN también los escribe mal. Recorta la barra en el momento del nombre y léela.
- Dos niveles: `glossary.json > asr_fixes` para errores que se repiten en todos los episodios (`fix_terms.py`), y `data/caption_fixes.json` para los del episodio. Los arreglos conservan el tiempo de las palabras.
- Revisa el texto completo una vez: también hay palabras repetidas ("de de"), mayúsculas sueltas y puntuación faltante.

## Segmentación

- Clasificar por similitud de píxeles falla: las pantallas oscuras de código forman el grupo más grande y las etiquetas salen invertidas.
- **Detección de cara (Haar) + comparación del fondo con el del presentador** acertó todos los bloques de 26-17 y distingue a invitados con webcam.
- `opencv-python-headless` debe ser `<5`: OpenCV 5 quitó `CascadeClassifier`.
- El EN usa cortes secos, sin fundidos. Muestrear a 4 fps deja el límite hasta 0,25 s fuera de sitio y **el host EN asomaba 2-3 frames en el corte**. `segment_en.py` ajusta cada límite al corte real (`exact_cut`, salto máximo entre frames a 30 fps).
- Un plano del host de menos de 1,5 s se funde con el bloque anterior y quedaría visible en un bloque `screen`: `segment_en.py` lo avisa con `WARNING`.

## Tiempos y composición

- El audio ES manda. El EN se ajusta con `data-playback-rate`, siempre ≤ `enLen / duración ES` para no invadir el bloque siguiente, y a 1,25× como máximo.
- El narrador ES sigue el mismo guion y orden, así que alinear por significado es directo. El ES suele ser ~8 % más corto.
- Los bloques pueden no tener frase EN propia (una frase larga cruza dos bloques): reparte el ES por contenido.

## Subtítulos

- `/embedded-captions` trae un pipeline de matte para quemar texto sobre una persona. Aquí la barra es negra, sin nadie detrás: se usa su contrato de *rail* (≤ 2 líneas, cortes por cláusula, 1-2 palabras de énfasis), no sus motores.
- La palabra activa se **eleva** 5 px. Con escala invadía el espacio de la palabra anterior ("es|NG").
- La línea entra 0,14 s antes de su primera palabra; si no, esa palabra se pronuncia durante el fundido y se pierde. Nunca antes de que termine la palabra anterior.
- Una frase puede cruzar un corte de plano cuando los clips siguen la misma toma; si no, el corte la parte a mitad ("...Federation de / Angular Architects").
- El gris de las palabras pendientes es `#8b8b99`: más oscuro no se lee a 360 px.
- Faster-whisper a veces une un término en un solo token tras `fix_terms.py` ("Native Federation"). En `caption_fixes.json` usa espacio duro para mantenerlo unido.

## Audio

- **La grabación ES llega a −28 LUFS**, muy baja para YouTube. `compose.mjs` genera `voice.wav` a −16 LUFS con `loudnorm`. `review.sh` mide los LUFS del render.

## Revisión

- El borrador 1080p usa captura `beginframe` y a veces deja negro el primer segundo y medio. Es del borrador: la captura por screenshot de `--resolution 4k` no lo tiene. El dato que vale es `checks.json` del final.
- **Comprueba la fecha del render antes de opinar.** Un `review.sh` en segundo plano deja los PNG viejos hasta terminar; se revisó una vez material antiguo por error. `[ checks.json -nt index.html ]`.
- Whisper estira a veces una palabra sobre una pausa ("marcando" 1,18 s): su relleno arranca hasta 0,7 s antes. Es raro (p95 de 50 ms) y no se corrige.
- Sin medir no hay nota: `verify_sync.py` retranscribe el render y compara con los subtítulos. Una nota de sincronía sin ese dato no vale.
- `captions.png` muestra cada subtítulo para leerlos todos. Una hoja de contactos no alcanza para corregir texto.
- **Las tiras de corte tienen que ir a 30 fps y ±0,2 s.** A 10 fps el flash del host EN no se veía; el primer ciclo de revisión lo dio por bueno.
- Los avisos `timeline_track_too_dense` y `nested_structure_needs_subcomposition` de `check` son de estilo del Studio y no afectan al render.
- `--limit 30` en `compose.mjs` da una prueba corta a 4K en ~2,5 min antes de pagar el render completo.

## Tiempos de referencia (5 min de video, RTX 3090, 24 núcleos)

| Paso | Tiempo |
|---|---|
| Transcripción EN + ES | ~70 s |
| `hq.mp4` (EN 4K H.264) | ~3 min |
| Borrador 1080p | ~8,5 min |
| Final 4K | ~15 min |
| `review.sh` sobre el final | ~2 min |

## Guion

- **El presentador varía**: Ricardo Chavarría en 26-17, Nicolás Molina en 26/11. Es un dato de `data/episode.json`, no una constante.
- La versión ES dura 92 % del EN en los dos episodios medidos y usa 100-109 % de sus palabras: **no es un resumen**. El primer guion de prueba, con la instrucción de "apretar", quedó en 80 %. Ritmo: 2,6 palabras/s Ricardo, 2,8 Nicolás.
- **Una webcam de invitado no indica entrevista**: en 26/11 el host narra encima de todas.
- **Whisper puede saltarse por completo la voz de un invitado** y estirar las palabras vecinas sobre el hueco (`and@328 she@333 also@336`). La entrevista de Martina Kraus no estaba en el transcript. Los subtítulos quemados sí la tienen.
- Detección: huecos de más de 2 s entre palabras con audio (la encontró, 0 falsos positivos) y 3+ frases seguidas con otra voz por MFCC (probado insertando una voz). Una frase suelta da falsos positivos.
- Los subtítulos quemados son el guion EN exacto: mejor fuente que el transcript.
- **Los límites de una entrevista salen de los cambios de subtítulo quemado**, no de estimaciones. El límite a ojo de 26/11 (341 s) metía casi 1 s de voz del host; el real es 340,3 s.
- Transcribir el clip de la entrevista aislado sí funciona: sirve para confirmar que solo contiene al invitado.
- El audio EN está a -32 LUFS: cada entrevista se normaliza aparte a -16 LUFS para igualar al host.

## Metadata de YouTube

- Se genera al final con `/ng-news-youtube`, sobre `data/timeline.json`: los tiempos de la grabación ES no sirven para capítulos.
- YouTube pide 3 capítulos como mínimo y 10 s por capítulo, **incluidos el primero y el último**. Una "Introducción" de 6 s o una "Despedida" de 6 s invalidan todos. El episodio 26/11 publicado tiene una introducción de 6 s.
- Los links salen de la descripción del episodio EN, que `prepare` busca por número en @ng-news sin descargar video.

## Trampas del entorno

- `cp` tiene alias interactivo y se queda esperando: usa `/bin/cp -f`.
- `pkill -f <patrón>` mata a la propia shell si el patrón aparece en su línea de comando. Usa el PID o `pkill -x`.
- En zsh, `echo == x` falla: `==` se expande. Usa comillas.
- `/tmp` es tmpfs de 24 GB: `HYPERFRAMES_EXTRACT_CACHE_DIR` debe apuntar al disco.
