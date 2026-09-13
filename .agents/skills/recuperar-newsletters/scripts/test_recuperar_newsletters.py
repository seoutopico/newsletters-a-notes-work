"""Pruebas de conservación del archivo, sin acceso a red."""
import copy
import json
import uuid
import shutil
import unittest
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from recuperar_newsletters import Archive, save_json

NOW = datetime(2026, 9, 12, 18, tzinfo=timezone.utc)


@contextmanager
def temporary_archive():
    workspace = Path.cwd().resolve()
    directory = (workspace / ('prueba_newsletters_' + uuid.uuid4().hex)).resolve()
    directory.mkdir()
    try:
        yield directory
    finally:
        if directory.parent != workspace or not directory.name.startswith('prueba_newsletters_'):
            raise ValueError('Ruta temporal fuera del proyecto.')
        shutil.rmtree(directory)


def post(identifier=1, slug='prueba'):
    return {'id': identifier, 'slug': slug, 'title': 'Título con acentos',
            'subtitle': 'Subtítulo', 'post_date': '2026-09-09T05:54:34.887Z',
            'canonical_url': f'https://ainalluna.substack.com/p/{slug}',
            'audience': 'everyone', 'body_html': '<h2>Hola</h2><p>Contenido completo.</p>',
            'type': 'newsletter'}


class Client:
    def __init__(self, entries):
        self.entries = entries
        self.archive_error = False
        self.fail_ids = set()
        self.calls = []

    def __call__(self, url):
        self.calls.append(url)
        if '/archive?' in url:
            if self.archive_error:
                raise RuntimeError('Fallo de archivo simulado')
            offset = int(parse_qs(urlparse(url).query)['offset'][0])
            return copy.deepcopy(self.entries[offset:offset + 1])  # Deliberately short pages.
        entry = next(p for p in self.entries if url.endswith('/' + p['slug']))
        if entry['id'] in self.fail_ids:
            raise RuntimeError('Fallo de consulta simulado')
        return copy.deepcopy(entry)


