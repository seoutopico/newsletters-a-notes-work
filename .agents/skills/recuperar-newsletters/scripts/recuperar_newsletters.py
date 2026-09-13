"""Archivo incremental de Think & Hack. Python 3.10+ y requests."""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from html_legible import readable, date_of
from configuracion import Layout, DEFAULTS

BASE = DEFAULTS['publicacion']
START = DEFAULTS['desde']
COMPLETE = 'Completo (cuerpo público de la API)'
MEDIA = 'Texto y enlaces conservados. Imágenes y recursos multimedia enlazados, sin descargar sus archivos.'


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(text, encoding='utf-8')
    os.replace(temp, path)


def save_json(path, data):
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def load_json(path, default=None):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else default


def fingerprint(post):
    # Ignore reactions, counters and retrieval times, which are not editorial changes.
    fields = ('title', 'subtitle', 'slug', 'post_date', 'canonical_url', 'type',
              'audience', 'body_html', 'free_unlock_required', 'post_preview_limit')
    values = {key: post.get(key) for key in fields}
    if not post.get('body_html'):
        values['excerpt'] = post.get('truncated_body_text') or post.get('description')
    return hashlib.sha256(json.dumps(values, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def recover_inventory(root, rows, base=BASE):
    """Reconcile unregistered files by explicit ID, original URL, or exact legacy name.

    Ambiguous files stop recovery before writing, so a missing index cannot duplicate
    or overwrite the archive. Never infer identity from a title similarity.
    """
    known = {p['file'].replace('\\', '/').casefold() for p in rows if p.get('file')}
    raw = {}
    for path in (root / 'control' / 'datos_api').glob('post_*.json'):
        post = load_json(path)
        raw[str(post['id'])] = post
    recovered = []
    for path in (root / 'articulos').glob('*.md'):
        relative = path.relative_to(root).as_posix()
        if relative.casefold() in known:
            continue
        header = path.read_text(encoding='utf-8-sig').split('\n---', 1)[0]
        explicit = re.search(r'\*\*ID de Substack:\*\*\s*(\d+)', header)
        link = re.search(r'\*\*Enlace original:\*\*\s*(https?://\S+)', header)
        candidates = []
        for key, post in raw.items():
            url = post.get('canonical_url') or f"{base}/p/{post['slug']}"
            legacy = f"{post['post_date'][:10]}_{post['slug']}.md"
            if ((explicit and explicit.group(1) == key) or
                (link and link.group(1).rstrip('/') == url.rstrip('/')) or
                path.name == legacy or path.name.startswith(f"{post['post_date'][:10]}_{key}_")):
                candidates.append(post)
        if len(candidates) != 1:
            raise ValueError(f'No se puede identificar de forma única {relative}; se conserva sin crear duplicados.')
        post = candidates[0]
        if any(str(p['id']) == str(post['id']) for p in rows + recovered):
            raise ValueError(f"Más de un archivo para el ID {post['id']}; se conservan para revisión.")
        status, _, limitation = classify(post, base)
        recovered.append({'id': post['id'], 'title': post['title'], 'date': post['post_date'],
                          'slug': post['slug'], 'url': post.get('canonical_url') or f"{base}/p/{post['slug']}",
                          'file': relative, 'status': status, 'limitation': limitation,
                          'content_hash': fingerprint(post)})
    return rows + recovered, recovered


class Client:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (compatible; NewsletterArchive/2.0)'

    def __call__(self, url):
        for attempt in range(3):
            try:
                response = self.session.get(url, timeout=40)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError):
                if attempt == 2:
                    raise
                time.sleep(attempt + 1)


def classify(post, base=BASE):
    body = post.get('body_html') or ''
    text = readable(body, base)
    gate = bool(post.get('free_unlock_required')) or bool(re.search(
        r'class=[\"\'][^\"\']*(?:paywall|premium-gate)', body, re.I))
    if text and post.get('audience') == 'everyone' and not gate:
        return COMPLETE, text, MEDIA
    if text:
        return 'Extracto / integridad no verificable', text, 'No se puede acreditar el cuerpo completo; posible acceso restringido. ' + MEDIA
    text = readable(post.get('truncated_body_text') or post.get('description') or '', base)
    return ('Extracto' if text else 'No recuperado'), text, 'La API no ha devuelto body_html completo.'


def render(post, row, now, base=BASE):
    subtitle = (post.get('subtitle') + '\n\n') if post.get('subtitle') else ''
    return (f"# {row['title']}\n\n{subtitle}"
            f"- **Fecha de publicación (API):** {row['date']}\n"
            f"- **Enlace original:** {row['url']}\n"
            f"- **Estado:** {row['status']}\n"
            f"- **Tipo:** {row['type']}\n"
            f"- **ID de Substack:** {row['id']}\n"
            f"- **Fuente:** {row['api_url']}\n"
            f"- **Recuperado:** {now}\n\n"
            f"**Alcance y limitaciones:** {row['limitation']}\n\n---\n\n"
            + classify(post, base)[1] + '\n')


class Archive:
    def __init__(self, root, fetch=None, now=None, config=None):
        self.root = Path(root).resolve()
        self.control = self.root / 'control'
        self.config = config or {}
        self.base = self.config.get('publicacion', BASE).rstrip('/')
        self.start = self.config.get('desde', START)
        self.fetch = fetch or Client()
        self.now = now or datetime.now(timezone.utc)
        self.stamp = self.now.strftime('%Y%m%dT%H%M%S%fZ')
        self.run_dir = self.control / 'descargas' / self.stamp
        rows = load_json(self.control / 'inventario.json', [])
        rows, recovered = recover_inventory(self.root, rows, self.base)
        self.rows = {str(p['id']): p for p in rows}
        if len(self.rows) != len(rows):
            raise ValueError('El inventario contiene IDs duplicados; revisar antes de continuar.')
        files = [p['file'].casefold() for p in rows if p.get('file')]
        if len(set(files)) != len(files):
            raise ValueError('Dos IDs comparten archivo; revisar inventario.')
        self.report = {'inicio': self.now.isoformat(), 'publicacion': self.base, 'desde': self.start,
                       'carpeta': str(self.root), 'anadidas': [], 'actualizadas': [],
                       'sin_cambios': [], 'no_recuperadas': [], 'errores_archivo': [],
                       'paginas': [], 'cobertura_completa': False,
                       'inventario_reconstruido': [p['id'] for p in recovered]}

    def path(self, relative):
        path = (self.root / relative).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError('Ruta fuera del archivo de newsletters.')
        return path

    def event(self, key, row, reason=None):
        value = {k: row.get(k) for k in ('id', 'title', 'url', 'file')}
        if reason:
            value['motivo'] = reason
        self.report[key].append(value)

    def persist(self):
        save_json(self.control / 'inventario.json', sorted(self.rows.values(), key=lambda p: p['date'], reverse=True))

    def list_posts(self):
        offset, seen, posts = 0, set(), {}
        while True:
            url = f'{self.base}/api/v1/archive?sort=new&search=&offset={offset}&limit=12'
            try:
                page = self.fetch(url)
                if not isinstance(page, list):
                    raise ValueError('Respuesta de archivo no válida.')
                self.report['paginas'].append({'url': url, 'cantidad': len(page), 'ids': [p.get('id') for p in page]})
                if not page:
                    self.report['cobertura_completa'] = True
                    break
                ids = [str(p['id']) for p in page]
                if not set(ids) - seen:
                    raise ValueError('Página repetida; no se puede acreditar la cobertura.')
                seen.update(ids)
                for post in page:
                    if datetime.fromisoformat(self.start) <= date_of(post) <= self.now:
                        posts[str(post['id'])] = post
                # Keep traversing to the empty page: shorter pages are not an end signal.
                offset += len(page)
            except Exception as exc:
                self.report['errores_archivo'].append({'url': url, 'motivo': str(exc)})
                break
        # Recheck saved posts even if removed from the public list or outside the original window.
        for key, row in self.rows.items():
            if key not in posts:
                slug = row.get('slug') or row.get('api_url', row['url']).rstrip('/').rsplit('/', 1)[-1]
                posts[key] = {'id': row['id'], 'title': row['title'], 'slug': slug,
                              'post_date': row['date'], 'canonical_url': row['url']}
        return list(posts.values())

    def update_post(self, summary):
        key = str(summary['id'])
        old = self.rows.get(key)
        url = f"{self.base}/api/v1/posts/{summary['slug']}"
        reference = old or {'id': summary['id'], 'title': summary.get('title'),
                            'url': summary.get('canonical_url') or f"{self.base}/p/{summary['slug']}"}
        try:
            post = self.fetch(url)
            if not isinstance(post, dict) or str(post.get('id')) != key:
                raise ValueError('La respuesta individual no coincide con el ID solicitado.')
            status, text, limitation = classify(post, self.base)
            if status != COMPLETE:
                save_json(self.run_dir / f'post_{key}.json', post)
                self.event('no_recuperadas', reference, limitation)
            if not text or (old and old['status'].startswith('Completo') and status != COMPLETE):
                return  # Never replace an existing complete article with an error or preview.
            raw_path = self.control / 'datos_api' / f'post_{key}.json'
            previous = load_json(raw_path)
            old_hash = old.get('content_hash') if old else None
            if not old_hash and previous:
                old_hash = fingerprint(previous)
            new_hash = fingerprint(post)
            relative = old.get('file') if old else None
            if not relative:
                slug = re.sub(r'[^a-zA-Z0-9_-]+', '-', post.get('slug') or key).strip('-')[:100]
                relative = f"articulos/{post['post_date'][:10]}_{key}_{slug}.md"
            article_path = self.path(relative)
            if not old and article_path.exists():
                raise ValueError('Existe un archivo sin registrar con esta ruta; se conserva y se informa del conflicto.')
            usable = article_path.is_file() and bool(article_path.read_text(encoding='utf-8').strip())
            damaged = not usable or bool(old and old.get('file_hash') and old['file_hash'] != file_hash(article_path))
            changed = not old or old_hash != new_hash or damaged
            row = {'id': post['id'], 'title': post['title'], 'date': post['post_date'],
                   'url': post.get('canonical_url') or f"{self.base}/p/{post['slug']}",
                   'slug': post['slug'], 'type': post.get('type'), 'audience': post.get('audience'),
                   'status': status, 'limitation': limitation, 'file': relative, 'api_url': url,
                   'body_html_characters': len(post.get('body_html') or ''),
                   'readable_characters': len(text), 'api_wordcount': post.get('wordcount'),
                   'post_preview_limit': post.get('post_preview_limit'),
                   'free_unlock_required': post.get('free_unlock_required'),
                   'content_hash': new_hash, 'last_checked': self.now.isoformat(), 'error': None}
            if changed:
                if old:
                    backup = self.control / 'historial' / key / (file_hash(article_path) if article_path.is_file() else self.stamp)
                    if article_path.exists():
                        backup.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(article_path, backup / article_path.name)
                    if previous:
                        save_json(backup / f'post_{key}.json', previous)
                write_text(article_path, render(post, row, self.now.isoformat(), self.base))
                save_json(raw_path, post)
                self.event('actualizadas' if old else 'anadidas', row,
                           'Copia local reparada; versión anterior conservada si existía.' if old and damaged else None)
            else:
                self.event('sin_cambios', row)
            row['file_hash'] = file_hash(article_path)
            self.rows[key] = row
            self.persist()
        except Exception as exc:
            self.event('no_recuperadas', reference, str(exc))

    def finish(self):
        self.persist()
        self.report['fin'] = datetime.now(timezone.utc).isoformat()
        self.report['total_registradas'] = len(self.rows)
        self.report['total_guardadas'] = sum(
            1 for row in self.rows.values() if row.get('file') and self.path(row['file']).is_file()
            and self.path(row['file']).stat().st_size > 0)
        self.report['conteos'] = {key: len(self.report[key]) for key in
                                 ('anadidas', 'actualizadas', 'sin_cambios', 'no_recuperadas', 'errores_archivo')}
        save_json(self.run_dir / 'informe.json', self.report)
        save_json(self.control / 'ultima_ejecucion.json', self.report)
        report = '# Resultado de la descarga\n\n'
        report += f"Consulta: {self.report['inicio']}\n\nPublicación: {self.base}\n\n"
        for key, label in (('anadidas', 'Añadidas'), ('actualizadas', 'Actualizadas'),
                           ('sin_cambios', 'Sin cambios'), ('no_recuperadas', 'No recuperadas íntegramente')):
            report += f"## {label}: {len(self.report[key])}\n\n"
            for item in self.report[key]:
                report += f"- {item['title']} — {item['url']}" + (f" — {item['motivo']}" if item.get('motivo') else '') + '\n'
            report += '\n'
        report += f"Cobertura del archivo: {'completa hasta página vacía' if self.report['cobertura_completa'] else 'incompleta'}.\n\n"
        for error in self.report['errores_archivo']:
            report += f"- {error['url']}: {error['motivo']}\n"
        report += '\nLos extractos nuevos pueden figurar como añadidos y también como no recuperados íntegramente. Ante una pérdida de acceso se conserva la copia anterior.\n'
        write_text(self.run_dir / 'INFORME.md', report)
        write_text(self.control / 'ULTIMA_EJECUCION.md', report)
        rows = sorted(self.rows.values(), key=lambda p: p['date'], reverse=True)
        index = ('# Archivo de newsletters\n\n'
                 f'Publicación: {self.base}\n\nArchivo acumulativo desde {self.start[:10]}. '
                 f'Total guardado: **{len(rows)}**. Consulta: {self.now.isoformat()}.\n\n'
                 '[Resultado de la última descarga](control/ULTIMA_EJECUCION.md)\n\n'
                 'El estado describe la copia conservada; los fallos actuales aparecen en el informe. '
                 'Completo significa cuerpo público de la API con audiencia everyone y sin bloqueo explícito detectado; '
                 'no es una comparación con el original editorial. No se recuperan publicaciones ocultas o eliminadas desconocidas. '
                 'Multimedia enlazada; comentarios y Notes excluidos.\n\n'
                 '| Fecha (UTC) | Título | Copia guardada |\n|---|---|---|\n')
        for row in rows:
            title = row['title'].replace('|', '\\|')
            index += f"| {row['date'][:10]} | [{title}]({row['file']}) | {row['status']} |\n"
        write_text(self.root / 'INDICE.md', index)
        print(json.dumps(self.report['conteos'], ensure_ascii=False), flush=True)
        return self.report

    def run(self):
        posts = self.list_posts()
        for number, post in enumerate(posts, 1):
            self.update_post(post)
            print(f"{number}/{len(posts)}: {post.get('title', post['id'])}", flush=True)
        return self.finish()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', type=Path, default=Path(__file__).resolve().parents[4])
    args = parser.parse_args()
    layout = Layout(args.project_root)
    root = layout.library
    root.mkdir(parents=True, exist_ok=True)
    # OS lock is released even after interruption; the lock file itself is retained.
    layout.control.mkdir(parents=True, exist_ok=True)
    with (layout.control / '.descarga.lock').open('a+b') as lock:
        lock.seek(0)
        if os.name == 'nt':
            import msvcrt
            if not lock.read(1):
                lock.write(b'0')
                lock.flush()
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        report = Archive(root, config=layout.config).run()
        return 1 if report['no_recuperadas'] or report['errores_archivo'] else 0


if __name__ == '__main__':
    sys.exit(main())
