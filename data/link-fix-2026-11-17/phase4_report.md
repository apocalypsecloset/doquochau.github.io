# Báo cáo Pha 4

- Branch: `fix/internal-links-topical-map`; mốc đối chiếu: `bddd970` (Pha 3).
- Thêm 365 link ngữ cảnh trong 267 bài, qua 364 thay thế đoạn khớp chính xác và duy nhất. Mỗi bài thêm tối đa 3 link.
- Tổng quan hệ nguồn → đích trong thân bài: **2.316 → 2.681**.
- Thực hiện 11 lô (tối đa 25 file/lô), chạy audit sau từng lô; không gate nào tăng số lỗi. Không đổi quy tắc hay điều kiện audit.

## Kết quả audit

440 bài VI thật, bỏ qua 9 redirect stub. Kết quả cuối: **ĐẠT TẤT CẢ — 11/11 gate PASS**.

| Gate còn lỗi trước Pha 4 | Trước | Sau |
|---|---:|---:|
| G2: dưới 2 link ngữ cảnh | 3 | 0 |
| G3: thiếu link ngữ cảnh vào | 187 | 0 |
| G6: cặp áo/quần cùng màu thiếu chiều liên kết | 7 | 0 |

Các gate khác giữ PASS. Bảy cặp áo/quần cùng màu đã có đủ hai chiều; các bài hướng dẫn phối màu được nối với item phù hợp.

## Kiểm tra bổ sung

- 440/440 bài có 2–12 đích ngữ cảnh, có link ngữ cảnh từ bài khác, và có link tới bài cùng cụm khác bài cha.
- 440/440 đích có ít nhất 3 biến thể anchor không rỗng trên toàn bộ liên kết blog.
- 23 bài địa điểm/dịp có quan hệ hai chiều với item cụ thể; 17 bài chất liệu có quan hệ hai chiều với bài chăm sóc/thao tác tương ứng.
- Liên kết chất liệu nêu đúng trường hợp: hướng dẫn giặt đồ đen chỉ cho nền tối, gấp áo len chỉ áp dụng phần đồ dệt kim bằng len; không suy rộng cách chăm sóc cho mọi loại vải.
- Giữ nguyên độ phủ cha/con của Pha 3, bao gồm liên kết lên cha trong thân bài.
- So sánh từng file với mốc Pha 3 xác nhận chỉ các đoạn đã duyệt thay đổi. Title, H1, meta, canonical, JSON-LD, ảnh, heading, TOC, reading path, FAQ và nguồn đều giữ nguyên.
- Nhật ký cũ được giữ nguyên; thêm 365 dòng vào `link_changes.csv`, tổng 1.326 dòng dữ liệu.
- `git diff --check -- blog 'tools/*.py'` đạt. Git có thông báo chuyển LF/CRLF theo cấu hình checkout; không có lỗi whitespace.

Mỗi câu mới được viết riêng sau khi đọc đoạn nguồn. Các câu ở bài liên quan burnout chỉ nói về việc áp dụng vào tủ đồ; không sửa nội dung sức khỏe.

## Bằng chứng và phạm vi

- `audit_phase4_before.*`, `audit_phase4_after.*`: số liệu trước/sau.
- `audit_phase4_batch_*`, `phase4_batches.json`: kết quả từng lô.
- `phase4_verification.json`: kiểm tra độc lập giới hạn link, liên kết hai chiều và bảo toàn nội dung.
- `phase4_choices.py`, `phase4_plan.json`, `phase4_patches.json`: câu đã duyệt, vị trí và thay thế chính xác.
- `link_changes.csv`: đích, anchor, đoạn trước và sau cho từng link mới.

Chưa làm Pha 5 và chưa push/deploy. Kiểm tra toàn site bằng `scripts/qa_site.py` cùng báo cáo cuối 5 pha dành cho bước cuối. Chưa có kiểm tra giao diện bằng trình duyệt; lần thử localhost ở Pha 2 không truy cập được từ trình duyệt công cụ. Các kiểm tra hiện tại là audit và đối chiếu cấu trúc/nội dung HTML cục bộ.