class PreservationTests(unittest.TestCase):
    def test_configured_publication_controls_api_and_relative_links(self):
        with temporary_archive() as root:
            entry = post()
            entry['canonical_url'] = 'https://otra.substack.com/p/prueba'
            entry['body_html'] = '<p>Ver <a href="/p/detalle">detalle</a>.</p>'
            client = Client([entry])
            Archive(root, client, NOW, config={'publicacion': 'https://otra.substack.com'}).run()
            text = next((root / 'articulos').glob('*.md')).read_text(encoding='utf-8')
            self.assertIn('https://otra.substack.com/p/detalle', text)
            self.assertTrue(all(url.startswith('https://otra.substack.com/') for url in client.calls))

    def test_empty_missing_and_modified_files_are_repaired(self):
        with temporary_archive() as root:
            client = Client([post()])
            Archive(root, client, NOW).run()
            article = next((root / 'articulos').glob('*.md'))
            good = article.read_bytes()
            for damage in ('empty', 'missing', 'modified'):
                if damage == 'missing':
                    article.unlink()
                else:
                    article.write_text('' if damage == 'empty' else 'Contenido alterado', encoding='utf-8')
                result = Archive(root, client, NOW).run()
                self.assertEqual(result['conteos']['actualizadas'], 1)
                self.assertEqual(article.read_bytes(), good)
                self.assertIn('reparada', result['actualizadas'][0]['motivo'])

    def test_missing_inventory_recovers_legacy_path_without_duplicate(self):
        with temporary_archive() as root:
            entry = post()
            article = root / 'articulos' / '2026-09-09_prueba.md'
            article.parent.mkdir()
            article.write_text('Texto legado conservado', encoding='utf-8')
            save_json(root / 'control' / 'datos_api/post_1.json', entry)
            result = Archive(root, Client([entry]), NOW).run()
            self.assertEqual(result['inventario_reconstruido'], [1])
            self.assertEqual(result['conteos']['anadidas'], 0)
            self.assertEqual(result['conteos']['sin_cambios'], 1)
            self.assertEqual(len(list((root / 'articulos').glob('*.md'))), 1)
            self.assertEqual(article.read_text(encoding='utf-8'), 'Texto legado conservado')

    def test_unidentified_existing_file_blocks_without_writing(self):
        with temporary_archive() as root:
            article = root / 'articulos/desconocida.md'
            article.parent.mkdir()
            article.write_text('Conservar', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'identificar'):
                Archive(root, Client([post()]), NOW)
            self.assertFalse((root / 'control' / 'inventario.json').exists())
            self.assertEqual(article.read_text(encoding='utf-8'), 'Conservar')

    def test_failed_download_of_missing_file_does_not_count_it_as_saved(self):
        with temporary_archive() as root:
            client = Client([post()])
            Archive(root, client, NOW).run()
            next((root / 'articulos').glob('*.md')).unlink()
            client.fail_ids.add(1)
            result = Archive(root, client, NOW).run()
            self.assertEqual(result['total_guardadas'], 0)
            self.assertEqual(result['total_registradas'], 1)
            self.assertEqual(result['conteos']['no_recuperadas'], 1)

    def test_add_repeat_change_slug_and_restricted_access(self):
        with temporary_archive() as directory:
            root = Path(directory)
            client = Client([post(), post(2, 'segunda')])
            first = Archive(root, client, NOW).run()
            self.assertEqual(first['conteos']['anadidas'], 2)
            self.assertTrue(first['cobertura_completa'])
            rows = json.loads((root / 'control' / 'inventario.json').read_text(encoding='utf-8'))
            article = root / next(p for p in rows if p['id'] == 1)['file']
            before, modified = article.read_bytes(), article.stat().st_mtime_ns
            second = Archive(root, client, NOW).run()
            self.assertEqual(second['conteos']['sin_cambios'], 2)
            self.assertEqual(article.read_bytes(), before)
            self.assertEqual(article.stat().st_mtime_ns, modified)
            client.entries[0].update(title='Nuevo título', slug='nuevo-slug', body_html='<p>Contenido editado.</p>')
            third = Archive(root, client, NOW).run()
            self.assertEqual(third['conteos']['actualizadas'], 1)
            self.assertIn('Contenido editado', article.read_text(encoding='utf-8'))
            self.assertEqual(len(list((root / 'articulos').glob('*.md'))), 2)
            self.assertEqual(next((root / 'control' / 'historial' / '1').rglob('*.md')).read_bytes(), before)
            good = article.read_bytes()
            client.entries[0].update(audience='only_paid', body_html='<p>Extracto.</p>')
            fourth = Archive(root, client, NOW).run()
            self.assertEqual(fourth['conteos']['no_recuperadas'], 1)
            self.assertEqual(article.read_bytes(), good)
            client.fail_ids.add(1)
            fifth = Archive(root, client, NOW).run()
            self.assertEqual(fifth['conteos']['no_recuperadas'], 1)
            self.assertEqual(article.read_bytes(), good)

    def test_legacy_migration_and_missing_archive(self):
        with temporary_archive() as directory:
            root = Path(directory)
            entry = post()
            article = root / 'articulos' / 'ruta_original.md'
            article.parent.mkdir(parents=True)
            article.write_text('Copia antigua que debe permanecer intacta', encoding='utf-8')
            row = {'id': 1, 'title': entry['title'], 'date': entry['post_date'],
                   'url': entry['canonical_url'], 'api_url': 'https://ainalluna.substack.com/api/v1/posts/prueba',
                   'status': 'Completo (cuerpo público de la API)', 'file': 'articulos/ruta_original.md'}
            save_json(root / 'control' / 'inventario.json', [row])
            save_json(root / 'control' / 'datos_api' / 'post_1.json', entry)
            client = Client([entry])
            before = article.read_bytes()
            result = Archive(root, client, NOW).run()
            self.assertEqual(result['conteos']['sin_cambios'], 1)
            self.assertEqual(article.read_bytes(), before)
            client.archive_error = True
            result = Archive(root, client, NOW).run()
            self.assertFalse(result['cobertura_completa'])
            self.assertEqual(result['conteos']['errores_archivo'], 1)
            self.assertEqual(result['total_guardadas'], 1)
            self.assertEqual(article.read_bytes(), before)

    def test_new_excerpt_is_reported(self):
        with temporary_archive() as directory:
            entry = post()
            entry.update(body_html=None, description='Un resumen breve.')
            report = Archive(Path(directory), Client([entry]), NOW).run()
            self.assertEqual(report['conteos']['anadidas'], 1)
            self.assertEqual(report['conteos']['no_recuperadas'], 1)


if __name__ == '__main__':
    unittest.main()
