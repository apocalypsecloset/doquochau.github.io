# Báo cáo cuối — Internal link và topical map blog VI

Branch: `fix/internal-links-topical-map`. Baseline: `9e16c20`.

## Kết quả

Hoàn tất Pha 1–5. Audit cuối: **ĐẠT TẤT CẢ — 11/11 gate PASS**.

- Bài VI thật: 436 → 440 (thêm 4 trang tổng quan); giữ 9 redirect stub, không trỏ link mới vào stub.
- Quan hệ nguồn → đích blog phân biệt trong nội dung: **2,003 → 2,681**. Đây là số cặp nguồn–đích, không phải số thẻ `<a>` trên toàn site.
- Cả 440 bài có 2–12 đích blog ngữ cảnh, có bài khác link vào, và có bài ngang cùng cụm ngoài bài cha.
- 421 bài con được phủ liên kết cha/con; 7 cặp áo/quần cùng màu đã có đủ hai chiều.
- 23 bài địa điểm/dịp có link hai chiều với item; 17 bài chất liệu có link hai chiều với hướng dẫn chăm sóc/thao tác tương ứng.
- Nhật ký chứa 1,328 dòng trước/sau của các pha.

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
- `python -X utf8 scripts/qa_site.py`: exit 0; kiểm tra 1054 trang HTML, 1039 URL sitemap, 218 cặp VI/EN, 438 thẻ bài English Journal; đối chiếu metadata 605 trang lịch sử; không lỗi.
- Đã tải riêng commit baseline QA còn thiếu bằng `git fetch --depth=1 origin <SHA>`; không đổi file site hay script QA. Chạy với UTF-8 vì encoding mặc định Windows không đọc được dữ liệu Unicode.
- Kiểm tra độc lập từ baseline nhiệm vụ: metadata, H1, canonical, schema, ảnh và heading gốc còn nguyên trong 445 file blog; bốn trang mới đối chiếu với commit Pha 2. Các thẻ bài con mới được thêm ở Pha 3 có ảnh/heading riêng, không thay ảnh/heading gốc.
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

### 1. `blog/quan-slim-fit.html`

Đích: `blog/phoi-do-theo-quan-nu.html`; anchor: chọn cạp và ống quần

Trước:

```html
Áo slim với quần rộng làm phần thân trên gọn hơn trong tổng thể. Bạn có thể chọn áo chạm cạp hoặc sơ vin nếu vải không dồn. Guide phối đồ theo quần nữ giúp chọn cạp và ống theo mức rộng bạn muốn.
```

Sau:

```html
Áo slim với quần rộng làm phần thân trên gọn hơn trong tổng thể. Bạn có thể chọn áo chạm cạp hoặc sơ vin nếu vải không dồn. Guide chọn cạp và ống quần giúp chọn cạp và ống theo mức rộng bạn muốn.
```

### 2. `blog/cach-phoi-do-cho-nguoi-beo-bung-nu.html`

Đích: `blog/phoi-do-theo-quan-nu.html | blog/phoi-do-theo-ao-nu.html`; anchor: chọn phom quần nữ | chọn cổ và phom áo

Trước:

```html
Muốn hiểu sâu hơn về các form bottom, xem Item Guide Quần Nữ . Nếu vấn đề nằm ở top, Item Guide Áo Nữ giúp đọc form, neckline và layer trước khi mua thêm đồ.
```

Sau:

```html
Muốn hiểu sâu hơn về các form bottom, xem chọn phom quần nữ . Nếu vấn đề nằm ở top, chọn cổ và phom áo giúp đọc form, neckline và layer trước khi mua thêm đồ.
```

### 3. `blog/chon-trang-phuc-nu-theo-dia-diem-va-dip.html`

Đích: `/blog/rave-outfits.html`; anchor: Rave outfits: Cách phối đồ đi rave dễ vận động Rave outfits dễ vận động: bốn công thức, cách chọn lớp mặc trong, giày, túi và điểm nhấn; thử cả bộ theo động tác trước buổi đi.

Trước:

```html

```

Sau:

