# NHIỆM VỤ: Sửa toàn bộ internal link + topical map blog VI (làm một lần, có kiểm tra)

Repo: apocalypsecloset.com (HTML tĩnh, GitHub Pages/Cloudflare Pages). Chỉ sửa **blog tiếng Việt** (`/blog/*.html`) và 4 hub mới. KHÔNG sửa `/en/`, `/docs`, `/data`, `/scripts`, `/cloudflare`.

## 0. Chuẩn bị
1. Tạo branch `fix/internal-links-topical-map`. Commit sau MỖI pha (pha 1, 2, 3, 4, 5).
2. Chép `scripts/internal_link_audit.py` vào repo và chạy `python scripts/internal_link_audit.py --root . --csv data/link-fix-2026-11-17/audit_before.csv`. Lưu kết quả làm baseline. Script này là **thước đo duy nhất**. Chỉ được báo "xong" khi nó in `ĐẠT TẤT CẢ` (exit code 0).
3. Đọc `docs/en-translation-seo-guardrails.md` và `scripts/qa_site.py` (nếu chạy được thì chạy lại ở cuối).

## 1. Thước đo (đã đo trước khi sửa, 436 bài VI)
- 211 bài không có bài blog nào link vào trong thân bài (G3). 10 bài có <2 link ra (G2).
- Cụm Phối màu (47 bài) và Vải (20 bài) gần như không link ngang; 7 cặp áo↔quần cùng màu chưa link nhau (G5, G6).
- Chưa có hub cho: Phối màu, Địa điểm/dịp, Chăm sóc đồ, Tóc & làm đẹp (G4). Hub Áo thiếu ~31 bài con, hub Giày/Váy/Quần/Phụ kiện/Kính cũng thiếu.
- 79 câu chứa link dùng chữ "hub", "trang trụ cột", "bổ trợ cho" (G7). 63 cặp bài–đích bị link trùng trong cùng bài (G9). Nhiều anchor lặp y hệt >5 lần (G10). 2 anchor generic ở `badgirl.html` (G8). 1 bài >12 link (G11).

## 2. Các pha (làm tuần tự)

**Pha 1 – Dọn lỗi sẵn có (G7, G8, G9, G10, G11):**
- G7: viết lại câu chứa "hub / trang trụ cột / bổ trợ cho / cụm chủ đề" thành câu tự nhiên cho người đọc (vd: "Nếu chưa chắc chọn áo theo phom nào, bài hướng dẫn chọn áo nữ theo phom sẽ giúp bạn khoanh vùng nhanh hơn").
- G9: một đích chỉ link 1 lần/bài. Giữ link ở vị trí hợp ngữ cảnh nhất, các lần còn lại bỏ thẻ `<a>` nhưng giữ nguyên chữ.
- G10: với anchor đang lặp >5 lần, đổi các lần dư sang biến thể khác (2–6 từ, đúng nghĩa trang đích).
- G8: đổi "Xem thêm về … →" thành anchor mô tả. G11: bớt link thừa ở bài >12 link.

**Pha 2 – Tạo 4 hub mới** (copy cấu trúc/template từ một hub hiện có như `blog/phoi-do-theo-giay-nu.html`):
`Phoi-mau`, `Dia-diem-dip`, `Cham-soc`, `Toc-lam-dep`.
- Mỗi hub: ≥1.200 từ nội dung thật (hướng dẫn cách chọn/nhóm, không phải danh sách trần), trỏ xuống 100% bài con của cụm (tên cụm và danh sách bài con xem cột `cluster` trong `data/link-fix-2026-11-17/audit_before.csv`), title/H1/meta description/canonical duy nhất, BreadcrumbList, JSON-LD như các bài khác.
- Thêm hub mới vào `sitemap.xml`, `blog.html` và `search-index.js` theo đúng cách các bài hiện có đang làm.
- Điền slug hub mới vào dict `HUBS` trong `scripts/internal_link_audit.py`.
- Slug mới đặt theo ý định tìm kiếm, ví dụ `phoi-mau-quan-ao-nu`, `cach-cham-soc-do-nu`. Không trùng ý định bài đang có.

**Pha 3 – Hub trỏ đủ xuống, con trỏ lên (G4):**
- Với mọi cụm: hub trỏ xuống 100% bài con trong phần nội dung (viết thành đoạn/nhóm có chữ dẫn, không dump danh sách), mỗi bài con có ít nhất 1 link lên hub trong thân bài.
- Cụm Aesthetic/Style: từ điển + 6 hub con (goth, punk-grunge, egirl, dark-feminine, badgirl, baddie-streetwear) cùng phải phủ hết bài con.

