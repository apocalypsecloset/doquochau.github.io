from pathlib import Path
from bs4 import BeautifulSoup
import re,json,html
p=Path('blog.html');raw=p.read_text()
if 'Lossless search-index reconstruction' in raw:print('Already compacted');raise SystemExit(0)
s=BeautifulSoup(raw,'html.parser');records=[]
def encode(m):
 a=BeautifulSoup(m[0],'html.parser').a
 if not a or 'post-card' not in a.get('class',[]):return m[0]
 old=a.get('data-search')
 if old is None:return m[0]
 # Read the original complete card to derive visible text exactly.
 full=next(x for x in s.select('#post-grid a.post-card') if x.get('href')==a.get('href'))
 values=[full.select_one('.card-title').get_text().lower(),full.select_one('.card-desc').get_text().lower(),a.get('data-category','').lower(),a.get('data-tags','').lower()]
 parts=[];i=0;literal=''
 while i<len(old):
  candidates=[(len(v),j) for j,v in enumerate(values) if v and old.startswith(v,i)]
  if candidates:
   if literal:parts.append(literal);literal=''
   n,j=max(candidates);parts.append(j);i+=n
  else:literal+=old[i];i+=1
 if literal:parts.append(literal)
 assert ''.join(values[v] if isinstance(v,int) else v for v in parts)==old
 encoded=json.dumps(parts,ensure_ascii=False,separators=(',',':'))
 if len(html.escape(encoded,quote=True))+20>=len(html.escape(old,quote=True)):return m[0]
 records.append({'href':a['href'],'search':old,'parts':parts})
 return re.sub(r'data-search="[^"]*"','data-search-parts="'+html.escape(encoded,quote=True)+'"',m[0])
raw=re.sub(r'<a\b[^>]*>',encode,raw)
loader="""// Lossless search-index reconstruction from the already visible card text.
    document.querySelectorAll('#post-grid a[data-search-parts]').forEach(card => {
      const values = [card.querySelector('.card-title').textContent, card.querySelector('.card-desc').textContent, card.dataset.category || '', card.dataset.tags || ''].map(s => s.toLocaleLowerCase('vi'));
      card.dataset.search = JSON.parse(card.dataset.searchParts).map(part => typeof part === 'number' ? values[part] : part).join('');
      delete card.dataset.searchParts;
    });
    """
raw=raw.replace('    const BATCH = 12;', '    '+loader+'const BATCH = 12;',1)
# Remove only inter-tag indentation in cards, retaining text nodes and all card data.
a=raw.index('<div class="post-grid" id="post-grid">');b=raw.index('<div id="load-more-wrap"',a)
raw=raw[:a]+re.sub(r'>\s+<','><',raw[a:b])+raw[b:]
p.write_text(raw);Path('docs/schema-pod-performance-2026-11-15/journal-search.json').write_text(json.dumps({'cards_encoded':len(records),'all_original_search_strings_preserved':True,'records':records},ensure_ascii=False,indent=2)+'\n');print('encoded',len(records),'bytes',len(raw.encode()))
