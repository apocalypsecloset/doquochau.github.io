"""Create collection pages from the existing footwear template; register by exact insertions."""
import collections, copy, csv, html, json, re
from pathlib import Path
from bs4 import BeautifulSoup, Comment
from internal_link_audit import cluster
from phase2_content import PAGES

ROOT=Path(__file__).resolve().parents[1]
BASE='https://apocalypsecloset.com'
DATE='2026-11-17'
escape=lambda s:html.escape(s,quote=True)
template=(ROOT/'blog/phoi-do-theo-giay-nu.html').read_bytes().decode('utf8')
baseline=list(csv.DictReader((ROOT/'tools/audit_phase2_before.csv').open(encoding='utf8')))
metadata={}
for r in baseline:
    slug=r['slug'];s=BeautifulSoup((ROOT/f'blog/{slug}.html').read_bytes(),'lxml')
    def meta(selector,default=''):
        node=s.select_one(selector)
        return node.get('content',default) if node else default
    metadata[slug]=dict(title=s.title.get_text(),description=meta('meta[name=description]'),
        image=meta('meta[property="og:image"]'),alt=meta('meta[property="og:image:alt"]',s.h1.get_text(' ',strip=True)),
        width=meta('meta[property="og:image:width"]','1080'),height=meta('meta[property="og:image:height"]','1920'))

def card(slug):
    m=metadata[slug]
    assert m['image'],slug
    return f'<a class="hub-card" href="/blog/{slug}.html"><img src="{escape(m["image"])}" alt="{escape(m["alt"])}" width="{escape(m["width"])}" height="{escape(m["height"])}" loading="lazy" decoding="async"><div class="hub-card-body"><h3>{escape(m["title"])}</h3><p>{escape(m["description"])}</p></div></a>'

