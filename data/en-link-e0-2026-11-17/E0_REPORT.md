# E0 — Baseline EN và chẩn đoán khóa bảo toàn

Ngày 17/11/2026. Repo `apocalypsecloset/doquochau.github.io`, branch `master`, commit `6d8a9c4f13b59bc12e0db087a2779fbcfa2480db`. Đối chiếu trước sửa VI: `9e16c20`.

**Chỉ hoàn tất E0. Chưa làm E1–E4, chưa re-baseline, chưa sửa nội dung EN/VI, manifest, TSV hay script QA hiện hữu. Chưa commit/push công việc EN.**

## Phạm vi đã thực hiện

- Chép nguyên hai file người dùng cung cấp vào `scripts/internal_link_audit_en.py` và `docs/CODEX_TASK_EN.md`.
- Audit VI vẫn chạy từ `tools/internal_link_audit.py`: chưa chuyển đường dẫn vì dọn thư mục thuộc E1.
- Tải đủ lịch sử Git bằng `git fetch --unshallow origin master`, để các QA đọc được commit khóa lịch sử như CI.
- Chạy và lưu riêng stdout/stderr của 48 lệnh Python: hai audit, bảy QA chung, 37 batch translation (bỏ batch05b), hai lần gọi trực tiếp hub gate. Batch37 hỗn hợp tự chạy cả article và hub gate; gọi hub riêng với `--hubs-only` để không bỏ sót.
- Chạy đúng ba file test Node của CI, với jsdom 31.0.0 cài trong thư mục tạm ngoài repo.
- Snapshot xác nhận **2.014 file đã được Git theo dõi không thay đổi byte nào** trong E0 (`tracked_preservation.json`). Hai file đầu vào và báo cáo là file mới, không nằm trong snapshot đó.

Môi trường cục bộ: Windows, Python 3.14, Node 24; Python chạy `-X utf8` và dùng dependencies hiện có. CI dùng Python 3.12/Node 24. Không sửa encoding trong script QA để vượt lỗi.

## Audit VI và EN

VI: **ĐẠT TẤT CẢ, 11/11 gate PASS**, 440 trang thật, bỏ qua 9 redirect stub.

EN: **425 bài + 13 hub**, ghép được 436 cặp VI↔EN. Link tới bài EN khác/bài: min 0, trung bình 4,5, max 13. Script trả exit 1: **11/14 gate FAIL**, không phải 12.

| Gate | Kết quả | Số mục lỗi do script báo |
|---|---|---:|
| E1 link gãy | PASS | 0 |
| E2 dưới 2 link EN ngữ cảnh | FAIL | 9 bài |
| E3 thiếu link ngữ cảnh vào | FAIL | 211 bài |
| E4 cha/con chưa đủ | FAIL | 21 mục chẩn đoán, không phải 21 file |
| E5 thiếu link ngang cùng cụm | FAIL | 171 bài |
| E6 dưới 80% parity link với VI | FAIL | 126 bài |
| E7 EN trỏ VI có bản EN | FAIL | 4 lần xuất hiện; xem ngoại lệ bên dưới |
| E8 anchor có tiếng Việt | FAIL | 1 lần xuất hiện; xem ngoại lệ bên dưới |
| E9 chữ hub/pillar/cornerstone… | FAIL | 35 lần xuất hiện |
| E10 anchor generic/rỗng | PASS | 0 |
| E11 trùng đích trong bài | FAIL | 90 cặp bài–đích |
| E12 một anchor dùng trên 5 lần/đích | FAIL | 52 nhóm anchor–đích |
| E13 quá 12 đích EN | FAIL | 1 bài (`what-is-goth-style`) |
| E14 thiếu ghép cặp VI ngoài hai bài EN gốc | PASS | 0 |

Các nhóm lặp nhiều gồm “online sizing guide” ×26, “aesthetic dictionary” ×19, “layering outfits for women” ×16. Số mục của các gate khác nhau không được cộng thành số file cần sửa.

### Điểm cần duyệt trong chính thước đo EN

1. **E7 đang đếm nhầm bốn link về chính bản VI nguồn**, không phải link tài liệu khác bị bỏ quên bản dịch:
   - Corporate Goth: “VIETNAMESE GUIDE” trong article-meta và “original Corporate Goth article” sau “Prefer Vietnamese?”.
   - Soft Goth: “VIETNAMESE STYLE GUIDE” trong article-meta và nhan đề VI sau “Read in Vietnamese:”.
   - Cả bốn có `lang="vi"`; hai link chuyển ngôn ngữ trong đoạn còn có `hreflang="vi"`. Tài liệu refresh trước đây yêu cầu giữ nguyên các original-language switch này. Không nên đổi chúng thành self-link EN.
