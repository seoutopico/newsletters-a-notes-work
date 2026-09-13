"""Contrato de almacenamiento compartido por descarga y trabajo editorial."""
import json
from pathlib import Path

DEFAULTS = {'version': 1, 'publicacion': 'https://ainalluna.substack.com',
            'desde': '2025-09-12T00:00:00+02:00', 'zona': 'Europe/Madrid',
            'biblioteca': 'biblioteca', 'tandas': 'tandas'}


class Layout:
    def __init__(self, project):
        self.project = Path(project).resolve()
        config = self.project / 'newsletter.config.json'
        self.config = dict(DEFAULTS)
        if config.exists():
            self.config.update(json.loads(config.read_text(encoding='utf-8-sig')))
        if self.config['version'] != 1:
            raise ValueError('Versión de configuración no compatible.')
        for key in ('biblioteca', 'tandas'):
            name = self.config[key]
            if not isinstance(name, str) or name in ('', '.', '..') or '/' in name or '\\' in name or ':' in name:
                raise ValueError(f'{key} debe ser una carpeta directamente dentro del proyecto.')
        if self.config['biblioteca'].casefold() == self.config['tandas'].casefold():
            raise ValueError('La biblioteca y las tandas necesitan carpetas distintas.')
        self.library = self.project / self.config['biblioteca']
        self.control = self.library / 'control'
        self.articles = self.library / 'articulos'
        self.batches = self.project / self.config['tandas']

    def relative(self, path):
        return Path(path).resolve().relative_to(self.project).as_posix()

    def resolve(self, relative):
        path = (self.project / relative).resolve()
        if not path.is_relative_to(self.project):
            raise ValueError('La referencia sale del proyecto.')
        return path

    def source(self, row):
        """Find the recorded byte version in the library, including old versions."""
        import hashlib
        current = self.resolve(row['archivo'])
        candidates = [current]
        candidates.extend((self.control / 'historial' / str(row['id'])).rglob('*.md'))
        for path in candidates:
            if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == row['file_hash']:
                return path
        raise ValueError(f"No está disponible la versión registrada de la newsletter {row['id']}.")
