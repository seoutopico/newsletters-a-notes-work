# Usar las skills en Work

Abre el proyecto local en la aplicación de escritorio y empieza una conversación en Work. Escribe `@` y selecciona la skill indicada. Después añade el mensaje que corresponda.

Los bloques siguientes son ejemplos de solicitudes; leerlos no ejecuta ninguna acción.

## Probar el flujo entero

Selecciona `flujo-newsletter`:

> Ejecuta el flujo completo en una tanda nueva. Actualiza la biblioteca, prepara cinco ideas y redacta tres Notes. Si no hay newsletters nuevas, continúa con las guardadas y busca enfoques distintos de los anteriores. Guarda todo según la estructura del proyecto y abre las Notes para revisarlas. No publiques nada.

## Revisar las ideas antes de redactar

Selecciona `flujo-newsletter`:

> Actualiza la biblioteca y prepara cinco ideas en una tanda nueva. Detente después de las ideas y ábrelas para revisarlas conmigo. Espera mis correcciones antes de redactar las Notes.

Después de revisarlas, en la misma conversación:

> Continúa esta tanda con redactar-notes. Utiliza las ideas I01, I03 e I05, incorporando mis correcciones. Lee sus originales y guarda las tres Notes junto a las ideas.

## Solo actualizar la biblioteca

Selecciona `recuperar-newsletters`:

> Actualiza las newsletters. Dime cuáles has añadido, cuáles has actualizado y cuáles no has podido recuperar. Abre una para comprobar la descarga.

## Crear ideas sin descargar de nuevo

Selecciona `ideas-para-notes`:

> Trabaja con la biblioteca guardada y crea una tanda nueva con cinco enfoques distintos. Lee completas las fuentes elegidas. No descargues de nuevo ni redactes todavía las Notes.

## Redactar a partir de ideas existentes

Selecciona `redactar-notes` y sustituye FECHA por la carpeta real:

> Usa las ideas de tandas/FECHA. Elige las tres con mejor combinación de utilidad propia, respaldo y variedad. Redacta las Notes y guárdalas en esa misma tanda. Abre el resultado para revisión.

## Retomar una tanda

> Lee el resumen y el estado de tandas/FECHA. Continúa desde la etapa pendiente, conservando las correcciones y los resultados existentes. No empieces una tanda nueva.

## Corregir un texto

> Revisa la Note N02 de esta tanda: quiero una apertura más concreta y una explicación más breve del ejemplo. Conserva las otras dos Notes y mis cambios anteriores.

## Programación opcional

Úsalo después de probar el flujo manualmente. Este repositorio no instala ninguna tarea programada.

> Crea una tarea programada local llamada «Preparar Notes de newsletters». Cada sábado a las 19:45, zona Europe/Madrid, debe ejecutar la skill flujo-newsletter dentro de este proyecto usando su configuración. Comprueba primero si existe una tarea equivalente para no duplicarla. Al terminar, deja un resumen de añadidas, actualizadas, ideas, Notes y pendientes. Si falla la descarga, conserva los archivos y continúa con las fuentes completas disponibles señalando la limitación. No publiques nada. Muéstrame la tarea y su próxima ejecución.

Para usar archivos locales, deja el ordenador encendido y la aplicación abierta. La interfaz y disponibilidad de programación dependen del entorno: [documentación oficial](https://learn.chatgpt.com/docs/automations).
