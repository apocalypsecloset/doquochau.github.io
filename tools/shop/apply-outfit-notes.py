"""Apply individually edited outfit guidance without reformatting the page shell."""
from pathlib import Path
import json,re,html
ROOT=Path(__file__).resolve().parents[2]
notes=json.loads(Path(__file__).with_name('outfit-notes.json').read_text(encoding='utf-8'))
for slug,note in notes.items():
    path=ROOT/'outfits'/f'{slug}.html'
    source=path.read_text(encoding='utf-8')
    block='<section class="outfit-styling-notes" aria-labelledby="outfit-styling-title"><h2 id="outfit-styling-title">'+html.escape(note['heading'])+'</h2>'+''.join('<p>'+html.escape(p)+'</p>' for p in note['paragraphs'])+'</section>'
    if 'class="outfit-styling-notes"' in source:
        source,count=re.subn(r'<section class="outfit-styling-notes".*?</section>',lambda _:block,source,flags=re.S)
        assert count==1,slug
    else:
        anchor='<div class="section-title">'
        assert source.count(anchor)==1,slug
        source=source.replace(anchor,block+anchor,1)
    stylesheet='<link rel="stylesheet" href="/assets/css/outfit-notes.css?v=20261125a">'
    if stylesheet not in source:source=source.replace('</head>',stylesheet+'\n</head>',1)
    # The reading nav was a third flex column and squeezed both primary columns.
    # Keep it inside the text column when adding the editorial guidance.
    source=re.sub(r'(</div>)(<nav class="ac-reading-path".*?</nav>)(</main>)',r'\2\1\3',source,flags=re.S)
    source=re.sub(r'("dateModified":")[^"]+',r'\g<1>2026-11-25T00:00:00+07:00',source)
    source=re.sub(r'(<meta content=")[^"]+(" property="article:modified_time">)',r'\g<1>2026-11-25T00:00:00+07:00\2',source)
    path.write_text(source,encoding='utf-8')
sitemap=ROOT/'sitemap.xml';source=sitemap.read_text(encoding='utf-8')
for slug in notes:
    url='https://apocalypsecloset.com/outfits/'+slug+'.html'
    pattern=r'(<loc>'+re.escape(url)+r'</loc>(?:(?!</url>).)*?<lastmod>)[^<]+'
    source,count=re.subn(pattern,r'\g<1>2026-11-25',source,flags=re.S)
    assert count==1,slug
sitemap.write_text(source,encoding='utf-8')
print('Updated',len(notes),'outfit pages and sitemap dates')
