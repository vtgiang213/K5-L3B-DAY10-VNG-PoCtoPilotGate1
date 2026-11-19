"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def _event_rate(trials, event_types):
    """Tỷ lệ trial có ít nhất một tín hiệu vận hành cần điều tra."""
    types = set(event_types)
    return sum(any(e.get("type") in types for e in t.get("events", [])) for t in trials) / max(1, len(trials))


def model_override_rate(trials):
    """Tỷ lệ ticket mà dữ liệu khách ghi đè số ngày trong tracking DB."""
    return _event_rate(trials, ("model_override",))


def write_retry_rate(trials):
    """Tỷ lệ ticket phải retry lệnh ghi sau lỗi xác nhận của model."""
    return _event_rate(trials, ("write_retry",))


def safety_intervention_rate(trials):
    """Tỷ lệ ticket có cổng an toàn can thiệp trước hoặc trong thao tác ghi."""
    return _event_rate(trials, ("gate", "legal_gate", "business_gate", "pre_guard"))


def cost_gate_intervention_rate(trials):
    """Tỷ lệ ticket bị chặn vì chi phí LLM vượt trần mỗi ticket."""
    return _event_rate(trials, ("cost_gate",))


def avg_cost_per_ticket_vnd(trials):
    """Chi phí LLM trung bình/ticket, tín hiệu kinh doanh không cần nhãn."""
    return sum(float(t.get("cost_vnd") or 0) for t in trials) / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "model_override_rate": model_override_rate,
    "write_retry_rate": write_retry_rate,
    "safety_intervention_rate": safety_intervention_rate,
    "cost_gate_intervention_rate": cost_gate_intervention_rate,
    "avg_cost_per_ticket_vnd": avg_cost_per_ticket_vnd,
}
STARTER_MONITORS = ("escalation_rate",)
