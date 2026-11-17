import json,sys
from pathlib import Path
D=Path(__file__).resolve().parent;p=json.loads((D/'rename_plan.json').read_text(encoding='utf-8'))
start=int(sys.argv[1]);count=int(sys.argv[2]) if len(sys.argv)>2 else 45
for n,r in enumerate(p[start:start+count],start):print(n,'ID',r['id'],r['source'][8:-5],'->',r['target'][8:-5],'|',r['anchor'],'\n',r['context'],'\n')
