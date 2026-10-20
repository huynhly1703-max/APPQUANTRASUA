import streamlit as st
import random
import qrcode
from io import BytesIO
from datetime import datetime

# =========================================================
# CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="Hiên Xưa | Tiệm trà hoài niệm",
    page_icon="🪷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# DỮ LIỆU QUÁN VÀ THỰC ĐƠN
# Bạn có thể thay ảnh bằng URL ảnh của riêng quán.
# =========================================================
TEN_QUAN = "HIÊN XƯA"
SLOGAN = "Một ngụm trà, một miền ký ức."

MENU = {
    "Trà sữa": [
        {
            "name": "Trà Sữa Cô Ba",
            "price": 35000,
            "image": "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=900&q=85",
            "description": "Trà đen thơm đậm hòa cùng sữa béo dịu, gợi nhớ những buổi chiều phố cũ.",
            "message": "☕ Cô Ba gửi bạn chút ngọt ngào, mong ngày hôm nay của bạn dịu dàng hơn nhé!",
        },
        {
            "name": "Trà Sữa Gánh Hàng Rong",
            "price": 39000,
            "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=900&q=85",
            "description": "Vị trà đậm đà, sữa mượt mà, thêm chút hoài niệm của những con phố xưa.",
            "message": "🧺 Chúc bạn đi đâu cũng gặp điều lành, ghé đâu cũng có niềm vui!",
        },
        {
            "name": "Trà Sữa Mực Tím",
            "price": 42000,
            "image": "https://images.unsplash.com/photo-1525385133512-2f3d320c6df0?auto=format&fit=crop&w=900&q=85",
            "description": "Vị trà sữa dịu êm, dành cho những tâm hồn yêu trang vở và ký ức học trò.",
            "message": "✉️ Gửi bạn một lời nhắn: hãy luôn giữ lại một góc nhỏ cho những điều mình yêu!",
        },
        {
            "name": "Trà Sữa Đêm Phố",
            "price": 40000,
            "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=85",
            "description": "Trà thơm sâu vị, ngọt vừa phải, hợp với những buổi tối chậm rãi.",
            "message": "🏮 Mong mọi muộn phiền hôm nay đều khép lại, nhường chỗ cho bình yên.",
        },
    ],
    "Matcha": [
        {
            "name": "Matcha Nàng Thơ",
            "price": 42000,
            "image": "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=900&q=85",
            "description": "Matcha xanh thơm, hậu vị thanh nhẹ, kết hợp cùng sữa mềm mịn.",
            "message": "🍃 Chúc bạn luôn xanh tươi như chiếc lá, nhẹ lòng như làn gió!",
        },
        {
            "name": "Matcha Ngọc Bích",
            "price": 45000,
            "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=900&q=85",
            "description": "Matcha đậm vị, màu xanh dịu mắt, dành cho người thích vị trà rõ nét.",
            "message": "💚 Một chút xanh cho tâm trí an nhiên. Cảm ơn bạn đã ghé Hiên Xưa!",
        },
        {
            "name": "Matcha Sương Mai",
            "price": 47000,
            "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=900&q=85",
            "description": "Matcha kết hợp lớp sữa mịn màng, nhẹ nhàng như sương sớm.",
            "message": "🌿 Mong ngày mới của bạn bắt đầu bằng một điều thật dễ thương!",
        },
    ],
}

TOPPINGS = {
    "Trân châu đen": 7000,
    "Trân châu trắng": 7000,
    "Thạch củ năng": 8000,
    "Pudding trứng": 8000,
    "Kem cheese": 10000,
    "Không thêm topping": 0,
}

VOUCHERS = {
    "HIENXUA10": {"type": "percent", "value": 10, "description": "Giảm 10% tổng tiền đồ uống"},
    "NGAYXUA15": {"type": "percent", "value": 15, "description": "Giảm 15% tổng tiền đồ uống"},
    "GIAM5000": {"type": "amount", "value": 5000, "description": "Giảm 5.000đ"},
    "TANGTOPPING": {"type": "topping", "value": 0, "description": "Tặng topping miễn phí cho một món"},
}

