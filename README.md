# Tu primera prueba: de newsletters a Notes con ChatGPT Work

Esta guía es para quien todavía no sabe usar Work ni ha utilizado una skill.

Vas a pedirle a ChatGPT que descargue newsletters de Substack, encuentre cinco ideas y escriba tres **Notes**: publicaciones cortas para Substack que aporten algo útil y enlacen al artículo original. Al terminar tendrás documentos que podrás leer y corregir conversando con Work.

**Para probarlo, sigue los pasos de esta página.** Puedes ver antes [una muestra del resultado](ejemplos/README.md). La muestra es ficticia; los textos de tu prueba se crearán a partir de las newsletters que se puedan recuperar.

## Tres palabras que encontrarás

- **Work** es la forma de trabajar con ChatGPT en la que le encargas una tarea y puede utilizar herramientas y archivos para entregarte un resultado.
- **Proyecto local** es el espacio de trabajo al que das acceso a una carpeta de tu ordenador. Ahí quedarán guardados los documentos.
- **Skill** es un procedimiento guardado que ChatGPT puede reutilizar. Este ejemplo ya incluye las skills necesarias. Las eliges desde el cuadro del mensaje escribiendo `@`.

Un **prompt** es simplemente la petición que escribes a ChatGPT. Más abajo encontrarás las peticiones listas para copiar.

## Usarlo desde ChatGPT Work

### 1. Abre Work y prepara una carpeta