2. **E8 duy nhất** là “Soft Goth Là Gì? Cách Phối Goth Mềm Hơn” trong chính nút “Read in Vietnamese:”. Đây là nhãn của bản VI gốc, không phải một anchor tư vấn thời trang EN bị dịch sót. Đề xuất ngoại lệ hẹp cho link tới đúng counterpart VI và được đánh dấu ngôn ngữ/chuyển bản gốc; vẫn kiểm tra toàn bộ anchor nội dung EN còn lại.
3. RULES EN chưa có 15 điều chỉnh phân cụm đã duyệt ở VI. Ví dụ `ao-ba-lo-nu` đang thành Phụ kiện, `da-ngam-mac-mau-gi` thành Vải. Đủ 15 dòng đối chiếu trong `cluster_differences.json`.
4. `VI_HUBS` EN thiếu cả khai báo `Outfit-core: phoi-do-theo-item`, dù counterpart `womens-item-styling-guides` đã tồn tại; ngoài bốn hub mới chưa có EN. Cần đồng bộ mapping/cluster đúng nguồn VI trong pha được duyệt, không tạo thêm một hub Outfit-core.
5. E6 hiện dùng link ở bất kỳ vị trí nào trong trang EN (`en_any`), không chỉ link ngữ cảnh, và ngưỡng 80%. E3 của nhiệm vụ yêu cầu phản chiếu mọi link đủ điều kiện, nên PASS E6 chưa tự chứng minh đã làm đủ E3. Script hiện cũng không có gate cặp áo/quần cùng màu riêng; các cặp đó cần kiểm tra bổ sung theo yêu cầu E3.

**E0 giữ nguyên script đầu vào và giữ nguyên các số đo FAIL ở trên; chưa áp dụng ngoại lệ hay sửa RULES.**

## QA chung và CI: đỏ ở đâu

| Kiểm tra | Kết quả thực chạy | Nguyên nhân/số lượng |
|---|---|---|
| `qa_privacy_policies` | FAIL, exit 1 | 854 thông báo trên 427 file: 427 `reviewed bytes changed` + 427 `change beyond exact consent migration` |
| `qa_schema_pod_performance` | FAIL, exit 1 | 852 thông báo: 427 `reviewed HTML changed` + 425 `main visible text preserved` |
| `qa_blog_repair` | FAIL, exit 1 | 650 thông báo trên 216 file: mỗi file lệch exact release hashes/deterministic scoped edits/historical predecessor; thêm 2 so sánh ảnh ở các trang đã thêm card |
| `qa_storefront_ux` | ERROR, exit 1 | Dừng vì `blog/cach-cham-soc-do-nu.html` chưa tồn tại trong baseline `9c6ab137…`; chưa xuất JSON tổng kết |
| `qa_site` | **PASS, exit 0** | 1.054 HTML, 1.039 URL sitemap, 218 cặp song ngữ gốc+mở rộng, 438 thẻ English Journal; metadata 605 trang lịch sử giữ nguyên |
| `qa_audit_followup` | ERROR, exit 1 | Dừng khi tìm cùng hub mới trong baseline `490cb5f`; chưa xuất JSON tổng kết |
| `qa_r2_image_seo` | FAIL, exit 1 | Hai trang VI thiếu ảnh card trong image sitemap: `cac-loai-vai` và `cach-chon-kinh-phu-hop-voi-khuon-mat-nu` |
| 37 `qa_en_translations <batch>` | **37/37 FAIL** | Tất cả lệch inventory VI sitemap do 4 URL mới; 36 batch có ít nhất một source hash lệch; còn parity cascade bên dưới |
| `qa_en_hubs batch24` | FAIL | 51 thông báo; source hash, parity card/nội dung/ảnh và inventory |
| `qa_en_hubs batch37 --hubs-only` | FAIL | 20 thông báo; source hash, parity card/nội dung/ảnh và inventory |
| Node shop/journal/privacy | **18 PASS, 1 FAIL** | `scripts/test_journal.cjs:35`: actual 427, expected 423; chính là bốn thẻ hub VI mới |

