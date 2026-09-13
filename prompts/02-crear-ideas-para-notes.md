# Crear ideas-para-notes

Crea una skill local llamada `ideas-para-notes` en `.agents/skills/` de este proyecto.

Lee `ESTRUCTURA.md`, `newsletter.config.json` y la skill `recuperar-newsletters`. Reutiliza su biblioteca y su configuración.

La skill debe preparar cinco ideas para dar una segunda vida a las newsletters en Notes de Substack. Debe leer completas las publicaciones seleccionadas, captar el tono de Aina y revisar propuestas anteriores para evitar repetir enfoques.

Para cada idea incluirá:

- Newsletter de origen y enlace.
- Ángulo concreto y pasaje que lo respalda.
- Problema o deseo del lector.
- Aprendizaje útil por sí mismo.
- Posible apertura.
- Motivo concreto para profundizar en la newsletter.
- Aspectos que necesitan verificación.

Si recibe una tanda, trabajará dentro de ella. Si se invoca sola para crear nuevas ideas, abrirá una tanda en `tandas/FECHA/`. Guardará `ideas-para-notes.md` y registrará las fuentes, sus versiones y los identificadores de las ideas en `estado.json`, sin copiar las newsletters.

Priorizará novedades y fuentes pendientes. La ausencia de nuevas descargas no impedirá aprovechar el archivo existente. Debe distinguir las afirmaciones de la fuente de las interpretaciones y ejemplos propuestos.

No debe redactar Notes completas ni publicarlas. Muéstrame el `SKILL.md` creado.
