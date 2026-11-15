# Đối chiếu audit và bản sửa ngày 15/11/2026

Baseline GitHub: `490cb5f` (master sau PR #71). Chỉ tạo PR để review; báo cáo này không xác nhận đã merge hoặc deploy.

## Lỗi xác nhận và sửa trong PR

| Hạng mục | Bản master trước sửa | Bản sửa |
|---|---:|---|
| Article thiếu datePublished/dateModified | 436 | Bổ sung theo ngày công bố đã ghi ở journal; không bịa ngày cũ |
| Ngày chưa hiện ở article-meta-top | 438 | Thêm ngày công bố đồng nhất với journal |
| Title EN >65 ký tự | 207 | Rút thương hiệu và viết lại 7 title dài nhất; giữ intent, không cắt giữa câu |
| Description EN >165 ký tự | 21 | Viết gọn, đồng bộ OG/Twitter; giữ description trang chủ ngoài phạm vi |
| Link logo/footer về /en/ | 654 link /218 trang | Trỏ thẳng / |
| Hreflang | 2 bài EN gốc thiếu self; 2 journal thiếu cặp | Thêm 5 thẻ; không tạo cặp VI giả cho bài EN gốc |
| FAQ | Thiếu schema ở 168 trang có FAQ nhận diện được | Sao chép nguyên câu hỏi/trả lời đang hiển thị |
| Thumbnail ảnh lặp | 10 trang / 5 cặp VI–EN | Bỏ thumbnail lặp ở card liên quan, giữ ảnh chính, link và chữ |
| Cover | 2 bản EN thiếu cover gốc | Dùng lại cover VI của Corporate Goth và Soft Goth |
| Cloudflare beacon cứng | 76 trang | Gỡ script nhúng cứng, giữ GA4 chung |
| Chia sẻ Twitter | 427 trang | Dùng x.com/intent/post |
| Tài liệu nội bộ bị index | Chưa có header riêng | Thêm X-Robots-Tag: noindex cho /docs/, /data/, /scripts/, /cloudflare/ trên Cloudflare |

Danh sách thay title/description cũ–mới: `metadata.json`. Danh sách ảnh xử lý: `duplicate-images.json`, `covers.json`. Source hash được cập nhật có đối chiếu trước–sau trong `source-hashes.json`; không tắt kiểm tra bản dịch. Các gate metadata chỉ chấp nhận đúng giá trị thay thế đã ghi, các trường khác vẫn giữ nguyên.

## Nhận xét audit cũ cần điều chỉnh

- 874 URL blog gồm 848 Article/BlogPosting và 26 trang bộ sưu tập. Trang CollectionPage không bắt buộc mang datePublished/dateModified của Article; lỗi thiếu ngày Article đo được là 436, không phải 462.
- Solarpunk VI/EN đã có cover SVG `/assets/editorial/solarpunk-wardrobe.svg`. Hai bài EN gốc đã có ảnh editorial. Không dùng riêng tên CSS `.article-cover` để kết luận thiếu ảnh.
- `G-G2DW7R3BBW` trong login.html là measurementId của cấu hình Firebase. Loader GA4 thực tế dùng `G-452MPHT894`. Không đổi cấu hình Firebase theo audit này.
- Cùng lastmod không tự chứng minh sai. 436 URL được xuất bản đồng loạt qua PR #67 ngày 15/11, nên không chia ngày giả để tăng số giá trị khác nhau. Sitemap được giữ nguyên URL và lastmod.
- Organization là kiểu author hợp lệ; thiếu danh tính cá nhân là vấn đề thông tin biên tập cần xác minh, không phải schema hỏng.
- Trang chủ shop tiếng Anh là lựa chọn ngôn ngữ hiện có; giữ `lang=en` đúng nội dung đang hiển thị.
- Hai bài EN gốc có mục đích riêng; số từ thấp tự nó chưa đủ kết luận thin content. Không kéo dài bằng văn lặp.

## Chưa thể đánh dấu hoàn tất

1. Tác giả/biên tập viên cá nhân: cần tên công khai, vai trò và dữ liệu thật. Không tự gán kinh nghiệm mặc thử hay tác giả cho người quản lý SEO.
2. Nguồn tham khảo: scan có 376 Article không có link ngoài sau khi loại social/affiliate; đây không tương đương 376 bài bắt buộc phải thêm nguồn. Cần kiểm tra từng nhận định, nhất là định nghĩa/vật liệu/lịch sử; chưa bổ sung nguồn hàng loạt khi chưa đọc và kiểm chứng.
3. Bài thưa ảnh và 11 vị trí mỗi ngôn ngữ đã bỏ do trùng/lệch chủ đề: chưa có bộ ảnh mới phù hợp; không dùng lại ảnh trùng để lấp chỗ.
4. `/images-grid/`: có 6 trang dùng đường dẫn này theo scan hiện tại. Môi trường thử HTTP nhận 403 đồng loạt, kể cả logo; chưa thể phân biệt chặn môi trường và lỗi resource. Không đổi sang URL chưa được xác minh.
5. HTML journal vẫn lớn dù đã có pagination/search ở giao diện. Chưa tách thành phân trang HTML phía máy chủ; CSS chặn render và CWV chưa đo trên trình duyệt live. Không tuyên bố đã tối ưu tốc độ.
6. 21 CSS/JS bị nghi thừa và 10 redirect HTML: chưa xóa trước khi xác minh import động và fallback GitHub Pages. Header noindex không xóa hay bảo vệ truy cập báo cáo; GitHub Pages không áp dụng _headers.
7. Không có llms.txt là ghi chú, không phải lỗi cần tạo file để đủ checklist. robots và menu closet noindex được giữ.

## QA

- `python scripts/qa_site.py`
- `python scripts/qa_r2_image_seo.py`
- Tất cả 37 batch article/hub gate hiện có.
- `NODE_PATH=/tmp/ac-shop-tests/node_modules node --test scripts/test_shop.cjs scripts/test_journal.cjs`
- `python scripts/qa_audit_followup.py`: đối chiếu body từng byte sau khi chuẩn hóa đúng các thay đổi được cho phép; kiểm tra canonical, robots, ngôn ngữ, metadata và FAQ.

Kết quả cuối được lưu trong `qa-summary.json`. Chưa xác nhận response header, analytics receipt hay trạng thái production sau deploy.
