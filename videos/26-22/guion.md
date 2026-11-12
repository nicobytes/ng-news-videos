# Guion Ng-News en español 26/22

Duración estimada: 06:24 (1039 palabras)

## Introducción

Hola, mi nombre es _____ y esto es NG News en español con las últimas novedades de la comunidad de Angular.

## TypeScript 7.1 y el compilador de Angular

Empecemos con algo de contexto. El código de Angular no lo compila TypeScript directamente. En su lugar, usa un compilador de Angular que se sitúa encima de TypeScript. TypeScript 7 es la última versión y ha sido reescrito en Go. Promete diez veces más rendimiento en la compilación. Y, por supuesto, un cambio tan grande en TypeScript también tiene un enorme impacto en Angular, y de eso quiero hablarles.

El compilador de Angular usa una API programática para analizar y también modificar nuestro código TypeScript. De cierta forma, pueden ver esa API programática como si Angular importara TypeScript como una librería. Ahora bien, esa API programática no está disponible en TypeScript 7.

Esto, de por sí, no es realmente un problema, al menos por ahora, porque TypeScript 7.0 es compatible con TypeScript 6, lo que significa que Angular puede usar la API programática de TypeScript 6.

Ahora bien, si Angular quiere soportar TypeScript 7.1, tiene que usar la API programática. Y aquí está el problema: Angular está escrito en TypeScript, y de repente necesita usar una librería de una aplicación que ha sido escrita en Go.

TypeScript solucionará esto mediante una API de interoperabilidad, o interop, pero esa no soportará la transform API, que es justo la que Angular necesita.

Por eso, el plan que tienen es que Angular use Oxc, que está escrito en Rust y ya se usa en herramientas muy populares como Vite. A grandes rasgos, Angular usa Oxc para analizar y preparar sus pasos de compilación.

Para entender esto mejor, lo que necesitamos saber es que Angular tiene dos pipelines diferentes. En el primero, Angular toma, por ejemplo, los decoradores y otras cosas de TypeScript, y convierte ese código en código TypeScript, que luego entrega al compilador de TypeScript.

El otro es solo para la verificación de tipos. Aquí es donde el template también se compila en un formato muy específico, para que el compilador de TypeScript pueda ejecutar verificaciones sobre él.

Al final, ambos serán ejecutados por el propio compilador de TypeScript, lo que significa que obtendremos estas mejoras de velocidad. Al momento de grabar este episodio, el pull request ya se ha fusionado en main, así que quizás ya tengamos una versión de esto en la próxima versión 22.3 de Angular.

## Angular Native

En otras noticias, hay que reconocer que desarrollar aplicaciones nativas con Angular nunca ha sido una alegría. Por supuesto, tenemos Ionic, pero ese renderiza en un web view, lo que requiere un middleware. También tenemos NativeScript, que usa interfaces de usuario nativas, pero nunca tuvimos algo como React Native, con un renderer probado en producción y un ecosistema enorme como Expo, que soporta todo el ciclo de vida del desarrollo.

El 29 de septiembre, esto cambió. Ashley Hunter lanzó Angular Native, que ha ganado cierta tracción en cuanto a contribuidores. Es un proyecto independiente de la comunidad, es decir, no es oficial, y actualmente está en alpha.

Y lo genial es que el renderer de React Native, que se llama Fabric, no depende de React. Lo que suele pasar es que React le dice a Fabric qué partes del árbol de componentes tienen que cambiar. Y la idea de Ashley fue usar un renderer de Angular en lugar de React.

El renderer de Angular normalmente habla con el DOM, pero se puede escribir un renderer propio para que ahora hable con Fabric. Esta idea de usar un renderer distinto ya se ha probado en el pasado. Por ejemplo, Chau Tran usa el mismo enfoque en su librería Angular 3. Para nosotros, esto significa entonces que podemos construir sobre una implementación de renderer a prueba de balas y bien mantenida. Y con Angular Native, ahora tenemos entonces un proyecto de la comunidad que ofrece la integración usando extensiones oficiales del renderer de Angular.

Como es nativo y no DOM, y a diferencia de Ionic, que usa un web view, tampoco podemos usar sin más los componentes existentes ni las librerías de UI que dependen del navegador. Para la UI nativa, tenemos que usar los componentes nativos. Las etiquetas conocidas como div y p sí funcionan, pero se mapean a vistas y texto nativos.

Hay una excepción, sin embargo. El componente DOM nos permite incrustar web components existentes de Angular, pero esa parte se ejecuta en un web view. La lógica, en cambio, puede quedarse, siempre que no dependa de APIs del navegador.

Angular Native también fue más allá e integró Tailwind, el router de Angular, hot reload y una librería de testing. Soporta el entorno de build de React Native, con el bundler Metro y Expo, que es algo parecido a lo que NX o Angular CLI son para Angular. Así que Angular no solo corre sobre React Native, sino que además desbloquea el acceso a todo su ecosistema.

## Polymorpheus

Para terminar, imagina que estás diseñando una librería de UI de uso general. Entonces tienes que soportar distintos casos de uso, y eso puede volverse bastante complicado. Por ejemplo, puede empezar con un simple string como input. Eso podría ampliarse y soportar también una función, porque el componente se llama dentro de un contexto y necesitamos acceso a ese contexto. Luego, los usuarios podrían querer añadir HTML, un template, o incluso un componente.

Piensen en un tooltip, por ejemplo, que todos conocemos. Puede que tengan un título sencillo, pero luego ese tooltip se ejecuta dentro de un loop y quieren acceder al elemento actual o algo así. Y más adelante, quizás quieran darle cierto formato HTML a ese tooltip en particular, algo que tampoco es tan sencillo.

Entonces, si eres el autor de un componente así, se necesita mucho trabajo para que ese componente sea aplicable a todos esos casos de uso.

Alex Inkin es el desarrollador líder detrás de Taiga UI, y ese tipo de desafíos son, por así decirlo, su pan de cada día. Alex ha publicado un artículo en Angular Space donde presenta su librería Polymorpheus, optimizada justo para estos desafíos. Se usa dentro de Taiga UI, y nosotros también podemos usarla.

## Cierre

Y eso es todo. Espero que tengas una excelente semana. Nos vemos en el próximo episodio. Hasta luego.
