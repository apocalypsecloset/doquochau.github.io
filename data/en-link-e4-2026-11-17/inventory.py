"""Read-only E4 inventory: exact contextual anchors, protected sections and diagnostics."""
import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'));import internal_link_audit_en as A
protected='.seo-faq,.faq-section,#faq,.faq,.toc,#toc,.article-toc,.ac-reading-path,.ac-sources'
rows=[];pages={};variants=collections.defaultdict(set)
for path in sorted((ROOT/'en/blog').glob('*.html')):
 source=path.relative_to(ROOT).as_posix();raw=path.read_bytes().decode('utf-8');s=BeautifulSoup(raw,'html.parser')
 if s.select_one('meta[http-equiv="refresh" i]'):continue
 lines=[0]+[m.end() for m in re.finditer('\n',raw)]
 for a in s.select('a[href]'):
  target=A.resolve(a['href'],source);tx=a.get_text(' ',strip=True)
  if target and target.startswith('en/blog/') and target!=source and tx:variants[target].add(tx.lower())
 body=s.select_one('article.editorial') or s.select_one('main.en-hub') or s.article or s.main
 guards={id(n) for section in s.select(protected) for n in [section,*section.descendants]}
 pages[source]={'vi':A.hreflang(s,'vi'),'hub':bool(s.select_one('main.en-hub')),'title':s.h1.get_text(' ',strip=True)}
 for a in body.select('a[href]'):
  target=A.resolve(a['href'],source)
  if not target or target==source:continue
  classes=set();ctx=None
  for n in a.parents:
   if n is body:break
   classes.update(n.get('class',[]))
   if ctx is None and n.name in ('p','li','td','blockquote','figcaption'):ctx=n
  if classes&A.MODULES or ctx is None or a.find('img') or A.SWITCH.search(a.get_text(' ',strip=True)):continue
  start=lines[a.sourceline-1]+a.sourcepos;end=raw.index('</a',start);end=raw.index('>',end)+1
  row={'id':len(rows),'source':source,'target':target,'anchor':a.get_text(' ',strip=True),'old':raw[start:end],
       'start':start,'end':end,'context':ctx.get_text(' ',strip=True),'protected':id(a) in guards,'container_tag':ctx.name,
       'container_start':lines[ctx.sourceline-1]+ctx.sourcepos}
  rows.append(row)
counts=collections.Counter((r['target'],r['anchor'].lower()) for r in rows if r['target'] in pages and not pages[r['source']]['hub'])
dups=[]
for source,p in pages.items():
 if p['hub']:continue
 freq=collections.Counter(r['target'] for r in rows if r['source']==source and r['target'] in pages)
 dups.extend({'source':source,'target':t,'ids':[r['id'] for r in rows if r['source']==source and r['target']==t]} for t,n in freq.items() if n>1)
result={'pages':pages,'anchors':rows,'duplicates':dups,'frequencies':[{'target':t,'anchor':tx,'count':n} for (t,tx),n in counts.most_common() if n>5],
        'bad_context_ids':[r['id'] for r in rows if A.BAD.search(r['context']) and not pages[r['source']]['hub']],
        'sitewide_variants':{p:sorted(variants[p]) for p in pages}}
destination=D/(sys.argv[1] if len(sys.argv)>1 else 'inventory.json');assert not destination.exists(),'Keep each frozen inventory intact.'
destination.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Duplicates:',len(dups),'overused groups:',len(result['frequencies']),'anchor overflow:',sum(r['count']-5 for r in result['frequencies']))
print('BAD contexts:',len(result['bad_context_ids']),'protected bad:',[i for i in result['bad_context_ids'] if rows[i]['protected']])
print('Protected duplicate conflicts:',[g for g in dups if sum(rows[i]['protected'] for i in g['ids'])>1])
print('Protected overused:',[(g['target'],g['anchor'],sum(r['protected'] for r in rows if r['target']==g['target'] and r['anchor'].lower()==g['anchor'])) for g in result['frequencies'] if sum(r['protected'] for r in rows if r['target']==g['target'] and r['anchor'].lower()==g['anchor'])>5])
