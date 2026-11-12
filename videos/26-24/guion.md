# Guion Ng-News en español 26/24

Duración estimada: 03:58 (645 palabras)

## Introducción

Hola, mi nombre es _____ y esto es NG News en español con las últimas novedades de la comunidad de Angular.

## Primeros benchmarks del compilador en Rust

Ya cubrimos la reescritura del compilador de Angular, o del pipeline, en Rust y Oxc, en los episodios anteriores. Y ahora tenemos, por primera vez, números oficiales sobre las mejoras de rendimiento. Cédric Exbrayat, de Ninja Squad, ejecutó tres benchmarks diferentes.

Descubrió que era aproximadamente dos o tres veces más rápido. Y en los proyectos más grandes, con más de 1000 componentes, el uso de memoria bajó cerca de un 50 %.

Como sabemos, el equipo de TypeScript mencionó una mejora de rendimiento de diez veces. Pero, como suele ocurrir, un pipeline de build como el de Angular no es solo la compilación de TypeScript. Tiene más partes. Y por eso no veremos la cantidad máxima que reportó el equipo de TypeScript.

Aun así, ya pueden probarlo. Brandon Roberts, del proyecto Analog, ha añadido soporte experimental para NGP, que es el nuevo pipeline del compilador, en el plugin de Vite de Analog. Analog es un meta framework para Angular, y allí pueden probarlo y ver los resultados por ustedes mismos.

## OpenAPI Generator con httpResource

Cuando trabajamos con una aplicación donde el backend está escrito en otro lenguaje, o quizás cuando usamos microservicios, siempre es un reto llevar el control de los endpoints y de los tipos de las respuestas y de las solicitudes. Podemos escribir ese código manualmente, o puede escribirlo un agente por nosotros, o podemos usar generadores de código que lo hagan de forma automática.

El más popular es OpenAPI, y hasta ahora teníamos el problema de que producía código usando el antiguo HttpClient y, por lo tanto, también observables. Por fin eso ha cambiado. Con la versión 7.27.0, por fin tenemos soporte también para httpResource.

Dicho esto, ya existían proyectos de la comunidad que podían hacerlo, pero ahora forma parte del propio OpenAPI Generator oficial.

## slide.ng

Slidev es una herramienta muy popular para desarrolladores que necesitan dar charlas. Les permite escribir las diapositivas en Markdown, lo que les da mucha más flexibilidad que otras herramientas comunes. Slidev además incluye muchas funcionalidades. Por ejemplo, soporta live coding, soporta la visualización del propio código, también gráficos, diagramas con Mermaid, zoom o modo presentador, y mucho más.

Sin embargo, el propio Slidev está construido con Vue. Ahora hay una herramienta inspirada en Slidev que está construida con Angular. Se llama slide.ng y la creó Erkam Yaman.

Ya lo presentamos en el episodio anterior de NG News, cuando hablamos de Pangular Inspector, el proyecto de devtools de Angular en el que trabaja junto con Santosh Yadav. También ha contribuido a Angular Native, que lidera Ashley Hunter. Así que este es otro buen proyecto que ahora tenemos para Angular.

## Más novedades de la comunidad

TanStack Query te ayuda a manejar el estado del servidor. Se encarga de cosas como obtener y almacenar en caché los datos, y también está disponible para Angular. Armen Vardanyan hizo un stream práctico en Angular Space para mostrar cómo funciona en una aplicación Angular.

Los error boundaries son un poco como un try-catch para los templates. Con el nuevo bloque @boundary de Angular 22.2, puedes mostrar un fallback si una parte de tu template falla al renderizarse. Igor Sedov, quien hace esos videos animados sobre Angular, tiene un nuevo video sobre cómo funciona.

Para terminar, Storybook suele ser la primera herramienta que viene a la mente cuando quieres mostrar componentes en una galería. También existen herramientas creadas específicamente para Angular, y ng-prism es una de ellas. En su versión 22.7 puede generar páginas de API para services y pipes. Además, les da a los componentes y a las directivas el mismo formato de página de API. Alexander Spies explica en detalle qué hay de nuevo en su release en el artículo que escribió.

## Cierre

Y eso es todo. Espero que tengas una excelente semana. Nos vemos en el próximo episodio. Hasta luego.