427 file ở consent bao gồm 426 file `blog/*.html` được chỉnh trong đợt VI và `blog.html`. Không có dấu hiệu E0 thay các file này: snapshot trước/sau E0 bằng nhau.

Hai image-sitemap gap là vấn đề đồng bộ cần sửa thật sau khi được duyệt, không nên bỏ gate hoặc chỉ cập nhật hash. `image_sitemap_gaps.json` có đủ URL ảnh: hub Vải thiếu 15 URL, hub Kính thiếu 4 URL.

Hai QA bị exception **không được tính là đã chạy xong mọi assertion**. Phải xử lý rõ các trang mới không có trong baseline rồi chạy lại toàn bộ, không được gọi exception này là PASS.

GitHub tại commit merge `6d8a9c4` cũng xác nhận `static-and-shop` FAIL; build/deploy/report-build-status và Cloudflare Pages SUCCESS; Workers Builds FAIL. Workers đã FAIL cả ở master trước sửa VI. Chi tiết và URL job trong `github_checks.json`. Local Node run tái hiện đúng lỗi số thẻ bài. Chưa đọc được log nội bộ Cloudflare Workers để kết luận nguyên nhân.

## `source_sha256`: đo chính xác

- 37 manifest đang được CI dùng, bỏ `batch05b`: **215 entry / 215 nguồn VI duy nhất**, gồm 202 article + 13 hub. Không phải mọi trang VI/EN đều nằm trong batch manifest kiểu này.
- **210/215** nguồn lệch `source_sha256`, trải trên **36/37 batch**.
- Áp dụng đúng chuỗi `privacy_release.original` (có blog-repair predecessor) và loại marker `AC-EN-BATCH` như generator; so với bản `9e16c20`, **0 hash lệch trước đợt sửa VI**. 210 nguồn vừa đổi chính là 210 khóa hiện lệch.
- Năm nguồn còn khớp: `dark-academia-la-gi-phoi-do-badgirl`, `phong-cach-egirl-la-gi`, `minimalist-style-la-gi`, `classic-style-la-gi`, `mcbling`.
- `source_hash_locks.csv`/`.json`: từng batch, VI/EN slug, expected hash, actual hash, hash trước sửa VI và trạng thái; `source_hash_summary.json`: tổng hợp theo batch.

Không dùng SHA-256 trực tiếp của file trên đĩa để thay `source_sha256`: khóa nguồn được tính sau các bước chuẩn hóa lịch sử nêu trên, không phải chỉ hash file có CRLF.

Ngoài hash, gate còn báo parity ở Capsule Wardrobe (batch17), bảy hub đã tăng card (batch24/37), Avant Garde (batch31), Solarpunk/White on White (batch39). Một phần là **cascade do chuỗi predecessor chỉ chấp nhận hash khớp chính xác**: EN vẫn được khôi phục về contract cũ, còn VI có byte mới nên không nhận normalization. Không được thêm lại FAQ/caption cũ hay xóa card mới chỉ để khớp số đếm. Phải phân biệt contract lịch sử với parity của nội dung hiện tại.

## Bốn hub EN đề xuất — chưa tạo

| Cụm | Hub VI hiện có | EN slug đề xuất | Intent riêng |
|---|---|---|---|
| Phối màu | `phoi-mau-quan-ao-nu` | `womens-color-coordination-guides` | Chọn bảng màu trang phục, tương phản và kết hợp áo/quần; điều hướng 41 bài con VI đã có EN, không trùng bài bánh xe màu hay một màu cụ thể |
| Địa điểm/dịp | `chon-trang-phuc-nu-theo-dia-diem-va-dip` | `occasion-destination-outfit-guides` | Chọn trang phục theo dịp, thời tiết và hoạt động tại điểm đến; điều hướng 23 bài con, khác công thức outfit cho riêng một nơi |
| Chăm sóc | `cach-cham-soc-do-nu` | `womens-clothing-care-guide` | Điều hướng chăm sóc theo nhãn, vật liệu và thao tác bảo quản; 11 bài con, không thay hướng dẫn giặt/gấp một món cụ thể |
| Tóc & làm đẹp | `chon-toc-va-makeup-theo-trang-phuc` | `hair-makeup-outfit-coordination` | Chọn tóc, makeup và nail theo neckline, tỷ lệ, chất liệu và độ nổi bật của outfit; 9 bài con, khác bài riêng về một kiểu tóc/makeup |

