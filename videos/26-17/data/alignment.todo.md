# alignment todo: 37 EN sentences, 40 ES sentences, EN 299s, ES 274s


## block 0  topic 0  presenter  EN 0.0-7.25
  EN   0 [   0.1] Hello, my name is Michael Small, and this is NG News with the latest updates from the Angular community.

## block 1  topic 0  screen  EN 7.25-25.75
  EN   1 [   7.2] PrimeNG, a popular UI component library, has announced that future major versions won't be available as open source anymore, except through a free community license for individuals, students, nonprofits, non -commercial open source projects, and small organizations.

## block 2  topic 0  presenter  EN 25.75-30.5
  EN   2 [  25.2] That doesn't just apply to the Angular version, but to the React and Vue versions as well.

## block 3  topic 0  screen  EN 30.5-68.25
  EN   3 [  30.1] The reason is that the library has grown over time, which means if you do this as an open source, you have to spend much more time on it, and at some point, the income that they got from selling things around the library itself
  EN   4 [  42.4] didn't cover the costs anymore.
  EN   5 [  44.7] The new licensing brand is Prime UI.
  EN   6 [  47.6] The launch price is $599 USD per developer.
  EN   7 [  52.6] That is perpetual, so for life for the covered versions, and includes one year of updates.
  EN   8 [  58.8] It includes Prime UI Pro, which contains components for charts, text editor, scheduler, task board, and more.

## block 4  topic 0  presenter  EN 68.25-72.25
  EN   9 [  67.7] The Pro components are not part of the community license.

## block 5  topic 0  screen  EN 72.25-97.75
  EN  10 [  72.7] That being said, OpenNG, which maintains unmaintained libraries, announced that PrimeNG went closed source.
  EN  11 [  80.5] source. The GitHub repository was archived on June 28, 2026, and OpenNG created a copy of the project with regenerated open issues and PRs.
  EN  12 [  91.9] Their goal is to release a beta version supporting Angular 22 for the fork.

## block 6  topic 0  presenter  EN 97.75-108.5
  EN  13 [  97.5] At the time of this writing, the current name is outstanding as OpenNG does not want to be too close to PrimeNG because Primetech plans hands to put trademarks on it.

## block 7  topic 1  screen  EN 108.5-119.5
  EN  14 [ 109.1] Devon Chastanoff from the Angular team has published an article on how to use A2UI with Angular, which enables dynamic UI that is controlled by an AI model.

## block 8  topic 1  presenter  EN 119.5-122.25
  EN  15 [ 119.4] The user expresses an intent through the front end.

## block 9  topic 1  screen  EN 122.25-146.5
  EN  16 [ 122.6] Front end sends that intent in relevant context to a model.
  EN  17 [ 125.9] This communication can also include a component catalog that the front end knows how to render.
  EN  18 [ 131.3] The model can then decide whether UI components are needed, which components are appropriate, and return structured UI instructions to the application.
  EN  19 [ 141.6] A2UI is a protocol used for these agent -generated UI use cases.

## block 10  topic 2  presenter  EN 146.5-152.25
  EN  20 [ 146.5] In other news, work on integrating resource behavior with the router seems to have begun.

## block 11  topic 2  screen  EN 152.25-186.75
  EN  21 [ 152.1] PR meant for internal usage at the moment popped up, which uses a snapshot -like router resource behavior to integrate great navigation specific information.
  EN  22 [ 163.0] That snapshot would freeze a resource's state, for example, the value, while a navigation happens.
  EN  23 [ 169.8] Once the navigation succeeds, the underlying value is exposed.
  EN  24 [ 174.2] And if a navigation is canceled, the frozen value would still be there during rollback recovery.
  EN  25 [ 180.7] Now imagine the following use case without this router resource behavior.

