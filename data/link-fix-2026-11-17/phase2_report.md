# Pha 2 — Bốn trang tổng quan mới

Baseline: `581927e`. Branch: `fix/internal-links-topical-map`.

| Trang | Từ hướng dẫn tự viết | Bài con đã phủ |
| --- | ---: | ---: |
| `/blog/phoi-mau-quan-ao-nu.html` | 1.331 | 41/41 |
| `/blog/chon-trang-phuc-nu-theo-dia-diem-va-dip.html` | 1.371 | 23/23 |
| `/blog/cach-cham-soc-do-nu.html` | 1.401 | 11/11 |
| `/blog/chon-toc-va-makeup-theo-trang-phuc.html` | 1.362 | 9/9 |

Đếm từ bằng khoảng trắng trên phần giới thiệu và các đoạn hướng dẫn, không tính tiêu đề, mục lục, thẻ bài, footer hoặc mô tả được lấy từ bài cũ. Mỗi trang có 7 phần hướng dẫn, chia bài con theo nhu cầu thực tế. Nội dung riêng là hướng dẫn chọn nhóm; câu trả lời chi tiết theo màu, địa điểm hoặc thao tác vẫn ở bài con.

## Cấu trúc và đăng ký

- Dùng cấu trúc và CSS của `blog/phoi-do-theo-giay-nu.html`, với phần hướng dẫn và thẻ bài có ảnh, tiêu đề, mô tả. Tái sử dụng ảnh của bài con; không tạo thêm tài nguyên hình ảnh.
- Mỗi đích xuất hiện đúng một lần trong nội dung trang mới: nằm trong đoạn hướng dẫn hoặc trên thẻ bài theo nhóm. Tổng cộng 84 link xuống bài con và 4 link ngữ cảnh giữa các trang mới.
- Title, H1, description, canonical riêng; `CollectionPage`, `ItemList`, `BreadcrumbList`, Organization và WebSite JSON-LD hợp lệ. Không sao chép hreflang hoặc nút tiếng Anh khi chưa có bản dịch.
- Thêm đúng một mục/trang vào sitemap, blog và search-index. Giữ nguyên mọi thẻ bài và mục tìm kiếm cũ. Blog có 423 → 427 thẻ; search-index giữ nguyên 367 mục cũ và thêm 4 mục.
- Thêm đủ 4 slug vào `HUBS`. Không thay đổi thuật toán hoặc điều kiện của các gate.

## Phân cụm

Sửa 15 bài bị quy tắc slug xếp sai; danh sách cụ thể ở `phase2_cluster_changes.csv`. Các trường hợp gồm áo ba lỗ, trouser, mẫu đầm nhung/sơ mi, các câu hỏi phối áo theo phom quần/chân váy, da ngăm, giày lội nước, phối đồ theo dáng người và white-on-white. Nguyên tắc là phân loại theo ý định bài đã kiểm tra, không coi mọi slug có `mau` là câu hỏi về màu hoặc mọi câu hỏi “phối với áo gì” là phối màu.

Danh sách bài con lấy từ inventory baseline, sau khi áp dụng các sửa phân loại này. Vì vậy số lượng khác dự kiến cũ ở Pha 0. Giữ nguyên `audit_before.csv` và lưu thêm baseline Pha 2 để đối chiếu.

## Kiểm tra

- `phase2_verify.py`: PASS. 445 file blog cũ không thay đổi; bốn trang đủ tối thiểu 1.200 từ, trỏ đủ bài con, không trùng title/H1/description với các trang HTML khác của site, canonical đúng, JSON-LD đúng inventory, không trùng ID hoặc đích link trong nội dung, link nội bộ hợp lệ và đăng ký đủ cả ba nơi.
- Giữ nguyên metadata và JSON-LD của `blog.html`; chỉ chèn bốn thẻ bài. Mọi mục tìm kiếm cũ giữ nguyên dữ liệu.
- `node --check search-index.js`: PASS. Thực thi search-index trong Node VM và kiểm tra cú pháp JavaScript inline của bốn trang: PASS.
- Audit: 440 bài VI và 9 redirect. G1, G7–G11 PASS. G2=10, G3=202, G4=20, G5=99, G6=7. Vẫn còn 5 gate chưa đạt, thuộc các pha tiếp theo.
- Bốn trang đều phủ 100% liên kết xuống. Việc các bài con trỏ lên trang mới chưa thực hiện, đúng phạm vi Pha 3. Sửa phân cụm làm thay đổi một số thống kê theo nhóm; không sửa nội dung các bài cũ trong Pha 2.
- Kiểm tra khoảng trắng trên HTML, JavaScript, XML và Python: PASS. Log TXT lưu nguyên output script.

## Giới hạn và công việc chưa làm

Trình duyệt xem trước không truy cập được máy chủ loopback của máy chạy lệnh (`ERR_CONNECTION_TIMED_OUT`). Đã dừng máy chủ thử; chưa xác minh bố cục bằng ảnh trình duyệt. CSS dùng lại nguyên mẫu đang có. Chưa chạy QA toàn site yêu cầu ở cuối Pha 5; chưa thực hiện Pha 3–5, chưa push hoặc triển khai.

Các thao tác tạo trang và chèn index được lưu trong `phase2_build.py`, nội dung tự viết trong `phase2_content.py`, thống kê và xác minh trong `phase2_pages.json` và `phase2_verification.json`. `link_changes.csv` được bổ sung 88 dòng cho các link mới; cột trước để trống vì đây là trang mới.
