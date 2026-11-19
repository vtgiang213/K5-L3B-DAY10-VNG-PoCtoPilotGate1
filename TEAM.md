# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `VNG`
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-VNG-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S5`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Vương Trường Giang | 2A202603834 | Sản phẩm và kinh doanh | x |
|   2 | Đinh Quốc Việt | 2A202603885 | Kỹ sư cổng |   |
|   3 | Lê Sỹ Long Nhật | 2A202603881 | Vận hành và pháp lý |   |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Phân công và cách phối hợp

- **Vương Trường Giang (trưởng nhóm):** tiêu chí chấp nhận, chi phí/ROI, phạm vi pilot và quyết định Gate 1.
- **Đinh Quốc Việt:** trace, guard trước khi đọc/ghi, monitor và kiểm regression.
- **Lê Sỹ Long Nhật:** PIC/người duyệt, pháp lý dữ liệu, HAZOP, checklist, runbook và hồ sơ nộp.
- Cả nhóm đối chiếu bằng chứng trước mỗi mốc: `base` → `prepared` → `after`; Lê Sỹ Long Nhật gom hồ sơ sau khi Phiếu C và `submission.json` đã khớp.

## Khai báo sử dụng AI

Nhóm có sử dụng trợ lý AI để đọc cấu trúc repo, rà soát câu chữ Markdown và gợi ý kiểm tra. Nhóm tự quyết định ngưỡng, nội dung hồ sơ, thay đổi code/config và trực tiếp chạy test, grade, check submission; không dùng AI để viết xử lý riêng theo mã ticket.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## VuongTruongGiang-2A202603834

### Phần việc phụ trách

Sản phẩm và kinh doanh; Phiếu A A1–A5, Phiếu B B7.4/B8; `config/acceptance_criteria.json` và `submission/submission.json`.

### Đóng góp cụ thể

Đặt tiêu chí trước khi chạy, ký tiêu chí, đọc chi phí/ROI, xác định phạm vi pilot và chốt v1/v2.

### Bằng chứng

Commit `cd7da3c`, `338e2b7`, `9cbe10a`; mốc sau cùng `R-S5-grade-20261119-171844-162450`; Phiếu A A4–A5, B8, C12.

### Exit ticket

Học được rằng ROI phải đọc theo phân khúc và công người duyệt, không chỉ nhìn pass rate. Còn phải đo economics bằng dữ liệu production trước Gate 2.

## DinhQuocViet-2A202603885

### Phần việc phụ trách

Kỹ sư cổng; trace, cổng trong `lab10/guards.py`, monitor trong `lab10/monitors.py`, eval/grade/regression.

### Đóng góp cụ thể

Giữ cổng tracking/PII, thêm chặn hoàn lặp theo `order_id`, chặn ticket vượt trần LLM 1.500đ và thêm `avg_cost_per_ticket_vnd`.

### Bằng chứng

Commit `23ad675`, `0544afa`; các mốc `R-S5-before-20261119-171845-162450`, `R-S5-after-20261119-171845-162450`; Phiếu C C7–C9.

### Exit ticket

Học được rằng cổng phải nằm trước lệnh ghi và phải kiểm regression. Còn phải kiểm chứng cost gate với ticket dài mới trong hidden test và production.

## LeSyLongNhat-2A202603881

### Phần việc phụ trách

Vận hành và pháp lý; Phiếu A A1/A2, Phiếu B B4–B7.6, Phiếu C C1–C12; `config/operating_gates.json`, runbook và `submission/`.

### Đóng góp cụ thể

Đặt PIC/người duyệt/SLA, cổng PII và nguyên nhân lỗi hãng; lập HAZOP, checklist 9 nhóm, runbook, risk register và gom bài.

### Bằng chứng

Commit `0544afa`, `cb96bbc`, `9cbe10a`; checkpoint `27cb570c`; grade `R-S5-grade-20261119-171844-162450`; Phiếu B B4–B7.6, Phiếu C C2–C12; `submission/manifest.json`.

### Exit ticket

Học được rằng tác hại kinh doanh có thể đến từ phạm vi và hàng chờ chứ không chỉ từ model. Còn phải đo cost, ticket lặp và ROI theo kho trong pilot thật.
