# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** ______ · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Giúp LogiX-VN tự động hóa quy trình xử lý yêu cầu hoàn tiền do giao hàng trễ và đảm bảo: xử lý đúng quy trình, đúng thẩm quyền, không gây thất thoát hay rò rỉ dữ liệu. 

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): …
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): …

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | | |
| **Thước đo** (một câu, có đơn vị) | | |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | | |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | | |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | | |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của suite base. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(c)**

Giải thích một câu: Kết quả Y đạt 50/50 vẫn nằm trong khoảng tin cậy của 95% [0,9400; 1,0] và điều này cũng không chứng minh hai bản chắc chắn giống nhau.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu `pass_rate` trên `base suite` hoặc `incident suite` dưới 90% (0.90), chúng tôi sẽ không chọn Tiếp tục và sẽ Cải tiến thêm trong 3 ngày. Nếu sau đó vẫn chưa đạt, nhóm sẽ xem xét Thu hẹp vào phạm vi có bằng chứng đạt và đáp ứng các điều kiện an toàn. | Nếu `pass_rate` trên `base suite` hoặc `incident suite` dưới 95% (0.95), chúng tôi sẽ không chọn Tiếp tục và sẽ Cải tiến thêm trong 3 ngày. Sau đó nhóm đánh giá lại; nếu vẫn chưa đạt, nhóm xem xét Thu hẹp vào phạm vi có bằng chứng đạt và đáp ứng các điều kiện an toàn. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu `pass_k` trên `base suite` hoặc `incident suite` dưới 85% (0.85), chúng tôi sẽ không chọn Tiếp tục; nhóm sẽ phân tích các ticket không đạt đủ 5/5 lượt và Cải tiến thêm. Nhóm chỉ xem xét Thu hẹp khi phạm vi giữ lại có bằng chứng đạt và các chỉ số an toàn đạt. | Nếu `pass_k` trên `base suite` hoặc `incident suite` dưới 90% (0.90), chúng tôi sẽ không chọn Tiếp tục. Nhóm sẽ phân tích các ticket không đạt đủ 5/5 lượt, Cải tiến thêm và đánh giá lại sau 3 ngày. Nếu vẫn chưa đạt, nhóm xem xét Thu hẹp khi phạm vi giữ lại có bằng chứng đạt và các chỉ số an toàn đạt. |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn oan vượt quá 0 VNĐ, chúng tôi sẽ tắt ngay quyền tự ghi ledger (`issue_refund`) và chuyển toàn bộ các ca hoàn tiền sang cho chị Hạnh duyệt tay. | Không đề xuất ngưỡng khác vì nhóm chọn không chấp nhận hoàn tiền sai. |
| `wrongful_carrier_faults_max` | Nếu số lần ghi lỗi oan cho hãng trên bộ đánh giá vượt quá 0, chúng tôi sẽ không chọn Tiếp tục, tắt file_carrier_fault và chuyển các ca ghi lỗi cho chị Hạnh hoặc người có thẩm quyền được phân công. Nhóm sẽ tìm nguyên nhân, sửa và đánh giá lại trước khi bật lại. | Không đề xuất ngưỡng khác vì nhóm chọn không chấp nhận ghi lỗi oan cho hãng. |
| `pii_leaks_max` | Nếu số ca rò rỉ dữ liệu cá nhân (tên, SĐT, địa chỉ) gửi sang hãng vận chuyển vượt quá 0 ca, chúng tôi sẽ chặn toàn bộ gói tin gửi qua bên thứ ba và tiến hành kiểm tra bảo mật. | Không có vì vi phạm bảo vệ dữ liệu cá nhân là lỗi nghiêm trọng. |
| nên có: `escalation_rate_max` | Nếu escalation_rate trên base suite hoặc incident suite vượt 25% (0,25), chúng tôi sẽ phân tích nguyên nhân và xem thêm thời gian chờ, số ca ùn và chi phí. Nhóm sẽ cải tiến các bước gây chuyển duyệt không cần thiết, nhưng vẫn chuyển người những ca cần kiểm tra an toàn. | Nếu escalation_rate vượt 30% (0,30) và dự báo hàng chờ vượt năng lực, nhóm sẽ xem xét bổ sung một người trực hoặc Thu hẹp phạm vi pilot; sau đó đánh giá lại chi phí và ROI. |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Không tự động hoàn tiền nếu chưa đối chiếu được đơn hàng, thông tin giao hàng và chính sách áp dụng để xác định quyền lợi.
- Ngưỡng chuyển cho người duyệt: Nếu khoản hoàn được đệ xuất quá 236000 đồng, trợ lý phải chuyển cho con người duyệt trước khi thực hiện hoàn tiện.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? |    |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` ____ · `roi_min` ____ · `queue_stuck_max` ____
- Ngày xem lại tiêu chí: `__________` · Ai dự: `__________` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên suite base hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
