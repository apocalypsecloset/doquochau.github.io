"""Order journal cards by their recorded publication date, newest first.

Paired articles use the date already displayed in the Vietnamese journal.
English-only articles use BlogPosting.datePublished. Undated collection hubs
stay at the end in their existing order; no publication dates are invented.
"""
import argparse,json,re
from datetime import datetime,date
from pathlib import Path
from urllib.parse import urljoin,urlsplit
from bs4 import BeautifulSoup
from translation_inventory import rows,publication_rows
ROOT=Path(__file__).resolve().parents[1]
BASE='https://apocalypsecloset.com'

def grid(raw,lang):
    pattern=r'<div\b[^>]*\bid="post-grid"[^>]*>' if lang=='vi' else r'<div\b[^>]*\bclass="cards"[^>]*>'
    start=re.search(pattern,raw);assert start,'Journal grid missing'
    depth=1
    for m in re.finditer(r'</?div\b[^>]*>',raw[start.end():]):
        depth+=-1 if m.group().startswith('</') else 1
        if depth==0:return start.end(),start.end()+m.start()
    raise AssertionError('Unclosed journal grid')

def cards(raw,lang):
    a,b=grid(raw,lang)
    return re.findall(r'<a\b[\s\S]*?</a>',raw[a:b])

def href(card,lang):
    return urljoin(BASE+('/blog.html' if lang=='vi' else '/en/blog.html'),BeautifulSoup(card,'html.parser').a['href'])

def publication_dates():
    vi_raw=(ROOT/'blog.html').read_text();dates={}
    for c in cards(vi_raw,'vi'):
        node=BeautifulSoup(c,'html.parser');text=node.select_one('.card-meta').select('span')[-1].get_text(strip=True)
        dates[href(c,'vi')]=datetime.strptime(text,'%d %b %Y').date().isoformat()
    for row in rows()+publication_rows():
        if row['vi_url'] in dates:dates[row['en_url']]=dates[row['vi_url']]
    for c in cards((ROOT/'en/blog.html').read_text(),'en'):
        url=href(c,'en')
        if url in dates:continue
        soup=BeautifulSoup((ROOT/urlsplit(url).path.lstrip('/')).read_text(),'html.parser')
        for tag in soup.select('script[type="application/ld+json"]'):
            obj=json.loads(tag.string);nodes=obj.get('@graph',[obj])
            for node in nodes:
                if node.get('@type')=='BlogPosting' and node.get('datePublished'):
                    dates[url]=date.fromisoformat(node['datePublished'][:10]).isoformat()
    return dates

def errors():
    dates=publication_dates();result=[]
    for lang,path in [('vi','blog.html'),('en','en/blog.html')]:
        cs=cards((ROOT/path).read_text(),lang);actual=[]
        for c in cs:
            url=href(c,lang);recorded=BeautifulSoup(c,'html.parser').a.get('data-published')
            expected=dates.get(url,'')
            if recorded!=expected:result.append(path+': incorrect/missing listing date '+url)
            actual.append(expected)
        if actual!=sorted(actual,reverse=True):result.append(path+': articles must be newest first')
    return result

def write():
    dates=publication_dates()
    for lang,path in [('vi','blog.html'),('en','en/blog.html')]:
        p=ROOT/path;raw=p.read_text();a,b=grid(raw,lang);cs=cards(raw,lang)
        ordered=sorted(cs,key=lambda c:dates.get(href(c,lang),''),reverse=True)
        out=[]
        for i,c in enumerate(ordered,1):
            d=dates.get(href(c,lang),'')
            c=re.sub(r'\sdata-published="[^"]*"','',c,count=1)
            c=c.replace('<a ',f'<a data-published="{d}" ',1)
            if lang=='en':c=re.sub(r'(<span class="eyebrow">)\d+(\s*/)',lambda m:m[1]+f'{i:02d}'+m[2],c,count=1)
            out.append(c)
        p.write_text(raw[:a]+'\n'+'\n'.join(out)+'\n'+raw[b:])

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    if args.write:write()
    failures=errors();print(json.dumps({'errors':failures},indent=2));raise SystemExit(bool(failures))