Necesitas la aplicación de escritorio de ChatGPT y acceso a Work con archivos locales. Este recorrido utiliza **Work locally / Trabajar en local** porque los resultados se guardan en tu ordenador. Si tu aplicación no muestra esa opción, comprueba la [guía oficial de acceso a Work](https://learn.chatgpt.com/docs/get-started-with-work) antes de continuar.

1. Crea una carpeta en tu ordenador llamada **Mis newsletters**. Para la primera prueba, utiliza una carpeta vacía: será fácil reconocer lo que Work vaya guardando.
2. En la sección **Proyectos** de ChatGPT, crea un proyecto para este trabajo. Puedes llamarlo también **Mis newsletters**.
3. Abre el menú del proyecto y entra en **Edit project / Editar proyecto**. Usa **Add folder / Añadir carpeta** y elige la carpeta que acabas de crear. Si hay varias carpetas, establece esta como principal.
4. Abre una conversación dentro de ese proyecto. Selecciona **Work** y comprueba que está activado **Work locally / Trabajar en local**.

**Antes de seguir:** el proyecto debe tener asociada la carpeta de tu ordenador. Ponerle el mismo nombre al proyecto y a la carpeta no los conecta por sí solo. Puedes consultar estos controles en la [guía oficial de proyectos](https://learn.chatgpt.com/docs/projects).

Si ya tienes este ejemplo preparado en un proyecto, abre ese proyecto y pasa al paso 3.

### 2. Pídele a Work que prepare el ejemplo

Este repositorio de GitHub es la carpeta pública que contiene las instrucciones y los archivos del ejemplo. Copia la siguiente petición en el cuadro del mensaje de Work y pulsa **Enviar**. En este paso todavía no tienes que seleccionar ninguna skill:

> Prepara en la carpeta principal de este proyecto el ejemplo de https://github.com/seoutopico/newsletters-a-notes-work. Lee su README e incorpora las cuatro skills y sus archivos de apoyo. Conserva lo que ya exista y comprueba que puedes leer y escribir en la carpeta. Revisa el entorno y prepara lo necesario para ejecutar los scripts. Para esta primera prueba, utiliza la publicación de Aina Lluna que incluye el ejemplo y configura la descarga de los últimos doce meses. Si ya existe una biblioteca, conserva su configuración y sus archivos. Al terminar, dime qué carpeta has utilizado, si la preparación está completa y cómo encontrar flujo-newsletter con @. Todavía no ejecutes el flujo.

Espera a que Work termine. **El resultado de este paso es tener el ejemplo preparado**, todavía sin las cinco ideas ni las tres Notes. Si necesita acceso a la carpeta o alguna autorización, te lo indicará; si informa de un problema, resuélvelo en esa conversación antes de pasar al siguiente paso.

La publicación de esta prueba es [Think & Hack, de Aina Lluna](https://ainalluna.substack.com). Sus newsletters reales no vienen incluidas en GitHub: Work las descargará cuando ejecutes el flujo.

### 3. Selecciona la skill con @ y lanza la prueba

Abre una **conversación nueva dentro del mismo proyecto**, en Work y con trabajo local seleccionado. Así podrás comprobar si aparecen las skills que acabas de preparar.

1. Haz clic en el cuadro donde escribes tus mensajes.
2. Escribe **`@`** para abrir el selector.
3. Busca **`flujo-newsletter`** y **haz clic en ese resultado**.
4. Con la skill seleccionada en el mensaje, añade esta petición y pulsa **Enviar**:

> Ejecuta el flujo completo en una tanda nueva. Actualiza la biblioteca, prepara cinco ideas y redacta tres Notes. Si no hay newsletters nuevas, continúa con las que ya están guardadas y busca enfoques distintos de los anteriores. Abre las Notes para revisarlas conmigo y dime qué has añadido, actualizado o dejado pendiente. No publiques nada.

**Una tanda es un grupo de ideas y Notes creado en esta ejecución.** La skill `flujo-newsletter` se encarga de coordinar la descarga, las ideas y la redacción. Para la prueba completa basta con seleccionar esa skill.

Seleccionarla añade la skill al mensaje; **Enviar** inicia el trabajo. No queda programada para repetirse. La selección mediante `@` está descrita en la [guía oficial de skills](https://learn.chatgpt.com/docs/build-skills).

Si no aparece en el menú, sigue [estos pasos para comprobarlo](prompts/05-usar-en-work.md#si-la-skill-no-aparece).

### 4. Lee y corrige el resultado

Work debería entregarte un resumen y enlaces a los documentos creados. El objetivo es obtener **cinco ideas y tres Notes para revisar**. Si no dispone de suficientes artículos completos o encuentra un fallo, debe explicarte qué falta y qué ha podido hacer.

Abre **notes-para-revisar.md** desde el enlace que te dé. La extensión `.md` indica un documento de texto que puedes leer en Work. Encontrarás cada propuesta separada de una breve explicación editorial: el texto publicable es el que utilizarías en Substack.

Puedes corregirlas en la misma conversación. Por ejemplo, envía:

> Haz más concreta la apertura de la segunda Note y acorta su ejemplo. Conserva su idea central, el enlace y las otras dos Notes. Guarda los cambios en el mismo documento y ábrelo otra vez.

**La prueba está terminada cuando puedes abrir y revisar esos textos.** Guardar las propuestas no las publica en Substack; la publicación queda fuera de este flujo.

## Dónde se guarda cada cosa

Dentro de la carpeta **Mis newsletters**, el trabajo se organiza así:

| Qué quieres consultar | Dónde lo encontrarás |
|---|---|
| Newsletters descargadas | `biblioteca/articulos/` |
| Lista de newsletters disponibles | `biblioteca/INDICE.md` |
| Ideas de una prueba | `tandas/FECHA-HORA/ideas-para-notes.md` |
| Notes para corregir | `tandas/FECHA-HORA/notes-para-revisar.md` |
| Qué se hizo y qué quedó pendiente | `tandas/FECHA-HORA/RESUMEN.md` |

`FECHA-HORA` representa el nombre que Work pone a cada tanda, por ejemplo `2026-09-13_10-30-00`. Cada tanda nueva tiene su propia carpeta. Las newsletters se conservan en una biblioteca común para poder reutilizarlas.

No necesitas recorrer las carpetas para empezar: puedes decir **«Abre las Notes de esta tanda»**. Los archivos de control que también encontrarás ayudan a Work a recordar qué ha descargado y qué queda por hacer.

## La próxima vez

Vuelve a este proyecto, abre una conversación de Work, selecciona **`@` → `flujo-newsletter`** y envía de nuevo la petición del paso 3. La preparación del paso 2 solo es necesaria la primera vez.

Work incorporará las newsletters nuevas, actualizará las que hayan cambiado y preparará otra tanda. **Si la descarga no tiene novedades, el trabajo editorial continúa con las newsletters guardadas.** Si no hay ninguna fuente completa disponible, debe explicar el bloqueo.

Para continuar corrigiendo los textos anteriores, vuelve a su conversación y pide que siga con esa misma tanda.

## Cuando ya hayas probado el flujo

- [Peticiones listas para copiar](prompts/05-usar-en-work.md): revisar las ideas antes de redactar, ejecutar una sola etapa, continuar otro día o programar el trabajo.
- [Cambiar la publicación del ejemplo](prompts/05-usar-en-work.md#utilizar-tu-propia-newsletter): adaptar las fuentes y el tono a tu publicación.
- [Prompts para crear tus propias skills](prompts/README.md#crear-las-skills-opcional): aprender a construir este proceso desde cero. Las de este ejemplo ya están creadas.

## Referencia opcional

Esta parte sirve para entender o mantener el funcionamiento interno una vez que lo hayas probado.

| Archivo | Qué explica |
|---|---|
| [Skills del proyecto](.agents/skills/) | Los procedimientos que sigue Work. |
| [Estructura de carpetas](ESTRUCTURA.md) | Cómo se relacionan las fuentes, las ideas y las Notes. |
| [Configuración](newsletter.config.json) | Publicación, periodo y carpetas. La copia incluida parte del 12 de septiembre de 2025; el paso 2 pide ajustar la primera descarga. |
| [Guía técnica](docs/GUIA-TECNICA.md) | Scripts, requisitos y comprobaciones para mantenimiento. |

La recuperación utiliza la API de lectura de Substack. Señala extractos y errores y conserva las copias completas anteriores cuando una descarga falla. No recupera contenido privado sin acceso; los recursos multimedia quedan enlazados. La disponibilidad de la API puede cambiar.

El repositorio incluye procedimientos y ejemplos ficticios, sin newsletters descargadas ni borradores privados. Las carpetas de resultados están excluidas de las subidas habituales a GitHub; si cambias sus nombres, hay que adaptar también esas exclusiones.

Las indicaciones sobre Work se contrastaron con documentación oficial el 13 de septiembre de 2026. Los nombres y la disponibilidad de los controles pueden variar según la versión o la cuenta.