Đã kiểm tra bốn slug đề xuất chưa có trong EN/sitemap. Số bài con lấy từ cụm VI hiện đã sửa, không từ RULES EN còn lệch.

**`batch39.json` đã có Solarpunk + White on White. Đề xuất dùng `batch40` (hiện chưa có), không ghi đè batch39.** Chưa đổi slug EN cũ, redirect hay hreflang.

## Đề xuất phương án cần duyệt trước khi tiếp tục

Đề xuất theo cơ chế exact reviewed successor đã được repo dùng tại `docs/blog-repair-2026-11-17/README.md`, `docs/privacy-pod-2026-11-16/README.md`, `docs/schema-pod-performance-2026-11-15/README.md`; nguồn hash trước/sau có tiền lệ tại `docs/audit-followup-2026-11-15/source-hashes.json` và README cùng thư mục.

1. **Lập release manifest mới, không ghi đè lịch sử:** khóa commit `9e16c20` → `6d8a9c4`, đường dẫn và before/after SHA cùng danh sách thay thế đã duyệt từ các pha VI. Đặt bằng chứng mới trong `data/…` hoặc tài liệu mới; giữ nguyên `docs/qa/*` và các manifest review cũ. Gate mới kiểm tra byte thực tế, phạm vi sửa, metadata/ảnh/FAQ, và bác bỏ successor khác dù chỉ thêm một ký tự.
2. **Ưu tiên lớp predecessor hẹp cho QA lịch sử**, chỉ nhận đúng hash successor đã duyệt rồi phục hồi contract trước đó. Cách này theo mô hình repo đã có và giữ nguyên 215 `source_sha256` lịch sử. QA hiện tại vẫn phải độc lập kiểm tra link/EN/card/sitemap thực tế; không normalize rộng mọi thay đổi thân bài. Chỉ thay các entrypoint bảo toàn/QA được duyệt cần thiết, không tắt assertion.
3. Nếu muốn **re-baseline trực tiếp 210 `source_sha256`** thay vì predecessor, cần duyệt riêng đúng danh sách CSV. Cập nhật khóa phải đi cùng trích xuất lại và remap TSV theo nội dung nguồn, đồng bộ bản EN/FAQ/ItemList rồi chạy parity. Chỉ thay hash mà giữ chỉ số TSV cũ có thể ghép sai câu; E0 không đề xuất làm như vậy.
4. Cho QA biết bốn hub là trang mới có contract mới, không cố đọc chúng từ Git baseline chưa có. Mở rộng publication/inventory có whitelist đúng bốn cặp mới; giữ hợp đồng gốc 216/218 riêng. Sửa test journal để bảo toàn toàn bộ 423 thẻ/chữ tìm kiếm gốc và cho phép đúng bốn thẻ mới, thay vì bỏ kiểm tra hoặc chỉ đổi con số thành bất kỳ số mới.
5. Sửa đồng bộ image sitemap thật cho hai hub Vải/Kính và kiểm tra các ảnh card tương ứng. Đây là hạng mục riêng ngoài re-baseline hash, cần bao gồm trong phạm vi duyệt vì sitemap là file sản phẩm.
6. Duyệt các sửa thước đo hẹp đã nêu (original-language switch E7/E8, 15 cluster, Outfit-core), giữ số baseline gốc để so sánh, rồi mới thực hiện E1 dọn thư mục, E2 hub mới bằng batch40 và E3–E4 nội dung EN.

Những việc trên là **đề xuất**, chưa thực hiện. **Dừng tại E0, chờ người dùng duyệt phương án re-baseline/phạm vi QA trước khi làm các pha tiếp theo.**

## File bằng chứng

- `../audit_en_before.csv`: baseline EN theo từng bài; `audit_en.stdout.txt`/`audit_vi.stdout.txt`: output gốc.
- `qa_results.json`: command, exit code, thời gian và JSON output của đủ 48 lệnh Python; `*.stdout.txt`/`*.stderr.txt`: output đầy đủ, kể cả exception.
- `node_tests.txt`, `node_tests.stderr.txt`: 19 test Node.
- `source_hash_locks.csv`, `source_hash_locks.json`, `source_hash_summary.json`: đối chiếu khóa nguồn.
- `cluster_differences.json`, `image_sitemap_gaps.json`, `github_checks.json`: các phát hiện bổ sung.
- `tracked_before.json`, `tracked_preservation.json`: xác nhận không sửa các file đang được Git theo dõi.