```html
Rave outfits: Cách phối đồ đi rave dễ vận động Rave outfits dễ vận động: bốn công thức, cách chọn lớp mặc trong, giày, túi và điểm nhấn; thử cả bộ theo động tác trước buổi đi.
```

### 4. `blog/wafuku.html`

Đích: `blog/phoi-do-layering-nu.html`; anchor: cân độ dài lớp ngoài

Trước:

```html
Cách kiểm soát độ dài giữa các lớp trong bài phối đồ layering nữ có thể hỗ trợ bước thử này. Hãy giữ một điểm nhấn rõ và kiểm tra khi cởi lớp ngoài: phần nền vẫn nên là một bộ đồ bạn thấy thoải mái sử dụng.
```

Sau:

```html
Cách kiểm soát độ dài giữa các lớp trong bài cân độ dài lớp ngoài có thể hỗ trợ bước thử này. Hãy giữ một điểm nhấn rõ và kiểm tra khi cởi lớp ngoài: phần nền vẫn nên là một bộ đồ bạn thấy thoải mái sử dụng.
```

### 5. `blog/phoi-mau-quan-ao-nu.html`

Đích: `/blog/ao-vang-phoi-quan-mau-gi.html`; anchor: Áo vàng phối quần màu gì? Công thức theo sắc vàng Chọn quần trắng, đen, xám, navy, denim và nâu cho áo vàng nhạt, vàng tươi, vàng mù tạt; cân màu, độ rộng và phụ kiện theo dịp.

Trước:

```html

```

Sau:

```html
Áo vàng phối quần màu gì? Công thức theo sắc vàng Chọn quần trắng, đen, xám, navy, denim và nâu cho áo vàng nhạt, vàng tươi, vàng mù tạt; cân màu, độ rộng và phụ kiện theo dịp.
```

### 6. `blog/quan-hong-phoi-ao-mau-gi.html`

Đích: `/blog/phoi-mau-quan-ao-nu.html`; anchor: nối các mảng màu trang phục

Trước:

```html
Quần hồng phấn cũng đi được với áo đen. Sự chênh lệch sáng tối có thể khiến phần thân trên và dưới tách rõ; bạn có thể nối lại bằng giày đen, hoặc giữ giày sáng để phần dưới nhẹ hơn. Cả hai đều là lựa chọn về tỷ lệ màu, không phải cách nào bắt buộc mới đúng.
```

Sau:

```html
Quần hồng phấn cũng đi được với áo đen. Việc nối các mảng màu trang phục giúp bạn so hai cách kết thúc ở giày mà vẫn giữ nguyên áo đen. Sự chênh lệch sáng tối có thể khiến phần thân trên và dưới tách rõ; bạn có thể nối lại bằng giày đen, hoặc giữ giày sáng để phần dưới nhẹ hơn. Cả hai đều là lựa chọn về tỷ lệ màu, không phải cách nào bắt buộc mới đúng.
```

### 7. `blog/quan-cargo-la-gi.html`

Đích: `/blog/phoi-do-theo-quan-nu.html`; anchor: những đường ống quần nữ

Trước:

```html
Ống quần cũng quan trọng. Nếu đùi rộng nhưng ống thu quá nhanh, phần túi sẽ càng nổi. Dáng suông hoặc rộng đều từ đùi xuống thường tạo đường dọc ổn định hơn. Màu đen, xám than hoặc olive tối dễ hòa túi vào tổng thể, phù hợp closet dark aesthetic.
```

Sau:

```html
Ống quần cũng quan trọng. Đặt cargo cạnh những đường ống quần nữ giúp bạn nhận ra phần khối do túi và phần khối do dáng cắt. Nếu đùi rộng nhưng ống thu quá nhanh, phần túi sẽ càng nổi. Dáng suông hoặc rộng đều từ đùi xuống thường tạo đường dọc ổn định hơn. Màu đen, xám than hoặc olive tối dễ hòa túi vào tổng thể, phù hợp closet dark aesthetic.
```

### 8. `blog/phoi-mau-quan-ao-nu.html`

