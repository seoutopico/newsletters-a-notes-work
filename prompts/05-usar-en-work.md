# Usar las skills en Work

Esta guía explica qué hacer en la interfaz de **ChatGPT Work**. Las skills ya están creadas: para usarlas, las seleccionas y les pides el trabajo.

## Seleccionar una skill

1. Abre la aplicación de escritorio y entra en el **proyecto local** que contiene este ejemplo.
2. Abre una conversación en **Work**, con **Trabajar en local / Work locally** seleccionado.
3. Haz clic en el cuadro donde escribes el mensaje y escribe **`@`**.
4. En el selector que se abre, busca el nombre de la skill. Para el flujo completo, busca **`flujo-newsletter`** y **selecciona su resultado en el menú**.
5. Con la skill seleccionada, añade la petición del ejemplo que quieras utilizar.
6. Pulsa **Enviar**. Work utilizará las instrucciones de esa skill para realizar el encargo.

**Escribir `@` abre el selector. Elegir una skill la incorpora al mensaje. El trabajo empieza cuando envías la petición.** La selección no crea una tarea programada ni activa ejecuciones permanentes.

Para seleccionar expresamente una skill, elige el resultado del menú: copiar su nombre como texto normal no es el mismo gesto. Work también puede elegir skills a partir de lo que le pidas, pero aquí usamos la selección explícita para que quede claro cuál debe aplicar. [Documentación oficial sobre invocación de skills](https://learn.chatgpt.com/docs/build-skills).

## Qué nombre buscar después de escribir @

| Qué quieres hacer | Skill que debes seleccionar |
|---|---|
| Descargar, sacar ideas y redactar Notes | `flujo-newsletter` |
| Solo descargar o actualizar newsletters | `recuperar-newsletters` |
| Preparar ideas con las newsletters guardadas | `ideas-para-notes` |
| Redactar o corregir Notes a partir de las ideas | `redactar-notes` |

Para el flujo completo basta con seleccionar **`flujo-newsletter`**: esa skill coordina las otras tres.

## Si la skill no aparece en el selector

Comprueba que estás en el proyecto local adecuado y que contiene las cuatro carpetas de skills. Si acabas de incorporarlas, abre una conversación nueva dentro de ese proyecto y vuelve a probar `@`.

Puedes pedirle a Work que lo compruebe:

> Comprueba que este proyecto contiene .agents/skills/flujo-newsletter/SKILL.md y sus tres skills asociadas. Si están disponibles, explícame cómo seleccionarlas. Todavía no ejecutes el flujo.

También puedes indicarle explícitamente que lea el `SKILL.md` correspondiente cuando no consigas seleccionarlo. Esta alternativa le señala el archivo de instrucciones; no garantiza que aparezca en el menú.

Los ejemplos siguientes son peticiones para enviar después de seleccionar la skill indicada.

## Preparar el proyecto por primera vez

Si todavía no tienes las skills en tu proyecto, puedes encargarle la preparación a Work:

> Prepara este proyecto con el ejemplo de https://github.com/seoutopico/newsletters-a-notes-work. Lee el README, incorpora las skills y los archivos de apoyo, comprueba qué necesita el entorno y prepara lo que falte. Conserva mis archivos existentes. Todavía no ejecutes el flujo.

Si ya tienes las skills disponibles, omite esta preparación.

## Probar el flujo entero

Escribe **`@`**, selecciona **`flujo-newsletter`** en el menú y después envía:

> Ejecuta el flujo completo en una tanda nueva. Actualiza la biblioteca, prepara cinco ideas y redacta tres Notes. Si no hay newsletters nuevas, continúa con las guardadas y busca enfoques distintos de los anteriores. Guarda todo según la estructura del proyecto y abre las Notes para revisarlas. No publiques nada.

## Revisar las ideas antes de redactar

Escribe **`@`**, selecciona **`flujo-newsletter`** en el menú y después envía:

> Actualiza la biblioteca y prepara cinco ideas en una tanda nueva. Detente después de las ideas y ábrelas para revisarlas conmigo. Espera mis correcciones antes de redactar las Notes.

Después de revisarlas, en la misma conversación escribe **`@`**, selecciona **`redactar-notes`** y envía:

> Continúa esta tanda con redactar-notes. Utiliza las ideas I01, I03 e I05, incorporando mis correcciones. Lee sus originales y guarda las tres Notes junto a las ideas.

## Solo actualizar la biblioteca

Escribe **`@`**, selecciona **`recuperar-newsletters`** en el menú y después envía:

> Actualiza las newsletters. Dime cuáles has añadido, cuáles has actualizado y cuáles no has podido recuperar. Abre una para comprobar la descarga.

## Crear ideas sin descargar de nuevo

Escribe **`@`**, selecciona **`ideas-para-notes`** en el menú y después envía:

> Trabaja con la biblioteca guardada y crea una tanda nueva con cinco enfoques distintos. Lee completas las fuentes elegidas. No descargues de nuevo ni redactes todavía las Notes.

## Redactar a partir de ideas existentes

Escribe **`@`**, selecciona **`redactar-notes`** en el menú y después envía lo siguiente, sustituyendo FECHA por la carpeta real:

> Usa las ideas de tandas/FECHA. Elige las tres con mejor combinación de utilidad propia, respaldo y variedad. Redacta las Notes y guárdalas en esa misma tanda. Abre el resultado para revisión.

## Retomar una tanda

Escribe **`@`**, selecciona **`flujo-newsletter`** y envía lo siguiente, sustituyendo FECHA por la carpeta real:

> Lee el resumen y el estado de tandas/FECHA. Continúa desde la etapa pendiente, conservando las correcciones y los resultados existentes. No empieces una tanda nueva.

## Corregir un texto

En la conversación de esa tanda, escribe **`@`**, selecciona **`redactar-notes`** y envía:

> Revisa la Note N02 de esta tanda: quiero una apertura más concreta y una explicación más breve del ejemplo. Conserva las otras dos Notes y mis cambios anteriores.

## Programación opcional

Úsalo después de probar el flujo manualmente. Escribe esta petición en Work e indica el nombre `flujo-newsletter` en el texto para que quede guardado en la programación. Puedes seleccionarla también con `@`. Este repositorio no instala ninguna tarea programada.

> Crea una tarea programada local llamada «Preparar Notes de newsletters». Cada sábado a las 19:45, zona Europe/Madrid, debe ejecutar la skill flujo-newsletter dentro de este proyecto usando su configuración. Comprueba primero si existe una tarea equivalente para no duplicarla. Al terminar, deja un resumen de añadidas, actualizadas, ideas, Notes y pendientes. Si falla la descarga, conserva los archivos y continúa con las fuentes completas disponibles señalando la limitación. No publiques nada. Muéstrame la tarea y su próxima ejecución.

Para usar archivos locales, deja el ordenador encendido y la aplicación abierta. La interfaz y disponibilidad de programación dependen del entorno: [documentación oficial](https://learn.chatgpt.com/docs/automations).
