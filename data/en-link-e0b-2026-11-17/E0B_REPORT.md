# E0b — Successor VI, dừng trước E1

Branch: `codex/en-link-e0b`. Bản VI đã duyệt: `6d8a9c4`; baseline gốc: `9e16c20`.

## Đã thực hiện

- Thêm `docs/link-fix-2026-11-17/release-manifest.json`, khóa đúng 431 file: 426 bài VI cũ, bốn hub VI mới, `blog.html`. Có hash LF và hash CRLF cụ thể, không chấp nhận thay đổi whitespace tùy ý.
- Giữ nguyên mọi manifest/hash lịch sử, toàn bộ EN HTML, TSV và `source_sha256`.
- Thêm `scripts/qa_link_fix.py`: replay 1.074 span từ patch gốc, đối chiếu CSV, bảo toàn metadata/hreflang/JSON-LD/TOC và thứ tự ảnh/heading gốc; kiểm tra 1.073 lượt href mới/được thay trỏ nội bộ thật.
- 159 ảnh và 159 heading card điều hướng đã được thêm trong đợt VI trước đây; QA chỉ nhận những phần thêm trong span đã ghi, không tuyên bố tổng số ảnh/heading bất biến. Bốn hub mới đối chiếu với lần tạo đầu ở `985f5e3`.
- Bổ sung đúng 12 bản ghi span điều hướng còn thiếu vào CSV. 1.328 bản ghi cũ không đổi, tổng 1.340 bản ghi.
- Chỉ thêm nhận diện successor tại các phép so sánh lịch sử của năm QA; không sửa assertion thành lỏng hơn và không thêm normalization vào đường nguồn bản dịch.
- Nhận diện đúng bốn hub mới trong inventory VI. Node vẫn dùng phép bằng: 423 thẻ gốc nguyên vẹn + đúng bốn URL hub = 427; không cho thẻ dư/trùng.
- Image sitemap Vải/Kính đã khớp ảnh card. Toàn bộ 19 URL bổ sung đã có trong asset map cùng status 200 và SHA-256 thật; không đổi ảnh hoặc bịa hash.
- Thêm gate mới và audit VI vào CI. Job VI/general độc lập với job EN; EN chạy đủ mọi batch và vẫn exit 1 khi có lỗi, không dùng `continue-on-error`.

## Kết quả cục bộ — cùng các lệnh của CI

| Lệnh | Kết quả |
|---|---|
| `audit_vi` | PASS, exit 0 |
| `qa_link_fix` | PASS, exit 0 |
| `qa_privacy_policies` | PASS, exit 0 |
| `qa_schema_pod_performance` | PASS, exit 0 |
| `qa_blog_repair` | PASS, exit 0 |
| `qa_storefront_ux` | PASS, exit 0 |
| `qa_site` | PASS, exit 0 |
| `qa_audit_followup` | PASS, exit 0 |
| `qa_r2_image_seo` | PASS, exit 0 |
| Node shop/journal/privacy | 19/19 PASS |

37 batch EN: **36 FAIL, một PASS (`batch19`)**. Hai lần hub gate trực tiếp còn đỏ, nằm trong các batch EN chưa duyệt, không phải lỗi được che đi. 210/215 source hash vẫn lệch; `en_source_successors` rỗng và QA bắt buộc giữ nguyên trạng thái này trước E3.

36 batch chưa đạt: `batch02`, `batch03`, `batch04`, `batch05`, `batch07`, `batch08`, `batch09`, `batch10`, `batch11`, `batch12`, `batch13`, `batch14`, `batch15`, `batch16`, `batch17`, `batch18`, `batch20`, `batch21`, `batch22`, `batch23`, `batch24`, `batch25`, `batch26`, `batch27`, `batch28`, `batch29`, `batch30`, `batch31`, `batch32`, `batch33`, `batch34`, `batch35`, `batch36`, `batch37`, `batch38`, `batch39`.

Đây là kết quả cục bộ. Kết quả job GitHub cụ thể được xác nhận riêng trong báo cáo chat/PR sau khi CI chạy; không dùng kết quả local để tự nhận remote đã xanh.

## Phạm vi QA đã thay

`qa_privacy_policies`, `qa_blog_repair`, `qa_schema_pod_performance`: chỉ chuẩn hóa exact successor ở điểm so sánh contract lịch sử. Các phép kiểm tra nội dung thực tế vẫn chạy.

`qa_storefront_ux`, `qa_audit_followup`: thêm cùng phép so sánh successor; bốn hub mới có đúng hash riêng được kiểm tra bởi `qa_link_fix`, thay vì đọc Git blob chưa tồn tại trong baseline cũ.

`qa_site`, `qa_r2_image_seo`, `qa_en_translations`, `qa_en_hubs` giữ nguyên. Tất cả file trong `docs/qa` và các manifest lịch sử giữ nguyên. Không thay điều kiện đạt của batch EN.

## Chưa thực hiện

- Chưa E1: không chuyển/dọn `tools/`.
- Chưa E2: chưa tạo hub EN hay batch40, chưa sửa hreflang VI.
- Chưa E3: chưa sửa câu EN, TSV hoặc chấp nhận source successor của bất kỳ batch nào.
- Chưa merge E0b vào master; PR chỉ dùng để review và chạy CI.
- Bản audit EN mới chưa có ở đường dẫn được cung cấp: file Downloads vẫn có SHA-256 `8557b8429a361e853f3abf506cfe75e446c69c72d9e848c5ab853feb709a7ad3`, giống bản E0 cũ. Đã hỏi đường dẫn bản mới; không tự viết bản thay thế. Bản cũ không được dùng để thay cho bản mới trong E0b.

Các lựa chọn E2 đã ghi nhận đúng yêu cầu: batch40; `womens-color-coordination-guides`, `occasion-destination-outfit-guides`, `womens-clothing-care-guides`, `alternative-hair-makeup-guides`.

**Dừng ở E0b để báo cáo CI trước E1.**
