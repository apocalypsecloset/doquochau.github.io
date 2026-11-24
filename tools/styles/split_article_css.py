"""Split legacy article bundles into cached shared blocks, preserving cascade order.

Dry run by default. Run from the site root with --write to apply.
"""
from pathlib import Path
from collections import Counter
import argparse,difflib,hashlib,json,re
import tinycss2

ROOT=Path(__file__).resolve().parents[2]
CSS=ROOT/'assets/css/compiled'
LEGACY=re.compile(r'article-[a-f0-9]{16}\.css$')
def parse(text):
    nodes=tinycss2.parse_stylesheet(text,skip_comments=True,skip_whitespace=True)
    if any(n.type=='error' for n in nodes):raise ValueError('Invalid CSS')
    if any(n.type=='at-rule' and n.lower_at_keyword in ['import','namespace','charset'] for n in nodes):
        raise ValueError('Stylesheet-scoped directives require manual review')
    return [re.sub(r'(?m)^[ \t]+$','',tinycss2.serialize([n])) for n in nodes]
def locate(sequence,block,start=0):
    for i in range(start,len(sequence)-len(block)+1):
        if sequence[i:i+len(block)]==block:return i
    return -1
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');args=ap.parse_args()
    paths=sorted(p for p in CSS.glob('article-*.css') if LEGACY.fullmatch(p.name))
    if not paths:print('No legacy bundles remain.');return
    originals={p.name:parse(p.read_text(encoding='utf8')) for p in paths}
    reference=originals[paths[0].name];candidates={}
    for name,sequence in originals.items():
        if name==paths[0].name:continue
        for match in difflib.SequenceMatcher(None,reference,sequence,autojunk=False).get_matching_blocks():
            block=tuple(reference[match.a:match.a+match.size])
            if block:candidates[block]=sum(len(x.encode()) for x in block)
    selected=[];occupied=set()
    for block,size in sorted(candidates.items(),key=lambda x:-x[1]):
        if size<10000:break
        block=list(block);start=locate(reference,block)
        positions=set(range(start,start+len(block)))
        if occupied&positions:continue
        support=sum(locate(sequence,block)>=0 for sequence in originals.values())
        if support>=len(paths)*.9:
            selected.append(block);occupied.update(positions)
        if len(selected)==3:break
    if not selected:raise ValueError('No safe shared blocks found')
    assets={};mapping={};segments={}
    def asset(kind,rules):
        content='\n'.join(rules)+'\n';digest=hashlib.sha256(content.encode()).hexdigest()[:16]
        name=f'article-{kind}-{digest}.css';assets[name]=content;segments[name]=rules;return name
    shared=[asset('shared',block) for block in selected]
    for name,sequence in originals.items():
        matches=sorted((pos,block,shared[index]) for index,block in enumerate(selected) if (pos:=locate(sequence,block))>=0)
        parts=[];cursor=0
        for pos,block,shared_name in matches:
            if pos<cursor:raise ValueError('Overlapping shared blocks')
            if pos>cursor:parts.append(asset('detail',sequence[cursor:pos]))
            parts.append(shared_name);cursor=pos+len(block)
        if cursor<len(sequence):parts.append(asset('detail',sequence[cursor:]))
        assert [rule for part in parts for rule in segments[part]]==sequence,name
        mapping[name]=parts
    # Reparse the actual emitted bytes: top-level rule order/content must remain identical.
    emitted={name:parse(content) for name,content in assets.items()}
    for name,parts in mapping.items():assert sum((emitted[p] for p in parts),[])==originals[name],name
    changed=0;usage=Counter();html_updates={}
    for page in ROOT.rglob('*.html'):
        raw=page.read_bytes();text=raw.decode('utf8')
        def links(m):
            tag=m.group(0)
            href=re.search(r'''\bhref=(["'])(/assets/css/compiled/(article-[a-f0-9]{16}\.css)(?:\?[^"']*)?)\1''',tag)
            if not href:return tag
            if 'integrity=' in tag:raise ValueError('SRI needs a separate update')
            usage[href[3]]+=1
            return '\n'.join(tag.replace(href[2],'/assets/css/compiled/'+part) for part in mapping[href[3]])
        revised=re.sub(r'<link\b[^>]*>',links,text,flags=re.I)
        if revised!=text:changed+=1;html_updates[page]=revised.encode('utf8')
    if set(mapping)-set(usage):raise ValueError('Unreferenced bundles require separate review')
    before=sum(p.stat().st_size for p in paths);after=sum(len(v.encode()) for v in assets.values())
    report={'original_bundles':len(paths),'shared_assets':shared,'shared_bytes':sum(len(assets[n].encode()) for n in shared),'new_assets':len(assets),'html_pages':changed,'before_bytes':before,'after_bytes':after,'saved_bytes':before-after,'ordered_rules_identical':True,'mapping':mapping}
    if args.write:
        for name,content in assets.items():(CSS/name).write_text(content,encoding='utf8',newline='\n')
        for page,content in html_updates.items():page.write_bytes(content)
        for p in paths:
            assert p.parent.resolve()==CSS.resolve() and LEGACY.fullmatch(p.name)
            p.unlink()
        (Path(__file__).parent/'article-css-manifest.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in report.items() if k!='mapping'},indent=2))
if __name__=='__main__':main()
