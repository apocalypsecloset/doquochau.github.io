"""Pin completed HTML/TSV pairs; never edit old manifest records."""
import csv,hashlib,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from en_link_fix_release import digest
from privacy_release import original
BASE='a0272175089f56498bfecc40961a21baeb46fcf2';VBASE='9e16c2012f417cf5e4634b1c771a2c5d773e1ee8'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
context=read(D/'context_batches.json');nav=read(D/'navigation_patches.json');sync=read(D/'existing_link_sync_patches.json')
assert len(sync)==27
ids=[i for b in context for f in b['files'] for i in f['link_ids']]
assert sorted(ids)==list(range(644))
inventory={r['en']:r for r in read(D/'inventory.json')}
files={};tables={}
def register(source,table):
 if source not in files:
  before=subprocess.check_output(['git','show',BASE+':'+source],cwd=ROOT).decode('utf-8').replace('\r\n','\n')
  raw=(ROOT/source).read_text(encoding='utf-8');v=inventory[source]['vi'] or ''
  assert before!=raw,source
  files[source]={'before_sha256':digest(before),'after_sha256':digest(raw),'vi_source':v,
   'vi_source_sha256':digest((ROOT/v).read_text(encoding='utf-8')) if v else None,'tsvs':[]}
 if table not in files[source]['tsvs']:files[source]['tsvs'].append(table)
 if table not in tables:
  raw=(ROOT/table).read_text(encoding='utf-8');rows=list(csv.DictReader(raw.splitlines(keepends=True),delimiter='\t'))
  assert rows and all(r['source']==source for r in rows),table
  tables[table]={'sha256':digest(raw),'source':source,'rows':len(rows)}
for batch in context:
 assert len(batch['files'])<=25
 for f in batch['files']:register(f['source'],f['tsv'])
for row in nav+sync:register(row['source'],row['tsv'])
assert set(tables)=={p.relative_to(ROOT).as_posix() for p in (ROOT/'data/en-translations/internal-links').glob('*.tsv')}
sources={};locks={}
for p in sorted((ROOT/'data/en-translations').glob('batch*.json')):
 if p.stem in ('batch05b','batch40'):continue
 for c in read(p):
  vp='blog/'+c['vi_slug']+'.html';ep='en/blog/'+c['en_slug']+'.html'
  locks[vp]=c['source_sha256']
  raw=original(vp,(ROOT/vp).read_text(encoding='utf-8'));raw=re.sub(r'<!-- AC-EN-BATCH[0-9]{2}-START -->.*?<!-- AC-EN-BATCH[0-9]{2}-END -->','',raw,flags=re.S)
  if digest(raw)==c['source_sha256']:continue
  assert ep in files and files[ep]['tsvs'],(vp,ep)
  before=subprocess.check_output(['git','show',VBASE+':'+vp],cwd=ROOT).decode('utf-8').replace('\r\n','\n')
  legacy=original(vp,before);legacy=re.sub(r'<!-- AC-EN-BATCH[0-9]{2}-START -->.*?<!-- AC-EN-BATCH[0-9]{2}-END -->','',legacy,flags=re.S)
  assert digest(legacy)==c['source_sha256'],vp
  sources[vp]={'before_sha256':digest(before),'after_sha256':digest((ROOT/vp).read_text(encoding='utf-8')),'locked_source_sha256':c['source_sha256'],'en':ep}
assert len(locks)==215 and len(sources)==210
result={'phase':'E3','baseline':BASE,'source_baseline':VBASE,'authored_contextual_links':644,'navigation_cards':203,
        'existing_link_sentence_updates':27,'files':files,'tables':tables,'sources':sources,'historical_source_locks':locks}
dest=ROOT/'docs/link-fix-2026-11-17/en-e3-release.json';assert not dest.exists()
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'files':len(files),'tables':len(tables),'sources':len(sources)}))