Đích: `/blog/ao-xanh-reu-phoi-quan-mau-gi.html`; anchor: Áo xanh rêu phối quần màu gì? Cách chọn cho nữ Áo xanh rêu phối quần màu gì? Thử kem, be, đen, xám, denim và nâu theo sắc rêu; cân form áo, màu giày và túi để dễ mặc.

Trước:

```html

```

Sau:

```html
Áo xanh rêu phối quần màu gì? Cách chọn cho nữ Áo xanh rêu phối quần màu gì? Thử kem, be, đen, xám, denim và nâu theo sắc rêu; cân form áo, màu giày và túi để dễ mặc.
```

### 9. `blog/quan-nau-phoi-ao-mau-gi.html`

Đích: `/blog/phoi-mau-quan-ao-nu.html`; anchor: phối từ màu quần có sẵn

Trước:

```html
Sơ mi xanh nhạt với quần nâu là cách phối dễ dùng cho đi học hoặc nơi làm việc có quy định trang phục phù hợp. Xanh nhạt tạo khoảng sáng ở thân trên, còn nâu giữ phần dưới trầm hơn. Với quần caramel, sự khác biệt giữa hai màu thường nhìn thấy rõ.
```

Sau:

```html
Sơ mi xanh nhạt với quần nâu là cách phối dễ dùng cho đi học hoặc nơi làm việc có quy định trang phục phù hợp. Phần phối từ màu quần có sẵn giúp bạn thử xanh nhạt trên từng sắc nâu thay vì áp một công thức chung. Xanh nhạt tạo khoảng sáng ở thân trên, còn nâu giữ phần dưới trầm hơn. Với quần caramel, sự khác biệt giữa hai màu thường nhìn thấy rõ.
```

### 10. `blog/phoi-do-theo-item.html`

Đích: `/blog/local-brand-la-gi.html`; anchor: Local Brand Là Gì? Cách Chọn Local Brand Nữ

Trước:

```html

```

Sau:

```html
Local Brand Là Gì? Cách Chọn Local Brand Nữ Local brand là gì? Phân biệt local brand với shop order, fast fashion và cách chọn local brand nữ theo fit, size, chất liệu, gu và ngân sách.
```

### 11. `blog/harajuku-style.html`

Đích: `blog/aesthetic-dictionary.html`; anchor: từ điển các aesthetic

Trước:

```html
Nếu chưa chắc mình nghiêng về hướng nào, xem Aesthetic Dictionary ; mix hiệu quả hơn khi bạn biết mình đang trộn tín hiệu nào.
```

Sau:

```html
Nếu chưa chắc mình nghiêng về hướng nào, xem từ điển các aesthetic ; mix hiệu quả hơn khi bạn biết mình đang trộn tín hiệu nào.
```

### 12. `blog/ao-vang-phoi-quan-mau-gi.html`

Đích: `blog/phoi-do-theo-quan-nu.html`; anchor: chọn ống và cạp quần

Trước:

```html
Denim đậm tạo nền sâu hơn và có thể làm áo vàng nhạt tách rõ. Nếu áo rộng và quần cũng rộng, để một điểm gọn ở cạp hoặc tay áo để thử cân khối. Guide phối đồ theo quần nữ giúp chọn kiểu ống, cạp và độ dài trước khi đổi màu.
```

Sau:

```html
Denim đậm tạo nền sâu hơn và có thể làm áo vàng nhạt tách rõ. Nếu áo rộng và quần cũng rộng, để một điểm gọn ở cạp hoặc tay áo để thử cân khối. Guide chọn ống và cạp quần giúp chọn kiểu ống, cạp và độ dài trước khi đổi màu.
```

### 13. `blog/outfit-di-choi-dem-badgirl.html`

Đích: `/blog/chon-trang-phuc-nu-theo-dia-diem-va-dip.html`; anchor: phối theo lịch đi chơi

Trước:

```html
Xám wash tốt hơn đen tuyệt đối khi bạn muốn ảnh có texture dưới ánh đèn. Túi chain, túi bạc hoặc túi đen có buckle nên là statement duy nhất; không cần cộng thêm nhiều necklace lớn. Nếu quần đã rộng và dài, sneaker hoặc boots đế vừa giúp hem không quét đất. Đọc thêm quần baggy là gì nếu cần chọn độ rộng theo tỷ lệ cơ thể.
```