## block 12  topic 2  presenter  EN 186.75-220.75
  EN  26 [ 187.3] Regular old resource has a router parameter as its own parameter.
  EN  27 [ 191.2] That could be a product ID which loads the product by its given ID.
  EN  28 [ 195.6] If the user stays on the same component but navigates to a different product ID, the resource would immediately change its state and the UI would change while the navigation happens.
  EN  29 [ 207.2] That would cause flickering effects, especially if the navigation gets cancelled via guard and the product ID changes back to its initial value.
  EN  30 [ 215.8] With the introduced router resource source behavior that is not going to happen.

## block 13  topic 2  screen  EN 220.75-235.0
  EN  31 [ 220.8] Again, PR's description explicitly states that this is not currently exposed for public use, but it is very likely the start of getting resources and the router working together.

## block 14  topic 3  presenter  EN 235.0-244.75
  EN  32 [ 234.5] In other news, going with micro front -ends is an architectural choice, which we find often in enterprises.

## block 15  topic 3  screen  EN 244.75-267.0
  EN  33 [ 241.5] Although they are not an Angular framework feature, feature, there are two common community solutions in the form of Native Federation and Module Federation.
  EN  34 [ 251.4] The main distinction in Angular is that Native Federation works with ESBuild, so the modern Angular builder, and Module Federation traditionally works with the old Webpack builder or alternative builders such as RSPack.

## block 16  topic 3  presenter  EN 267.0-276.75

## block 17  topic 3  screen  EN 276.75-291.75
  EN  35 [ 266.2] native federation is maintained by angular architects and module federation support in nx has been common for angular workspaces in the release blog for nx 23 nx now recommends angular architects native federation package for angular and deprecates the older nx specific module federation generators

## block 18  topic 3  presenter  EN 291.75-298.75
  EN  36 [ 290.0] and executors and that's it i wish you a nice week and see you in the next step so goodbye


