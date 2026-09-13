"""Pruebas del relevo entre descarga, ideas y Notes, sin publicar ni acceder a red."""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'recuperar-newsletters/scripts'))
from test_recuperar_newsletters import temporary_archive, Client, post, NOW
from recuperar_newsletters import Archive
from flujo_newsletter import prepare, select, close, read, save, history, register_ideas
from configuracion import Layout


class FlowTests(unittest.TestCase):
    def test_standalone_ideas_then_notes_use_the_same_batch(self):
        with temporary_archive() as project:
            self.archived(project)
            run = prepare(project, download=False)
            self.draft(run)
            state = read(run / 'estado.json')
            state['notes'] = []
            save(run / 'estado.json', state)
            (run / 'notes-para-revisar.md').unlink()
            register_ideas(run)
            self.assertEqual(read(run / 'estado.json')['estado'], 'pendiente_notes')
            self.assertFalse((project / 'ideas-para-notes.md').exists())
            self.draft(run)
            close(run)
            self.assertEqual(len(list((project / 'tandas').iterdir())), 1)
            self.assertFalse((run / 'newsletters').exists())

    def test_recorded_source_survives_updates_without_per_batch_copy(self):
        with temporary_archive() as project:
            archive = self.archived(project)
            run = prepare(project, download=False)
            self.draft(run)
            state = read(run / 'estado.json')
            row = state['fuentes'][0]
            original = Layout(project).source(row).read_bytes()
            changed = post()
            changed['body_html'] = '<p>Una versión posterior para otra tanda.</p>'
            Archive(archive, Client([changed, post(2, 'segunda')]), NOW).run()
            historic = Layout(project).source(row)
            self.assertIn('historial', historic.parts)
            self.assertEqual(historic.read_bytes(), original)
            close(run)
            self.assertFalse((run / 'newsletters').exists())
            self.assertEqual(len(list((archive / 'control/datos_api').glob('post_*.json'))), 2)
            self.assertEqual(len(list((archive / 'control/descargas').glob('*/post_*.json'))), 0)

    def test_configuration_and_relocation_keep_references_valid(self):
        with temporary_archive() as parent:
            project = parent / 'origen'
            project.mkdir()
            save(project / 'newsletter.config.json', {'version': 1, 'biblioteca': 'fuentes', 'tandas': 'editorial'})
            Archive(Layout(project).library, Client([post()]), NOW).run()
            run = prepare(project, download=False)
            self.draft(run)
            state = read(run / 'estado.json')
            self.assertFalse(Path(state['fuentes'][0]['archivo']).is_absolute())
            relative_run = run.relative_to(project)
            destination = (parent / 'trasladado').resolve()
            self.assertTrue(destination.is_relative_to(parent.resolve()))
            project.rename(destination)
            moved_run = destination / relative_run
            self.assertTrue(Layout(destination).source(state['fuentes'][0]).is_file())
            close(moved_run)
            self.assertEqual(read(moved_run / 'estado.json')['estado'], 'para_revision')

    def archived(self, project):
        root = project / 'biblioteca'
        Archive(root, Client([post(), post(2, 'segunda')]), NOW).run()
        return root

    def draft(self, run):
        select(run, ['1'])
        state = read(run / 'estado.json')
        state['ideas'] = [{'id': 'I01', 'newsletter_id': 1, 'enfoque': 'Un aprendizaje de prueba'}]
        state['notes'] = [{'id': 'N01', 'idea_id': 'I01'}]
        save(run / 'estado.json', state)
        (run / 'ideas-para-notes.md').write_text('I01. https://ainalluna.substack.com/p/prueba', encoding='utf-8')
        (run / 'notes-para-revisar.md').write_text('N01. https://ainalluna.substack.com/p/prueba', encoding='utf-8')

    def test_unchanged_download_still_prepares_pending_sources(self):
        with temporary_archive() as project:
            archive = self.archived(project)
            def download(*args, **kwargs):
                Archive(archive, Client([post(), post(2, 'segunda')])).run()
                return SimpleNamespace(returncode=0, stderr='', stdout='')
            with patch('flujo_newsletter.subprocess.run', side_effect=download):
                run = prepare(project)
            state = read(run / 'estado.json')
            self.assertEqual(state['descarga']['conteos']['anadidas'], 0)
            self.assertEqual(state['estado'], 'pendiente_ideas')
            self.assertEqual(len(state['candidatas']), 2)
            self.assertFalse(any(p['con_notes_registradas'] for p in state['candidatas']))

    def test_failed_download_ignores_old_report_and_preserves_sources(self):
        with temporary_archive() as project:
            self.archived(project)
            with patch('flujo_newsletter.subprocess.run', return_value=SimpleNamespace(returncode=1, stderr='Red bloqueada', stdout='')):
                run = prepare(project)
            state = read(run / 'estado.json')
            self.assertTrue(state['descarga']['fallida'])
            self.assertIn('Red bloqueada', state['descarga']['motivo'])
            self.assertEqual(state['estado'], 'pendiente_ideas')
            self.assertEqual(len(state['candidatas']), 2)

    def test_close_records_only_real_outputs_and_next_run_prioritizes_unused(self):
        with temporary_archive() as project:
            self.archived(project)
            run = prepare(project, download=False, now=NOW)
            with self.assertRaises(ValueError):
                close(run)
            self.draft(run)
            close(run)
            state = read(run / 'estado.json')
            self.assertEqual(state['estado'], 'para_revision')
            before = (run / 'notes-para-revisar.md').read_bytes()
            second = prepare(project, download=False, now=NOW)
            self.assertNotEqual(run, second)
            next_state = read(second / 'estado.json')
            self.assertEqual(next_state['candidatas'][0]['id'], 2)
            self.assertTrue(next_state['candidatas'][1]['con_notes_registradas'])
            self.assertEqual((run / 'notes-para-revisar.md').read_bytes(), before)

    def test_broken_relation_and_changed_copy_cannot_close(self):
        with temporary_archive() as project:
            self.archived(project)
            run = prepare(project, download=False)
            self.draft(run)
            state = read(run / 'estado.json')
            source = project / state['fuentes'][0]['archivo']
            source.write_text('Cambio local', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'versión'):
                close(run)
            self.assertEqual(read(run / 'estado.json')['estado'], 'pendiente_ideas')

    def test_no_sources_is_explained_and_does_not_finish(self):
        with temporary_archive() as project:
            run = prepare(project, download=False)
            self.assertEqual(read(run / 'estado.json')['estado'], 'sin_fuentes_utilizables')
            with self.assertRaises(ValueError):
                close(run)

    def test_removed_notes_are_pending_again(self):
        with temporary_archive() as project:
            self.archived(project)
            run = prepare(project, download=False)
            self.draft(run)
            close(run)
            (run / 'notes-para-revisar.md').unlink()
            second = prepare(project, download=False)
            state = read(second / 'estado.json')
            self.assertFalse(any(p['con_notes_registradas'] for p in state['candidatas']))
            self.assertTrue(state['pendientes'])

    def test_updated_version_is_pending_again(self):
        with temporary_archive() as project:
            archive = self.archived(project)
            run = prepare(project, download=False)
            self.draft(run)
            close(run)
            changed = post()
            changed['body_html'] = '<p>Una nueva explicación.</p>'
            Archive(archive, Client([changed, post(2, 'segunda')]), NOW).run()
            second = prepare(project, download=False)
            state = read(second / 'estado.json')
            self.assertFalse(next(p for p in state['candidatas'] if p['id'] == 1)['con_notes_registradas'])


if __name__ == '__main__':
    unittest.main()
