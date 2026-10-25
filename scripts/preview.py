#!/usr/bin/env python3
"""Create a dependency-free static preview of this site's supported templates.
Jekyll is the deployment renderer. This preview is deliberately specific to
these templates, and is not a general Liquid interpreter.
"""
from pathlib import Path
from html import escape
import json, re, shutil, argparse
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', default='', help='e.g. /research-site')
args = parser.parse_args()
base = args.baseurl.rstrip('/')
OUT = ROOT / 'preview'
OUT.mkdir(exist_ok=True)
publications = json.loads((ROOT / '_data/publications.json').read_text())
def authors(value):
    return escape(value).replace('Priyesh Vijayan', '<strong class="author-self">Priyesh Vijayan</strong>').replace('P Vijayan', '<strong class="author-self">P Vijayan</strong>')
def publication(p):
    links = ''.join(f'<a href="{escape(v, quote=True)}">{escape(k)} ↗</a>' for k,v in p['links'].items())
    note_class = 'pub-note award-note' if p.get('note_style') == 'award' else 'pub-note'
    note = f'<p class="{note_class}">{escape(p["note"])}</p>' if p['note'] else '' 
    versions = ''
    for v in p.get('occurrences', []):
        versions += f'<p class="venue occurrence" id="{v["id"]}">{escape(v["venue"])}</p>'
    if versions: versions = f'<div class="occurrences" aria-label="Workshop presentations">{versions}</div>'
    return f'<article class="pub" id="{p["id"]}" data-year="{p["year"]}" data-topic="{escape(p["topic"], quote=True)}"><div class="pub-year">{p["year"]}</div><div><h3>{escape(p["title"])}</h3><p class="authors">{authors(p["authors"])}</p><p class="venue">{escape(p["venue"])}</p><div class="pub-links">{links}</div>{note}{versions}</div></article>'
def include(match):
    name = match[1]
    ids = None
    if name == 'selected-publications': ids = ['p1','p2','p4','p5']
    if name.startswith('project-'): ids = json.loads((ROOT / '_data' / (name+'.json')).read_text())
    return ''.join(publication(p) for p in publications if ids is None or p['id'] in ids)
for src in list(ROOT.glob('*.html')) + list((ROOT/'projects').glob('*.html')):
    _, front, body = src.read_text().split('---', 2)
    metadata = {}
    for line in front.strip().splitlines():
        key, value = line.split(':',1)
        metadata[key] = value.strip().strip('"')
    body = re.sub(r"{% assign topics =.*?{% endfor %}", ''.join(f'<option>{escape(t)}</option>' for t in sorted({p['topic'] for p in publications})), body)
    body = re.sub(r"{% assign years =.*?{% endfor %}", ''.join(f'<option>{y}</option>' for y in sorted({p['year'] for p in publications}, reverse=True)), body)
    body = body.replace('{{ site.data.publications | size }}', str(len(publications)))
    body = re.sub(r'{% include ([a-z-]+)\.html %}', include, body)
    rendered = (ROOT / '_layouts/default.html').read_text().replace('{{ content }}',body)
    for key in ['title','description']:
        rendered = rendered.replace('{{ page.'+key+' }}',escape(metadata[key],quote=True))
    rendered = re.sub(r"{{ '([^']*)' \| relative_url }}", lambda m:base+m[1], rendered)
    assert '{{' not in rendered and '{%' not in rendered, src
    dest = OUT / base.lstrip('/') / metadata['permalink'].strip('/') / 'index.html'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(rendered)
assets = OUT / base.lstrip('/') / 'assets'
shutil.copytree(ROOT/'assets',assets,dirs_exist_ok=True)
print(f'Wrote static preview to {OUT}. Serve with: python3 -m http.server 8000 --directory preview')
