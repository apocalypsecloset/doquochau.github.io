"""Append an E2 release manifest without replacing E0b or historical hash records."""
import hashlib,json,subprocess
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
def sha(s):return hashlib.sha256(s.encode('utf-8')).hexdigest()
baseline=subprocess.check_output(['git','rev-parse','61515ae9'],cwd=ROOT,text=True).strip()
configs=json.loads((ROOT/'data/en-translations/batch40.json').read_text(encoding='utf-8'))
files={}
for c in configs:
 p=ROOT/'en/blog'/(c['en_slug']+'.html');raw=p.read_text(encoding='utf-8');s=BeautifulSoup(raw,'html.parser')
 for a in s.select('.batch40-additional-guides a.hub-card'):
  if a.select_one('.hub-card-body'):continue
  body=s.new_tag('div',attrs={'class':'hub-card-body'})
  for n in list(a.contents):body.append(n)
  a.append(body)
 p.write_text(str(s)+'\n',encoding='utf-8')
paths=['en/blog.html','sitemap.xml']+['blog/'+c['vi_slug']+'.html' for c in configs]+['en/blog/'+c['en_slug']+'.html' for c in configs]
for path in paths:
 raw=(ROOT/path).read_text(encoding='utf-8');added=path.startswith('en/blog/')
 before=None if added else subprocess.check_output(['git','show',baseline+':'+path],cwd=ROOT).decode('utf-8').replace('\r\n','\n')
 files[path]=dict(kind='added' if added else 'modified',before_sha256=sha(before) if before is not None else None,
                  after_sha256=sha(raw),after_crlf_sha256=sha(raw.replace('\n','\r\n')))
parity=json.loads((D/'source_parity_snapshots_v2.json').read_text(encoding='utf-8'))
data=['data/en-translations/batch40.json']+['data/en-translations/'+c['vi_slug']+'.tsv' for c in configs]
release=dict(version=1,phase='E2',baseline=baseline,files=files,
             pairs=[dict(vi_url='https://apocalypsecloset.com/blog/'+c['vi_slug']+'.html',en_url='https://apocalypsecloset.com/en/blog/'+c['en_slug']+'.html') for c in configs],
             parity_snapshots='data/en-batch40-2026-11-17/source_parity_snapshots_v2.json',
             parity_sha256={p:sha(raw) for p,raw in parity.items()},data_sha256={p:sha((ROOT/p).read_text(encoding='utf-8')) for p in data},
             english_journal=dict(count=442,old_count=438,latest_date='2026-11-17',first_url='/en/blog/'+configs[0]['en_slug']+'.html'),
             translation_source_successors={})
dest=ROOT/'docs/link-fix-2026-11-17/batch40-release.json'
if dest.exists():assert json.loads(dest.read_text(encoding='utf-8'))==release,'Existing release records are immutable'
else:dest.write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Locked four complete EN hubs, four VI head-only successors, Journal/sitemap and five new batch data files.')
