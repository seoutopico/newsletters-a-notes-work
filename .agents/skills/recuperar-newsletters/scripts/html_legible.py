import re
from datetime import datetime
from html.parser import HTMLParser
from configuracion import DEFAULTS
BASE = DEFAULTS['publicacion']

class ReadableHTML(HTMLParser):
    def __init__(self, base=BASE):
        super().__init__(convert_charrefs=True)
        self.base = base.rstrip('/')
        self.parts = []
        self.links = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style'):
            self.skip += 1
        if self.skip:
            return
        if tag in ('p', 'div', 'blockquote', 'figure', 'figcaption', 'ul', 'ol', 'table', 'tr'):
            self.parts.append('\n\n')
        elif re.fullmatch(r'h[1-6]', tag):
            self.parts.append('\n\n' + '#' * int(tag[1]) + ' ')
        elif tag == 'br':
            self.parts.append('\n')
        elif tag == 'li':
            self.parts.append('\n- ')
        elif tag == 'a':
            self.links.append(attrs.get('href', ''))
        elif tag == 'img':
            alt = attrs.get('alt', '').strip() or 'Imagen del artículo'
            src = attrs.get('src', '')
            if src:
                self.parts.append(f'\n\n[{alt}]({src})\n\n')
        elif tag == 'iframe':
            src = attrs.get('src', '')
            if src:
                self.parts.append(f'\n\n[Contenido incrustado]({src})\n\n')
        elif tag in ('td', 'th'):
            self.parts.append(' | ')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag == 'a' and self.links:
            href = self.links.pop()
            if href and not href.startswith('javascript:'):
                if href.startswith('/'):
                    href = self.base + href
                self.parts.append(f' ({href})')
        if tag in ('p', 'div', 'blockquote', 'figure', 'figcaption', 'li', 'tr') or re.fullmatch(r'h[1-6]', tag):
            self.parts.append('\n\n')

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(re.sub(r'\s+', ' ', data))

    def result(self):
        text = ''.join(self.parts)
        text = re.sub(r'[ \t]+\n', '\n', text)
        text = re.sub(r'\n[ \t]+', '\n', text)
        return re.sub(r'\n{3,}', '\n\n', text).strip()


def readable(html, base=BASE):
    parser = ReadableHTML(base)
    parser.feed(html or '')
    return parser.result()


def date_of(post):
    return datetime.fromisoformat(post['post_date'].replace('Z', '+00:00'))
