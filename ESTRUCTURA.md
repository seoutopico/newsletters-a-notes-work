# Carpetas y relevo entre skills

La biblioteca conserva las newsletters. Las tandas agrupan el trabajo editorial que se hace con ellas. Una descarga actualiza la biblioteca; una tanda pasa de ideas a Notes sin cambiar de carpeta.

## Estructura compartida

```text
newsletters-a-notes-work/
  newsletter.config.json
  ESTRUCTURA.md
  biblioteca/
    INDICE.md
    articulos/                  newsletters legibles, una copia actual por ID
    control/
      inventario.json           identidad, ruta y versión de cada artículo
      datos_api/                respuesta actual necesaria para actualizarlo
      historial/                versiones anteriores cuando un artículo cambia
      descargas/                informes de cada consulta e incidencias
      ultima_ejecucion.json
      ULTIMA_EJECUCION.md
  tandas/
    AAAA-MM-DD_HH-mm-ss/
      ideas-para-notes.md
      notes-para-revisar.md
      RESUMEN.md
      estado.json               fuentes y relación newsletter → idea → Note
  .agents/skills/                instrucciones y scripts reutilizables
```

Las carpetas de tanda se crean al empezar trabajo editorial. Los documentos aparecen cuando se completa su etapa; no se generan Notes vacías ni resultados ficticios para rellenar la estructura.

`newsletter.config.json` es la configuración compartida: publicación, fecha inicial, zona horaria y nombres de las carpetas de biblioteca y tandas. Los scripts reciben `--project-root`; las referencias de fuentes se guardan relativas a esa raíz. Para trasladar el proyecto se conserva toda la estructura. Cambiar solo el nombre en la configuración no mueve datos existentes: cualquier cambio de rutas necesita una migración.

## Responsabilidad de cada skill

| Skill | Entrada | Salida | Qué puede modificar |
|---|---|---|---|
| recuperar-newsletters | API y biblioteca existente | Biblioteca e informe nuevo de descarga | Artículos y control de la biblioteca |
| ideas-para-notes | Biblioteca, historial editorial y tanda | Ideas registradas en la tanda | Ideas y su registro |
| redactar-notes | Ideas y versiones originales de esa tanda | Notes para revisar en la misma tanda | Notes y su registro |
| flujo-newsletter | Configuración del proyecto | Una tanda que recorre las tres etapas | Coordina las anteriores |

Ejecutar una skill sola utiliza las mismas carpetas. No hay destinos alternativos en la raíz ni una carpeta por etapa. Las instrucciones editoriales permanecen en sus respectivas skills.

## Fuentes sin duplicados

Cada fuente se registra por ID de Substack, enlace, ruta relativa, huella editorial y huella del archivo leído. Las tandas no reciben copias de las newsletters.

Cuando un artículo cambia, el descargador conserva la versión anterior una sola vez en el historial de la biblioteca. La acción `fuentes` busca la versión registrada por la tanda, primero en la copia actual y después en el historial. Si no la encuentra, señala el problema en vez de sustituirla silenciosamente por otra versión.

El registro de descarga indica novedades de la API. El registro editorial indica ideas y Notes existentes. Son estados distintos: una newsletter descargada y sin Notes sigue disponible, aunque la última descarga diga «sin cambios».

## Operaciones compartidas

Desde la raíz del proyecto se usa este ayudante, conservado junto a la skill que coordina el flujo:

```powershell
python -B -X utf8 .agents/skills/flujo-newsletter/scripts/flujo_newsletter.py preparar --project-root .
```

`preparar` actualiza la biblioteca y crea una tanda. Para invocar ideas-para-notes sola, añadir `--sin-descarga`: utiliza las newsletters guardadas y no consulta Substack. Para continuar una tanda existente, no ejecutar `preparar` de nuevo.

Las acciones siguientes usan el mismo script y `--project-root . --tanda tandas/FECHA`:

| Acción | Uso |
|---|---|
| `seleccionar --ids ID1 ID2` | Registrar las newsletters elegidas sin copiarlas. |
| `fuentes` | Mostrar las rutas de las versiones originales que debe leer la skill. |
| `registrar-ideas` | Validar el documento de ideas y dejar la tanda pendiente de Notes. |
| `cerrar` | Validar ambos documentos y sus relaciones; dejar la tanda para revisión. |
| `resumen` | Actualizar el resumen de una tanda pendiente o interrumpida. |

El agente redacta los documentos aplicando las skills. El ayudante organiza y comprueba archivos; no genera textos ni evalúa su calidad editorial.

Después de escribir, actualizar únicamente las listas correspondientes de `estado.json`. Ejemplo de registros, que no sustituye el archivo completo:

```json
{
  "ideas": [{"id": "I01", "newsletter_id": 123, "enfoque": "Ángulo concreto respaldado por la fuente"}],
  "notes": [{"id": "N01", "idea_id": "I01"}],
  "pendientes": []
}
```

Conservar las incidencias anteriores y registrar resultados reales. El documento de ideas incluye sus IDs y enlaces originales. Las Notes incluyen sus IDs, enlaces y relación con la idea de origen fuera del texto publicable.

Una tanda nueva crea otra carpeta fechada. Una corrección continúa en la misma; solo cuando haga falta conservar el texto sustituido se crea `revisiones/` dentro de ella. Nunca se considera publicado o aprobado un texto por estar guardado.

Si adaptas un archivo existente a esta estructura, conserva sus informes históricos y documenta la migración. El inventario actual y la configuración compartida deben reflejar las rutas vigentes.