# ES sentences

  ES   0 [   0.9-   6.7] Hola, mi nombre es Ricardo Chavarría y esto es Engie News en español con las últimas novedades de la comunidad de Angular.
  ES   1 [   7.0-  23.1] Prime Engie, la popular librería de componentes de interfaz de usuario, anunció que sus futuras versiones principales ya no estarán disponibles como código abierto, salvo a través de una licencia comunitaria gratuita para personas individuales, estudiantes, organizaciones sin fines de lucro, proyectos open source no
  ES   2 [  23.1-  24.5] comerciales y pequeñas empresas.
  ES   3 [  24.5-  29.1] empresa. Esto no solo aplica a la versión de Angular, sino también a la de React y Vue.
  ES   4 [  29.2-  34.6] La razón es que la librería ha crecido con el tiempo, lo que exige dedicarle mucho más trabajo.
  ES   5 [  34.9-  40.6] Y en cierto punto, los ingresos generados por la venta de productos complementarios ya no cubrían los costos de desarrollo.
  ES   6 [  41.8-  44.0] La nueva marca comercial es Prime UI.
  ES   7 [  44.3-  48.0] El precio de lanzamiento fue de $599 por desarrollador.
  ES   8 [  48.3-  53.1] Una licencia perpetua para las versiones cubiertas que incluye un año de de actualizaciones.
  ES   9 [  53.3-  61.6] También da acceso a Prime UI Pro, que incluye componentes avanzados para gráficos, editor de texto, planificador, tablero de tareas y más.
  ES  10 [  61.7-  64.9] Estos componentes Pro no forman parte de la licencia comunitaria.
  ES  11 [  65.8-  72.5] Ante esto, OpenNG, que se dedica a mantener librerías abandonadas, anunció que PrimeNG cerró su código.
  ES  12 [  72.6-  82.5] El repositorio oficial de GitHub fue archivado el 28 de junio de 2026 y OpenNG creó una copia del proyecto regenerando issues y pull requests pendientes.
  ES  13 [  82.5-  87.8] Su objetivo es lanzar una versión beta compatible con Angular 22 para este fork.
  ES  14 [  88.0-  97.2] Por el momento, el nombre definitivo no está cerrado, ya que OpenAngie busca evitar similitudes con PrimeAngie debido a los planes de registro de la marca PrimeTech.
  ES  15 [  97.8- 107.8] Serge Chassanov del equipo de Angular publicó un artículo sobre cómo usar A2UI con Angular, lo que permite crear interfaces dinámicas controladas por el modelo de inteligencia artificial.
  ES  16 [ 108.1- 114.6] El usuario expresa una intención a través del frontend y este envía dicha intención junto con el contexto relevante a un modelo.
  ES  17 [ 115.3- 120.3] Esta comunicación puede incluir además de un catálogo de componentes que el frontend sabe renderizar.
  ES  18 [ 120.5- 128.4] El modelo decide si necesitan componentes visuales, cuáles son los más adecuados y devuelve instrucciones estructuradas a la aplicación.
  ES  19 [ 128.8- 133.9] A2UI es el protocolo utilizado para estos casos de uso de interfaces generadas por agente.
  ES  20 [ 134.6- 139.4] En otras noticias, ha comenzado el trabajo para integrar el comportamiento de resource con router.
  ES  21 [ 140.0- 148.8] Apareció un pull request para uso interno que utiliza un comportamiento de tipo snapshot en el router result para incorporar información específica de navegación.
  ES  22 [ 149.1- 154.7] Ese snapshot congelaría el estado del recurso, por ejemplo, su valor, mientras ocurre la navegación.
  ES  23 [ 154.8- 159.5] Una vez que la navegación se completa con éxito, el nuevo valor queda expuesto.
  ES  24 [ 159.7- 163.7] Si se cancela, el valor congelado permanece durante la recuperación.
  ES  25 [ 164.6- 167.1] Imaginen el caso habitual sin esta funcionalidad.
  ES  26 [ 167.2- 172.2] Un recurso tradicional toma como parámetro un dato en la ruta, por ejemplo, un ID de producto, para cargarlo.
  ES  27 [ 172.8- 183.9] Si el usuario permanece en el mismo componente, pero navega hacia otro ID de producto, el recurso cambiaría inmediatamente su estado y la interfaz parpadearía durante la navegación.
  ES  28 [ 184.3- 192.6] Esto provocaría efectos visuales molestos, sobre todo si un guard cancela la navegación y el ID debe regresar a su valor inicial.
  ES  29 [ 193.5- 196.7] Con este nuevo comportamiento, esto ya no sucederá.
  ES  30 [ 196.8- 206.8] La descripción del pull request aclara que no está expuesto aún para uso público, pero es claramente el primer paso para hacer que resource y router trabajen juntos.
  ES  31 [ 207.6- 214.9] Para terminar, la adopción de micro -frontends sigue siendo una decisión arquitectónica común en entornos empresariales.
  ES  32 [ 215.1- 223.0] Aunque no sea una característica nativa del framework Angular, Existen dos soluciones populares en la comunidad, Native Federation y Model Federation.
  ES  33 [ 223.4- 238.2] La diferencia principal en Angular es que Native Federation funciona con Sbuild, el builder modelo de Angular, mientras que Model Federation trabaja tradicionalmente con el antiguo Webpack o alternativas como Rspack.
  ES  34 [ 238.2- 259.0] native federation está mantenido por angular architect y el soporte de model federation en nx ha sido el estándar habitual en estos espacios de trabajo sin embargo en la publicación de lanzamiento de nx 23 el equipo ahora recomienda oficialmente el paquete native federation de
  ES  35 [ 259.0- 268.6] angular architect para angular marcando como obsoletos los generadores y ejecutores específicos del módulo Federation anteriores dentro de NX.
  ES  36 [ 268.8- 269.8] Y eso es todo.
  ES  37 [ 269.9- 271.8] Espero que tengas una excelente semana.
  ES  38 [ 272.0- 273.6] Nos vemos en el próximo episodio.
  ES  39 [ 273.6- 274.2] Hasta luego.
