# Pha 3 — Trang tổng quan và bài con liên kết hai chiều

Baseline: `985f5e3`. Branch: `fix/internal-links-topical-map`.

## Kết quả

G4 PASS. Cả 13 cụm đã phủ đủ liên kết xuống 421 bài con; 421/421 bài có link lên trang tổng quan trong thân bài. Cụm Aesthetic/Style được kiểm tra theo tập gồm từ điển và 6 trang nhánh, đúng cách audit định nghĩa.

- Bổ sung 177 link xuống các bài còn thiếu, chia theo nhóm có đoạn hướng dẫn riêng. Dùng thẻ bài cùng ảnh, tiêu đề và mô tả cho phần điều hướng, như cấu trúc đã dùng ở Pha 2.
- Viết riêng 276 câu liên kết lên trong các đoạn có sẵn. Không tính link chỉ nằm trong điều hướng là đã đáp ứng yêu cầu thân bài.
- Khai báo trang có sẵn `phoi-do-theo-item.html` cho Outfit-core trong `HUBS`; không tạo trang mới và không thay điều kiện gate.
- Một bài mua sắm đang có 12 đích blog trong thân bài. Lô thử thêm link thứ 13 đã được tự động hoàn tác. Sau khi đọc lại, bỏ thẻ liên kết tới bài thời tiết mùa hè, giữ nguyên chữ, để dành vị trí cho link lên trang tổng quan. Giữ nguyên các link mua hàng và kiểm tra sản phẩm cụ thể.
- Tổng cộng 285 file blog được chỉnh bằng 289 chuỗi thay thế khớp chính xác, duy nhất. Có 453 link mới và 1 lần bỏ thẻ link. Tổng cặp nguồn–đích ngữ cảnh phân biệt: 2.023 → 2.316.

## Audit trước và sau

| Gate | Trước | Sau |
| --- | ---: | ---: |
| G1 link gãy/redirect | 0 | 0 |
| G2 bài thiếu 2 link ra | 10 | 3 |
| G3 bài chưa có link ngữ cảnh vào | 202 | 187 |
| G4 lỗi liên kết tổng quan–con | 20 | 0 |
| G5 bài thiếu link cùng cụm | 99 | 0 |
| G6 cặp áo–quần cùng màu | 7 | 7 |
| G7 câu dẫn kỹ thuật | 0 | 0 |
| G8 anchor chung chung/rỗng | 0 | 0 |
| G9 link trùng đích trong bài | 0 | 0 |
| G10 anchor lặp quá 5 lần | 0 | 0 |
| G11 quá 12 đích blog trong thân bài | 0 | 0 |

Kết quả còn **3 gate chưa đạt: G2, G3, G6**. G5 tính cả link tới trang tổng quan cùng cụm; việc chọn link ngang giữa các bài con theo nhu cầu người đọc vẫn thuộc Pha 4. Không coi PASS G5 ở đây là đã thực hiện xong toàn bộ yêu cầu của Pha 4.

## Kiểm tra bảo toàn

`phase3_verify.py` xác nhận:

- Title, H1, meta, canonical, JSON-LD, TOC, ac-reading-path, seo-faq và ac-sources của mọi file chỉnh sửa giữ nguyên.
- Các ảnh và heading gốc vẫn nguyên vẹn, đúng thứ tự; chỉ bổ sung thẻ bài trong các nhóm điều hướng.
- Mọi thay đổi byte trong HTML đều thuộc chuỗi thay thế đã lưu trong `phase3_patches.json`.
- Link xuống và link lên trong thân bài đủ 100% cho từng cụm, được kiểm tra riêng với audit G4 vốn chấp nhận cả link trong điều hướng.
- Nhật ký các pha trước được giữ nguyên, bổ sung 454 dòng trong `link_changes.csv`. Phần điều hướng mới có cột trước trống; câu trước/sau của đoạn cũ được lưu cho các link lên và lần bỏ thẻ link.

Audit chạy sau 13 lô thành công; số lỗi của không gate nào tăng so với lô thành công trước đó. Log lô bị từ chối do quá mật độ được giữ ở `audit_phase3_rejected_12.txt`. Lô cuối cùng và audit sau cùng đều giữ G1, G7–G11 PASS.

Kiểm tra khoảng trắng trên mã Python PASS. `git diff --check` báo một dòng HTML đã có sẵn hai dấu cách cuối dòng ở bài chân váy jean ngắn; dòng này chứa đoạn được chèn link nên xuất hiện lại trong diff. Giữ nguyên khoảng trắng gốc để không sửa ngoài các đoạn đã duyệt. File TXT audit cũng giữ nguyên output gốc.

## Giới hạn và bước tiếp theo

Không thay RULES phân cụm trong Pha 3. Bài về burnout vẫn là trường hợp nội dung giao thoa trong inventory có sẵn; chỉ chèn link tại đoạn ứng dụng tủ đồ, không sửa các đoạn sức khỏe. Phần đọc mở rộng ở từ điển ghi rõ bài này không phải một aesthetic và quần áo không có vai trò điều trị.

Chưa chạy QA toàn site yêu cầu ở cuối Pha 5, chưa kiểm tra bố cục bằng ảnh trình duyệt do giới hạn xem trước đã ghi ở Pha 2. Chưa làm Pha 4–5, chưa push hay triển khai site.

Các script Pha 3 dùng baseline riêng và inventory đã đóng băng; không dùng chúng để ghi đè công việc ở các pha sau. Khi tiếp tục, chạy audit hiện tại để xác định phần còn thiếu.