**Pha 4 – Link ngang + bài chưa được link vào (G2, G3, G5, G6):**
- Mỗi bài ≥2 link ngữ cảnh tới bài khác và ≥1 link ngang cùng cụm; mỗi bài ≥1 link ngữ cảnh đến từ bài khác.
- Cặp áo X ↔ quần X cùng màu: link hai chiều. Bài "màu X phối với màu gì" ↔ bài áo/quần cùng màu.
- Bài vải ↔ bài chăm sóc tương ứng; bài kính ↔ hub kính; bài địa điểm ↔ hub địa điểm và bài item liên quan.
- Chọn đích **cùng ý định** (người đọc đang đọc A thì B thật sự là bước tiếp theo hợp lý). Không chọn bừa hub chung cho đủ số.
- Mỗi bài cần thêm link: tối đa +3 link mới (bài đang thiếu nặng được tối đa +4). Tổng link tới bài khác ≤12/bài.

**Pha 5 – Kết nối lõi (không có gate, làm sau cùng):**
- Từ các bài lõi (goth, e-girl, baddie, dark feminine, punk-grunge) thêm 1 link ngữ cảnh tới `/style/<tương ứng>.html` hoặc `/phoi-do-nu-ca-tinh.html` nếu tự nhiên. Tối đa 1 link loại này/bài.

## 3. Quy tắc viết link (bắt buộc)
- **Mỗi câu liên kết phải do bạn viết riêng cho đoạn đó.** Cấm dùng template/f-string chung, cấm một mẫu câu dùng lại >3 lần. Đọc đoạn văn trước khi chèn.
- Link nằm giữa đoạn, ở chỗ người đọc cần; không dồn vào cuối bài; không tạo đoạn "Xem thêm:" mới.
- Anchor 2–6 từ, mô tả trang đích. Cùng 1 đích dùng ≥3 anchor khác nhau trên toàn site, mỗi anchor ≤5 lần. Cấm "xem thêm, tại đây, click".
- Không dùng chữ "hub", "trang trụ cột", "bổ trợ", "cụm chủ đề", "Item Guide" làm câu dẫn.
- Chỉ chèn link tới `/blog/*.html` thật (không phải stub redirect `alt-fashion-la-gi-va-tai-sao-no-quan-*` ngoại trừ bản chuẩn `-quan-trong`). Dùng đường dẫn dạng `/blog/<slug>.html` (root-relative).
- Chỉ sửa đoạn chứa link. Giữ nguyên title, H1, meta, canonical, schema, ảnh, TOC, heading, `ac-reading-path`, `seo-faq`, `ac-sources`. Không đụng JSON-LD.

## 4. Cách sửa an toàn
- Sửa bằng script Python áp danh sách `(file, old_str, new_str)` với `old_str` khớp chính xác và duy nhất; không viết lại cả file, không format lại HTML.
- Làm theo lô ~25 file; sau mỗi lô chạy audit script. Không để lô nào làm tăng số FAIL của gate trước đó.
- Lưu toàn bộ thay đổi vào `data/link-fix-2026-11-17/link_changes.csv` với cột: `file, đích, anchor, câu_trước, câu_sau`.

## 5. Điều kiện hoàn thành
1. `python scripts/internal_link_audit.py --root .` in **ĐẠT TẤT CẢ**.
2. Không file nào ngoài `/blog/*.html` (+ 4 hub mới, `sitemap.xml`, `blog.html`, `search-index.js`, `data/link-fix-2026-11-17/`) bị thay đổi: kiểm bằng `git diff --stat`.
3. Mọi trang giữ nguyên title/H1/canonical/meta description (so với trước). Không có title/H1/description trùng với trang khác.
4. Chạy lại `scripts/qa_site.py` nếu được.
5. Báo cáo cuối: số link trước/sau, danh sách hub mới, 20 câu link mẫu ngẫu nhiên (trước/sau), và mọi chỗ bạn **không làm được hoặc phải đoán**.

Nếu gặp tình huống không có chỉ dẫn, hãy chọn phương án ít rủi ro hơn và ghi lại trong báo cáo thay vì tự ý mở rộng phạm vi.
