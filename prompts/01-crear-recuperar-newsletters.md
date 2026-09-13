# Crear recuperar-newsletters

Crea una skill local llamada `recuperar-newsletters` en `.agents/skills/` de este proyecto.

Debe descargar las newsletters de https://ainalluna.substack.com mediante su API de lectura. La primera ejecución cubrirá los últimos 12 meses; las siguientes incorporarán nuevas publicaciones y actualizarán las modificadas, conservando el archivo acumulado.

Establece esta arquitectura compartida para las futuras skills:

- `biblioteca/articulos/`: newsletters legibles con título, fecha y enlace.
- `biblioteca/control/`: inventario, datos de actualización, versiones anteriores e informes de descarga.
- `biblioteca/INDICE.md`: índice para consultar los artículos.
- `tandas/FECHA/`: futuros resultados editoriales.
- `newsletter.config.json`: publicación, fecha inicial, zona horaria y rutas.
- `ESTRUCTURA.md`: responsabilidades y relación entre estas carpetas.

Si ya existe configuración o contenido, reutilízalo y adapta las rutas conservando los archivos.

Conserva un script reutilizable que recorra las páginas necesarias, identifique artículos por ID y distinga contenido completo, extractos y fallos. No debe duplicar archivos, perder versiones anteriores ni sustituir contenido completo por un extracto. Debe detectar copias vacías o desaparecidas y recuperar asociaciones inequívocas si falta el inventario.

Evita almacenar de nuevo todos los cuerpos cuando no hayan cambiado. No eludas suscripciones. La skill debe informar de añadidas, actualizadas y pendientes, y abrir un artículo para comprobar su legibilidad.

Comprueba el script con pruebas de conservación y actualización. Muéstrame el `SKILL.md` creado y explica cómo seleccionarlo desde Work.
