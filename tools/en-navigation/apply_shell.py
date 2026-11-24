"""Apply the shared visual shell to English pages without changing navigation targets."""
from pathlib import Path
import re,json
from collections import Counter
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2]
VERSION='20261124shell1'
def fragment(text):return BeautifulSoup(text,'lxml')
def classes(node,old,new):
    node['class']=[c for c in node.get('class',[]) if c not in old]+[new]
def links(node):return Counter(a.get('href','') for a in node.find_all('a'))
def make_header(raw):
    soup=fragment(raw);old=soup.header;before=links(old)
    out=fragment('<header class="en-shell-header"><nav class="en-shell-nav" id="ac-primary-nav" aria-label="Main navigation"></nav><div class="en-shell-actions"></div></header>')
    header=out.header;brand=old.find('a');brand.extract();brand['class']=['en-shell-brand'];header.insert(0,brand)
    nav=header.nav;source=old.find('nav')
    for node in list(source.contents):nav.append(node.extract())
    for dropdown in nav.select('.ac-nav-dropdown,.en-shell-dropdown'):
        dropdown['class']=['en-shell-dropdown']
        button=dropdown.find('button');button['class']=['en-shell-dropdown-toggle'];button['aria-expanded']='false'
        menu=dropdown.select_one('.ac-dropdown-menu,.en-shell-dropdown-menu');menu['class']=['en-shell-dropdown-menu']
    actions=header.select_one('.en-shell-actions');cart=old.select_one('#ac-cart-button')
    if cart:
        cart.extract();cart['class']=['en-shell-cart'];actions.append(cart)
    toggle=fragment('<button class="en-shell-toggle" type="button" aria-label="Toggle menu" aria-expanded="false" aria-controls="ac-primary-nav"><svg aria-hidden="true" fill="none" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-linecap="round" stroke-width="2"/></svg></button>').button
    actions.append(toggle)
    assert links(header)==before,'Header links changed'
    return str(header)
def make_footer(raw):
    soup=fragment(raw);old=soup.footer;before=links(old)
    grid=old.select_one('.ac-footer-grid,.footer-grid,.en-shell-footer-grid')
    bottom=old.select_one('.ac-footer-bottom,.copyright,.en-shell-bottom')
    old['class']=['en-shell-footer'];grid['class']=['en-shell-footer-grid'];bottom['class']=['en-shell-bottom']
    groups=grid.find_all('div',recursive=False)
    about=groups[0];about['class']=['en-shell-footer-about']
    logo=about.find('a')
    if logo:
        logo['class']=['en-shell-footer-brand']
    else:
        heading=about.find(['h2','h3'])
        if heading:heading.decompose()
        logo=fragment('<a class="en-shell-footer-brand" href="/" aria-label="Apocalypse Closet home"><img src="/Logo-Apocalypse-Closet.webp" width="88" height="88" alt="" loading="lazy"><img src="/wordmark-hd.webp" width="280" height="128" alt="Apocalypse Closet" loading="lazy"></a>').a
        about.insert(0,logo);before['/']+=1
    for group in groups[1:]:
        title=group.find(['h2','h3','span']);title['class']=['en-shell-title']
        for ul in group.find_all('ul'):ul['class']=['en-shell-footer-links']
    assert links(old)==before,'Footer links changed'
    return str(old)
def main():
    count=0
    for path in ROOT.rglob('*.html'):
        raw=path.read_bytes();text=raw.decode('utf8')
        if not re.search(r'''<html\b[^>]*\blang=["']en(?:-[^"']*)?["']''',text,re.I):continue
        revised,n=re.subn(r'<header\b[^>]*>.*?</header>',lambda m:make_header(m[0]),text,count=1,flags=re.S|re.I);assert n==1,path
        revised,n=re.subn(r'<footer\b[^>]*>.*?</footer>',lambda m:make_footer(m[0]),revised,count=1,flags=re.S|re.I);assert n==1,path
        # The old English shell script only controls the replaced navigation.
        revised=re.sub(r'''\s*<script\b[^>]*src=["']/assets/js/site-shell-20260807\.js[^"']*["'][^>]*>\s*</script>''','',revised)
        revised=re.sub(r'''\s*<link\b[^>]*href=["']/assets/css/en-navigation\.css[^"']*["'][^>]*>''','',revised)
        revised=re.sub(r'''\s*<script\b[^>]*src=["']/assets/js/en-navigation\.js[^"']*["'][^>]*>\s*</script>''','',revised)
        revised=re.sub(r'\s*</head>',f'\n<link rel="stylesheet" href="/assets/css/en-navigation.css?v={VERSION}">\n</head>',revised,count=1,flags=re.I)
        revised=re.sub(r'\s*</body>',f'\n<script defer src="/assets/js/en-navigation.js?v={VERSION}"></script>\n</body>',revised,count=1,flags=re.I)
        if revised!=text:path.write_bytes(revised.encode('utf8'));count+=1
    print(json.dumps({'changed_english_pages':count,'navigation_targets_preserved':True}))
if __name__=='__main__':main()
