# Transcripción final 26/17 (04:29)

[00:00] Hola, mi nombre es Ricardo Chavarría y esto es NG News
[00:03] en español con las últimas novedades de la comunidad de Angular.
[00:06] PrimeNG, la popular librería de componentes de interfaz de usuario,
[00:09] anunció que sus futuras versiones principales
[00:12] ya no estarán disponibles como código abierto,
[00:14] salvo a través de una licencia comunitaria gratuita
[00:17] para personas individuales, estudiantes,
[00:19] organizaciones sin fines de lucro,
[00:20] proyectos open source no comerciales y pequeñas empresas.
[00:24] Esto no solo aplica a la versión de Angular, sino también a la de React y Vue.
[00:28] La razón es que la librería ha crecido con el tiempo,
[00:31] lo que exige dedicarle mucho más trabajo.
[00:33] Y en cierto punto, los ingresos generados por la venta
[00:36] de productos complementarios ya no cubrían los costos de desarrollo.
[00:40] La nueva marca comercial es PrimeUI.
[00:42] El precio de lanzamiento fue de $599 por desarrollador.
[00:46] Una licencia perpetua para las versiones cubiertas
[00:49] que incluye un año de actualizaciones.
[00:51] También da acceso a PrimeUI Pro,
[00:53] que incluye componentes avanzados para gráficos,
[00:56] editor de texto, planificador, tablero de tareas y más.
[01:00] Estos componentes Pro no forman parte de la licencia comunitaria.
[01:03] Ante esto, OpenNG, que se dedica a mantener librerías abandonadas,
[01:07] anunció que PrimeNG cerró su código.
[01:10] El repositorio oficial de GitHub fue archivado
[01:12] el 28 de junio de 2026 y OpenNG creó
[01:16] una copia del proyecto regenerando issues y pull requests pendientes.
[01:20] Su objetivo es lanzar una versión beta compatible con Angular 22 para este fork.
[01:25] Por el momento, el nombre definitivo no está cerrado, ya que OpenNG busca evitar
[01:30] similitudes con PrimeNG debido a los planes de registro de la marca PrimeTek.
--- el panel derecho cambia de tema ---
[01:35] Devin Chasanoff del equipo de Angular publicó
[01:37] un artículo sobre cómo usar A2UI con Angular,
[01:41] lo que permite crear interfaces dinámicas controladas
[01:43] por el modelo de inteligencia artificial.
[01:45] El usuario expresa una intención a través del frontend
[01:48] y este envía dicha intención junto con el contexto relevante a un modelo.
[01:52] Esta comunicación puede incluir además de un catálogo
[01:55] de componentes que el frontend sabe renderizar.
[01:57] El modelo decide si necesitan componentes visuales,
[02:01] cuáles son los más adecuados y devuelve
[02:03] instrucciones estructuradas a la aplicación.
[02:05] A2UI es el protocolo utilizado para estos casos
[02:08] de uso de interfaces generadas por agentes.
--- el panel derecho cambia de tema ---
[02:11] En otras noticias, ha comenzado el trabajo
[02:13] para integrar el comportamiento de resource con router.
[02:16] Apareció un pull request para uso interno
[02:18] que utiliza un comportamiento de tipo snapshot
[02:21] en el routerResource para incorporar información específica de navegación.
[02:25] Ese snapshot congelaría el estado del recurso,
[02:28] por ejemplo, su valor, mientras ocurre la navegación.
[02:31] Una vez que la navegación se completa con éxito, el nuevo valor queda expuesto.
[02:36] Si se cancela, el valor congelado permanece durante la recuperación.
[02:40] Imaginen el caso habitual sin esta funcionalidad.
[02:42] Un recurso tradicional toma como parámetro un dato en la ruta,
[02:46] por ejemplo, un ID de producto, para cargarlo.
[02:48] Si el usuario permanece en el mismo componente,
[02:51] pero navega hacia otro ID de producto,
[02:53] el recurso cambiaría inmediatamente su estado
[02:57] y la interfaz parpadearía durante la navegación.
[03:00] Esto provocaría efectos visuales molestos,
[03:03] sobre todo si un guard cancela la navegación
[03:06] y el ID debe regresar a su valor inicial.
[03:08] Con este nuevo comportamiento, esto ya no sucederá.
[03:12] La descripción del pull request aclara
[03:14] que no está expuesto aún para uso público,
[03:17] pero es claramente el primer paso para hacer
[03:19] que resource y router trabajen juntos.
--- el panel derecho cambia de tema ---
[03:22] Para terminar, la adopción de micro-frontends sigue siendo
[03:25] una decisión arquitectónica común en entornos empresariales.
[03:29] Aunque no sea una característica nativa del framework Angular,
[03:32] existen dos soluciones populares en la comunidad,
[03:35] Native Federation y Module Federation.
[03:38] La diferencia principal en Angular
[03:41] es que Native Federation funciona con esbuild,
[03:44] el builder moderno de Angular,
[03:46] mientras que Module Federation trabaja tradicionalmente
[03:49] con el antiguo Webpack o alternativas como Rspack.
[03:53] Native Federation está mantenido por Angular Architects y el soporte
[03:58] de Module Federation en Nx ha sido
[04:00] el estándar habitual en estos espacios de trabajo.
[04:04] Sin embargo, en la publicación de lanzamiento de Nx 23,
[04:08] el equipo ahora recomienda oficialmente
[04:12] el paquete Native Federation de Angular Architects
[04:14] para Angular, marcando como obsoletos los generadores
[04:18] y ejecutores específicos de Module Federation anteriores dentro de Nx.
[04:23] Y eso es todo.
[04:24] Espero que tengas una excelente semana.
[04:26] Nos vemos en el próximo episodio.
[04:28] Hasta luego.
