---
name: recuperar-newsletters
description: Descargar y actualizar newsletters de Aina Lluna desde la API de lectura de Substack. Conservar las copias anteriores, reparar archivos vacíos y recuperar el inventario sin duplicar artículos; informar de extractos y fallos.
---

# Recuperar newsletters

Leer el [contrato de carpetas y etapas](../../../ESTRUCTURA.md). La publicación, fecha inicial, zona y carpetas se definen una sola vez en `newsletter.config.json`, en la raíz del proyecto. Usar la biblioteca compartida; esta skill no crea tandas editoriales.

## Ejecutar

Reutilizar [scripts/recuperar_newsletters.py](scripts/recuperar_newsletters.py) y su conversor [html_legible.py](scripts/html_legible.py). Requiere Python y requests, disponibles en este equipo.

Desde la raíz del proyecto:

```powershell
python -B -X utf8 .agents/skills/recuperar-newsletters/scripts/recuperar_newsletters.py --project-root .
```

Desde otra carpeta, pasar la raíz absoluta a `--project-root`. Cuando flujo-newsletter ya haya ejecutado este script, utilizar ese informe; no descargar dos veces.

## Método y conservación

- Leer `/api/v1/archive?sort=new&search=&offset=0&limit=12` en la publicación. Avanzar por el número real de resultados hasta una página vacía, incluso si una página es corta. Las páginas repetidas o los errores implican cobertura incompleta.
- Consultar `/api/v1/posts/{slug}`, comprobar el ID y convertir `body_html` a Markdown legible con título, fecha y enlace. Consultar desde la fecha inicial configurada, y volver a comprobar todas las entradas guardadas. El archivo es acumulativo.
- Identificar artículos por ID y conservar sus rutas aunque cambien título o slug. Comparar contenido y metadatos editoriales, excluyendo contadores. No reescribir copias sin cambios.
- Comprobar que el archivo local existe, tiene contenido y coincide con su huella cuando esté registrada. Reparar copias vacías, desaparecidas o alteradas mediante la respuesta completa; conservar antes la versión local existente en `control/historial/`.
- Si falta el inventario o contiene menos entradas que los archivos, reconstruir las asociaciones mediante las respuestas de `control/datos_api/` y el ID, enlace original o nombre exacto del archivo. Si la identidad es ambigua, detenerse y señalar los archivos: no adivinar ni duplicarlos. Un inventario mal formado también exige revisión; no sustituirlo por uno vacío.
- Conservar copias y registros ante errores o pérdida de acceso; nunca sustituir un artículo completo por un extracto. No borrar el archivo ni sus versiones históricas. El bloqueo del descargador evita actualizaciones simultáneas.

«Completo» significa cuerpo público devuelto por la API, audiencia `everyone` y ausencia de bloqueo explícito detectado. No acredita equivalencia con una versión privada. `description` y `truncated_body_text` son extractos. Multimedia queda enlazada; no se descargan comentarios ni Notes ni se eluden suscripciones.

Son endpoints de lectura comprobados, sujetos a cambios. El script conserva informes de consulta y respuestas de incidencias. Guarda una sola respuesta actual por artículo y versiones anteriores cuando cambian; no vuelve a guardar todos los cuerpos ni las páginas completas si no hay cambios. Para las páginas conserva URL, cantidad e IDs en el informe. El cliente usa timeout de 40 segundos y hasta tres intentos. Un bloqueo de red no significa archivo vacío: utilizar el mecanismo de permisos disponible para la descarga autorizada o informar del bloqueo.

## Resultado para el siguiente paso

Devolver las rutas de la biblioteca, el inventario y el informe nuevo definidas en el contrato. Los artículos viven en `articulos/`; los datos de actualización y los informes de descarga, en `control/`. Mantener el índice de lectura en la raíz de la biblioteca.

Leer el informe nuevo y comunicar añadidas, actualizadas, sin cambios, no recuperadas y cobertura. Señalar las reparaciones y las asociaciones reconstruidas. Un extracto puede contar como añadido y no recuperado íntegramente. La salida 1 indica incidencias, no necesariamente una descarga vacía. Si el proceso falla antes de generar informe, no atribuirle el de una ejecución anterior.

Indicar el total de copias presentes y su ubicación. Si se invoca sola, abrir una newsletter para comprobar legibilidad. Si forma parte del flujo, devolver inventario e informe al siguiente paso; las newsletters completas ya guardadas también son fuentes disponibles aunque esta descarga no añada ninguna.
