#!/usr/bin/env python3
"""Check generated HTML navigation, anchors, publication data, and assets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'preview'
class Document(HTMLParser):
 def __init__(self):
  super().__init__();self.links=[];self.ids=[];self.h1=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if 'id' in a:self.ids.append(a['id'])
  for k in ['href','src']:
   if k in a:self.links.append(a[k])
errors=[];pages={}
for p in OUT.rglob('*.html'):
 d=Document();d.feed(p.read_text());pages[p]=d
 if d.h1!=1:errors.append(f'{p}: expected one H1')
 if len(d.ids)!=len(set(d.ids)):errors.append(f'{p}: duplicate IDs')
 if '{{' in p.read_text() or '{%' in p.read_text():errors.append(f'{p}: unresolved template')
for p,d in pages.items():
 for link in d.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  target=(OUT/unquote(u.path).lstrip('/')) if u.path.startswith('/') else (p.parent/unquote(u.path))
  if not u.path:target=p
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{p}: missing {link}')
  elif u.fragment and target in pages and u.fragment not in pages[target].ids:errors.append(f'{p}: missing anchor {link}')
data=json.loads((ROOT/'_data/publications.json').read_text())
assert len({p['id'] for p in data})==len(data)
for p in data:
 assert all(k in p for k in ['id','title','authors','year','venue','links','topic','note'])
 assert all(urlsplit(v).scheme in ['https','http'] for v in p['links'].values())
for f in (ROOT/'_data').glob('project-*.json'):
 assert set(json.loads(f.read_text())) <= {p['id'] for p in data}
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages, all internal links and anchors, asset paths, unique IDs, {len(data)} publication records and project references.')
