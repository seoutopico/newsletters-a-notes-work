# Crear flujo-newsletter

Crea una skill local llamada `flujo-newsletter` que coordine estas skills existentes:

1. `recuperar-newsletters`.
2. `ideas-para-notes`.
3. `redactar-notes`.

Lee sus `SKILL.md`, `ESTRUCTURA.md` y `newsletter.config.json`. Reutiliza sus instrucciones y scripts; no copies sus procedimientos dentro de la skill coordinadora.

La salida de cada etapa debe ser la entrada de la siguiente. El flujo actualizará la biblioteca una vez y creará una única tanda editorial con sus ideas, Notes, resumen y registro de relaciones.

Distingue el estado de descarga del estado editorial: cero newsletters nuevas no significa que no haya material pendiente. Prioriza novedades y continúa con fuentes guardadas y enfoques todavía no utilizados. Si falla la descarga, conserva el archivo y aprovecha fuentes completas disponibles indicando la limitación.

Permite retomar una tanda desde la etapa pendiente sin repetir lo completado. Una tanda con ideas y sin Notes debe continuar por redacción.

Conserva únicamente los ayudantes necesarios para gestionar rutas, estados, versiones y comprobaciones. La lectura y escritura editorial corresponde a las skills.

Al terminar, informa de añadidas, actualizadas, ideas, Notes y pendientes, y abre las Notes para revisión. No publiques ni cambies programaciones.

Comprueba que las tres skills usan la misma arquitectura tanto por separado como dentro del flujo. Muéstrame la skill coordinadora creada.
