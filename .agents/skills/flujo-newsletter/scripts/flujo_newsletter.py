"""Prepara y registra el flujo local. Las skills editoriales escriben ideas y Notes."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'recuperar-newsletters/scripts'))
from configuracion import Layout


def read(path, default=None):
    return json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else default


def save(path, value):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    tmp.replace(path)


def within(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Ruta fuera de la carpeta correspondiente.')
    return path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def history(project):
    used, files, warnings = set(), set(), []
    for path in Layout(project).batches.glob('*/estado.json'):
        try:
            state = read(path)
            if state.get('estado') != 'para_revision':
                continue
            if any(not (path.parent / name).is_file() or not (path.parent / name).stat().st_size
                   for name in ('ideas-para-notes.md', 'notes-para-revisar.md')):
                warnings.append(f'Faltan resultados de una tanda anterior: {path.parent}. Sus fuentes siguen pendientes.')
                continue
            sources = {str(s['id']): s for s in state['fuentes']}
            ideas = {i['id']: i for i in state['ideas']}
            for note in state['notes']:
                source = sources[str(ideas[note['idea_id']]['newsletter_id'])]
                used.add((str(source['id']), source['version']))
        except (ValueError, KeyError, TypeError) as exc:
            warnings.append(f'Historial no interpretable: {path}: {exc}')
    for name in ('ideas-para-notes.md', 'notes-para-revisar.md'):
        if (project / name).exists():
            files.add(Layout(project).relative(project / name))
        for path in Layout(project).batches.rglob(name):
            files.add(Layout(project).relative(path))
    return used, sorted(files), warnings


def prepare(project, download=True, now=None):
    project = project.resolve()
    layout = Layout(project)
    now = now or datetime.now(ZoneInfo(layout.config['zona']))
    parent = layout.batches
    parent.mkdir(exist_ok=True)
    name = now.astimezone(ZoneInfo(layout.config['zona'])).strftime('%Y-%m-%d_%H-%M-%S')
    run = parent / name
    suffix = 1
    while True:
        try:
            run.mkdir()
            break
        except FileExistsError:
            run = parent / f'{name}_{suffix:02d}'
            suffix += 1
    archive = layout.library
    report = {'omitida': True, 'motivo': 'Uso explícito del archivo local, sin nueva consulta.'}
    errors = []
    state = {'version_esquema': 2, 'inicio': now.isoformat(), 'zona': layout.config['zona'],
             'estado': 'preparando', 'descarga': report, 'pendientes': errors,
             'candidatas': [], 'historial_editorial': [], 'fuentes': [], 'ideas': [], 'notes': []}
    save(run / 'estado.json', state)
    summary(run, state)
    if download:
        started = datetime.now(timezone.utc)
        script = project / '.agents/skills/recuperar-newsletters/scripts/recuperar_newsletters.py'
        result = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(script),
                                 '--project-root', str(project)], capture_output=True, text=True, encoding='utf-8')
        try:
            current = read(layout.control / 'ultima_ejecucion.json', {})
        except (ValueError, OSError) as exc:
            current = {}
            errors.append(f'Informe de descarga ilegible: {exc}')
        if current.get('inicio') and datetime.fromisoformat(current['inicio']) >= started:
            report = current
            if result.returncode:
                errors.append('Descarga con incidencias; consultar el detalle de descarga en estado.json.')
        else:
            report = {'fallida': True, 'codigo_salida': result.returncode,
                      'motivo': (result.stderr or result.stdout or 'No se generó un informe nuevo.')[-6000:]}
            errors.append('No se completó una consulta nueva. Se utiliza el archivo conservado.')
    state['descarga'] = report
    used, previous, warnings = history(project)
    errors.extend(warnings)
    state['historial_editorial'] = previous
    additions = {str(p['id']) for p in report.get('anadidas', [])}
    updates = {str(p['id']) for p in report.get('actualizadas', [])}
    try:
        inventory = read(layout.control / 'inventario.json', [])
        if not isinstance(inventory, list):
            raise ValueError('Se esperaba una lista de newsletters.')
    except (ValueError, OSError) as exc:
        inventory = []
        errors.append(f'No se puede leer el inventario; se conservan los archivos: {exc}')
    for row in inventory:
        try:
            path = within(archive, row['file'])
            if not row.get('status', '').startswith('Completo'):
                raise ValueError('Solo hay un extracto o no se ha acreditado el cuerpo completo.')
            if not path.is_file() or not path.read_text(encoding='utf-8').strip():
                raise ValueError('La copia local falta o está vacía.')
            local_hash = digest(path)
            if row.get('file_hash') and row['file_hash'] != local_hash:
                raise ValueError('La copia local difiere de la versión comprobada por el descargador.')
            version = row.get('content_hash') or local_hash
            key = str(row['id'])
            origin = 'añadida' if key in additions else 'actualizada' if key in updates else 'archivo existente'
            already = (key, version) in used
            state['candidatas'].append({
                'id': row['id'], 'title': row['title'], 'date': row['date'], 'url': row['url'],
                'archivo': layout.relative(path), 'version': version, 'file_hash': local_hash,
                'procedencia': origin, 'con_notes_registradas': already,
                'prioridad': 0 if key in additions | updates else 2 if already else 1,
                'ultima_comprobacion': row.get('last_checked')})
        except (ValueError, KeyError, OSError) as exc:
            errors.append(f"Newsletter {row.get('id')}: {exc}")
    state['candidatas'].sort(key=lambda p: p['date'], reverse=True)
    state['candidatas'].sort(key=lambda p: p['prioridad'])
    state['estado'] = 'pendiente_ideas' if state['candidatas'] else 'sin_fuentes_utilizables'
    save(run / 'estado.json', state)
    summary(run, state)
    return run


def select(run, ids):
    state = read(run / 'estado.json')
    if state['estado'] == 'para_revision':
        raise ValueError('Esta ejecución ya está cerrada; crear otra para una nueva tanda.')
    candidates = {str(p['id']): p for p in state['candidatas']}
    if len(ids) != len(set(ids)) or not set(ids) <= candidates.keys():
        raise ValueError('Seleccionar IDs distintos que existan en candidatas.')
    selected = {str(p['id']): p for p in state['fuentes']}
    for key in ids:
        row = candidates[key]
        source = Layout(run.parent.parent).resolve(row['archivo'])
        if digest(source) != row['file_hash']:
            raise ValueError(f'La fuente {key} cambió tras preparar la ejecución; preparar una nueva.')
        selected[key] = dict(row)
    state['fuentes'] = list(selected.values())
    save(run / 'estado.json', state)
    summary(run, state)


def register_ideas(run):
    state = read(run / 'estado.json')
    sources = {str(p['id']): p for p in state['fuentes']}
    text = (run / 'ideas-para-notes.md').read_text(encoding='utf-8')
    if not state['ideas'] or len({i['id'] for i in state['ideas']}) != len(state['ideas']):
        raise ValueError('Faltan ideas o tienen identificadores repetidos.')
    for idea in state['ideas']:
        source = sources[str(idea['newsletter_id'])]
        if not idea.get('enfoque', '').strip() or idea['id'] not in text or source['url'] not in text:
            raise ValueError('Una idea no tiene respaldo o no aparece en el documento.')
        Layout(run.parent.parent).source(source)
    state['estado'] = 'pendiente_notes'
    save(run / 'estado.json', state)
    summary(run, state)


def close(run):
    state = read(run / 'estado.json')
    sources = {str(p['id']): p for p in state['fuentes']}
    ideas = {p['id']: p for p in state['ideas']}
    if not ideas or not state['notes']:
        raise ValueError('Faltan ideas o Notes: la ejecución sigue pendiente, no terminada.')
    if len(ideas) != len(state['ideas']) or len({n['id'] for n in state['notes']}) != len(state['notes']):
        raise ValueError('Los identificadores editoriales deben ser únicos.')
    idea_text = (run / 'ideas-para-notes.md').read_text(encoding='utf-8')
    note_text = (run / 'notes-para-revisar.md').read_text(encoding='utf-8')
    for idea in ideas.values():
        source = sources[str(idea['newsletter_id'])]
        if not idea.get('enfoque', '').strip() or idea['id'] not in idea_text or source['url'] not in idea_text:
            raise ValueError('Una idea carece de enfoque, identificador o enlace en el documento.')
        Layout(run.parent.parent).source(source)
    for note in state['notes']:
        source = sources[str(ideas[note['idea_id']]['newsletter_id'])]
        if note['id'] not in note_text or source['url'] not in note_text:
            raise ValueError('Una Note carece de identificador o enlace en el documento.')
    state['estado'] = 'para_revision'
    state['fin'] = datetime.now(ZoneInfo(state['zona'])).isoformat()
    save(run / 'estado.json', state)
    summary(run, state)


def summary(run, state):
    counts = state['descarga'].get('conteos', {})
    text = f"# Ejecución de newsletters\n\nEstado: **{state['estado']}**.\n\nInicio: {state['inicio']} ({state['zona']}).\n\n"
    if counts:
        text += (f"Descarga: {counts.get('anadidas', 0)} añadidas, {counts.get('actualizadas', 0)} actualizadas, "
                 f"{counts.get('sin_cambios', 0)} sin cambios; {counts.get('no_recuperadas', 0)} no recuperadas íntegramente "
                 f"y {counts.get('errores_archivo', 0)} errores de paginación.\n\n")
    else:
        text += 'No hay una descarga nueva acreditada. Consultar el registro para el motivo.\n\n'
    text += f"Fuentes disponibles: {len(state['candidatas'])}. Seleccionadas: {len(state['fuentes'])}.\n\n"
    text += f"Ideas registradas: {len(state['ideas'])}. Notes registradas: {len(state['notes'])}. Los textos son borradores para revisión.\n\n"
    for filename, label in [('ideas-para-notes.md', 'Ideas'), ('notes-para-revisar.md', 'Notes para revisar')]:
        if (run / filename).is_file():
            text += f'- [{label}]({filename})\n'
    text += '\n[Registro de descarga, fuentes y relaciones](estado.json)\n\n'
    if state['fuentes']:
        text += 'Fuentes utilizadas:\n\n'
        for row in state['fuentes']:
            try:
                source = Layout(run.parent.parent).source(row)
                link = Path(os.path.relpath(source, run)).as_posix()
                text += f"- [{row['title']}]({link}) — {row['procedencia']}.\n"
            except ValueError as exc:
                text += f"- {row['title']}: {exc}\n"
    if state['pendientes']:
        text += '\nPendientes o incidencias:\n\n' + '\n'.join(f'- {p}' for p in state['pendientes']) + '\n'
    if state['estado'] != 'para_revision':
        text += '\nEl trabajo editorial no está terminado. La ausencia de novedades en la descarga no lo cancela.\n'
    (run / 'RESUMEN.md').write_text(text, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('accion', choices=['preparar', 'seleccionar', 'registrar-ideas', 'cerrar', 'resumen', 'fuentes'])
    parser.add_argument('--project-root', type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument('--tanda', '--ejecucion', dest='ejecucion', type=Path)
    parser.add_argument('--ids', nargs='+')
    parser.add_argument('--sin-descarga', action='store_true', help='Solo si el usuario pide usar el archivo local.')
    args = parser.parse_args()
    if args.accion == 'preparar':
        run = prepare(args.project_root, download=not args.sin_descarga)
    else:
        if not args.ejecucion:
            parser.error('Esta acción necesita --tanda.')
        run = args.ejecucion.resolve()
        if run.parent != Layout(args.project_root).batches:
            parser.error('La ejecución debe estar dentro de la carpeta de tandas del proyecto.')
        if args.accion == 'seleccionar':
            if not args.ids:
                parser.error('Seleccionar necesita --ids.')
            select(run, args.ids)
        elif args.accion == 'registrar-ideas':
            register_ideas(run)
        elif args.accion == 'fuentes':
            state = read(run / 'estado.json')
            for row in state['fuentes']:
                print(Layout(args.project_root).source(row))
        elif args.accion == 'cerrar':
            close(run)
        else:
            summary(run, read(run / 'estado.json'))
    print(str(run), flush=True)


if __name__ == '__main__':
    main()
