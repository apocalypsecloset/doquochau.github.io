"""Write concise per-link phase-three records, retaining earlier phases byte-for-byte."""
import csv,io,json,subprocess
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]

def write_log():
    patches=json.loads((ROOT/'tools/phase3_patches.json').read_text(encoding='utf8'))
    baseline=subprocess.check_output(['git','show','985f5e3:tools/link_changes.csv'],cwd=ROOT)
    current=(ROOT/'tools/link_changes.csv').read_bytes()
    candidates=[baseline,baseline.replace(b'\n',b'\r\n')]
    prefix=next((p for p in candidates if current.startswith(p)),None)
    assert prefix is not None,'Previous phase log does not match baseline'
    prior_count=len(list(csv.reader(io.StringIO(prefix.decode('utf8')))))
    current_count=len(list(csv.reader(io.StringIO(current.decode('utf8')))))
    assert current_count in (prior_count,prior_count+454),'Log contains work beyond phase three'
    output=io.StringIO(newline='');writer=csv.writer(output);count=0
    for p in patches:
        soup=BeautifulSoup(p['new'],'html.parser')
        for link in p['links']:
            if p['kind']=='down':
                a=soup.find('a',href=link['target']);assert a,(p['file'],link)
                context=a.find_parent('p') or a
                before='';after=context.get_text(' ',strip=True)
            else:
                before=BeautifulSoup(p['old'],'html.parser').get_text(' ',strip=True)
                after=soup.get_text(' ',strip=True)
            writer.writerow([p['file'],link['target'],link['anchor'],before,after]);count+=1
    assert count==454,count
    (ROOT/'tools/link_changes.csv').write_bytes(prefix+output.getvalue().encode('utf8'))
    print('Phase-three log records:',count)

if __name__=='__main__':write_log()