PRIZES = [
    {"name": "Voucher giảm 10%", "code": "HIENXUA10", "kind": "voucher"},
    {"name": "Voucher giảm 15%", "code": "NGAYXUA15", "kind": "voucher"},
    {"name": "Tặng topping miễn phí", "code": "TANGTOPPING", "kind": "voucher"},
    {"name": "Quà nhỏ: sticker hoài cổ", "code": "", "kind": "gift"},
    {"name": "Chúc bạn may mắn lần sau", "code": "", "kind": "none"},
    {"name": "Voucher giảm 5.000đ", "code": "GIAM5000", "kind": "voucher"},
]

# =========================================================
# CSS GIAO DIỆN HOÀI CỔ
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap');

:root {
  --cream: #f7f0e3;
  --paper: #fffaf0;
  --brown: #4b2e22;
  --brown2: #76513b;
  --red: #8f2f26;
  --gold: #c49a55;
}
.stApp {
  background: linear-gradient(180deg, #f7f0e3 0%, #f3e7d4 100%);
  color: var(--brown);
  font-family: 'Be Vietnam Pro', sans-serif;
}
h1, h2, h3, h4 {
  font-family: 'Playfair Display', serif !important;
  color: #4b2e22 !important;
}
[data-testid="stSidebar"] {
  background: #ead9bf;
  border-right: 1px solid #c9ad82;
}
.hero {
  padding: 2.2rem 1.4rem;
  border: 2px solid #c49a55;
  border-radius: 18px;
  text-align: center;
  background: linear-gradient(135deg, #fff8e9, #ead7b7);
  box-shadow: 0 8px 24px rgba(75,46,34,.09);
  margin-bottom: 1.2rem;
}
.hero-kicker { letter-spacing: 4px; color: #8f2f26; font-size: .82rem; font-weight: 700; }
.hero-title { font-family: 'Playfair Display', serif; font-size: clamp(2.6rem, 7vw, 4.8rem); line-height: 1.1; color: #4b2e22; font-weight: 700; }
.hero-sub { font-size: 1.08rem; color: #76513b; font-style: italic; margin-top: .6rem; }
.menu-card {
  background: #fffaf0; border: 1px solid #ddc7a4; border-radius: 16px;
  padding: 14px; margin-bottom: 14px; box-shadow: 0 4px 15px rgba(75,46,34,.06);
}
.price { color: #8f2f26; font-size: 1.15rem; font-weight: 700; }
.note {
  background: #f4e5c9; border-left: 4px solid #c49a55; border-radius: 8px;
  padding: 12px 14px; color: #4b2e22; margin: 8px 0 14px 0;
}
.bill {
  background: #fffaf0; border: 2px dashed #b38a55; border-radius: 14px;
  padding: 18px; color: #4b2e22;
}
.small-muted { color: #856b53; font-size: .9rem; }
div.stButton > button {
  background: #8f2f26; color: #fff8e9; border: 1px solid #8f2f26;
  border-radius: 9px; font-weight: 600;
}
div.stButton > button:hover { background: #6f211b; color: #fff8e9; border-color: #6f211b; }
div[data-testid="stMetric"] {
  background: #fffaf0; border: 1px solid #ddc7a4; border-radius: 12px; padding: 12px;
}
hr { border-color: #d6bd96; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================
if "cart" not in st.session_state:
    st.session_state.cart = []
if "voucher_code" not in st.session_state:
    st.session_state.voucher_code = ""
if "voucher_applied" not in st.session_state:
    st.session_state.voucher_applied = ""
if "spin_result" not in st.session_state:
    st.session_state.spin_result = None
if "spun" not in st.session_state:
    st.session_state.spun = False
if "order_number" not in st.session_state:
    st.session_state.order_number = f"HX{datetime.now().strftime('%y%m%d%H%M%S')}"

def vnd(amount):
    return f"{int(round(amount)):,}".replace(",", ".") + "đ"

def get_subtotal():
    return sum(item["line_total"] for item in st.session_state.cart)

def calculate_discount(subtotal, voucher_code):
    code = voucher_code.strip().upper()
    voucher = VOUCHERS.get(code)
    if not voucher:
        return 0, "Mã voucher không hợp lệ hoặc đã hết hạn."
    if code == "TANGTOPPING":
        # Topping miễn phí: trừ giá topping có tính phí cao nhất trong giỏ.
        topping_values = [
            TOPPINGS.get(topping, 0)
            for item in st.session_state.cart
            for topping in item["toppings"]
            if topping != "Không thêm topping"
        ]
        if not topping_values:
            return 0, "Voucher TANGTOPPING hợp lệ, nhưng giỏ hàng chưa có topping tính phí."
        return max(topping_values), voucher["description"]
    if voucher["type"] == "percent":
        return round(subtotal * voucher["value"] / 100), voucher["description"]
    if voucher["type"] == "amount":
        return min(voucher["value"], subtotal), voucher["description"]
    return 0, voucher["description"]

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 🪷 HIÊN XƯA")
    st.caption("Tiệm trà của những miền ký ức")
    page = st.radio(
        "DANH MỤC",
        ["🏠 Về Hiên Xưa", "📜 Khám phá thực đơn", "🧾 Giỏ hàng & thanh toán", "🎡 Vòng quay may mắn"],
        label_visibility="collapsed",
        key="page",
    )
    st.divider()
    st.markdown("**Giờ mở cửa**")
    st.write("09:00 – 22:00 mỗi ngày")
    st.markdown("**Thông điệp hôm nay**")
    st.write("“Chậm một chút, nhấp một ngụm trà, thương mình nhiều hơn.”")

# =========================================================
# HEADER
# =========================================================
st.markdown(f"""
<div class="hero">
  <div class="hero-kicker">TIỆM TRÀ • GÓC PHỐ • KÝ ỨC</div>
  <div class="hero-title">🪷 {TEN_QUAN} 🪷</div>
  <div class="hero-sub">{SLOGAN}</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# TRANG GIỚI THIỆU
# =========================================================
if page == "🏠 Về Hiên Xưa":
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown("## Chuyện kể bên hiên")
        st.write(
            "Hiên Xưa là một góc nhỏ dành cho những ai yêu nét đẹp bình dị của Việt Nam ngày trước. "
            "Từ màu giấy ngà, chiếc đèn lồng, đến những cái tên thân thương như Cô Ba, Gánh Hàng Rong "
            "hay Mực Tím — mỗi chi tiết đều được gửi gắm như một lời mời trở về với ký ức."
        )
        st.write(
            "Chúng mình tin rằng một ly trà ngon không chỉ nằm ở hương vị, mà còn ở cảm giác an yên "
            "khi bạn dành một chút thời gian cho bản thân. Hãy chọn món yêu thích, tùy chỉnh vị ngọt, "
            "thêm topping và để Hiên Xưa gửi bạn một lời nhắn nhỏ."
        )
        st.markdown('<div class="note">🪷 <b>Triết lý của Hiên Xưa:</b> Giữ vị trà chân thành, trao điều tử tế, lưu lại những khoảnh khắc dịu dàng.</div>', unsafe_allow_html=True)
        if st.button("📜 Khám phá thực đơn", use_container_width=True):
            st.session_state["page"] = "📜 Khám phá thực đơn"
            st.rerun()
    with right:
        st.image(
            "https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=1100&q=85",
            use_container_width=True,
            caption="Một góc nhỏ bình yên dành cho người yêu trà."
        )
    st.markdown("### Điều làm nên Hiên Xưa")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 🍵 Vị trà")
        st.write("Trà thơm, vị cân bằng, tùy chỉnh theo sở thích của bạn.")
    with c2:
        st.markdown("#### 🏮 Chuyện xưa")
        st.write("Tên món lấy cảm hứng từ góc phố, trang vở và nếp sống xưa.")
    with c3:
        st.markdown("#### 💌 Lời nhắn")
        st.write("Mỗi món đều đi kèm một lời chúc nhỏ dành riêng cho khách.")
# =========================================================
# TRANG MENU VÀ CHỌN MÓN
# =========================================================
elif page == "📜 Khám phá thực đơn":
    st.markdown("## 📜 Thực đơn nhà Hiên")
    st.write("Chọn thức uống, điều chỉnh theo gu riêng rồi thêm vào giỏ hàng nhé.")
    category = st.radio("Chọn nhóm thức uống", list(MENU.keys()), horizontal=True)
    drinks = MENU[category]

    # Danh sách thẻ món
    for start in range(0, len(drinks), 2):
        cols = st.columns(2)
        for col, drink in zip(cols, drinks[start:start+2]):
            with col:
                st.markdown('<div class="menu-card">', unsafe_allow_html=True)
                st.image(drink["image"], use_container_width=True)
                st.markdown(f"### {drink['name']}")
                st.markdown(f'<div class="price">{vnd(drink["price"])}</div>', unsafe_allow_html=True)
                st.write(drink["description"])
                st.markdown('</div>', unsafe_allow_html=True)
                with st.expander(f"✨ Chọn {drink['name']}", expanded=False):
                    st.markdown(f'<div class="note">{drink["message"]}</div>', unsafe_allow_html=True)
                    quantity = st.number_input(
                        "Số lượng",
                        min_value=1,
                        max_value=20,
                        value=1,
                        step=1,
                        key=f"qty_{category}_{drink['name']}",
                    )
                    toppings = st.multiselect(
                        "Topping kèm",
                        list(TOPPINGS.keys()),
                        default=[],
                        key=f"top_{category}_{drink['name']}",
                        help="Bạn có thể chọn nhiều topping.",
                    )
                    sweet = st.select_slider(
                        "Độ ngọt",
                        options=["0%", "25%", "50%", "70%", "100%"],
                        value="70%",
                        key=f"sweet_{category}_{drink['name']}",
                    )
                    ice = st.radio(
                        "Lượng đá",
                        ["Đá bình thường", "Ít đá", "Không đá"],
                        horizontal=True,
                        key=f"ice_{category}_{drink['name']}",
                    )
                    topping_price = sum(TOPPINGS[t] for t in toppings)
                    unit_price = drink["price"] + topping_price
                    st.write(f"Giá một ly: **{vnd(unit_price)}**")
                    if st.button("➕ Thêm vào giỏ hàng", key=f"add_{category}_{drink['name']}", use_container_width=True):
                        st.session_state.cart.append({
                            "name": drink["name"],
                            "category": category,
                            "base_price": drink["price"],
                            "toppings": toppings,
                            "topping_price": topping_price,
                            "sweet": sweet,
                            "ice": ice,
                            "quantity": int(quantity),
                            "unit_price": unit_price,
                            "line_total": unit_price * int(quantity),
                            "message": drink["message"],
                        })
                        st.success(f"Đã thêm {quantity} × {drink['name']} vào giỏ!")
                        st.rerun()

    st.divider()
    st.markdown("### 🧺 Giỏ hàng nhanh")
    if st.session_state.cart:
        st.write(f"Bạn đang có **{len(st.session_state.cart)} dòng món** trong giỏ.")
        st.metric("Tạm tính", vnd(get_subtotal()))
        if st.button("🧾 Sang giỏ hàng & thanh toán", use_container_width=True):
            st.session_state["go_checkout"] = True
            st.rerun()
    else:
        st.caption("Giỏ hàng đang trống. Hãy chọn món bạn yêu thích nhé!")

# =========================================================
# TRANG GIỎ HÀNG VÀ THANH TOÁN
# =========================================================
elif page == "🧾 Giỏ hàng & thanh toán":
    st.markdown("## 🧾 Hóa đơn của bạn")
    if not st.session_state.cart:
        st.info("Giỏ hàng hiện đang trống. Hãy ghé thực đơn để chọn món nhé!")
    else:
        # Cho phép xóa từng dòng
        for i, item in enumerate(st.session_state.cart):
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 2, 1])
                with c1:
                    st.markdown(f"**{item['name']}** × {item['quantity']}")
                    st.caption(f"Độ ngọt: {item['sweet']} • {item['ice']}")
                    topping_text = ", ".join(item["toppings"]) if item["toppings"] else "Không topping"
                    st.caption(f"Topping: {topping_text}")
                    st.caption(f"Đơn giá: {vnd(item['unit_price'])}")
                with c2:
                    st.markdown(f"**{vnd(item['line_total'])}**")
                with c3:
                    if st.button("🗑️ Xóa", key=f"remove_{i}"):
                        st.session_state.cart.pop(i)
                        st.rerun()
                st.markdown(f'<div class="note">{item["message"]}</div>', unsafe_allow_html=True)

        subtotal = get_subtotal()
        st.divider()
        st.markdown("### 🎟️ Mã voucher")
        v1, v2 = st.columns([3, 1])
        with v1:
            voucher_input = st.text_input(
                "Nhập mã voucher",
                value=st.session_state.voucher_code,
                placeholder="Ví dụ: HIENXUA10",
                label_visibility="collapsed",
            )
        with v2:
            apply_voucher = st.button("Áp dụng mã", use_container_width=True)

        if apply_voucher:
            code = voucher_input.strip().upper()
            discount, message = calculate_discount(subtotal, code)
            if code in VOUCHERS and (discount > 0 or code != "TANGTOPPING"):
                st.session_state.voucher_code = code
                st.session_state.voucher_applied = code
                st.success(f"Đã áp dụng {code}: {message}")
            else:
                st.session_state.voucher_code = voucher_input
                st.session_state.voucher_applied = ""
                st.warning(message)
            st.rerun()

        # Nếu giỏ trống hoặc thay đổi, tính lại voucher đã áp dụng
        applied = st.session_state.voucher_applied
        discount = 0
        if applied:
            discount, voucher_message = calculate_discount(subtotal, applied)
            if applied == "TANGTOPPING" and discount == 0:
                st.warning(voucher_message)
                st.session_state.voucher_applied = ""
                applied = ""

        total = max(0, subtotal - discount)
        a, b, c = st.columns(3)
        a.metric("Tạm tính", vnd(subtotal))
        b.metric("Giảm giá", f"-{vnd(discount)}")
        c.metric("Tổng thanh toán", vnd(total))

        st.markdown("### 💳 Phương thức thanh toán")
        payment = st.radio(
            "Chọn phương thức",
            ["Tiền mặt", "Quét mã QR"],
            horizontal=True,
        )

        if payment == "Quét mã QR":
            st.markdown("#### 📱 Quét mã để thanh toán")
            st.caption("Mã QR bên dưới là QR thanh toán mẫu chứa nội dung đơn hàng và số tiền. Để nhận tiền thật, hãy thay phần tạo QR bằng thông tin ngân hàng/đơn vị thanh toán của quán.")
            qr_payload = f"HIEN XUA | Don {st.session_state.order_number} | Thanh toan {total} VND"
            qr_img = qrcode.make(qr_payload)
            buf = BytesIO()
            qr_img.save(buf, format="PNG")
            q1, q2 = st.columns([1, 2])
            with q1:
                st.image(buf.getvalue(), caption="QR mẫu — chưa liên kết ngân hàng", width=230)
            with q2:
                st.write(f"**Mã đơn:** {st.session_state.order_number}")
                st.write(f"**Số tiền:** {vnd(total)}")
                st.write("QR mẫu này chỉ chứa nội dung văn bản, không tự động chuyển tiền. Muốn thanh toán thật, hãy dùng VietQR với mã ngân hàng, số tài khoản và mẫu nội dung hợp lệ.")
        else:
            st.info("Bạn vui lòng thanh toán bằng tiền mặt tại quầy khi nhận món.")

        st.divider()
        if st.button("✅ Xác nhận đặt hàng", type="primary", use_container_width=True):
            st.session_state["confirmed_order"] = {
                "order_number": st.session_state.order_number,
                "items": [dict(item) for item in st.session_state.cart],
                "subtotal": subtotal,
                "discount": discount,
                "total": total,
                "payment": payment,
                "voucher": applied,
                "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
            }
            st.success("Đặt hàng thành công! Hóa đơn được hiển thị bên dưới.")
            st.rerun()

        if st.session_state.get("confirmed_order"):
            order = st.session_state.confirmed_order
            st.markdown("---")
            st.markdown('<div class="bill">', unsafe_allow_html=True)
            st.markdown(f"## 🪷 {TEN_QUAN}")
            st.markdown("**HÓA ĐƠN THANH TOÁN**")
            st.write(f"Mã đơn: {order['order_number']}")
            st.write(f"Thời gian: {order['time']}")
            st.write(f"Phương thức: {order['payment']}")
            st.write("---")
            for idx, item in enumerate(order["items"], 1):
                st.write(f"{idx}. **{item['name']}** × {item['quantity']} — {vnd(item['line_total'])}")
                if item["toppings"]:
                    st.caption("   Topping: " + ", ".join(item["toppings"]))
                st.caption(f"   Độ ngọt {item['sweet']} • {item['ice']}")
            st.write("---")
            st.write(f"Tạm tính: **{vnd(order['subtotal'])}**")
            st.write(f"Giảm giá: **-{vnd(order['discount'])}**")
            st.markdown(f"### Tổng cộng: {vnd(order['total'])}")
            st.markdown("*Cảm ơn bạn đã ghé Hiên Xưa. Mong sớm được gặp lại!*")
            st.markdown('</div>', unsafe_allow_html=True)

            bill_text = [
                f"{TEN_QUAN} - HOA DON",
                f"Ma don: {order['order_number']}",
                f"Thoi gian: {order['time']}",
                f"Thanh toan: {order['payment']}",
                *[
                    f"{i}. {it['name']} x{it['quantity']} | {vnd(it['line_total'])} | {it['sweet']} | {it['ice']} | Topping: {', '.join(it['toppings']) if it['toppings'] else 'Khong'}"
                    for i, it in enumerate(order["items"], 1)
                ],
                f"Tam tinh: {vnd(order['subtotal'])}",
                f"Giam gia: -{vnd(order['discount'])}",
                f"TONG CONG: {vnd(order['total'])}",
            ]
            st.download_button(
                "⬇️ Tải hóa đơn dạng TXT",
                data="\n".join(bill_text),
                file_name=f"hoa_don_{order['order_number']}.txt",
                mime="text/plain",
                use_container_width=True,
            )
            if st.button("🆕 Tạo đơn hàng mới", use_container_width=True):
                st.session_state.cart = []
                st.session_state.voucher_code = ""
                st.session_state.voucher_applied = ""
                st.session_state.confirmed_order = None
                st.session_state.order_number = f"HX{datetime.now().strftime('%y%m%d%H%M%S')}"
                st.rerun()

# =========================================================
# TRANG VÒNG QUAY MAY MẮN
# =========================================================
elif page == "🎡 Vòng quay may mắn":
    st.markdown("## 🎡 Vòng quay may mắn")
    st.write("Mỗi lượt quay mang đến một bất ngờ nho nhỏ. Hãy thử vận may của bạn!")
    st.markdown('<div class="note">🎁 Phần thưởng có thể là mã giảm giá, topping miễn phí, sticker hoài cổ hoặc lời chúc may mắn.</div>', unsafe_allow_html=True)

    # Hình vòng quay minh họa bằng biểu đồ dạng vòng
    import matplotlib.pyplot as plt
    labels = ["Giảm 10%", "Giảm 15%", "Tặng topping", "Sticker", "May mắn", "Giảm 5k"]
    values = [1] * len(labels)
    fig, ax = plt.subplots(figsize=(6, 5), facecolor="#fffaf0")
    ax.pie(
        values,
        labels=labels,
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.38, "edgecolor": "#fffaf0", "linewidth": 2},
        textprops={"fontsize": 9, "color": "#4b2e22"},
    )
    ax.text(0, 0, "HIÊN\nXƯA", ha="center", va="center", fontsize=17, fontweight="bold", color="#8f2f26")
    ax.set_title("VÒNG QUAY LỘC NHỎ", color="#4b2e22", fontsize=14, pad=15)
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)

    if not st.session_state.spun:
        if st.button("🎯 QUAY NGAY", type="primary", use_container_width=True):
            result = random.choice(PRIZES)
            st.session_state.spin_result = result
            st.session_state.spun = True
            st.rerun()
    else:
        result = st.session_state.spin_result
        st.success(f"🎉 Kết quả của bạn: **{result['name']}**")
        if result["code"]:
            st.code(result["code"], language=None)
            st.caption("Hãy sao chép mã và nhập tại mục Voucher trong trang Giỏ hàng & thanh toán.")
            if st.button("📋 Dùng mã voucher này"):
                st.session_state.voucher_code = result["code"]
                st.session_state.voucher_applied = ""
                st.success("Đã lưu mã vào ô voucher. Vào Giỏ hàng & thanh toán để áp dụng.")
        elif result["kind"] == "gift":
            st.info("Bạn nhận được một sticker hoài cổ nhỏ xinh. Hãy báo nhân viên khi nhận món nhé!")
        else:
            st.info("Cảm ơn bạn đã chơi. Hiên Xưa chúc bạn một ngày thật vui!")
        if st.button("🔄 Chơi lại", use_container_width=True):
            st.session_state.spun = False
            st.session_state.spin_result = None
            st.rerun()

    st.caption("Lưu ý: Đây là vòng quay minh họa cho ứng dụng mẫu. Phần thưởng được chọn ngẫu nhiên ở phía ứng dụng; nếu dùng thực tế, quán nên quy định số lượt quay và điều kiện nhận quà.")

# =========================================================
# CHÂN TRANG
# =========================================================
st.divider()
st.markdown(
    f"<div style='text-align:center;color:#856b53;padding:8px'>🪷 <b>{TEN_QUAN}</b> · {SLOGAN}<br>"
    "Cảm ơn bạn đã ghé thăm góc nhỏ hoài niệm này.</div>",
    unsafe_allow_html=True,
)

