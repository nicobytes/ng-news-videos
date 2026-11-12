# Guion Ng-News en español 26/21

Duración estimada: 06:35 (1069 palabras)

## Introducción

Hola, mi nombre es _____ y esto es NG News en español con las últimas novedades de la comunidad de Angular.

## Angular 22.2

Ya fue lanzado Angular 22.2. Y como ahora solo recibimos un major por año, las funcionalidades que llegan en las versiones minor también son bastante importantes. En este caso, hablamos del router resource y los nuevos error boundaries, ambas funcionalidades en developer preview, pero también de la posibilidad de acceder a propiedades privadas desde el template.

## Router resources

Empecemos primero con el router resource. Veamos cómo funciona esto en la práctica. Aquí tenemos una página de vacaciones que usa un service, el cual genera un resource que este componente utiliza. Si volvemos a nuestra aplicación, vemos que una vez que se muestran las vacaciones, también se muestran las distintas tarjetas de cada una.

El problema es que el resource, antes que nada, empieza cuando entramos a la página de vacaciones, es decir, al componente. Y este componente además tiene que manejar el estado de carga, donde quizás el valor todavía no está disponible. Y es precisamente por esto que ahora podríamos usar el router resource.

Así, podría definir el mismo resource, pero ahora en el router, lo que significa que el router esperaría, es decir, bloquearía la navegación, hasta que los datos se carguen, y entonces nuestra página o componente recibiría el valor final.

Entonces tendríamos aquí la propiedad resources, y accedería a mi service de vacaciones con inject. Luego devolvería el resource. Como mi componente va a recibir el valor cargado del resource bajo un nombre determinado, tengo que dar aquí un object literal donde defino con qué nombre quiero registrar ese valor. Así que diría, por ejemplo: estas son las holidays, y devuelvo el resource.

El context también está disponible, como vemos aquí. Recibimos los query parameters y los parámetros normales, y están disponibles como signals en caso de que actúen como parámetros del propio resource. Es decir, si tenemos un id en una URL y ese id cambia, queremos darle ese id como signal al resource para que se actualice automáticamente por nosotros.

Ahora, en el componente, lo que tengo que hacer es decir que estas holidays son simplemente una input property. Entonces diría que la tengo aquí como required con input, donde estoy pidiendo no el resource, sino el array de vacaciones. Y como estamos haciendo un property binding, también necesito hacerla pública.

El último paso es ir a mi config. Tengo que habilitar explícitamente los router resources a través del provider, con provideRouter y withRouterResources. Y eso es todo.

Si ahora vuelvo a la aplicación, hago clic en Home y luego en Holidays, se carga. Y como dije antes, la carga ahora empieza mucho más temprano, ya en la propia navegación del router, y el componente recibe el valor final. Ni siquiera sabe, como acaban de ver, que en realidad está recibiendo el valor de un resource.

## Error boundaries

Pasemos ahora a la segunda funcionalidad, que son los error boundaries. Veamos cómo funcionan. Aquí vemos, primero que todo, un componente app title y un componente app holiday card, es decir, dos componentes hijos.

Si por alguna razón uno de estos componentes hijos lanza un error, entonces nuestros componentes padre también tienen un problema, y toda la página falla. Déjenme ir rápidamente al componente title, donde tenemos el constructor, y ahí, por alguna razón, simplemente lanzo un error. Es decir, algún tipo de error cualquiera, solo para probarlo.

Si ahora vuelvo a la aplicación y hago clic en Holidays, vemos que no se carga nada; mejor dicho, ya no se muestra nada. Y aquí es donde los error boundaries se vuelven muy útiles, porque ahora puedo aislar el error para que no afecte al resto de la página.

Y la forma de hacerlo es a través del template, con una nueva sintaxis. Podría decir que este es un subcomponente riesgoso, y entonces uso un boundary. En caso de que app title falle, el resto debería mostrarse.

Si ahora vuelvo a la aplicación y hago clic de nuevo en Holidays, vemos entonces que las vacaciones se muestran. Y también puedo capturar el error. ¿Por qué usar error? Por supuesto, hay más opciones, donde también puedo definir capturas condicionales, con matches. Pero aquí lo mantenemos muy simple.

Y entonces, podría definir también una especie de fallback, un componente o template, donde simplemente diría: estas son las holidays. Si algo lanza un error y vuelvo, vemos que las vacaciones también se muestran.

## Propiedades privadas en el template

La tercera funcionalidad o cambio principal es la posibilidad de acceder también a propiedades privadas en nuestros templates. Antes de la 22.2, este código no habría sido posible: que yo tenga aquí mis vacaciones y que luego acceda a esa signal title desde el template. Eso solo habría funcionado si title fuera public, o como mucho si fuera protected.

Por eso, en mucho código hoy en día probablemente veremos protected, que significa que solo el template puede acceder a la variable. Con la 22.2, esto va a cambiar. Como ven, simplemente funciona. Y la razón es que para el equipo de Angular era muy importante que entendamos, desde un punto de vista conceptual, que el template, el HTML, y la clase de TypeScript forman en realidad una sola unidad. No son dos partes separadas, es una unidad.

Así que veremos que, con el código moderno de Angular, se usarán cada vez más las palabras clave private. Y lo que también veremos es que el private de ECMAScript desaparecerá. Porque si uso el private de ECMAScript con la notación de hash, eso significa que también es privado en tiempo de ejecución, y entonces esto no funciona. Aquí también obtengo un error, como pueden ver, lo que por supuesto significa que tengo que dejar atrás el de ECMAScript y usar la palabra clave private normal en el futuro.

Y con esto llegamos al final de las tres funcionalidades principales de Angular 22.2, que son las que quería mostrarles hoy. Por razones obvias, los router resources y los error boundaries tienen muchas más opciones que las que he mostrado; esta es solo su funcionalidad básica. Y también llegaron otras funcionalidades en este lanzamiento, como siempre, pero si quieres saber más, consulta la documentación oficial y el changelog. Y, por supuesto, desde la comunidad también hay mucho contenido en forma de videos, artículos y más.

## Cierre

Y eso es todo. Espero que tengas una excelente semana. Nos vemos en el próximo episodio. Hasta luego.
