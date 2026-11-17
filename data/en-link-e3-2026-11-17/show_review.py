"""Print one bounded editorial batch from the frozen plan."""
import json,sys
from pathlib import Path
D=Path(__file__).resolve().parent
plan=json.loads((D/'plan.json').read_text(encoding='utf-8'))
paras=json.loads((D/'paragraphs.json').read_text(encoding='utf-8'))
start=int(sys.argv[1]);count=int(sys.argv[2]) if len(sys.argv)>2 else 20
for p in plan[start:start+count]:
 para=next(x for x in paras[p['source']] if x['index']==p['paragraph'])
 vi=p['vi_context'];anchor=p['vi_anchor'];at=vi.find(anchor) if anchor else 0
 if len(vi)>380:vi=vi[max(0,at-140):at+240]
 print(f"{p['id']} {p['source'][8:-5]} -> {p['target'][8:-5]} [p{p['paragraph']}]\nEN: {para['old']}\nVI: {vi}\n")
