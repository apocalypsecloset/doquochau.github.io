# Sửa topical map và internal link — 18/11/2026

Baseline: `97ba710f3e23cde22c9dc72b87052b507049ddaa` (`master`). Branch: `codex/topical-links-editorial`.

## Kết quả trên mã nguồn hiện tại

- Sửa 289 trang HTML: 160 blog VI, 128 blog EN và trang lõi `/phoi-do-nu-ca-tinh.html`.
- Bổ sung **299 quan hệ link ngữ cảnh giữa các trang blog**: VI **2.678 → 2.820** (+142), EN **2.696 → 2.853** (+157). Không mất quan hệ ngữ cảnh có sẵn. Đếm nhất quán bằng cùng bộ tách thân bài, loại các module đã biết; không cộng menu/card để làm đẹp số liệu.
- Cả **882 trang blog** có ít nhất **hai trang khác dẫn link ngữ cảnh vào**. Không còn danh sách 139 trang VI / 147 trang EN chỉ có một nguồn dẫn như audit trước.
- Mỗi bài lá VI có link sang bài lá trong cùng nhóm đã rà soát; link về trang cha không được dùng để thay cho tiêu chí này.
- VI → EN đạt **100% quan hệ ngữ cảnh tương ứng**. Các liên kết đổi ngôn ngữ có chủ đích vẫn được giữ.
- Quét **1.058 trang HTML**, **52.537 thẻ link nội bộ**: không có đích thiếu file, fragment sai hoặc link vào redirect stub. Đủ **1.043 URL sitemap** đi được từ trang chủ, tối đa ba lần bấm.
- Audit cũ giữ nguyên mã và ngưỡng: **VI 11/11 PASS; EN 15/15 PASS** trên HTML thực tế sau sửa.

## Đã chỉnh những gì

### Câu chứa link

Viết lại các câu ghép anchor sai ngữ pháp hoặc lặp ý, dùng nhãn dễ hiểu và đúng đích. Ưu tiên bọc link vào tên món/phong cách đã có trong đoạn; khi cần thêm câu, dùng tình huống riêng của trang nguồn và bản EN tương ứng.

Ví dụ:

| Trang | Trước | Sau |
|---|---|---|
| Phối đồ vùng bụng | “xem chọn phom quần nữ” | “tham khảo hướng dẫn chọn phom quần nữ” |
| Rock Chic | “Bạn có thể dùng tra tên phong cách” | “Bạn có thể tra cứu các phong cách thời trang” |
| Slim Fit | “Guide chọn cạp và ống quần giúp chọn cạp và ống…” | “Tham khảo cách chọn phom quần nữ để so sánh độ cao cạp và độ rộng ống…” |
| Phối màu vàng | “bài xử lý gấu lớp ngoài giúp xử lý chiều dài lớp ngoài” | “Hướng dẫn cân chiều dài khi layering giải thích cách phối áo khoác với lớp trong…” |
| Edgy | “Bài tổ chức lớp áo nữ đi sâu vào cách tổ chức các lớp” | “Tham khảo cách phối lớp áo nữ để chọn lớp trong, độ dài và bề mặt vải.” |
| Hime Gyaru | “Pillar Gyaru” | “Tổng quan Gyaru” |

Đã rà thêm các mẫu “xem chọn…”, “dùng tra…” và nhãn `pillar` trong phần nội dung liên kết. Không đổi tên metadata/heading để đạt điều kiện kiểm tra.

### Topical map rõ từng URL

`data/topical-map.json` đăng ký đủ 882 URL: ngôn ngữ, vai trò, chủ đề chính, ý định, trang cha và chủ đề liên quan. Trang mới chưa khai báo sẽ làm kiểm tra thất bại, không tự rơi vào Aesthetic.

- Burnout chuyển về tuyến **lifestyle và quyết định tủ đồ**.
- Auth, like auth, local brand, boutique và sold out thuộc **thuật ngữ mua sắm**, có điều hướng tới trang mua sắm và ngược lại.
- Các nhánh Goth, Punk/Grunge, E-Girl, Dark Feminine, streetwear, Y2K, academic/preppy, phong cách đời thường, fantasy và các tham chiếu Nhật/lịch sử được ghi rõ, thay cho một nhóm mặc định quá rộng.
- Toàn bộ quan hệ trang cha trong registry được đối chiếu với link HTML thực tế hai chiều. Hai bài EN gốc có trang English Journal làm điểm cha, giữ nguyên ý định riêng.
- Giữ nguyên 13 nhóm của audit cũ để không sửa thước đo lịch sử. Registry mới kiểm tra thêm vai trò/ý định và liên kết thực tế độc lập.

