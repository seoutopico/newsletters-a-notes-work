# Guía técnica

## Dependencias y ejecución

Python 3.11 o posterior; instalar `requirements.txt`. El desarrollo inicial se comprobó en Windows con Python 3.14. Las instrucciones de uso editorial están en las skills, no en un servicio externo de generación de texto.

Todos los comandos de esta página se ejecutan desde la raíz del repositorio. En macOS o Linux, utilizar `python3` si `python` no apunta a Python 3.

Solo descargar o actualizar:

```sh
python -B -X utf8 .agents/skills/recuperar-newsletters/scripts/recuperar_newsletters.py --project-root .
```

Actualizar la biblioteca y preparar una tanda para Work:

```sh
python -B -X utf8 .agents/skills/flujo-newsletter/scripts/flujo_newsletter.py preparar --project-root .
```

Preparar una tanda a partir del archivo existente, sin descargar:

```sh
python -B -X utf8 .agents/skills/flujo-newsletter/scripts/flujo_newsletter.py preparar --project-root . --sin-descarga
```

Estos comandos preparan datos. Para obtener textos hay que continuar con las skills editoriales en Work. El [contrato de etapas](../ESTRUCTURA.md) documenta `seleccionar`, `fuentes`, `registrar-ideas`, `cerrar` y `resumen`.

## API y conservación

El descargador consulta `/api/v1/archive?sort=new&search=&offset=0&limit=12`. Avanza el desplazamiento por el número real de elementos recibidos y continúa hasta una página vacía; una página corta no se considera el final.

Después consulta `/api/v1/posts/{slug}` y comprueba el ID. Conserva `body_html` convertido a Markdown, así como el título, la fecha y el enlace. Los contadores sociales y las fechas de consulta no se consideran cambios editoriales.

La identidad estable es el ID de Substack. El inventario conserva la ruta aunque cambie el título o el slug. Si cambia el contenido, la copia anterior pasa a `control/historial/`. Si falta el inventario, intenta recuperar asociaciones inequívocas a partir de los archivos y las respuestas actuales; una identidad ambigua bloquea la reconstrucción en vez de adivinar.

El informe conserva URL, cantidad e IDs de cada página. Las consultas sin cambios no generan otra copia de todos los cuerpos. Los fallos o extractos pueden conservar su respuesta específica para revisión.

La salida 1 del descargador indica incidencias; puede haber guardado parte de los artículos. Consultar el informe de esa ejecución. El flujo comprueba su fecha para no atribuirle un informe antiguo.

## Pruebas locales

```sh
python -B -X utf8 .agents/skills/recuperar-newsletters/scripts/test_recuperar_newsletters.py
python -B -X utf8 .agents/skills/flujo-newsletter/scripts/test_flujo_newsletter.py
```

Son 8 pruebas del descargador y 10 del flujo. Usan fuentes simuladas en carpetas temporales y no llaman a Substack ni publican contenido.

Cubren altas, ausencia de cambios, actualización, cambio de slug, extractos, fallos, reparación local, inventario ausente, configuración, referencias históricas, continuidad entre ideas y Notes y traslado del proyecto.

El cierre automático comprueba archivos, identificadores, enlaces y versiones. La lectura completa, el respaldo de los argumentos, la voz y la calidad de las Notes necesitan revisión editorial.

## Personalizar

La configuración efectiva se carga desde `newsletter.config.json`. `configuracion.py` comparte la resolución de rutas entre ambos scripts y aporta valores por defecto si falta el archivo. Conserva la configuración explícita para que otro usuario entienda qué se ejecutará.

Si cambias la publicación, revisa también la fecha de inicio y las instrucciones editoriales sobre autor, audiencia y tono. Si cambias nombres de carpetas con datos existentes, migra los datos y actualiza las referencias; cambiar una cadena en el JSON no mueve archivos.

El ejemplo no incluye publicación en Substack, métricas de rendimiento, programación instalada ni credenciales. No requiere una clave de OpenAI para los scripts: Work realiza la parte editorial con las capacidades disponibles en su sesión.
