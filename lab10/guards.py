"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    """Ghim phiên bản chính sách theo as_of thay vì tin cờ index_active."""
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.escalate("không có chính sách hiệu lực theo ngày hiện hành")
    return Verdict.allow(policy_id=policy["policy_id"])


def _effective_policy(ctx):
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _strip_pii(value, blocked_fields):
    if isinstance(value, dict):
        return {
            key: _strip_pii(val, blocked_fields)
            for key, val in value.items()
            if key not in blocked_fields
        }
    if isinstance(value, list):
        return [_strip_pii(item, blocked_fields) for item in value]
    return value


def _check_issue_refund(ctx, action):
    ticket = ctx.ticket
    if action.get("ticket_id") != ticket.get("ticket_id"):
        return Verdict.deny("ticket trong lệnh hoàn không khớp ticket gốc")

    order = ctx.tools.lookup_order(action.get("order_id"))
    if order is None or action.get("order_id") != ticket.get("order_id"):
        return Verdict.escalate("đơn trong lệnh hoàn không tìm thấy hoặc không khớp ticket")
    if order.get("customer_id") != ticket.get("customer_id"):
        return Verdict.escalate("ticket không thuộc chủ đơn")

    # S5: hoàn tiền là thao tác không idempotent nếu cùng đơn đã có dòng sổ cái.
    # Chuyển người thay vì ghi thêm khoản hoàn thứ hai (kể cả khi ticket_id khác).
    prior_refunds = ctx.tools.ledger_rows(order_id=order["order_id"])
    if any(int(row.get("amount_vnd") or 0) > 0 for row in prior_refunds):
        ctx.log("duplicate_refund_block", order_id=order["order_id"])
        return Verdict.escalate("đơn đã có khoản hoàn trong sổ cái, cần người đối soát")

    policy = _effective_policy(ctx)
    if policy is None:
        return Verdict.escalate("không có chính sách hiệu lực theo ngày hiện hành")

    amount = int(action.get("amount_vnd") or 0)
    if action.get("payer") != "LOGIX" or action.get("basis") == "fail_open":
        return Verdict.escalate("hoàn tiền ngoài chính sách tự động phải có người duyệt")

    target = H.ticket_parcel(order, ticket, ctx.as_of)
    delay = H.db_delay_days(target, ctx.as_of)
    cause = target.get("delay_cause") or ("CARRIER" if delay > 0 else None)
    expected = H.entitlement_vnd(policy, order, delay, cause)
    if expected <= 0 or amount > expected:
        return Verdict.escalate("số tiền hoàn không khớp quyền lợi tính lại từ tracking DB")

    approval_id = action.get("approval_id")
    if amount > policy["auto_limit_vnd"] or approval_id:
        rows = ctx.tools.lookup_approvals(approval_id=approval_id) if approval_id else []
        approval = rows[0] if rows else None
        if not approval:
            return Verdict.escalate("vượt hạn mức tự động, thiếu phê duyệt hợp lệ")
        if approval.get("status") != "valid" or int(approval.get("max_vnd") or 0) < amount:
            return Verdict.escalate("phê duyệt không hợp lệ hoặc không đủ hạn mức")
        expires_at = approval.get("expires_at")
        if expires_at and expires_at < ctx.as_of:
            return Verdict.escalate("phê duyệt đã hết hạn")
        if approval.get("order_id") and approval["order_id"] != order["order_id"]:
            return Verdict.escalate("phê duyệt không thuộc đơn này")

    limits = ctx.tools.ops_limits()
    cap = ctx.gates.get("business", {}).get("daily_refund_cap_vnd")
    if cap is None:
        cap = limits.get("daily_auto_refund_budget_vnd")
    if cap is not None and ctx.tools.auto_refund_today_vnd() + amount > cap:
        return Verdict.escalate("vượt trần hoàn tự động trong ngày, chuyển người duyệt")

    if amount != expected:
        return Verdict.modify("chuẩn hoá số tiền theo quyền lợi chính sách", amount_vnd=expected)
    return Verdict.allow()


def _check_carrier_fault(ctx, action):
    ticket = ctx.ticket
    order = ctx.tools.lookup_order(action.get("order_id"))
    if order is None or action.get("order_id") != ticket.get("order_id"):
        return Verdict.deny("đơn trong lệnh ghi lỗi hãng không khớp ticket")
    if order.get("customer_id") != ticket.get("customer_id"):
        return Verdict.deny("ticket không thuộc chủ đơn")

    policy = _effective_policy(ctx)
    if policy is None:
        return Verdict.deny("không có chính sách hiệu lực theo ngày hiện hành")

    parcel_id = action.get("parcel_id")
    target = next((p for p in order.get("parcels", []) if p.get("parcel_id") == parcel_id), None)
    if target is None:
        target = H.ticket_parcel(order, ticket, ctx.as_of)
    delay = H.db_delay_days(target, ctx.as_of)
    if delay < policy["late"]["min_days_fee"]:
        return Verdict.deny("tracking DB không xác nhận đơn trễ đủ ngưỡng")
    if target.get("delay_cause") not in policy["fault_causes"]:
        return Verdict.deny("tracking DB không ghi nguyên nhân thuộc lỗi hãng")
    if action.get("carrier_id") != target.get("carrier_id"):
        return Verdict.deny("hãng trong lệnh ghi lỗi không khớp hãng theo tracking DB")

    if action.get("parcel_id") != target.get("parcel_id") or action.get("delay_days") != delay:
        return Verdict.modify(
            "chuẩn hoá lỗi hãng theo kiện và độ trễ trong tracking DB",
            parcel_id=target.get("parcel_id"),
            carrier_id=target.get("carrier_id"),
            delay_days=delay,
        )
    return Verdict.allow()


def _check_notify_carrier(ctx, action):
    ticket = ctx.ticket
    fault_rows = ctx.tools.fault_rows(ticket_id=ticket.get("ticket_id"))
    if not fault_rows:
        return Verdict.deny("không ghi lỗi hãng trước đó thì không gửi thông báo cho hãng")
    if not any(
        row.get("carrier_id") == action.get("carrier_id")
        and row.get("parcel_id") == (action.get("payload") or {}).get("parcel_id")
        for row in fault_rows
    ):
        return Verdict.deny("thông báo hãng không khớp dòng lỗi đã ghi")

    configured = set(ctx.gates.get("legal", {}).get("pii_fields_blocked_to_third_party") or [])
    blocked = configured | {"name", "phone", "email", "street", "address", "recipient_contact", "customer_note"}
    payload = action.get("payload")
    if isinstance(payload, dict):
        clean_payload = _strip_pii(payload, blocked)
        if clean_payload != payload:
            return Verdict.modify("bỏ trường dữ liệu cá nhân trước khi gửi bên thứ ba", payload=clean_payload)
    return Verdict.allow()


def _check_send_reply(ctx, action):
    ticket = ctx.ticket
    if action.get("ticket_id") != ticket.get("ticket_id"):
        return Verdict.deny("ticket trong tin nhắn trả lời không khớp ticket gốc")
    amount = int(action.get("amount_vnd") or 0)
    if amount > 0:
        rows = ctx.tools.ledger_rows(ticket_id=ticket.get("ticket_id"))
        if not any(int(row.get("amount_vnd") or 0) == amount for row in rows):
            return Verdict.deny("không báo đã hoàn tiền khi sổ cái không có dòng khớp")
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    cost_budget = ctx.gates.get("business", {}).get("cost_budget_per_ticket_vnd")
    if cost_budget is None:
        cost_budget = ctx.tools.ops_limits().get("max_llm_cost_per_ticket_vnd")
    if cost_budget is not None and ctx.cost_vnd > cost_budget:
        ctx.log("cost_gate", cost_vnd=ctx.cost_vnd, limit_vnd=cost_budget)
        return Verdict.escalate("chi phí LLM của ticket vượt trần, chuyển người và không ghi tự động")

    checks = {
        "issue_refund": _check_issue_refund,
        "file_carrier_fault": _check_carrier_fault,
        "notify_carrier": _check_notify_carrier,
        "send_reply": _check_send_reply,
    }
    check = checks.get(action.get("tool"))
    return check(ctx, action) if check else Verdict.allow()
