"""Render final evidence and a reproducible random sample of 20 logged edits."""
import csv
import json
import random
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
T = ROOT/'tools'
rows = list(csv.DictReader((T/'link_changes.csv').open(encoding='utf-8-sig',newline='')))
qa = json.loads((T/'qa_phase5_site.json').read_text(encoding='utf-8-sig'))
verification = json.loads((T/'phase5_verification.json').read_text(encoding='utf-8'))
assert not qa['errors'] and verification['scope_pass']
def count(name):
    return sum(int(r['unique_prose_out']) for r in csv.DictReader((T/name).open(encoding='utf-8-sig')))
text = f'''# Báo cáo cuối — Internal link và topical map blog VI

Branch: `fix/internal-links-topical-map`. Baseline: `9e16c20`.

## Kết quả

Hoàn tất Pha 1–5. Audit cuối: **ĐẠT TẤT CẢ — 11/11 gate PASS**.

- Bài VI thật: 436 → 440 (thêm 4 trang tổng quan); giữ 9 redirect stub, không trỏ link mới vào stub.
- Quan hệ nguồn → đích blog phân biệt trong nội dung: **{count('audit_before.csv'):,} → {count('audit_phase5_after.csv'):,}**. Đây là số cặp nguồn–đích, không phải số thẻ `<a>` trên toàn site.
- Cả 440 bài có 2–12 đích blog ngữ cảnh, có bài khác link vào, và có bài ngang cùng cụm ngoài bài cha.
- 421 bài con được phủ liên kết cha/con; 7 cặp áo/quần cùng màu đã có đủ hai chiều.
- 23 bài địa điểm/dịp có link hai chiều với item; 17 bài chất liệu có link hai chiều với hướng dẫn chăm sóc/thao tác tương ứng.
- Nhật ký chứa {len(rows):,} dòng trước/sau của các pha.

## Bốn trang tổng quan mới

| File | Số từ nội dung biên soạn ở Pha 2 |
|---|---:|
| `blog/phoi-mau-quan-ao-nu.html` | 1.331 |
| `blog/chon-trang-phuc-nu-theo-dia-diem-va-dip.html` | 1.371 |
| `blog/cach-cham-soc-do-nu.html` | 1.401 |
| `blog/chon-toc-va-makeup-theo-trang-phuc.html` | 1.362 |

Đã đăng ký cả bốn trang trong sitemap, blog index và search index. Số từ đếm theo khoảng trắng, không tính danh sách thẻ bài con.

## Pha 5

Goth, E-Girl và Dark Feminine đã có một link ngữ cảnh tới trang `/style/` tương ứng. Giữ ba link đó; thêm hai câu riêng cho Baddie Streetwear và Punk/Grunge, mỗi bài đúng một link loại này trong đoạn nội dung. Các link menu, breadcrumb, CTA và footer được giữ nguyên.

Hai link mới dùng anchor “outfit Baddie theo tỷ lệ” và “cách ghép outfit Punk Grunge”, đặt giữa đoạn giải thích tỷ lệ/điểm nhấn. Không thêm một link trùng chỉ để đủ số thao tác. Đây là ngoại lệ `/style/` được chỉ định rõ riêng ở Pha 5 so với quy tắc `/blog/` chung.

## Kiểm tra cuối

- `internal_link_audit.py`: exit 0; đủ 11 gate PASS; không nới điều kiện gate để đạt.
- `python -X utf8 scripts/qa_site.py`: exit 0; kiểm tra {qa['html_pages']} trang HTML, {qa['sitemap_urls']} URL sitemap, {qa['bilingual_pairs']} cặp VI/EN, {qa['english_journal_cards']} thẻ bài English Journal; đối chiếu metadata {qa['existing_page_metadata_preserved']} trang lịch sử; không lỗi.
- Đã tải riêng commit baseline QA còn thiếu bằng `git fetch --depth=1 origin <SHA>`; không đổi file site hay script QA. Chạy với UTF-8 vì encoding mặc định Windows không đọc được dữ liệu Unicode.
- Kiểm tra độc lập từ baseline nhiệm vụ: metadata, H1, canonical, schema, ảnh và heading gốc còn nguyên trong {verification['original_blog_files_protected']} file blog; bốn trang mới đối chiếu với commit Pha 2. Các thẻ bài con mới được thêm ở Pha 3 có ảnh/heading riêng, không thay ảnh/heading gốc.
- Không trùng title, H1, description hoặc canonical giữa 440 bài thật.
- TOC, reading path, FAQ và nguồn giữ nguyên. Pha 5 chỉ thay đúng hai đoạn đã duyệt; nhật ký các pha trước giữ nguyên.
- File sản phẩm chỉ thay đổi trong blog VI, `sitemap.xml`, `blog.html`, `search-index.js`. Ngoài ra có tài liệu `CODEX_TASK.md` được chép vào theo yêu cầu chuẩn bị và các công cụ/báo cáo trong `tools/`. Không sửa EN, docs, data, scripts hay cloudflare.

## Giới hạn và quyết định cần nêu rõ

- Chưa push/deploy; kết quả là trên branch cục bộ.
- Chưa kiểm tra giao diện trực quan: trình duyệt công cụ không truy cập được localhost ở lần thử Pha 2. Đã kiểm tra HTML, liên kết, metadata và cấu trúc bằng script.
- Phân cụm dựa trên ý định/nội dung đọc được, chưa có dữ liệu GSC để xác nhận truy vấn. Pha 2 sửa 15 phân loại lệch trong RULES; Pha 3 khai báo cha Outfit-core. Không thay điều kiện gate. Bài burnout giữ phân loại hiện có, chỉ nối ngữ cảnh ứng dụng tủ đồ, không sửa nội dung sức khỏe.
- Link chăm sóc chất liệu mô tả trường hợp cụ thể (nền tối, đồ len, lớp lót giày…); nhãn chăm sóc sản phẩm vẫn là căn cứ, không suy rộng một cách giặt cho mọi loại vải.
- Yêu cầu tối đa một link lõi được hiểu là link trong đoạn nội dung; các link điều hướng có sẵn được bảo toàn. Ba bài đã có link phù hợp không cần thêm lần nữa.

## 20 thay đổi mẫu ngẫu nhiên trước/sau

Chọn bằng `random.Random(20261117).sample` từ toàn bộ nhật ký, không lọc theo kết quả. Một số dòng là thay anchor/bỏ trùng nên chữ hiển thị có thể giống nhau; khối HTML giúp thấy thay đổi thẻ link. Đoạn dưới đây giữ nguyên giá trị CSV để có đủ ngữ cảnh.
'''
for n,row in enumerate(random.Random(20261117).sample(rows,20),1):
    text += f"\n### {n}. `{row['file']}`\n\nĐích: `{row['đích']}`; anchor: {row['anchor']}\n\nTrước:\n\n```html\n{row['câu_trước']}\n```\n\nSau:\n\n```html\n{row['câu_sau']}\n```\n"
(T/'final_internal_links_report.md').write_text(text,encoding='utf-8')
print('Final report written with 20 reproducible random before/after samples.')
