"""Capture exact prose spans for reviewed, surgical phase-one edits."""
import collections, json, re
from pathlib import Path
from bs4 import BeautifulSoup
from internal_link_audit import MODULE_CLASSES, resolve, BAD_PHRASES, GENERIC

ROOT = Path(__file__).resolve().parents[1]

def inventory():
    result = []
    for path in sorted((ROOT / 'blog').glob('*.html')):
        raw = path.read_bytes().decode('utf-8')
        if re.search(r'http-equiv="refresh"', raw, re.I):
            continue
        soup = BeautifulSoup(raw, 'html.parser')
        art = soup.select_one('article.article-content') or soup.find('main')
        if art is None:
            continue
        lines = raw.splitlines(keepends=True)
        offsets = [0]
        for line in lines:
            offsets.append(offsets[-1] + len(line))
        for a in art.find_all('a', href=True):
            page = path.relative_to(ROOT).as_posix()
            target = resolve(a['href'], page)
            if not target or target == page:
                continue
            classes, context = set(), None
            for par in a.parents:
                if par is art:
                    break
                classes.update(par.get('class', []))
                if context is None and par.name in ('p','li','td','blockquote','figcaption'):
                    context = par
            if classes & (MODULE_CLASSES | {'seo-faq'}) or context is None or a.find('img'):
                continue
            start = offsets[a.sourceline - 1] + a.sourcepos
            end = raw.index('</a>', start) + 4
            cs = offsets[context.sourceline - 1] + context.sourcepos
            ce = raw.index('</' + context.name + '>', cs) + len(context.name) + 3
            result.append(dict(file=page,target=target,anchor=a.get_text(' ',strip=True),
                start=start,end=end,old=raw[start:end],cs=cs,ce=ce,context=raw[cs:ce]))
    for i, row in enumerate(result):
        row['id'] = i
    return result

if __name__ == '__main__':
    data = inventory()
    counts = collections.Counter((r['target'],r['anchor'].lower()) for r in data if r['target'].startswith('blog/'))
    duplicates = collections.Counter((r['file'],r['target']) for r in data if r['target'].startswith('blog/'))
    out = collections.Counter(r['file'] for r in { (r['file'],r['target']):r for r in data if r['target'].startswith('blog/') }.values())
    for r in data:
        r['flags'] = [x for x, flag in [('phrase', bool(BAD_PHRASES.search(BeautifulSoup(r['context'],'html.parser').get_text(' ',strip=True))) or bool(re.search('item guide',r['context'],re.I))),('generic',bool(GENERIC.match(r['anchor']))),('repeat',counts[r['target'],r['anchor'].lower()]>5),('duplicate',duplicates[r['file'],r['target']]>1),('dense',out[r['file']]>12)] if flag]
    (ROOT/'tools/phase1_inventory.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    for r in data:
        if r['flags']:
            print(f"{r['id']} {r['file'][5:-5]} -> {r['target'][5:-5]} [{','.join(r['flags'])}] {r['anchor']}\n{r['context']}")
