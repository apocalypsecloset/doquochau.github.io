# NHIỆM VỤ EN: đồng bộ cấu trúc link nội bộ sang bản tiếng Anh

Repo: apocalypsecloset.com. Bản VI (`/blog/*.html`) đã được sửa xong và đạt `scripts/internal_link_audit.py` (E1 đã chuyển audit và dữ liệu làm việc vào vị trí hiện tại). Giờ làm bản EN (`/en/blog/*.html`: 425 bài + 13 hub `main.en-hub`) cho **cùng cấu trúc topical map**, bằng tiếng Anh tự nhiên.

KHÔNG sửa: `/blog/*.html` (VI), ảnh, title/H1/meta/canonical của trang đã có, `docs/qa/*`. Ngoại lệ duy nhất ở VI: thêm `<link rel="alternate" hreflang="en">` cho 4 hub VI mới theo đúng quy trình `scripts/sync_en_batch.py`.

## Bối cảnh bắt buộc đọc trước
- `docs/en-translation-seo-guardrails.md` (1 intent = 1 URL đích; không tạo stub, không 301, không canonical EN→VI).
- `docs/en-internal-link-refresh.md` + `scripts/refresh_en_internal_links.py` (cách đã dùng để sửa link EN: chỉ sửa đúng thẻ `<a>` và JSON-LD cần đổi, giữ nguyên byte còn lại, idempotent).
- `docs/en-translation-batch24.md` + `scripts/en_translate_hubs.py` + `scripts/qa_en_hubs.py` (quy trình tạo hub EN).
- `scripts/qa_en_translations.py`: nó khóa `source_sha256` của file VI gốc trong `data/en-translations/batch*.json`. 426 bài VI vừa bị sửa nên các khóa này có thể đã lệch.

## Pha E0 — CHỈ ĐỌC VÀ BÁO CÁO, chưa sửa file nào, rồi DỪNG chờ tôi duyệt
1. Chạy và lưu kết quả:
   `python scripts/internal_link_audit.py --root .` (VI, phải ĐẠT)
   `python scripts/internal_link_audit_en.py --root . --csv data/audit_en_before.csv` (EN baseline)
   Toàn bộ QA của CI: `qa_privacy_policies`, `qa_schema_pod_performance`, `qa_blog_repair`, `qa_storefront_ux`, `qa_site`, `qa_audit_followup`, `qa_r2_image_seo`, và vòng lặp `qa_en_translations.py <batch>` cho mọi `data/en-translations/batch*.json` (trừ batch05b) cùng `qa_en_hubs.py`.
2. Báo cáo: gate nào đỏ, vì sao (hash khóa nào lệch, bao nhiêu file), và đề xuất cách re-baseline theo quy trình đã có trong `docs/` (ví dụ cập nhật `source_sha256` cho đúng các file VI đã sửa có chủ đích). KHÔNG tự sửa manifest hay script QA ở pha này.
3. Liệt kê 4 hub VI mới (slug) và các cụm, rồi đề xuất slug EN + intent riêng cho từng hub.
Dừng ở đây. Tôi sẽ trả lời "duyệt re-baseline" hoặc hướng khác.

## Pha E1 — Dọn thư mục (commit riêng, sau khi duyệt)
- Chuyển `scripts/internal_link_audit.py` và `scripts/internal_link_audit_en.py` vào `scripts/` (nếu chưa), `CODEX_TASK*.md` vào `docs/`, mọi file làm việc còn lại trong `tools/` (inventory, patches, plan, batches, baseline, CSV) vào `data/link-fix-2026-11-17/`. Xóa thư mục `tools/` rỗng. Sửa đường dẫn trong tài liệu và docstring. Lý do: `tools/` và gốc repo đang được phục vụ công khai, còn `docs/`, `data/`, `scripts/` đã gắn noindex và loại khỏi GitHub Pages.
- KHÔNG thêm `/tools/*` vào `_headers` (qa_site.py chỉ cho phép noindex trên 4 đường dẫn cố định).

## Pha E2 — 4 hub EN mới (batch40)
Hub VI mới: Phối màu, Địa điểm/dịp, Chăm sóc đồ, Tóc & làm đẹp. Làm đúng quy trình batch24: template `main.en-hub`, hub-card cho 100% bài con **đã có bản EN**, CollectionPage + ItemList + BreadcrumbList khớp card nhìn thấy, self-canonical, hreflang hai chiều với hub VI, title/H1/meta tiếng Anh duy nhất, đăng ký `sitemap.xml`, `en/blog.html`, `search-index.js` nếu quy trình hiện tại yêu cầu. Tạo `data/en-translations/batch40.json` theo đúng định dạng batch hub. Nội dung là bản chuyển thể thật (≥1.000 từ), không phải dịch máy rồi dán, không bịa dữ kiện. Điền 4 hub vào `VI_HUBS` trong `scripts/internal_link_audit_en.py`. Chạy `qa_en_hubs.py` và `qa_en_translations.py batch40` đến khi pass.