### Độ tự nhiên và lộ trình đọc

Tách các đoạn gom link ở Classic, Crop Top, Leather Jacket, Midi, A-line, Flared Skirt, Mob Wife, Baddie và hướng dẫn gấp đồ. Đưa các tham khảo EN về đoạn đang nói đúng vấn đề.

Giữ **tám đoạn liệt kê có ích** (hai ngôn ngữ) về các nhánh Goth, Gyaru/Hime Gyaru và các tham chiếu Nu Metal. Những đoạn này được ghi rõ trong `dense-reviewed-exceptions.json`; không áp quota máy móc cho danh sách so sánh có ý nghĩa.

Trang lõi phối đồ có đường dẫn trực tiếp tới phối màu, chọn đồ theo dịp, tóc/makeup và chăm sóc đồ. Item Guide cũng nối sang phối màu và chăm sóc; bài đi chơi nối sang lịch trình và tóc/makeup.

## Bảo toàn và kiểm tra hồi quy

`qa_topical_editorial.py` đọc **HTML hiện tại** và kiểm tra:

1. Replay chính xác toàn bộ thay đổi từ baseline; mọi HTML ngoài bản sửa phải giữ nguyên.
2. Title, meta, canonical/hreflang, H1–H4, ảnh, script/JSON-LD, mục lục, reading path, FAQ và nguồn giữ nguyên DOM.
3. Tối thiểu hai nguồn ngữ cảnh vào, link giữa bài lá, parity VI/EN 100%, cha–con có thật, phân loại đủ URL.
4. Toàn bộ đích nội bộ, fragment, redirect, khả năng đi tới URL sitemap và cả hai audit cũ trên bản hiện tại.
5. Các hồ sơ lịch sử, script cũ và tài sản không liên quan không được sửa.

Các test lịch sử trước đây khóa byte của từng đợt xuất bản. Vì nhiệm vụ mới được phép sửa nội dung, CI chạy nguyên các test đó trong một checkout **độc lập, chỉ có baseline đã ghim**, rồi kiểm tra bản hiện tại bằng gate mới ở trên và `qa_site.py`. Không sửa hash hoặc bỏ assertion trong test cũ; không cho nội dung lạ nhận bản xem lịch sử. Runner không cần mạng và không sửa working tree đang làm việc.

Kiểm tra đã có kết quả:

- `qa_topical_editorial.py`: PASS, không lỗi.
- `qa_site.py`: PASS; 1.058 HTML, 1.043 URL sitemap, 442 card EN; giữ metadata của 605 trang lịch sử.
- **38 batch dịch hiện có** theo đúng danh sách CI: PASS trên hợp đồng xuất bản đã ghim.
- E15, E4, E3 và VI link-release: PASS trên baseline lịch sử.
- Các kết quả kiểm tra bổ sung được lưu trong `history-results.json` khi hoàn tất.

## Dữ liệu review

- `data/topical-map.json`: registry đầy đủ dùng cho kiểm tra.
- `data/topical-editorial-2026-11-17/topical-map.csv`: map dễ lọc, kèm số nguồn vào và đích ngữ cảnh.
- `new-contextual-links.csv`: đủ 299 quan hệ mới, anchor và đoạn chứa link thực tế.
- `review-sample20.json`: 20 quan hệ mới chọn ngẫu nhiên với seed `20261117`.
- `patches.json`: bằng chứng replay chính xác của lần sửa này; các manifest/TSV cũ giữ nguyên.
- `verification.json`, `site-verification.json`, `translation-history-results.json`: kết quả kiểm tra.

## Giới hạn

Đây là sửa cấu trúc và nội dung trong repo. Không suy ra đã bao phủ mọi truy vấn thị trường, có topical authority tuyệt đối, hoặc hết cannibalization khi chưa có dữ liệu GSC/SERP. Kiểm tra đích là trên mã nguồn tĩnh; việc xác minh triển khai live thuộc bước sau khi merge/deploy. PR giữ bản sửa ở trạng thái có thể review trước khi đưa lên production.
