# Pha 1 — Dọn internal link hiện có

Repo: apocalypsecloset/doquochau.github.io. Baseline: `9e16c2012f417cf5e4634b1c771a2c5d773e1ee8`.
Branch: `fix/internal-links-topical-map`. Chưa push hoặc triển khai site.

## Kết quả

264 bài được chỉnh, với 419 đoạn thay thế khớp chính xác và duy nhất. Không định dạng lại HTML. Bỏ 67 lần đặt link trùng, giữ vị trí giải thích phù hợp hơn và giữ nguyên chữ ở vị trí còn lại. Bỏ thêm 6 link ở Baddie Streetwear, đưa số đích blog trong thân bài từ 18 xuống 12. Các anchor quá lặp được thay bằng lựa chọn riêng trong `phase1_choices.py`; các câu dẫn kỹ thuật được sửa theo nội dung từng đoạn.

| Gate | Trước | Sau |
| --- | ---: | ---: |
| G1 link gãy/redirect | 0 | 0 |
| G2 bài thiếu link ra | 10 | 10 |
| G3 bài chưa có link vào | 211 | 211 |
| G4 lỗi liên kết trang tổng quan–bài con | 21 | 21 |
| G5 bài thiếu link ngang | 112 | 112 |
| G6 cặp màu chưa liên kết hai chiều | 7 | 7 |
| G7 câu dẫn chứa thuật ngữ kỹ thuật | 79 | 0 |
| G8 anchor chung chung/rỗng | 2 | 0 |
| G9 cặp bài–đích link trùng | 63 | 0 |
| G10 nhóm anchor lặp quá 5 lần | 59 | 0 |
| G11 bài quá 12 đích blog | 1 | 0 |

Tổng số cặp nguồn–đích blog phân biệt trong nội dung: 2.003 → 1.997. Vẫn có 436 bài thật và 9 redirect. Audit còn 5 gate chưa đạt, thuộc phạm vi các pha sau; đây là hoàn thành Pha 1, chưa phải hoàn thành toàn bộ nhiệm vụ.

## Kiểm tra

- Audit sau mỗi lô khoảng 25 file, có lưu TXT/CSV và `phase1_batches.json`. Không gate nào tăng số lỗi so với lô trước. Lượt cuối kiểm tra thêm việc viết hoa đầu đoạn và chỉnh câu chữ.
- `phase1_verify.py` đối chiếu từng thay thế với Git baseline và xác nhận title, H1, meta, canonical, JSON-LD, ảnh, heading, TOC, ac-reading-path, seo-faq và ac-sources giữ nguyên.
- Kiểm tra khoảng trắng trên HTML và mã Python không phát hiện lỗi. File TXT lưu nguyên output audit có một số khoảng trắng cuối dòng do script cắt câu mẫu ở ký tự thứ 70; giữ nguyên các log này để đối chiếu output.
- Nhật ký trước/sau: `link_changes.csv`; danh sách chuỗi thay thế chính xác: `phase1_patches.json`.
- Chưa thay RULES, chưa tạo trang mới hoặc thực hiện Pha 2–5. Các bài phân cụm sai đã ghi nhận ở Pha 0 vẫn chờ xử lý trong công việc phân cụm tiếp theo.
- Chưa chạy QA toàn site của Pha 5. Repo được clone nông nên commit lịch sử mà `qa_site.py` yêu cầu chưa có trong checkout.

## Chạy lại audit trên máy này

Thư viện được cài trong `tools/.python-deps`, không đưa vào Git. PowerShell, tại gốc repo:

```powershell
$env:PYTHONPATH = Join-Path (Get-Location) 'tools/.python-deps'
$env:PYTHONIOENCODING = 'utf-8'
python tools/internal_link_audit.py --root . --csv tools/audit_phase1_after.csv
```

Audit trả exit code 1 vì G2–G6 vẫn FAIL đúng baseline. Công cụ áp thay thế là script chạy một lần trên baseline; không chạy lại `phase1_apply.py` lên nội dung đã sửa.