Sau:

```html
Xám wash tốt hơn đen tuyệt đối khi bạn muốn ảnh có texture dưới ánh đèn. Nếu buổi tối có nhiều chặng, phối theo lịch đi chơi để chọn khối giày dùng được suốt buổi rồi mới chốt túi nhấn. Túi chain, túi bạc hoặc túi đen có buckle nên là statement duy nhất; không cần cộng thêm nhiều necklace lớn. Nếu quần đã rộng và dài, sneaker hoặc boots đế vừa giúp hem không quét đất. Đọc thêm quần baggy là gì nếu cần chọn độ rộng theo tỷ lệ cơ thể.
```

### 14. `blog/denim-on-denim.html`

Đích: `/blog/phoi-do-theo-quan-nu.html`; anchor: các dáng quần nữ để so

Trước:

```html
Ở chân váy, kiểm tra độ dài bước chân cùng đường xẻ. Hai mảng denim lớn ở thân trên và dưới có thể đẹp khi đứng, nhưng phần váy cần đủ khoảng chuyển động để đi cầu thang hoặc ngồi xuống. Độ vừa phải được đánh giá ở cả hai món, không chỉ món gần mặt nhất.
```

Sau:

```html
Ở chân váy, kiểm tra độ dài bước chân cùng đường xẻ. Để chuyển từ váy denim sang quần mà vẫn giữ lớp áo, xem các dáng quần nữ để so rồi thử lại độ rộng và khả năng di chuyển. Hai mảng denim lớn ở thân trên và dưới có thể đẹp khi đứng, nhưng phần váy cần đủ khoảng chuyển động để đi cầu thang hoặc ngồi xuống. Độ vừa phải được đánh giá ở cả hai món, không chỉ món gần mặt nhất.
```

### 15. `blog/y2k-la-gi-phong-cach-y2k-nu.html`

Đích: `/blog/aesthetic-dictionary.html`; anchor: so sánh các hệ aesthetic

Trước:

```html
Một outfit màu hồng + túi bạc chưa chắc đã đọc thành Y2K nếu tỷ lệ hoàn toàn contemporary. Hãy kiểm tra theo thứ tự: silhouette → surface → accessory . Ví dụ, fitted baby tee + quần ống rộng/cạp vừa đã có nền Y2K; thêm shoulder bag nhỏ hoặc kính hẹp là đủ. Ngược lại, một set tối giản cạp cao + túi bạc chỉ mới có metallic accent.
```

Sau:

```html
Một outfit màu hồng + túi bạc chưa chắc đã đọc thành Y2K nếu tỷ lệ hoàn toàn contemporary. Dùng so sánh các hệ aesthetic để kiểm tra phần tham chiếu Y2K ngoài riêng hai màu hồng và bạc. Hãy kiểm tra theo thứ tự: silhouette → surface → accessory . Ví dụ, fitted baby tee + quần ống rộng/cạp vừa đã có nền Y2K; thêm shoulder bag nhỏ hoặc kính hẹp là đủ. Ngược lại, một set tối giản cạp cao + túi bạc chỉ mới có metallic accent.
```

### 16. `blog/ao-jersey.html`

Đích: `/blog/ao-anime-nu.html`; anchor: đọc bố cục áo anime

Trước:

```html
Ở khí hậu nóng, xem cả lớp lót và độ dày hình in. Vải có lỗ nhìn thấy không tự động bảo đảm toàn chiếc áo thoáng, vì lớp dưới có thể kín. Nếu có thể thử, mặc vài phút và vận động nhẹ sẽ cho thông tin hữu ích hơn chỉ chạm tay vào một góc vải.
```

Sau:

```html
Ở khí hậu nóng, xem cả lớp lót và độ dày hình in. Áo có mảng nhân vật lớn cũng cần bước thử này; đọc bố cục áo anime giúp tách phần hình in khỏi độ vừa của thân áo. Vải có lỗ nhìn thấy không tự động bảo đảm toàn chiếc áo thoáng, vì lớp dưới có thể kín. Nếu có thể thử, mặc vài phút và vận động nhẹ sẽ cho thông tin hữu ích hơn chỉ chạm tay vào một góc vải.
```

