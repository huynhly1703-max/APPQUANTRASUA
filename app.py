import streamlit as st
from datetime import datetime
from html import escape

# ============================================================
# TRÀ QUÁN HOÀI NIỆM - Streamlit app
# Chạy bằng: streamlit run app.py
# ============================================================

st.set_page_config(
    page_title="Trà Quán Hoài Niệm",
    page_icon="🍵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Bảng giá (có thể chỉnh sửa tại đây) ----------
DRINKS = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa ô long": 35000,
    "Trà đào cam sả": 32000,
    "Trà tắc mật ong": 25000,
    "Hồng trà vải": 32000,
    "Matcha sữa": 38000,
    "Cacao sữa": 35000,
    "Sữa tươi trân châu đường đen": 40000,
}
TOPPINGS = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch cà phê": 5000,
    "Pudding trứng": 7000,
    "Thạch trái cây": 6000,
    "Kem cheese": 10000,
}
SWEETNESS = ["0% (không đường)", "30%", "50%", "70%", "100%"]
ICE_OPTIONS = ["Đá bình thường", "Ít đá", "Không đá"]

# ---------- Phong cách giao diện ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --paper: #f6efdf;
    --paper2: #fffaf0;
    --ink: #38271d;
    --brown: #68432e;
    --red: #8f3028;
    --gold: #c29a55;
}
.stApp {
    background:
      radial-gradient(ellipse at top left, rgba(194,154,85,.14), transparent 38%),
      #f3ead8;
    color: var(--ink);
    font-family: 'Be Vietnam Pro', sans-serif;
}
[data-testid="stHeader"] { background: rgba(243,234,216,.92); }
.block-container { max-width: 1250px; padding-top: 1.5rem; padding-bottom: 3rem; }
.hero {
    padding: 2rem 1.5rem;
    border: 2px solid #68432e;
    outline: 1px solid #c29a55;
    outline-offset: -9px;
    border-radius: 8px;
    text-align: center;
    color: #fff7e8;
    background: linear-gradient(135deg, #493023, #74452e 65%, #8f3028);
    box-shadow: 0 8px 24px rgba(56,39,29,.14);
    margin-bottom: 1.4rem;
}
.hero .eyebrow { letter-spacing: .24em; font-size: .76rem; text-transform: uppercase; color: #e7c991; }
.hero h1 { font-family: 'Playfair Display', serif; font-size: clamp(2rem, 4vw, 3.2rem); margin: .35rem 0; color: #fff7e8; }
.hero p { margin: 0; color: #f2dfbf; }
.section-title {
    font-family: 'Playfair Display', serif;
    color: #68432e;
    font-size: 1.55rem;
    padding-bottom: .45rem;
    border-bottom: 1px solid #c9ac7b;
    margin: .3rem 0 1rem;
}
.menu-card {
    background: #fffaf0;
    border: 1px solid #dfcba8;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: .75rem;
    box-shadow: 0 3px 9px rgba(56,39,29,.045);
}
.menu-name { font-weight: 700; color: #493023; font-size: 1.04rem; }
.menu-price { color: #8f3028; font-weight: 700; }
.muted { color: #826e5b; font-size: .88rem; }
.bill {
    background: #fffaf0;
    color: #38271d;
    border: 1px solid #c9ac7b;
    border-radius: 4px;
    padding: 1.4rem;
    box-shadow: 0 6px 20px rgba(56,39,29,.08);
}
.bill-head { text-align: center; border-bottom: 1px dashed #b69a70; padding-bottom: 1rem; margin-bottom: 1rem; }
.bill-head h2 { font-family: 'Playfair Display', serif; margin: .2rem 0; color: #68432e; }
.bill-row { display: flex; justify-content: space-between; gap: 1rem; padding: .55rem 0; border-bottom: 1px dotted #dfcba8; }
.bill-sub { color: #826e5b; font-size: .85rem; margin-top: .15rem; }
.bill-total { display:flex; justify-content:space-between; font-weight:800; font-size:1.2rem; color:#8f3028; border-top:2px solid #68432e; padding-top:1rem; margin-top:1rem; }
.stButton > button {
    border-radius: 7px;
    border: 1px solid #68432e;
    font-weight: 700;
}
.stButton > button[kind="primary"] {
    background: #8f3028;
    color: #fffaf0;
    border: 1px solid #8f3028;
}
div[data-testid="stAlert"] { border-radius: 8px; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ---------- Trạng thái ----------
if "order_items" not in st.session_state:
    st.session_state.order_items = []
if "order_number" not in st.session_state:
    st.session_state.order_number = 1
if "payment_method" not in st.session_state:
    st.session_state.payment_method = "Tiền mặt"
if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

# ---------- Đầu trang ----------
st.markdown("""
<div class="hero">
  <div class="eyebrow">Since 19xx · Hương vị thân quen</div>
  <h1>🍵 Trà Quán Hoài Niệm</h1>
  <p>Một chút vị trà · Một chút ký ức · Một ngày an yên</p>
</div>
""", unsafe_allow_html=True)

# ---------- Thanh bên: thông tin đơn ----------
with st.sidebar:
    st.markdown("## 🧾 Thông tin đơn")
    st.caption(f"Mã đơn: HQN-{datetime.now().strftime('%y%m%d')}-{st.session_state.order_number:03d}")
    customer = st.text_input("Tên khách hàng (không bắt buộc)", key="customer_name")
    st.markdown("---")
    st.markdown("### 💳 Hình thức thanh toán")
    payment = st.radio(
        "Chọn phương thức",
        ["Tiền mặt", "Quét mã QR"],
        index=0 if st.session_state.payment_method == "Tiền mặt" else 1,
        key="payment_method",
    )
    st.markdown("---")
    st.caption("Giá niêm yết bằng VNĐ. Topping được tính theo từng ly.")

# ---------- Bố cục chính ----------
left, right = st.columns([1.08, .92], gap="large")

with left:
    st.markdown('<div class="section-title">✦ Thực đơn tiệm trà</div>', unsafe_allow_html=True)
    st.caption("Chọn số lượng, sau đó tùy chỉnh topping và khẩu vị cho từng món.")
    with st.form("order_form", clear_on_submit=False):
        selections = {}
        for idx, (drink, price) in enumerate(DRINKS.items()):
            st.markdown(
                f'<div class="menu-card"><span class="menu-name">{escape(drink)}</span>'
                f'<br><span class="menu-price">{price:,.0f} đ</span>'
                f'<br><span class="muted">Pha mới theo khẩu vị của bạn</span></div>',
                unsafe_allow_html=True,
            )
            c1, c2, c3 = st.columns([.8, 1.2, 1.2])
            with c1:
                qty = st.number_input(
                    "Số ly", min_value=0, max_value=30, value=0, step=1,
                    key=f"qty_{idx}", help="Để 0 nếu không gọi món này."
                )
            with c2:
                topping = st.selectbox(
                    "Topping", list(TOPPINGS.keys()), key=f"topping_{idx}"
                )
            with c3:
                sweetness = st.selectbox(
                    "Độ ngọt", SWEETNESS, index=2, key=f"sweet_{idx}"
                )
            ice = st.radio(
                "Lượng đá", ICE_OPTIONS, horizontal=True,
                key=f"ice_{idx}", label_visibility="collapsed"
            )
            if qty > 0:
                selections[drink] = {
                    "quantity": int(qty),
                    "unit_price": price,
                    "topping": topping,
                    "topping_price": TOPPINGS[topping],
                    "sweetness": sweetness,
                    "ice": ice,
                }
        submitted = st.form_submit_button("🧾 Thêm món vào hóa đơn", type="primary", use_container_width=True)

    if submitted:
        if not selections:
            st.warning("Bạn hãy chọn số lượng ít nhất một món trước nhé.")
        else:
            st.session_state.order_items = [
                {"drink": drink, **details} for drink, details in selections.items()
            ]
            st.success("Đã cập nhật các món trong hóa đơn!")

with right:
    st.markdown('<div class="section-title">✦ Hóa đơn của bạn</div>', unsafe_allow_html=True)
    items = st.session_state.order_items
    if not items:
        st.markdown("""
        <div class="bill" style="text-align:center;padding:2.4rem 1rem">
          <div style="font-size:2.5rem">🫖</div>
          <h3 style="font-family:'Playfair Display',serif;color:#68432e">Chờ bạn chọn món</h3>
          <p style="color:#826e5b">Hóa đơn sẽ xuất hiện tại đây sau khi bạn thêm món.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        subtotal = sum(
            (item["unit_price"] + item["topping_price"]) * item["quantity"]
            for item in items
        )
        now = datetime.now()
        order_code = f"HQN-{now.strftime('%y%m%d')}-{st.session_state.order_number:03d}"
        customer_line = f"<p>Khách hàng: {escape(customer)}</p>" if customer.strip() else ""
        bill_html = f"""
        <div class="bill">
          <div class="bill-head">
            <div style="font-size:1.8rem">🍵</div>
            <h2>TRÀ QUÁN HOÀI NIỆM</h2>
            <div style="font-size:.82rem;letter-spacing:.1em">HÓA ĐƠN THANH TOÁN</div>
            <p style="font-size:.82rem;margin:.5rem 0 0">Mã đơn: {order_code}</p>
            <p style="font-size:.82rem;margin:.2rem 0">{now.strftime('%d/%m/%Y %H:%M')}</p>
            {customer_line}
          </div>
        """
        for item in items:
            unit_total = item["unit_price"] + item["topping_price"]
            line_total = unit_total * item["quantity"]
            topping_text = item["topping"] if item["topping_price"] else "Không topping"
            bill_html += f"""
            <div class="bill-row">
              <div style="flex:1">
                <strong>{escape(item['drink'])}</strong>
                <div class="bill-sub">{item['quantity']} ly × {unit_total:,.0f} đ</div>
                <div class="bill-sub">Topping: {escape(topping_text)} · Độ ngọt: {escape(item['sweetness'])}</div>
                <div class="bill-sub">{escape(item['ice'])}</div>
              </div>
              <strong style="white-space:nowrap">{line_total:,.0f} đ</strong>
            </div>
            """
        bill_html += f"""
          <div class="bill-row"><span>Tạm tính</span><strong>{subtotal:,.0f} đ</strong></div>
          <div class="bill-total"><span>TỔNG CỘNG</span><span>{subtotal:,.0f} đ</span></div>
          <div style="text-align:center;margin-top:1.2rem;font-size:.9rem">
            <strong>Thanh toán: {escape(payment)}</strong>
            <p style="color:#826e5b;margin:.5rem 0 0">Cảm ơn quý khách đã ghé thăm!</p>
            <p style="font-family:'Playfair Display',serif;color:#8f3028;font-style:italic;margin:.2rem 0">Hẹn gặp lại trong một ngày bình yên.</p>
          </div>
        </div>
        """
        st.markdown(bill_html, unsafe_allow_html=True)

        if payment == "Quét mã QR":
            st.markdown("#### 📱 Thanh toán bằng QR")
            st.info(
                "Đây là khu vực hướng dẫn thanh toán QR. Để nhận tiền thật, hãy cấu hình "
                "mã VietQR của quán ở phần bên dưới hoặc thay bằng ảnh QR ngân hàng của quán."
            )
            with st.expander("Cấu hình thông tin QR"):
                st.caption("Điền thông tin tài khoản để tạo đường dẫn VietQR theo chuẩn VietQR.")
                bank_id = st.text_input("Mã ngân hàng (ví dụ: MB, VCB, ACB)", key="bank_id")
                account_no = st.text_input("Số tài khoản", key="account_no")
                account_name = st.text_input("Tên chủ tài khoản", key="account_name")
                if bank_id.strip() and account_no.strip():
                    from urllib.parse import quote
                    qr_url = (
                        f"https://img.vietqr.io/image/{quote(bank_id.strip())}-"
                        f"{quote(account_no.strip())}-compact2.png"
                        f"?amount={subtotal}&addInfo={quote('Thanh toan ' + order_code)}"
                        f"&accountName={quote(account_name.strip())}"
                    )
                    st.image(qr_url, caption="Quét mã để thanh toán đúng số tiền trên hóa đơn.", width=280)
                    st.caption("Vui lòng kiểm tra tên người nhận và số tiền trước khi chuyển khoản.")

        st.markdown("")
        col_a, col_b = st.columns(2)
        with col_a:
            st.download_button(
                "⬇️ Tải bill dạng TXT",
                data=(
                    f"TRÀ QUÁN HOÀI NIỆM\\nMã đơn: {order_code}\\n"
                    f"Thời gian: {now.strftime('%d/%m/%Y %H:%M')}\\n"
                    f"Khách: {customer or 'Khách lẻ'}\\n\\n"
                    + "\\n".join(
                        f"{i['drink']} x{i['quantity']} | "
                        f"Topping: {i['topping']} | Độ ngọt: {i['sweetness']} | {i['ice']} | "
                        f"{(i['unit_price'] + i['topping_price']) * i['quantity']:,.0f} đ"
                        for i in items
                    )
                    + f"\\n\\nTỔNG CỘNG: {subtotal:,.0f} đ\\nThanh toán: {payment}\\n"
                ),
                file_name=f"{order_code}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col_b:
            if st.button("🧹 Tạo đơn mới", use_container_width=True):
                st.session_state.order_items = []
                st.session_state.order_number += 1
                st.session_state.customer_name = ""
                for idx in range(len(DRINKS)):
                    for key in (f"qty_{idx}",):
                        if key in st.session_state:
                            st.session_state[key] = 0
                st.rerun()

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#826e5b;font-size:.82rem'>"
    "TRÀ QUÁN HOÀI NIỆM · Lưu giữ hương vị xưa trong từng ly trà"
    "</div>",
    unsafe_allow_html=True,
)