registrations=[];newlog=[];report=[]
for c,p in PAGES.items():
    slug=p['slug'];url=BASE+'/blog/'+slug+'.html';dest=ROOT/f'blog/{slug}.html'
    assert not dest.exists(),dest
    kids=[r['slug'] for r in baseline if cluster(r['slug'])==c]
    grouped=[x for section in p['sections'] for x in section[3]]
    assert collections.Counter(grouped)==collections.Counter(kids),(c,set(kids)-set(grouped),set(grouped)-set(kids))
    prose_soup=BeautifulSoup(''.join(s[2] for s in p['sections']),'html.parser')
    prose_targets={a['href'] for a in prose_soup.select('a[href]')}
    count=len((p['intro']+' '+prose_soup.get_text(' ',strip=True)).split())
    assert count>=1200,(c,count)
    parts=['<main class="hub-main" id="main-content" tabindex="-1">',
        '<section class="hub-hero"><div class="hub-kicker">'+escape(p['kicker'])+'</div><h1>'+escape(p['title'])+'</h1><p>'+escape(p['intro'])+'</p></section>',
        '<nav aria-label="Mục lục hướng dẫn" class="article-toc"><details open><summary>Chọn vấn đề bạn đang cần</summary><ol>'+''.join(f'<li><a href="#{sid}">{escape(title)}</a></li>' for sid,title,_,_ in p['sections'])+'</ol></details></nav>']
    for sid,title,prose,children in p['sections']:
        parts.append(f'<section class="hub-section" aria-labelledby="{sid}"><h2 id="{sid}">{escape(title)}</h2><div class="hub-copy" data-authored-copy="phase2">{prose.strip()}</div>')
        cards=[card(x) for x in children if '/blog/'+x+'.html' not in prose_targets]
        if cards:parts.append('<div class="hub-grid">'+''.join(cards)+'</div>')
        parts.append('</section>')
    parts.append('</main>')
    body='\n'.join(parts)
    s=BeautifulSoup(template,'html.parser')
    s.main.replace_with(BeautifulSoup(body,'html.parser'))
    for node in s.select('link[hreflang], [data-publication-discovery]'):
        node.decompose()
    for comment in list(s.find_all(string=lambda t:isinstance(t,Comment))):
        if 'AC-EN-' in comment:comment.extract()
    crumb=s.select_one('.hub-breadcrumb')
    if crumb:
        crumb.replace_with(BeautifulSoup('<nav aria-label="Đường dẫn" class="hub-breadcrumb"><a href="/">Trang chủ</a> / <a href="/blog.html">Blog</a> / <span>'+escape(p['title'])+'</span></nav>','html.parser'))
    s.title.string=p['title']
    cover=metadata[p['cover']]
    replacements={'meta[name=description]':p['description'],'meta[property="og:title"]':p['title'],
        'meta[property="og:description"]':p['description'],'meta[property="og:url"]':url,
        'meta[property="og:image"]':cover['image'],'meta[property="og:image:alt"]':cover['alt'],
        'meta[property="og:image:width"]':cover['width'],'meta[property="og:image:height"]':cover['height'],
        'meta[name="twitter:title"]':p['title'],'meta[name="twitter:description"]':p['description'],
        'meta[name="twitter:image"]':cover['image']}
    for selector,value in replacements.items():s.select_one(selector)['content']=value
    s.select_one('link[rel=canonical]')['href']=url
    alt=s.new_tag('meta',attrs={'name':'twitter:image:alt','content':cover['alt']});s.head.append(alt)
    old_schema=s.select_one('script[type="application/ld+json"]')
    org_graph=json.loads(old_schema.string)['@graph'][2:]
    graph=[{'@type':'CollectionPage','name':p['title'],'description':p['description'],'url':url,'inLanguage':'vi',
        'isPartOf':{'@id':BASE+'/#website'},'datePublished':DATE,'dateModified':DATE,
        'mainEntity':{'@type':'ItemList','numberOfItems':len(kids),'itemListElement':[
            {'@type':'ListItem','position':i,'name':metadata[k]['title'],'url':BASE+'/blog/'+k+'.html'} for i,k in enumerate(grouped,1)]}},
        {'@type':'BreadcrumbList','itemListElement':[
            {'@type':'ListItem','position':1,'name':'Trang chủ','item':BASE+'/'},
            {'@type':'ListItem','position':2,'name':'Blog','item':BASE+'/blog.html'},
            {'@type':'ListItem','position':3,'name':p['title'],'item':url}]}]+copy.deepcopy(org_graph)
    old_schema.string=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,separators=(',',':'))
    dest.write_bytes((str(s).rstrip()+'\n').encode('utf8'))
    category={'Phoi-mau':'Fashion Basics','Dia-diem-dip':'Dress Code Desk','Cham-soc':'Care Guide','Toc-lam-dep':'Beauty Guide'}[c]
    search=dict(title=p['title'],url='/blog/'+slug+'.html',type=category,description=p['description'],image=cover['image'].replace(BASE,''),keywords=p['kicker'].lower()+', '+p['title'].lower())
    index_card=f'<a data-published="{DATE}" class="post-card" data-category="{category}" data-search-parts="[0,&quot; &quot;,1,&quot; &quot;,2,&quot; &quot;,3]" data-tags="#FashionGuide" href="/blog/{slug}.html"><div class="card-cover"><img src="{escape(cover["image"])}" alt="{escape(cover["alt"])}" width="{cover["width"]}" height="{cover["height"]}" loading="lazy" decoding="async"></div><div class="card-body"><div class="card-meta"><span>{category}</span><span class="dot" aria-hidden="true"></span><span>17 Nov 2026</span></div><h2 class="card-title">{escape(p["title"])}</h2><p class="card-desc">{escape(p["description"])}</p><span class="card-link">Đọc thêm →</span></div></a>'
    registrations.append(dict(url=url,search=search,card=index_card))
    page=BeautifulSoup(body,'html.parser')
    for a in page.select('a[href^="/blog/"]'):
        context=a.find_parent('p') or a
        newlog.append([f'blog/{slug}.html',a['href'],a.get_text(' ',strip=True),'',context.get_text(' ',strip=True)])
    report.append(dict(cluster=c,slug=slug,authored_words=count,children=len(kids),contextual_blog_links=len(prose_targets),card_links=len(kids)-len(set('/blog/'+k+'.html' for k in kids)&prose_targets)))

# Insert only; never serialize the existing index or sitemap.
for file,needle,addition in [
 ('blog.html','<div class="post-grid" id="post-grid">',''.join(r['card'] for r in registrations)),
 ('search-index.js','window.searchIndex = [','\n'+',\n'.join('  '+json.dumps(r['search'],ensure_ascii=False,indent=2).replace('\n','\n  ') for r in registrations)+','),
]:
    path=ROOT/file;raw=path.read_bytes().decode('utf8');assert raw.count(needle)==1
    path.write_bytes(raw.replace(needle,needle+addition,1).encode('utf8'))
path=ROOT/'sitemap.xml';raw=path.read_bytes().decode('utf8');assert raw.count('</urlset>')==1
xml=''.join('  <url>\n    <loc>'+r['url']+'</loc>\n    <lastmod>'+DATE+'</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n' for r in registrations)
if '\r\n' in raw:xml=xml.replace('\n','\r\n')
path.write_bytes(raw.replace('</urlset>',xml+'</urlset>').encode('utf8'))
with (ROOT/'tools/link_changes.csv').open('a',encoding='utf8',newline='') as f:csv.writer(f).writerows(newlog)
with (ROOT/'tools/phase2_cluster_changes.csv').open('w',encoding='utf8',newline='') as f:
    w=csv.writer(f);w.writerow(['slug','before','after'])
    for r in baseline:
        new=cluster(r['slug'])
        if new!=r['cluster']:w.writerow([r['slug'],r['cluster'],new])
(ROOT/'tools/phase2_pages.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
