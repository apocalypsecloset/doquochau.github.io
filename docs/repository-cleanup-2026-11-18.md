# Dọn repo — 18/11/2026

Baseline đã merge PR #82: `51035256000a09c8879fd1577d6b44a23a025948`. Nhánh: `codex/repository-cleanup`.

## Đã dọn

Xóa **710 file**, tổng **44,118,596 byte (42.07 MiB)** trong checkout trước khi tính phần bằng chứng kiểm tra mới:

- **46 CSS** cũ không còn được HTML/JS/CSS đang dùng hoặc bộ tạo trang tham chiếu: 20 bundle, 24 shared-inline và hai shared minified; khoảng 1.16 MiB.
- **4 script dùng một lần**: `apply_reviewed_alts.py`, `compact_journal_search.py`, `compile_article_css.py`, `fix_audit_followup.py`. Không có workflow/import hay bộ tạo trang đang gọi.
- **660 file trung gian trong data/**: snapshot HTML/phân tích nhiều MB, kế hoạch áp patch, bản script dùng một lần, CSV audit tạm và log stdout/stderr. Chỉ chọn những file không được code giữ lại hoặc manifest dữ liệu tiêu thụ.

Những ví dụ chiếm chỗ lớn: `paragraphs.json` của E3 (8,5 MB), `phase4_inventory.json` (7,6 MB), `phase3_inventory.json` (6 MB), inventory và after_cleanup của E4. Đây là dữ liệu chuẩn bị/so sánh trong quá trình làm việc, không phải trang web, bản dịch hay đầu vào xuất bản.

## Đã giữ

- Mọi HTML, JavaScript phục vụ website, CSS đang dùng, 140 CSS compiled, ảnh và font giữ nguyên byte tương đương baseline.
- Sáu bundle còn dùng. Báo cáo cũ ghi “5” nhưng liệt kê sáu; lần rà này xác nhận đủ sáu.
- `en-hubs.css`: hiện **bốn trang tổng hợp EN tải trực tiếp**, đồng thời generator dùng nó. `en-translations.css`: generator EN vẫn cần.
- Toàn bộ `data/en-translations/`, registry topical map và hồ sơ editorial mới; các bảng dịch, manifest, lock và bằng chứng mà QA cần.
- Toàn bộ docs lịch sử đang có, gồm 162 file docs/qa; không xóa hay đổi các manifest/hash cũ.
- `cloudflare/`: cấu hình storefront trỏ tới Worker API thật, nên đây là hạ tầng cửa hàng, không phải file thừa chỉ vì không nhúng bằng script tag.
- File key xác minh, Google Search Console, login, 404, robots, sitemap, CNAME và cấu hình bảo mật/publish.

## Bảo toàn CI

Không tắt workflow, không comment hoặc xóa kiểm tra `Missing CSS source`. Các hợp đồng lịch sử tiếp tục chạy nguyên trạng trong checkout baseline đã ghim qua runner sẵn có từ PR #82; bản checkout lịch sử vẫn có toàn bộ nguồn CSS và bằng chứng cũ trong Git.

`qa_repository_cleanup.py` kiểm tra cleanup thực tế: mọi file còn giữ phải khớp blob baseline (chấp nhận chuyển dòng LF/CRLF của Git), chỉ một adapter QA được sửa đúng hash đã khai báo, và chỉ bốn file mới được thêm. Nó kiểm tra lại không có HTML/CSS/JS nào còn gọi CSS đã bỏ, code giữ lại không tiêu thụ các file bị xóa, và các file phải giữ vẫn còn. Gate hiện tại `qa_topical_editorial.py` gọi kiểm tra này trước khi cho phép đúng danh sách xóa; không nới điều kiện link hoặc bảo toàn nội dung.

Danh sách đầy đủ kèm blob Git, SHA-256, dung lượng và lý do: `data/repository-cleanup-2026-11-18.json`.

## Lưu ý về dung lượng và publish

Dung lượng giảm ở cây file/checkout của repo; lịch sử Git không bị viết lại, nên `.git` không tự nhỏ tương ứng. Có thể khôi phục từng file bằng baseline trên.

`_config.yml` loại docs/data/scripts/cloudflare khi **GitHub Pages/Jekyll** build. Không suy ra cấu hình đó cũng loại chúng trên Cloudflare Pages: repo đang ghi rõ Cloudflare có cấu hình build riêng và `_headers` là fallback noindex. Cleanup này không thay cấu hình hosting hoặc đưa ra kết luận rằng mọi file nội bộ đã bị chặn khỏi Cloudflare.

## Kiểm tra

Kết quả cuối được ghi trong PR: gate cleanup, gate editorial/link trên HTML hiện tại, qa_site và cả hai job GitHub Actions. Nội dung website không được chỉnh trong đợt dọn này.
