# Qué pedirle a Work: ejemplos para copiar

Un **prompt** es la petición que envías a ChatGPT. Aquí tienes peticiones para utilizar las skills del ejemplo.

**Si es tu primera vez, empieza por [la guía desde cero](../README.md#usarlo-desde-chatgpt-work).** Allí se explica cómo abrir Work, conectar una carpeta y preparar el proyecto. Los ejemplos de esta página se utilizan después de esa preparación.

## Seleccionar una skill

Cada ejemplo indica qué skill elegir antes de enviar la petición:

1. Abre una conversación de **Work dentro del proyecto donde preparaste el ejemplo**. Comprueba que utiliza **Work locally / Trabajar en local**.
2. En el cuadro del mensaje, escribe **`@`**.
3. Busca el nombre que indica el ejemplo y **selecciónalo en el menú**.
4. Añade la petición copiada y pulsa **Enviar**.

Escribir un nombre como texto no es lo mismo que seleccionarlo en el menú. Elegir la skill la añade al mensaje; enviar la petición ejecuta el encargo. No se programa ninguna repetición por seleccionarla. [Documentación oficial de skills](https://learn.chatgpt.com/docs/build-skills).

## Probar el flujo entero

**Úsalo cuando:** quieras pasar de la descarga a los borradores en una sola petición.

**Selecciona con `@`:** `flujo-newsletter`.

**Copia y envía:**

> Ejecuta el flujo completo en una tanda nueva. Actualiza la biblioteca, prepara cinco ideas y redacta tres Notes. Si no hay newsletters nuevas, continúa con las guardadas y busca enfoques distintos de los anteriores. Abre las Notes para revisarlas conmigo y dime qué has añadido, actualizado o dejado pendiente. No publiques nada.

**Qué recibirás:** una nueva carpeta con ideas, Notes y un resumen. Si faltan fuentes completas, Work debe explicar qué no ha podido completar. Puedes pedir cambios en esa misma conversación.

## Revisar las ideas antes de redactar

**Úsalo cuando:** quieras decidir los enfoques antes de que Work escriba las Notes.

**Selecciona con `@`:** `flujo-newsletter`.

**Copia y envía:**

> Actualiza la biblioteca y prepara cinco ideas en una tanda nueva. Detente después de las ideas y ábrelas para revisarlas conmigo. Espera mis correcciones antes de redactar las Notes.

**Qué recibirás:** el documento de ideas. Todavía no habrá Notes nuevas.

Cuando hayas revisado las ideas, sigue en esa conversación. Selecciona **`@` → `redactar-notes`** y envía, por ejemplo:

> Continúa esta tanda. Elige las tres ideas con más potencial, teniendo en cuenta mis comentarios. Lee las newsletters originales completas, redacta las tres Notes y abre el documento para revisarlo. No publiques nada.

Si prefieres elegir tú, sustituye la frase «Elige las tres ideas con más potencial» por los números o nombres de las ideas que quieras utilizar.

## Corregir las Notes

**Úsalo cuando:** ya tengas borradores y quieras ajustarlos.

En la conversación de esa tanda, selecciona **`@` → `redactar-notes`** y envía:

> Revisa la segunda Note de esta tanda: quiero una apertura más concreta y una explicación más breve del ejemplo. Conserva las otras dos Notes y mis cambios anteriores. Guarda los cambios en el mismo documento y ábrelo para revisarlo.

**Qué recibirás:** el documento actualizado en la misma carpeta. Cambia «segunda Note» y las correcciones por lo que quieras revisar.

## Hacer solo una parte del trabajo

### Solo descargar o actualizar newsletters

**Selecciona con `@`:** `recuperar-newsletters`.

> Actualiza las newsletters de este proyecto. Dime cuáles has añadido, cuáles has actualizado y cuáles no has podido recuperar. Abre una para comprobar la descarga. No prepares ideas ni Notes todavía.

**Resultado:** la biblioteca actualizada y el informe de descarga.

### Sacar ideas con lo que ya tienes guardado

**Selecciona con `@`:** `ideas-para-notes`.

> Trabaja con la biblioteca guardada y crea una tanda nueva con cinco enfoques distintos. Lee completas las fuentes elegidas y abre las ideas para revisarlas conmigo. No descargues de nuevo ni redactes todavía las Notes.

**Resultado:** un documento de ideas en una tanda nueva. Necesita que haya newsletters completas guardadas.

### Redactar desde las ideas que acabas de revisar

En la conversación de esas ideas, selecciona **`@` → `redactar-notes`**.

> Utiliza las ideas de esta tanda, incorporando mis correcciones. Elige tres enfoques diferentes, lee sus originales completos y redacta las Notes. Guárdalas junto a las ideas y abre el resultado. No publiques nada.

**Resultado:** el documento de Notes dentro de la misma tanda.

## Continuar otro día

La opción más sencilla es volver a la conversación donde estabas revisando los textos y pedir:

> Continúa con la misma tanda desde donde lo dejamos. Revisa sus archivos, conserva mis correcciones y dime qué queda pendiente antes de seguir.

Si abres **otra conversación del mismo proyecto**, selecciona **`@` → `flujo-newsletter`** y envía:

> Muéstrame las tandas guardadas y un breve resumen de cada una. Quiero elegir cuál continuar. Todavía no crees una tanda nueva ni modifiques los textos.

Cuando Work te muestre las opciones, señala la que quieras y pide que continúe. Así puedes localizarla sin tener que recordar el nombre de la carpeta.

## Utilizar tu propia newsletter

El ejemplo está preparado para Aina Lluna. Para cambiarlo, abre un proyecto con una carpeta nueva y sigue primero [la preparación del README](../README.md#usarlo-desde-chatgpt-work). Después, antes de la primera descarga, envía lo siguiente. **Sustituye `[ENLACE]` por la dirección de tu publicación en Substack**:

> Adapta este ejemplo a mi publicación: [ENLACE]. Actualiza la configuración y las referencias de autor, audiencia y tono de las skills. Usa mis artículos completos para identificar mi voz; no mantengas las indicaciones de voz de Aina Lluna. Configura la primera descarga para los últimos doce meses. Si esta carpeta ya contiene newsletters de otra publicación, detente y ayúdame a utilizar una carpeta separada. Todavía no ejecutes el flujo; dime cuándo está preparado.

Cuando Work confirme la preparación, utiliza [la petición del flujo entero](#probar-el-flujo-entero).

## Programación opcional

**Úsalo después de revisar una prueba manual.** Envía esta petición en Work dentro del mismo proyecto; el nombre de la skill se incluye en el texto para que forme parte de la tarea guardada:

> Crea una tarea programada local llamada «Preparar Notes de newsletters». Cada sábado a las 19:45, zona Europe/Madrid, debe ejecutar la skill flujo-newsletter dentro de este proyecto usando su configuración. Comprueba primero si existe una tarea equivalente para no duplicarla. Al terminar, deja un resumen de añadidas, actualizadas, ideas, Notes y pendientes. Si falla la descarga, conserva los archivos y continúa con las fuentes completas disponibles señalando la limitación. No publiques nada. Muéstrame la tarea y su próxima ejecución.

**Qué debes comprobar:** que Work te muestre la tarea, su horario y la próxima ejecución. Las tareas que utilizan archivos locales necesitan el ordenador encendido y la aplicación abierta. Puedes revisar su estado en **Scheduled / Tareas programadas**. [Documentación oficial de programación](https://learn.chatgpt.com/docs/automations).

## Si algo no sale como esperabas

### Si la skill no aparece

Comprueba que has abierto el mismo proyecto en el que preparaste el ejemplo. Si acabas de prepararlo, prueba en una conversación nueva de ese proyecto.

Si sigue sin aparecer, envía esta petición sin seleccionar ninguna skill:

> Comprueba si las cuatro skills del ejemplo están en la carpeta principal de este proyecto y si puedo seleccionarlas con @. Revisa en particular .agents/skills/flujo-newsletter/SKILL.md y sus skills asociadas. Dime qué falta o qué tengo que hacer en la interfaz. Todavía no ejecutes el flujo.

Si los archivos están disponibles pero el selector sigue sin mostrarlos, puedes pedir:

> Lee .agents/skills/flujo-newsletter/SKILL.md y aplica su procedimiento junto con las skills que referencia. Ejecuta una tanda completa y abre las Notes para revisión. No publiques nada.

Esta petición permite señalar el archivo de instrucciones directamente; no hace que aparezca por sí solo en el menú.

### Dice «sin novedades» y se detiene

Si ya hay newsletters completas guardadas, envía:

> Revisa por qué te has detenido. La falta de newsletters nuevas no debe impedir preparar ideas y Notes con la biblioteca guardada. Continúa la misma tanda si hay fuentes completas disponibles; si no las hay, explica qué no has podido recuperar.

### No puedes encontrar el documento

Envía:

> Dime en qué carpeta has guardado esta tanda, muéstrame los enlaces a sus ideas, Notes y resumen, y abre las Notes para revisarlas.

Si Work dice que la apertura quedó en cola, utiliza el enlace al archivo que te haya dado.

### No tienes la opción de trabajar en local

Esta guía necesita que Work acceda a la carpeta del ordenador. Revisa la disponibilidad de tu aplicación y cuenta en la [guía oficial de Work](https://learn.chatgpt.com/docs/get-started-with-work). Una conversación que no tenga acceso a esa carpeta no podrá guardar allí los resultados de este ejemplo.
