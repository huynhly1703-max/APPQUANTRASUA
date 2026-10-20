import random
from datetime import datetime
from html import escape
from urllib.parse import quote

import streamlit as st

st.set_page_config(page_title="Trà Quán Hoài Niệm", page_icon="🍵", layout="wide")

MENU = {
    "🧋 Trà sữa": {
        "Trà sữa truyền thống": 30000,
        "Trà sữa ô long": 35000,
        "Trà sữa khoai môn": 35000,
        "Trà sữa socola": 35000,
        "Sữa tươi trân châu đường đen": 40000,
    },
    "🍵 Matcha": {
        "Matcha latte": 38000,
        "Matcha sữa dừa": 42000,
        "Matcha đậu đỏ": 45000,
        "Matcha kem cheese": 45000,
    },
    "🍑 Trà trái cây": {
        "Trà đào cam sả": 32000,
        "Trà tắc mật ong": 25000,
        "Hồng trà vải": 32000,
        "Trà dâu tây": 35000,
        "Trà chanh dây": 30000,
    },
}
TOPPINGS = {
    "Không topping": 0, "Trân châu đen": 5000, "Trân châu trắng": 7000,
    "Thạch cà phê": 5000, "Pudding trứng": 7000, "Thạch trái cây": 6000,
    "Kem cheese": 10000, "Đậu đỏ": 7000,
}
SWEETNESS = ["0% - Không đường", "30%", "50%", "70%", "100%"]
ICE = ["Có đá bình thường", "Ít đá", "Không đá"]
VOUCHERS = {
    "HOAINIEM10": ("percent", 10, 50000, "Giảm 10% cho đơn từ 50.000đ"),
    "TRAXUA15": ("percent", 15, 100000, "Giảm 15% cho đơn từ 100.000đ"),
    "GIAM20000": ("amount", 20000, 150000, "Giảm 20.000đ cho đơn từ 150.000đ"),
}
PRIZES = [
    {"name": "Giảm 5% đơn hàng", "kind": "percent", "value": 5},
    {"name": "Giảm 10% đơn hàng", "kind": "percent", "value": 10},
    {"name": "Tặng topping miễn phí", "kind": "topping", "value": 0},
    {"name": "Tặng một món quà nhỏ", "kind": "gift", "value": 0},
    {"name": "Chúc bạn một ngày an yên 🌸", "kind": "none", "value": 0},
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
.stApp{background:radial-gradient(ellipse at top left,rgba(194,154,85,.16),transparent 38%),#f3ead8;color:#38271d;font-family:'Be Vietnam Pro',sans-serif}
[data-testid="stHeader"]{background:rgba(243,234,216,.92)}
.block-container{max-width:1320px;padding-top:1.4rem;padding-bottom:3rem}
.hero{padding:2rem 1.5rem;border:2px solid #68432e;outline:1px solid #c29a55;outline-offset:-9px;border-radius:8px;text-align:center;color:#fff7e8;background:linear-gradient(135deg,#493023,#74452e 65%,#8f3028);box-shadow:0 8px 24px #38271d24;margin-bottom:1.35rem}
.hero .eyebrow{letter-spacing:.22em;font-size:.75rem;text-transform:uppercase;color:#e7c991}
.hero h1{font-family:'Playfair Display',serif;font-size:clamp(2rem,4vw,3.1rem);margin:.35rem 0;color:#fff7e8}
.hero p{margin:0;color:#f2dfbf}
.section-title{font-family:'Playfair Display',serif;color:#68432e;font-size:1.55rem;padding-bottom:.45rem;border-bottom:1px solid #c9ac7b;margin:.3rem 0 1rem}
.menu-card{background:#fffaf0;border:1px solid #dfcba8;border-radius:10px;padding:.8rem 1rem;margin:.6rem 0 .35rem;box-shadow:0 3px 9px #38271d0b}
.menu-name{font-weight:700;color:#493023;font-size:1rem}.menu-price{color:#8f3028;font-weight:800}
.bill{background:#fffaf0;color:#38271d;border:1px solid #c9ac7b;border-radius:4px;padding:1.2rem;box-shadow:0 6px 20px #38271d14}
.bill-head{text-align:center;border-bottom:1px dashed #b69a70;padding-bottom:.9rem;margin-bottom:.8rem}
.bill-head h2{font-family:'Playfair Display',serif;margin:.2rem 0;color:#68432e}
.bill-row{display:flex;justify-content:space-between;gap:.8rem;padding:.6rem 0;border-bottom:1px dotted #dfcba8}
.bill-sub{color:#826e5b;font-size:.8rem;margin-top:.15rem}
.bill-total{display:flex;justify-content:space-between;font-weight:800;font-size:1.18rem;color:#8f3028;border-top:2px solid #68432e;padding-top:.9rem;margin-top:.9rem}
.stButton>button{border-radius:7px;border:1px solid #68432e;font-weight:700}
.stButton>button[kind="primary"]{background:#8f3028;color:#fffaf0;border:1px solid #8f3028}
footer{visibility:hidden}
</style>
<div class="hero"><div class="eyebrow">Hương vị thân quen · Phong vị ngày xưa</div>
<h1>🍵 Trà Quán Hoài Niệm</h1><p>Một chút vị trà · Một chút ký ức · Một ngày an yên</p></div>
""", unsafe_allow_html=True)

def money(n):
    return f"{int(round(n)):,}".replace(",", ".") + "đ"

def subtotal_for(items):
    return sum((x["price"] + x["topping_price"]) * x["quantity"] for x in items)

def get_voucher_discount(subtotal, code):
    v = VOUCHERS.get(code.strip().upper())
    if not v:
        return 0, "Mã voucher không hợp lệ."
    kind, value, minimum, label = v
    if subtotal < minimum:
        return 0, f"Mã này áp dụng cho đơn từ {money(minimum)}."
    discount = int(subtotal * value / 100) if kind == "percent" else value
    return min(discount, subtotal), f"Áp dụng thành công: {label}."

def prize_discount(subtotal, prize):
    return int(subtotal * prize["value"] / 100) if prize and prize["kind"] == "percent" else 0

def reset_order():
    st.session_state.cart = []
    st.session_state.order_number += 1
    st.session_state.voucher_code = ""
    st.session_state.voucher_applied = False
    st.session_state.voucher_message = ""
    st.session_state.prize = None
    st.session_state.spin_used = False
    st.session_state.customer_name = ""
    st.session_state.payment_method = "Tiền mặt"
    for k in list(st.session_state.keys()):
        if k.startswith(("qty_", "top_", "sweet_", "ice_")):
            del st.session_state[k]

for k, v in {
    "cart": [], "order_number": 1, "voucher_code": "", "voucher_applied": False,
    "voucher_message": "", "prize": None, "spin_used": False,
    "customer_name": "", "payment_method": "Tiền mặt",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

with st.sidebar:
    st.markdown("## 🧾 Thông tin đơn")
    st.text_input("Tên khách hàng (không bắt buộc)", key="customer_name")
    st.radio("Hình thức thanh toán", ["Tiền mặt", "Quét mã QR"], key="payment_method")
    st.caption(f"Mã đơn: HQN-{datetime.now():%y%m%d}-{st.session_state.order_number:03d}")
    st.divider()
    st.markdown("### 🎟️ Mã voucher")
    st.markdown("- `HOAINIEM10`: giảm 10% từ 50.000đ\n- `TRAXUA15`: giảm 15% từ 100.000đ\n- `GIAM20000`: giảm 20.000đ từ 150.000đ")

menu_col, bill_col = st.columns([1.08, .92], gap="large")
with menu_col:
    st.markdown('<div class="section-title">✦ Thực đơn tiệm trà</div>', unsafe_allow_html=True)
    st.caption("Chọn số lượng, topping, độ ngọt và lượng đá cho từng món.")
    chosen = []
    with st.form("menu_form"):
        idx = 0
        for category, drinks in MENU.items():
            st.markdown(f"### {category}")
            for drink, price in drinks.items():
                st.markdown(f'<div class="menu-card"><span class="menu-name">{escape(drink)}</span><br><span class="menu-price">{money(price)}</span></div>', unsafe_allow_html=True)
                a, b, c = st.columns([.7, 1.25, 1.15])
                with a:
                    qty = st.number_input("Số ly", 0, 30, 0, 1, key=f"qty_{idx}")
                with b:
                    topping = st.selectbox("Topping", list(TOPPINGS), key=f"top_{idx}")
                with c:
                    sweet = st.selectbox("Độ ngọt", SWEETNESS, index=2, key=f"sweet_{idx}")
                ice = st.radio("Lượng đá", ICE, horizontal=True, key=f"ice_{idx}", label_visibility="collapsed")
                if qty:
                    chosen.append({"drink": drink, "category": category, "quantity": int(qty),
                                   "price": price, "topping": topping, "topping_price": TOPPINGS[topping],
                                   "sweetness": sweet, "ice": ice})
                idx += 1
        submitted = st.form_submit_button("🧾 Cập nhật hóa đơn", type="primary", use_container_width=True)
    if submitted:
        if not chosen:
            st.warning("Bạn hãy chọn số lượng ít nhất một món nhé.")
        else:
            st.session_state.cart = chosen
            st.session_state.voucher_applied = False
            st.session_state.voucher_message = ""
            st.success("Đã cập nhật món vào hóa đơn!")

    st.divider()
    st.markdown('<div class="section-title">🎡 Vòng quay may mắn</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;background:#fffaf0;border:1px solid #dfcba8;border-radius:14px;padding:1rem"><div style="font-size:3.4rem">🎡</div><div style="font-family:Playfair Display,serif;font-size:1.2rem;color:#68432e">Vòng quay lộc trà</div><div style="color:#826e5b">May mắn ghé thăm · Quà vui mang về</div></div>', unsafe_allow_html=True)
    if st.button("✨ QUAY NGAY", type="primary", use_container_width=True, disabled=st.session_state.spin_used):
        st.session_state.prize = random.choice(PRIZES)
        st.session_state.spin_used = True
        st.rerun()
    if st.session_state.prize:
        p = st.session_state.prize
        st.success(f"🎉 Bạn nhận được: **{p['name']}**")
        if p["kind"] == "topping":
            st.caption("Tặng một topping tối đa 7.000đ cho một ly. Nhân viên xác nhận tại quầy.")
        elif p["kind"] == "gift":
            st.caption("Vui lòng báo nhân viên để nhận quà nhỏ.")
    else:
        st.caption("Mỗi đơn có một lượt quay.")

with bill_col:
    st.markdown('<div class="section-title">✦ Hóa đơn thanh toán</div>', unsafe_allow_html=True)
    items = st.session_state.cart
    if not items:
        st.markdown('<div class="bill" style="text-align:center;padding:2.2rem 1rem"><div style="font-size:2.5rem">🫖</div><h3 style="font-family:Playfair Display,serif;color:#68432e">Chờ bạn chọn món</h3><p>Chọn đồ uống rồi nhấn “Cập nhật hóa đơn”.</p></div>', unsafe_allow_html=True)
    else:
        sub = subtotal_for(items)
        vcol, bcol = st.columns([1.3, .7])
        with vcol:
            st.text_input("Nhập mã voucher", key="voucher_code", placeholder="Ví dụ: HOAINIEM10", label_visibility="collapsed")
        with bcol:
            if st.button("Áp dụng mã", use_container_width=True):
                d, msg = get_voucher_discount(sub, st.session_state.voucher_code)
                st.session_state.voucher_applied = d > 0
                st.session_state.voucher_message = msg
        if st.session_state.voucher_message:
            (st.success if st.session_state.voucher_applied else st.warning)(st.session_state.voucher_message)

        voucher_off = get_voucher_discount(sub, st.session_state.voucher_code)[0] if st.session_state.voucher_applied else 0
        prize = st.session_state.prize
        prize_off = prize_discount(sub, prize)
        total = max(0, sub - min(sub, voucher_off + prize_off))
        now = datetime.now()
        order_code = f"HQN-{now:%y%m%d}-{st.session_state.order_number:03d}"
        customer = st.session_state.customer_name.strip() or "Khách lẻ"
        bill = f"""<div class="bill"><div class="bill-head"><div style="font-size:1.8rem">🍵</div><h2>TRÀ QUÁN HOÀI NIỆM</h2><div style="font-size:.8rem;letter-spacing:.1em">HÓA ĐƠN THANH TOÁN</div><p style="font-size:.82rem;margin:.4rem 0 0">Mã đơn: {order_code}</p><p style="font-size:.82rem;margin:.15rem 0">{now:%d/%m/%Y %H:%M}</p><p style="font-size:.85rem;margin:.15rem 0">Khách hàng: {escape(customer)}</p></div>"""
        for item in items:
            unit = item["price"] + item["topping_price"]
            line = unit * item["quantity"]
            top = item["topping"] if item["topping_price"] else "Không topping"
            bill += f"""<div class="bill-row"><div style="flex:1"><strong>{escape(item['drink'])}</strong><div class="bill-sub">{item['quantity']} ly × {money(unit)}</div><div class="bill-sub">Topping: {escape(top)}</div><div class="bill-sub">Độ ngọt: {escape(item['sweetness'])} · {escape(item['ice'])}</div></div><strong style="white-space:nowrap">{money(line)}</strong></div>"""
        bill += f'<div class="bill-row"><span>Tạm tính</span><strong>{money(sub)}</strong></div>'
        if voucher_off:
            bill += f'<div class="bill-row"><span>Voucher {escape(st.session_state.voucher_code.strip().upper())}</span><strong>-{money(voucher_off)}</strong></div>'
        if prize_off:
            bill += f'<div class="bill-row"><span>Giảm giá vòng quay</span><strong>-{money(prize_off)}</strong></div>'
        if prize and prize["kind"] == "topping":
            bill += '<div class="bill-row"><span>Quà vòng quay</span><strong>Tặng topping*</strong></div>'
        if prize and prize["kind"] == "gift":
            bill += '<div class="bill-row"><span>Quà vòng quay</span><strong>Tặng quà nhỏ*</strong></div>'
        bill += f'<div class="bill-total"><span>TỔNG CỘNG</span><span>{money(total)}</span></div><div style="text-align:center;margin-top:1rem;font-size:.9rem"><strong>Thanh toán: {escape(st.session_state.payment_method)}</strong><p style="color:#826e5b;margin:.45rem 0 0">Cảm ơn quý khách đã ghé thăm!</p><p style="font-family:Playfair Display,serif;color:#8f3028;font-style:italic;margin:.2rem 0">Hẹn gặp lại trong một ngày bình yên.</p></div></div>'
        st.markdown(bill, unsafe_allow_html=True)

        if st.session_state.payment_method == "Quét mã QR":
            st.markdown("#### 📱 Mã QR thanh toán")
            with st.expander("Thiết lập QR ngân hàng"):
                st.caption("Nhập thông tin tài khoản của quán. Cần internet để tải QR.")
                bank = st.text_input("Mã ngân hàng (ví dụ MB, VCB, ACB)", key="bank_id")
                account = st.text_input("Số tài khoản", key="account_no")
                account_name = st.text_input("Tên chủ tài khoản", key="account_name")
                if bank.strip() and account.strip():
                    qr = f"https://img.vietqr.io/image/{quote(bank.strip())}-{quote(account.strip())}-compact2.png?amount={total}&addInfo={quote('Thanh toan ' + order_code)}&accountName={quote(account_name.strip())}"
                    st.image(qr, caption=f"Quét để chuyển {money(total)}. Kiểm tra tên người nhận trước khi chuyển.", width=280)
                    st.warning("QR không tự xác nhận giao dịch. Nhân viên cần kiểm tra tài khoản đã nhận tiền.")

        lines = ["TRÀ QUÁN HOÀI NIỆM", f"Mã đơn: {order_code}", f"Thời gian: {now:%d/%m/%Y %H:%M}", f"Khách hàng: {customer}", ""]
        for item in items:
            line = (item["price"] + item["topping_price"]) * item["quantity"]
            lines.append(f"{item['drink']} x{item['quantity']} | Topping: {item['topping']} | Độ ngọt: {item['sweetness']} | {item['ice']} | {money(line)}")
        lines += ["", f"Tạm tính: {money(sub)}", f"Giảm voucher: -{money(voucher_off)}", f"Giảm vòng quay: -{money(prize_off)}", f"TỔNG CỘNG: {money(total)}", f"Thanh toán: {st.session_state.payment_method}"]
        st.download_button("⬇️ Tải hóa đơn TXT", "\n".join(lines), file_name=f"{order_code}.txt", mime="text/plain", use_container_width=True)
        if st.button("🧹 Hoàn tất & tạo đơn mới", use_container_width=True):
            reset_order()
            st.rerun()

st.markdown("---")
st.markdown("<div style='text-align:center;color:#826e5b;font-size:.82rem'>TRÀ QUÁN HOÀI NIỆM · Lưu giữ hương vị xưa trong từng ly trà</div>", unsafe_allow_html=True)

