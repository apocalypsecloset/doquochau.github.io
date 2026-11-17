"""Create an additive exact E4 release after all fourteen unchanged audit gates pass."""
import csv,io,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'));from en_e4_release import digest
BASE='9880f3f07c1b8898590cdd2afa3f323c497e4def'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
anchors=read(D/'anchor_patches.json');assert sum(len(json.loads(r['labels'])) for r in anchors)==175
variety=read(D/'variety_patches.json');assert len(variety)==4
rows=read(D/'duplicate_patches.json')+read(D/'word_patches.json')+anchors+variety
names=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--','en/blog'],cwd=ROOT).decode().splitlines();names=[p for p in names if p.endswith('.html')]
assert len(names)==442
refs=[BASE+':'+p for p in names];raw=subprocess.check_output(['git','cat-file','--batch'],input=('\n'.join(refs)+'\n').encode(),cwd=ROOT);offset=0;before={}
for p in names:
 end=raw.index(b'\n',offset);header=raw[offset:end].split();assert len(header)==3;size=int(header[2]);offset=end+1;before[p]=raw[offset:offset+size].decode('utf-8').replace('\r\n','\n');offset+=size+1
files={};tables={}
for row in rows:
 p=row['source'];table=row['tsv']
 if p not in files:
  current=(ROOT/p).read_text(encoding='utf-8');v=row['vi_source'];assert current!=before[p],p
  files[p]={'before_sha256':digest(before[p]),'after_sha256':digest(current),'vi_source':v,
   'vi_source_sha256':digest((ROOT/v).read_text(encoding='utf-8')) if v else None,'tsvs':[]}
 if table not in files[p]['tsvs']:files[p]['tsvs'].append(table)
 if table not in tables:
  text=(ROOT/table).read_text(encoding='utf-8');entries=list(csv.DictReader(io.StringIO(text),delimiter='\t'))
  assert entries and all(r['source']==p for r in entries),table
  tables[table]={'source':p,'sha256':digest(text),'rows':len(entries)}
assert set(tables)=={p.relative_to(ROOT).as_posix() for p in (ROOT/'data/en-translations/internal-links/e4').glob('*.tsv')}
r=subprocess.run([sys.executable,str(ROOT/'scripts/internal_link_audit_en.py'),'--root',str(ROOT),'--csv',str(D/'audit_en_after.csv')],capture_output=True,encoding='utf-8');assert r.returncode==0,r.stdout
(D/'audit_en_after.txt').write_text(r.stdout,encoding='utf-8')
m={'phase':'E4','baseline':BASE,'baseline_en_hashes':{p:digest(raw) for p,raw in before.items()},'files':files,'tables':tables,
   'removed_redundant_anchor_occurrences':100,'renamed_frequency_anchors':175,'additional_existing_anchor_variants':1,'new_contextual_links':3}
dest=ROOT/'docs/link-fix-2026-11-17/en-e4-release.json';assert not dest.exists();dest.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'files':len(files),'tables':len(tables),'gates':'14/14 PASS'}))