## Pha E3 — Phản chiếu link VI sang EN
Nguồn sự thật: file `link_changes.csv` của lần sửa VI (xem `data/link-fix-2026-11-17/`) và trạng thái hiện tại của các bài VI.
- Với mỗi bài EN có bản VI, mọi link ngữ cảnh trong bài VI tới một bài VI **đã có bản EN** phải có link tương ứng trong bài EN trỏ `/en/blog/<en-slug>.html` kèm `hreflang="en"`. Ghép VI→EN bằng hreflang hoặc `scripts/translation_inventory.py`.
- Câu chứa link: viết lại bằng tiếng Anh tự nhiên theo ý của câu VI, KHÔNG dịch từng chữ, KHÔNG dùng khuôn chung. Mỗi câu viết riêng theo đoạn văn xung quanh.
- Nếu đích VI chưa có bản EN: bỏ qua link đó (không link sang VI trong thân bài EN, không bịa trang).
- Hub EN trỏ xuống 100% bài con đã có bản EN (hub-card), mỗi bài con EN có ≥1 link lên hub trong thân bài. Link ngang cùng cụm theo đúng cặp đã làm ở VI (vd áo X ↔ quần X cùng màu).
- Cách sửa: theo kiểu `refresh_en_internal_links.py` (sửa đúng thẻ/đoạn cần đổi, giữ nguyên byte còn lại, idempotent). Nếu đoạn văn thay đổi thì cập nhật TSV tương ứng trong `data/en-translations/` để HTML, TSV và JSON-LD FAQ/ItemList luôn đồng bộ.
- Lô ~25 bài, chạy `scripts/internal_link_audit_en.py` sau mỗi lô, không để số FAIL tăng.

## Pha E4 — Dọn lỗi riêng của EN (theo gate)
- E7: không còn link ngữ cảnh EN trỏ `/blog/…` khi đã có bản EN (vd `corporate-goth-office-outfits`, `soft-goth-style-outfits`). Giữ nguyên nút "Read the Vietnamese original".
- E8: anchor EN không chứa tiếng Việt (vd "Soft Goth Là Gì? Cách Phối Goth Mềm Hơn").
- E9: bỏ chữ "hub, pillar page, cornerstone, topic cluster" khỏi câu chứa link.
- E10/E11/E12/E13: không anchor generic; mỗi đích 1 link/bài; một anchor ≤5 lần/đích (hiện có "online sizing guide" ×26, "aesthetic dictionary" ×19, "layering…" ×14–16); mỗi bài ≤12 link tới bài EN khác.
- Mỗi đích dùng ≥3 anchor khác nhau trên toàn site EN.

## Quy tắc viết (EN)
- Tiếng Anh tự nhiên như người bản ngữ viết blog thời trang; link nằm giữa đoạn; anchor 2–6 từ mô tả đích; không "click here/read more/learn more".
- Không thêm quá 4 link mới/bài. Tổng link ngữ cảnh tới bài EN khác ≤12/bài.
- Giữ nguyên title, H1, meta, canonical, hreflang (trừ 4 hub mới), ảnh, heading, TOC, FAQ, schema (trừ phần JSON-LD bắt buộc đồng bộ với link nhìn thấy).

## Điều kiện hoàn thành
1. `python scripts/internal_link_audit_en.py --root .` in **ĐẠT TẤT CẢ** và `python scripts/internal_link_audit.py --root .` vẫn **ĐẠT TẤT CẢ**.
2. Mọi script QA trong CI pass, hoặc mỗi chỗ đỏ còn lại có lý do và đã được tôi duyệt ở Pha E0.
3. `git diff --stat` chỉ gồm: `en/blog/*.html`, 4 hub EN mới, 4 hub VI mới (chỉ thêm hreflang en), `data/en-translations/*`, `sitemap.xml`, `en/blog.html`, `search-index.js`, file QA manifest đã được duyệt, và thư mục `scripts/`, `docs/`, `data/` do dọn dẹp.
4. Báo cáo cuối: số link EN trước/sau, hub mới, 20 cặp câu mẫu (VI → EN), và mọi chỗ không làm được hoặc phải đoán.

Gặp tình huống không có chỉ dẫn: chọn phương án ít rủi ro nhất, ghi vào báo cáo, không tự mở rộng phạm vi.

## Quyết định đã duyệt sau E0

E1 rồi E2; chưa làm E3 khi chưa được duyệt. Batch40 dùng các slug `womens-color-coordination-guides`, `occasion-destination-outfit-guides`, `womens-clothing-care-guides`, `alternative-hair-makeup-guides`. Bốn hub VI được phép thêm cặp self-hreflang vi/en trong head, giữ nguyên body. Các source_sha256 cũ không được nhận successor trước khi TSV và EN HTML tương ứng được cập nhật ở E3.

## Cập nhật phê duyệt và tiến độ E3 — 2026-11-17

Người dùng đã nói “duyệt E3, làm tiếp”. E3 đã hoàn tất tại commit nội dung `59bf0e34903667bb233882195ffe007210886501`: 644 link ngữ cảnh, 203 card và 27 đoạn đồng bộ link có sẵn; 414 file EN, 416 TSV bổ sung, 210 successor nguồn có điều kiện. Hash và TSV/manifest cũ giữ nguyên. Hai job Website quality cùng 38 batch dịch EN đều PASS tại run `44110748229`. Báo cáo: `data/en-link-e3-2026-11-17/E3_REPORT.md` và `CI_REPORT.json`.

Chưa làm E4/E5 hoặc merge. Audit còn E9=31, E11=90, E12=51, E13=1; chờ chỉ dẫn tiếp theo của người dùng trước khi triển khai pha mới.

## Cập nhật E4 — 2026-11-17

Người dùng đã nói “tiếp E4”. E4 hoàn tất sửa 187 file EN với 215 TSV bổ sung: gỡ 100 thẻ link dư, sửa 25 đoạn có thuật ngữ xuất bản, đổi 176 anchor và thêm 3 link theo ngữ cảnh. EN đạt 14/14 gate, VI đạt 11/11; parity ngữ cảnh 100%. Toàn bộ hash cũ được giữ nguyên; manifest E4 chỉ bổ sung successor chính xác. Báo cáo tại `data/en-link-e4-2026-11-17/E4_REPORT.md`. E4 là pha cuối được định nghĩa trong tài liệu này; chưa merge.