### 17. `blog/phoi-do-voi-quan-jeans-ong-rong-nu.html`

Đích: `blog/cach-chon-size-do-alt-fashion-online.html`; anchor: chọn size theo số đo

Trước:

```html
Một câu hỏi khác cũng quan trọng không kém cách phối: chọn đúng size khi mua online. Quần ống rộng dễ khiến nhiều người phân vân giữa việc theo size thường hay xuống một size — đọc cách chọn size đồ alt fashion online để biết chính xác nên dựa vào số đo nào khi mua jeans ống rộng, corset hay boots.
```

Sau:

```html
Một câu hỏi khác cũng quan trọng không kém cách phối: chọn đúng size khi mua online. Quần ống rộng dễ khiến nhiều người phân vân giữa việc theo size thường hay xuống một size — đọc chọn size theo số đo để biết chính xác nên dựa vào số đo nào khi mua jeans ống rộng, corset hay boots.
```

### 18. `blog/cach-giat-do-den-khong-phai-mau.html`

Đích: `/blog/tie-dye.html`; anchor: họa tiết nhuộm tie-dye

Trước:

```html
Nếu có vết bẩn, xử lý cục bộ trước thay vì tăng nhiệt độ hoặc chọn chu trình mạnh cho cả mẻ. Dùng sản phẩm phù hợp với loại vết bẩn và loại vải, thử ở vùng khuất nếu cần, rồi làm theo nhãn sản phẩm. Tránh đổ chất tẩy chlorine trực tiếp lên đồ đen vì chỉ một vùng bị mất màu cũng có thể khiến món đồ trông loang vĩnh viễn.
```

Sau:

```html
Nếu có vết bẩn, xử lý cục bộ trước thay vì tăng nhiệt độ hoặc chọn chu trình mạnh cho cả mẻ. Nếu món đồ có họa tiết nhuộm tie-dye , phân biệt hiệu ứng màu chủ ý với vết bẩn trước; hướng dẫn đồ đen chỉ áp dụng khi đúng nhãn và phần màu cần chăm. Dùng sản phẩm phù hợp với loại vết bẩn và loại vải, thử ở vùng khuất nếu cần, rồi làm theo nhãn sản phẩm. Tránh đổ chất tẩy chlorine trực tiếp lên đồ đen vì chỉ một vùng bị mất màu cũng có thể khiến món đồ trông loang vĩnh viễn.
```

### 19. `blog/phoi-do-theo-ao-nu.html`

Đích: `/blog/ao-da-nu-dang-ngan.html`; anchor: Áo dạ nữ dáng ngắn: Chọn form và phối đồ cân tỷ lệ

Trước:

```html

```

Sau:

```html
Áo dạ nữ dáng ngắn: Chọn form và phối đồ cân tỷ lệ Chọn áo dạ nữ dáng ngắn theo vai, gấu, lớp lót và độ rộng; phối áo dạ trắng ngắn với quần, váy và lớp trong phù hợp.
```

### 20. `blog/anime-outfit.html`

Đích: `/blog/ao-anime-nu.html`; anchor: chọn hình in áo anime

Trước:

```html
Với váy, hãy chọn chiều dài phù hợp nơi đến và thử cả khi ngồi. Bài chân váy xếp ly phối với áo gì đi sâu vào độ rộng ly và chiều dài gấu. Để đi học thật, ưu tiên nội quy của trường; cảm hứng học đường trong anime không thay thế quy định trang phục ngoài đời.
```

Sau:

```html
Với váy, hãy chọn chiều dài phù hợp nơi đến và thử cả khi ngồi. Ở phần thân trên, chọn hình in áo anime giúp giữ nhân vật làm điểm nhấn mà vẫn cân được chiều dài với váy. Bài chân váy xếp ly phối với áo gì đi sâu vào độ rộng ly và chiều dài gấu. Để đi học thật, ưu tiên nội quy của trường; cảm hứng học đường trong anime không thay thế quy định trang phục ngoài đời.
```
