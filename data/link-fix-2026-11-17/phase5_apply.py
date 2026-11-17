"""Two individually reviewed core links; exact replacements, no HTML formatting."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDITS = [
    ('baddie-streetwear', '/style/baddie-streetwear.html', 'outfit Baddie theo tỷ lệ',
     'Baby tee/crop top + cargo, fitted long-sleeve + jeans ống rộng hoặc corset + baggy đều dùng cùng logic:',
     'Đối chiếu các <a href="/style/baddie-streetwear.html">outfit Baddie theo tỷ lệ</a> để thấy phần quần rộng được cân bằng với áo gọn ra sao.'),
    ('punk-grunge', '/style/punk.html', 'cách ghép outfit Punk Grunge',
     'Một outfit Grunge không cần toàn bộ xích, fishnet và combat boots cùng lúc;',
     'Các <a href="/style/punk.html">cách ghép outfit Punk Grunge</a> cho thấy bạn có thể giữ một điểm nhấn bằng chất liệu hoặc phom đồ trước khi tăng phụ kiện.'),
]

if __name__ == '__main__':
    patches = []
    for slug, dest, anchor, marker, sentence in EDITS:
        path = ROOT / 'blog' / (slug + '.html')
        text = path.read_bytes().decode('utf-8')
        assert text.count(marker) == 1
        start = text.rfind('<p', 0, text.index(marker))
        end = text.index('</p>', text.index(marker)) + 4
        old = text[start:end]
        new = old.replace(marker, sentence + ' ' + marker)
        assert text.count(old) == 1 and sentence not in text
        assert (ROOT / dest.lstrip('/')).is_file()
        patches.append(dict(file=path.relative_to(ROOT).as_posix(), destination=dest,
                            anchor=anchor, old=old, new=new))
    (ROOT / 'tools/phase5_patches.json').write_text(json.dumps(patches, ensure_ascii=False, indent=2), encoding='utf-8')
    for p in patches:
        path = ROOT / p['file']
        path.write_bytes(path.read_bytes().replace(p['old'].encode(), p['new'].encode(), 1))
    with (ROOT / 'tools/link_changes.csv').open('a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for p in patches:
            writer.writerow([p['file'], p['destination'], p['anchor'], p['old'], p['new']])
    print('Applied 2 exact paragraph replacements; logged 2 core links.')
