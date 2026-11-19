# incidents/ · Gói sự cố (chưa có gì ở đây cho tới phút 125)

Thư mục này cố ý để trống lúc đầu buổi. Đây là chỗ **gói sự cố của bàn** sẽ xuất hiện.

**Phút 125**, sau giờ nghỉ, Lab Coach báo **số thẻ của bàn** (S1–S8) và mở repo thẻ (chuyển sang công khai). Không cần tài khoản GitHub, lời mời hay gắn remote nào.

1. Từ thư mục gốc repo của bàn (nhánh `main`, đã commit hết), chạy lần lượt ba lệnh sau, gõ từng dòng. Thay `Sx` bằng số thẻ của bàn (cả hai chỗ):

   ```bash
   git fetch https://github.com/VinUni-AI20k/K5_L3_Day10_PoC-to-Pilot_Gate1_cards.git main
   git checkout FETCH_HEAD -- incidents/Sx
   git commit -m "Nhận thẻ Sx"
   ```

   `git fetch` tải repo thẻ về theo URL (không cần gắn remote, chưa đổi gì trong bài); `git checkout FETCH_HEAD -- incidents/Sx` chép **đúng thư mục thẻ của bàn**; `git commit` lưu lại. Lệnh không gộp lịch sử git, không đụng bài của bàn. Rồi `git push -u origin main` để các bạn khác trong bàn `git pull` về.

   Báo `Repository not found`, `Authentication failed` hoặc hỏi mật khẩu: repo thẻ chưa được mở (chưa tới phút 125) hoặc gõ sai URL. Không cần đăng nhập: bấm Ctrl+C, chờ Lab Coach báo rồi chạy lại. Nếu máy báo `Please tell me who you are`, làm bước 2a ở mục 2 của `README.md` rồi chạy lại. Máy không chạy được git: lấy thẻ bằng trình duyệt (FAQ trong `docs/guide.md`).

2. Bạn sẽ thấy thư mục mới `incidents/Sx/`.
3. Bàn **chỉ làm đúng thẻ của bàn**. Mở `incidents/Sx/card.md` và đọc mặt trước.
4. Ghi số thẻ vào dòng `Thẻ đã bốc:` ở đầu Phiếu C (`templates/form-c-incident.md`).
5. Chạy ngay `python3 -m lab10.grade --incident Sx`, khi chưa sửa gì, để xem cổng bàn dựng ở vòng 1 đỡ được bao nhiêu. Lấy thẻ đúng thì report có `1 integrity | ✅`.

Mỗi thư mục `incidents/Sx/` có:

| File | Nó là gì |
|---|---|
| `card.md` | Thẻ sự cố: mặt trước là tin nhắn báo sự cố, mặt sau là nhiệm vụ và luật |
| `tickets.jsonl` | Các ticket của sự cố, kèm kết quả đúng |
| `world_patch.json` | Dữ liệu bổ sung của sự cố (đơn hàng, phê duyệt, sổ cái có sẵn…) |
| `card.json` | Hai lệnh chạy và tự kiểm tra của thẻ |

Không sửa các file này: chúng bị khoá, lệnh tự kiểm tra sẽ phát hiện.

Nếu chạy lệnh tự kiểm tra (`python3 -m lab10.grade`) trước khi nhận thẻ, bạn sẽ thấy dòng `TỪ CHỐI KIỂM TRA: chưa có gói sự cố …`. Đó là đúng thiết kế, không phải lỗi máy.
