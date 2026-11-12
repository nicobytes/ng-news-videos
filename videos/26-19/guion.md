# Guion Ng-News en español 26/19

Duración estimada: 03:34 (579 palabras)

## Introducción

Hola, mi nombre es _____ y esto es NG News en español con las últimas novedades de la comunidad de Angular.

## Angular 22.1

Ya fue lanzado Angular 22.1. Y como ya comentamos en un episodio anterior, esta no será la única versión minor dentro de la serie 22. Debido al nuevo ciclo de lanzamientos, que ocurre una sola vez al año, ahora podemos esperar entre cuatro y seis versiones minor.

Al ser una versión minor, la 22.1 solo puede introducir funcionalidades nuevas, pero ningún breaking change. Esas solo pueden llegar en una versión major.

Y la principal novedad de esta versión es una propiedad set en linkedSignal, que lo extiende tanto que casi podría haber sido una función de signal completamente nueva. Por primera vez, tenemos algo parecido a un two-way binding para signals, es decir, una forma de enlazar los valores en ambas direcciones.

Veamos el ejemplo. El caso de uso es este: tenemos aquí un campo de euros. Si escribo algo en euros, los dólares se actualizan. Y si escribo algo en dólares, los euros también se actualizan.

¿Cómo se implementa esto? Fíjense bien. La signal USD, la que guarda los dólares, es un linkedSignal. Esto significa que cada vez que cambia el valor en euros, también cambia el valor en dólares, y eso ocurre de inmediato, de forma síncrona.

Para el camino inverso, es decir, de dólares a euros, tenemos que usar un effect, porque hasta la versión 22.1 no había otra opción. En este caso, el effect escucha el valor de USD y, dentro de un untracked, actualiza el valor en euros.

Lamentablemente, eso ocurre de forma asíncrona, porque es un effect. Y aquí tenemos además un botón de reset, que es una función que establece de inmediato el valor en dólares a 100.

Entonces, ¿qué pasa? Si volvemos a la aplicación y decimos que tenemos, por ejemplo, 10 dólares, tenemos que mirar la consola. Porque si ahora hacemos clic en este botón y cambiamos el valor de USD a 100, vemos que el euro todavía tiene el valor anterior. Claro, en el campo de entrada no se nota, pero este es el típico comportamiento asíncrono del effect, que resulta muy problemático.

Ahora, con esta nueva versión de linkedSignal, podemos usar directamente en el linkedSignal la propiedad set, donde podemos escribir de vuelta el valor en euros de inmediato, si el valor del campo de USD ha cambiado.

Y una vez hecho eso, también podemos deshacernos del effect por completo, porque ya no lo necesitamos. El linkedSignal ahora hace todo el trabajo por nosotros.

Veamos de nuevo el mismo ejemplo de antes: escribimos algo en euros, establecemos los dólares a 100, y vemos que ahora en la consola el valor en euros también se actualiza de inmediato, de forma síncrona, como debe ser.

Y hay algo más. Incluso se podría usar para saltarse el comportamiento glitch-free del effect, lo que significa que tendrías la opción de recibir una notificación sobre un cambio de signal cada vez que ocurre, varias veces y de forma síncrona.

La verdad, creo que podemos estar bastante seguros de que esta no era la intención original de esta funcionalidad.

Por supuesto, evidentemente también llegaron otras funcionalidades y correcciones de errores en esta versión, pero para esos casos, por favor consulten los videos, blogs y artículos de la comunidad, donde los explican con mucho más detalle.

## Cierre

Y eso es todo. Espero que tengas una excelente semana. Nos vemos en el próximo episodio. Hasta luego.
