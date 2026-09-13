# Crear redactar-notes

Este archivo sirve para pedirle a Work que cree esta skill desde cero. Si quieres utilizar las que ya vienen preparadas, sigue [la guía de uso](05-usar-en-work.md). Para recrearlas, consulta primero [el orden de creación](README.md#crear-las-skills-opcional).

Copia la petición que sigue y envíala en Work dentro de tu proyecto de prueba.

## Petición para copiar

Crea una skill local llamada `redactar-notes` en `.agents/skills/` de este proyecto.

Lee `ESTRUCTURA.md`, `newsletter.config.json` y la skill `ideas-para-notes`. Su entrada serán las ideas y las referencias de fuentes de una tanda existente.

Debe seleccionar las tres ideas con mayor potencial editorial y leer completas las versiones originales correspondientes antes de escribir. Utilizará los textos originales para captar el tono, las aperturas y la forma de explicar de Aina.

Cada Note desarrollará una sola idea, aportará utilidad autónoma, incluirá un ejemplo o aprendizaje respaldado y conectará naturalmente con la newsletter mediante su enlace y un motivo concreto para seguir leyendo.

Variará aperturas y estructuras. No inventará experiencias, datos ni resultados. Señalará las verificaciones pendientes sobre herramientas o funciones cambiantes.

Guardará `notes-para-revisar.md` junto a las ideas, separando texto publicable y comentario editorial. Registrará la relación Note → idea → newsletter en el mismo `estado.json`.

Si se invoca sola, continuará la tanda indicada o la más reciente con ideas pendientes de redacción. Las correcciones permanecerán en esa tanda. Los borradores previos no se considerarán ejemplos de voz aprobada hasta que el usuario lo confirme.

No debe descargar, crear otra carpeta para la redacción ni publicar. Muéstrame el `SKILL.md` creado.
