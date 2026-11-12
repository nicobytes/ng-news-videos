# Guion Ng-News en español 26/20

Duración estimada: 05:05 (824 palabras)

## Introducción

Hola, mi nombre es _____ y esto es NG News en español con las últimas novedades de la comunidad de Angular.

## Optimus UI y NG Switzerland

Empecemos con una noticia sobre Optimus UI. En el episodio 26/17 explicamos que PrimeNG, una librería de UI muy popular, se está convirtiendo en un producto comercial. Y justamente por eso nació Optimus UI, como un fork de PrimeNG que mantiene la librería totalmente open source, sin requerir ninguna licencia adicional.

Optimus UI se publicó primero como versión 1, y después llegó la versión 2, que lo alinea con Angular 22.

Y ahora Dominik Bachmann, que está detrás de OpenNG, la organización que aloja a Optimus UI y también a otros proyectos, ha empezado a organizar una conferencia en Suiza.

NG Switzerland se celebrará en febrero del próximo año. La convocatoria de ponencias ya está abierta y la venta de entradas también ha comenzado. Así que, para nosotros, eso la convierte en la primera conferencia ya confirmada del próximo año.

## Angular Space

En otras noticias, Armin Fardanyan ha vuelto con nuevos episodios de su podcast Angular Space. Ya tenemos tres episodios nuevos: uno sobre machine learning, otro sobre agentic UI, en el que también participé, y otro sobre RAG. Es decir, al final, los tres episodios nuevos se centran muchísimo en temas de inteligencia artificial alrededor de Angular.

Angular Space no es solo un podcast, sino también una plataforma donde los desarrolladores pueden publicar sus artículos. Recientemente se publicaron cuatro artículos nuevos de Jaroslav Solnovsky, Pavel Ostrometsky y Emmanuel Ojibo.

## Micro-frontends

Stefan Haas, senior software engineer en Microsoft, escribió un artículo bastante detallado sobre micro-frontends. En particular, analiza las diferencias entre los enfoques de federation, es decir, module federation y native federation, y los iframes.

Stefan sostiene que las grandes organizaciones muy a menudo usan iframes, no por un mejor rendimiento, ya que en realidad pagan una penalización de rendimiento, sino por su aislamiento. Ese aislamiento es muy importante cuando varias aplicaciones se han desarrollado durante muchos años y no funcionan juntas con facilidad.

Stefan también menciona que los enfoques de federation se pueden combinar con web components, pero que tampoco dan el mismo nivel de aislamiento que se encuentra en los iframes. Para él, native federation y module federation encajan perfectamente en proyectos greenfield, es decir, proyectos nuevos donde se pueden definir los límites desde el principio y asegurar que todo funcione bien en conjunto.

Stefan menciona además a web fragments como una posible alternativa, de la que también habla en su artículo. En conjunto, es un artículo bastante largo pero detallado sobre las distintas ventajas y desventajas de los micro-frontends.

Y siguiendo con el tema de micro-frontends, el Angular Meetup Graz organizó un meetup remoto con varias charlas diferentes sobre native federation. Si te interesa, puedes ver esas charlas también. La grabación completa está disponible en YouTube.

## NgRx 22

Por fin ya está disponible NgRx 22. Su principal novedad son las llamadas extensiones para resources. Permiten que un resource conserve su valor anterior cuando, por ejemplo, cambia el parámetro reactivo.

Eso es algo que también se puede hacer con los snapshots nativos para resources. Pero la extensión de NgRx mantiene el tipo original, lo que significa que si tienes un writable resource, sigue siendo writable. Y además, también conserva todos los parámetros de resources como httpResource.

Otra pequeña adición, aunque no menos útil, es el tipo signalStoreFeature, un utility type para una feature personalizada, que facilita su reutilización. Todo esto y mucho más está cubierto en el blog oficial de NgRx, en dev.to.

## RxJS 9

Y después de dos años y medio de espera, se ha retomado el trabajo en RxJS. Nunca hubo un major para RxJS 8, así que la siguiente versión será la versión 9.

La idea es que RxJS 9 se construya sobre el observable nativo de la plataforma web. Todavía no está disponible de forma amplia en los navegadores. Si el navegador no lo soporta, RxJS instala un fallback. La primera beta se publicó el 4 de agosto y se anunció el 5 de agosto.

## Dos artículos más

Y luego, para cerrar las noticias, tenemos dos artículos más. El primero es más bien un comentario de Andres Gastera sobre si Angular sigue siendo opinionated. Es una muy buena lectura, la verdad, y se las recomiendo. Analiza los cambios que hemos visto recientemente en la style guide de Angular y presenta su opinión sobre ellos. Como dije, es más bien un artículo de opinión que algo técnico.

El otro es un análisis técnico a fondo de Jaime Borgos. Su artículo profundiza en defer. No se trata solo de cómo funciona un bloque defer o de sus casos límite. Trata realmente de cómo funciona internamente y de qué genera el compilador. Así que si te interesan esas cosas, definitivamente échale un vistazo. Jaime es un contribuidor muy activo del proyecto Angular, así que definitivamente sabe bastante de lo que está pasando.

## Cierre

Y eso es todo. Espero que tengas una excelente semana. Nos vemos en el próximo episodio. Hasta luego.
