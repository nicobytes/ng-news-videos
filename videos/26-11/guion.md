# Guion Ng-News en español 26/11

Duración estimada: 06:22 (1033 palabras)

## Introducción

Hola, mi nombre es Nicolás Molina y esto es NG News en español con las últimas novedades de la comunidad de Angular.

## TypeScript 6

La versión 6 de TypeScript ya está disponible. Y como ya mencionamos hace algunos episodios, esta es la última versión escrita en el propio TypeScript. La siguiente estará escrita en Go.

Para nosotros como desarrolladores de Angular, en la versión 21 todavía tenemos TypeScript 5.9 como peer dependency, pero en las ramas de Git de la versión 22 ya tienen TypeScript 6.

Como TypeScript 6 pretende ser un puente entre las versiones antiguas y las nuevas, viene con muchas deprecaciones. Pero también actualiza sus configuraciones por defecto para reflejar cómo funciona el ecosistema en 2026.

Eso significa que el modo strict viene activado por defecto. La opción module ahora usa ESNext por defecto, así que en la práctica, en los proyectos nuevos estás en el mundo de los módulos de ECMAScript. Y target se ajusta al año actual de ECMAScript, que en este momento es ES2025.

En cuanto a las deprecaciones, target ES5 va de salida. Ese es el mundo de antes de las clases, las arrow functions, las promises, let o const, los template strings y todo lo demás. Para la mayoría de nosotros, eso ya es historia antigua de todos modos.

La opción baseUrl en tsconfig.json también queda obsoleta. Y el soporte para AMD, UMD y SystemJS como formatos de salida de módulos también está deprecado.

Por supuesto, también puedes optar por no aplicar todas esas deprecaciones, pero ten cuidado: en TypeScript 7 eso significaría game over.

También vale la pena mencionar que hay una herramienta de migración experimental disponible para pasar de TypeScript 5 a TypeScript 6.

Y TypeScript 6 no solo trae deprecaciones, también trae novedades. Una de ellas es la API Temporal, una nueva API de fecha y hora ya estandarizada que reemplaza al antiguo objeto Date.

Como tal, ofrece mucha más funcionalidad. Por ejemplo, zonas horarias, un calendario que se puede usar para reflejar el sistema chino u otros sistemas de calendario, inmutabilidad y una gama de otras funciones útiles.

Algunos veteranos recordaremos el cambio a la API de fecha y hora en Java, hace más de diez años. En cierto modo, se siente así.

## NgRx: delegatedSignal

NgRx es la librería de gestión de estado más usada en Angular, y ya empezó oficialmente el trabajo para soportar resources y también Signal Forms. Se han publicado dos nuevos RFC.

El primer RFC está relacionado con el soporte de Signal Forms e introduce un nuevo tipo de signal llamado delegatedSignal. Hacia afuera es un writable signal, pero no almacena ningún valor. En su lugar, lee y escribe en otro signal.

¿Para qué sirve esto? Digamos que tenemos un objeto de usuario en un signal, que tiene dos propiedades anidadas: name y address. Name tiene nombre y apellido, y address tiene calle y ciudad.

Si tenemos un formulario que requiere una versión aplanada del objeto de usuario, normalmente crearíamos un linkedSignal. El problema es que los cambios en el formulario podrían tener que sincronizarse de vuelta con el signal original. Por el momento, la única forma de hacerlo sería usar un effect, lo que sería una sincronización asíncrona.

delegatedSignal, por otro lado, resuelve este problema escribiendo de forma síncrona de vuelta en el signal original.

delegatedSignal también se puede usar para otros casos, pero la idea para el SignalStore es que, si usas Signal Forms, cada cambio en un campo del formulario actualice el estado de inmediato.

En cierto modo, puedes ver delegatedSignal como un linkedSignal mejorado, donde no se crea un clon, sino que los cambios se escriben directamente en el signal original.

## NgRx: extensiones de resource

El otro RFC trata sobre el soporte de resources. Permite extender un resource, lo que va más allá de las posibilidades de la función snapshot actual.

Por ejemplo, una extensión podría cambiar el comportamiento de un resource en estado de error, para que acceder a su valor no lance una excepción. También se pueden crear extensiones personalizadas, e incluso hay una opción para definir extensiones por defecto.

Los dos RFC son de Marko Stanimirovic, que también fue invitado en un episodio anterior del Angular Plus Show. Así que si te interesa saber más sobre gestión de estado y sobre el SignalStore en particular, deberías ver ese episodio.

## Martina Kraus y seguridad

En otras noticias, Martina Kraus fue invitada al Angular Plus Show, así que el tema fue la seguridad.

Junto a los tres presentadores, Lara Newsom, Brooke Avery y Jan-Niklas Wortmann, discutieron todo el abanico de temas de seguridad. Ya sean trusted types, sanitization, ataques como cross-site scripting o cross-site request forgery, pero también políticas de contenido y el mayor riesgo que llega con la IA.

Al final, Martina dio algunos consejos sobre por dónde empezar con la seguridad.

> ENTREVISTA 05:28-05:41: no se graba, queda el audio original con subtítulos.

También destacó OWASP Juice Shop, que está escrito en Angular y es un entorno para probar distintas vulnerabilidades.

## Tercera opción de debounce

Además, Angular tendrá una tercera opción de debounce. La primera fue la función debounce de Signal Forms, lo que significa que el debounce ocurre entre un campo del formulario y su modelo. La segunda es la función debounced, que se puede usar con cualquier signal. Y la nueva, la tercera, es para los validadores asíncronos de Signal Forms.

Esto permite tener validadores síncronos sin debounce, pero aplicar el debounce en un validador asíncrono.

Esa funcionalidad ya se integró en la rama de la versión 22, pero no llegó a la última versión, la 21.2.7. Así que parece que habrá que esperar a Angular 22.

## SpecKit Companion

Alfredo Pérez publicó una serie de tres artículos sobre spec-driven development con IA. Probablemente la herramienta más popular es SpecKit de GitHub, que Alfredo describe en sus artículos.

Pero además, creó una extensión de VS Code llamada SpecKit Companion, no solo para visualizar, sino también para editar y ejecutar esas especificaciones.

Como SpecKit de GitHub no es la única herramienta que existe, Alfredo también muestra alternativas y cómo se puede configurar SpecKit Companion para soportar esas herramientas.

## Angular Graz Meetup

Para terminar, las grabaciones del Angular Graz Meetup ya están disponibles en YouTube. No se publican todas de una vez, sino en intervalos regulares.

## Cierre

Y eso es todo. Espero que tengas una excelente semana. Nos vemos en el próximo episodio. Hasta luego.
