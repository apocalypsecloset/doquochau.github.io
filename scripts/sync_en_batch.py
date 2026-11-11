"""Wire only completed pages into VI alternates, sitemap, journal and status inventory."""
from pathlib import Path
import json,csv,io,html,re,sys
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];batch=sys.argv[1] if len(sys.argv)>1 else 'batch02';cs=json.loads((ROOT/'data/en-translations'/(batch+'.json')).read_text())
START='<!-- AC-EN-'+batch.upper()+'-START -->';END='<!-- AC-EN-'+batch.upper()+'-END -->'
assert all((ROOT/'en/blog'/f"{c['en_slug']}.html").is_file() for c in cs),'Generate every complete counterpart before wiring any source URL'
for c in cs:
 p=ROOT/'blog'/f"{c['vi_slug']}.html";s=p.read_text();s=re.sub(re.escape(START)+'.*?'+re.escape(END),'',s,flags=re.S)
 en='https://apocalypsecloset.com/en/blog/'+c['en_slug']+'.html'
 assert (ROOT/'en/blog'/f"{c['en_slug']}.html").is_file()
 vi='https://apocalypsecloset.com/blog/'+c['vi_slug']+'.html'
 alternate_vi='' if re.search(r'hreflang=[\"\x27]vi[\"\x27]',s) else f'<link rel="alternate" hreflang="vi" href="{vi}">'
 s=s.replace('</head>',START+alternate_vi+f'<link rel="alternate" hreflang="en" href="{en}">'+END+'</head>',1)
 match=re.search(r'<article\b[^>]*>',s) or re.search(r'<main\b[^>]*>',s);assert match
 switch=START+f'<p class="ac-locale-link" style="margin:0 0 20px"><a href="/en/blog/{c["en_slug"]}.html" lang="en" hreflang="en" style="display:inline-block;border:1px solid #c0392b;padding:10px 15px;color:inherit;text-decoration:none;font-weight:700">READ THE ENGLISH VERSION ↗</a></p>'+END
 s=s[:match.end()]+switch+s[match.end():];p.write_text(s)
p=ROOT/'sitemap.xml';s=p.read_text()
for c in cs:
 url='https://apocalypsecloset.com/en/blog/'+c['en_slug']+'.html'
 if '<loc>'+url+'</loc>' not in s:s=s.replace('</urlset>',f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{c.get('published_date','2026-11-03')}</lastmod>\n    <changefreq>yearly</changefreq>\n    <priority>0.7</priority>\n  </url>\n</urlset>')
p.write_text(s)
p=ROOT/'en/blog.html';s=p.read_text();s=re.sub(re.escape(START)+'.*?'+re.escape(END),'',s,flags=re.S)
journal=BeautifulSoup(s,'html.parser');grid=journal.select_one('#latest .cards');assert grid is not None
offset=len(grid.select('a.card'))+1
cards='\n'.join(f'<a class="card" href="/en/blog/{c["en_slug"]}.html"><span class="eyebrow">{i+offset:02d} / {html.escape(c["role"].replace("_"," "))}</span><h3>{html.escape(c["title"])}</h3><p>{html.escape(c["description"])}</p><span class="read">READ THE GUIDE ↗</span></a>' for i,c in enumerate(cs))
fragment=BeautifulSoup(START+'\n'+cards+'\n'+END,'html.parser')
for node in list(fragment.contents):grid.append(node)
for i,card in enumerate(grid.select('a.card'),1):
 eyebrow=card.select_one('.eyebrow')
 if eyebrow:eyebrow.string=re.sub(r'^\d+\s*/',f'{i:02d} /',eyebrow.get_text())
s=str(journal).replace('Original English-language guides. The full Vietnamese fashion archive remains available separately.','Original English guides and full translations from our Vietnamese fashion archive.')
p.write_text(s.rstrip()+'\n')
p=ROOT/'data/en-216-keyword-intent-audit.csv';rows=list(csv.DictReader(p.open()));fields=list(rows[0]);mapping={c['vi_slug']:c for c in cs}
for row in rows:
 slug=row['vi_url'].rsplit('/',1)[-1][:-5]
 if row['translation_status']=='DRAFT_READY':
  row['translation_status']='MERGED';row['notes']+='; Merged in PR #10, verified on master 14189d9'
 if slug in mapping:
  c=mapping[slug];row.update(en_url='https://apocalypsecloset.com/en/blog/'+c['en_slug']+'.html',page_role=c['role'],translation_status=(row['translation_status'] if row['translation_status'] in {'COMPLETE_QA_PASSED','MERGED'} else 'TRANSLATED_QA_PENDING'),intent_review='EDITORIAL_REVIEW_NO_GSC',notes=c['primary_intent']+'; No GSC query x page data: no confirmed cannibalization diagnosis.')
out=io.StringIO(newline='');out.write(','.join(fields)+'\n');w=csv.DictWriter(out,fieldnames=fields,lineterminator='\n',quoting=csv.QUOTE_ALL);w.writerows(rows);p.write_text(out.getvalue())
from collections import Counter
print(batch, len(cs), 'pages wired;', dict(Counter(r['translation_status'] for r in rows)))
