import streamlit as st
import random
import uuid
from datetime import datetime

# =========================================================
# 1. CẤU HÌNH ỨNG DỤNG
# =========================================================
st.set_page_config(
    page_title="Trà Quán Hoài Niệm",
    page_icon="🍵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. KHỞI TẠO TRẠNG THÁI
# =========================================================
def init_state():
    defaults = {
        "page_nav": "Trang chủ",
        "cart": [],
        "voucher_input": "",
        "voucher_code": "",
        "discount": 0,
        "paid": False,
        "payment_method": "",
        "order_id": "",
        "last_total": 0,
        "last_subtotal": 0,
        "last_discount": 0,
        "last_items": [],
        "rating": 5,
        "feedback": "",
        "feedback_sent": False,
        "spin_result": None,
        "spin_history": [],
        "gift_claimed": False,
        "customer_name": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# =========================================================
# 3. BẢNG MÀU VÀ CSS ĐÔNG DƯƠNG
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700;800&family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap');

:root {
    --wine: #641D2D;
    --wine-dark: #32121B;
    --cream: #F6EAD4;
    --pink: #C88C87;
    --gold: #D6B16D;
    --teal: #174D49;
    --ink: #281B18;
}

.stApp {
    background:
        radial-gradient(ellipse at top left, #4b2528 0%, transparent 45%),
        linear-gradient(135deg, #24171A, #3B2023 55%, #1E3531);
    color: var(--cream);
    font-family: 'Be Vietnam Pro', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(35, 19, 22, 0.92);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1C3834, #152722);
    border-right: 2px solid var(--gold);
}

[data-testid="stSidebar"] * {
    color: #F6EAD4;
}

h1, h2, h3 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: #F4DCA9 !important;
}

p, label, li, .stMarkdown {
    color: #F6EAD4;
}

.hero {
    padding: 42px 28px;
    border: 2px solid #D6B16D;
    outline: 1px solid rgba(214,177,109,.45);
    outline-offset: -10px;
    background:
        linear-gradient(120deg, rgba(43,16,23,.96), rgba(100,29,45,.90)),
        repeating-linear-gradient(45deg, transparent, transparent 10px, #ffffff05 10px, #ffffff05 20px);
    text-align: center;
    border-radius: 4px;
    margin: 12px 0 26px 0;
}

.hero-kicker {
    letter-spacing: 5px;
    font-size: 12px;
    color: #D6B16D;
    text-transform: uppercase;
}

.hero-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(34px, 5vw, 62px);
    font-weight: 800;
    color: #F5E5C4;
    line-height: 1.15;
    margin: 15px 0;
}

.hero-subtitle {
    font-size: 14px;
    color: #E5C5B8;
    letter-spacing: 1px;
}

.ornament {
    color: #D6B16D;
    letter-spacing: 7px;
    margin: 15px 0;
}

.section-label {
    color: #D6B16D;
    letter-spacing: 3px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
}

.menu-card {
    border: 1px solid #AA8052;
    background: linear-gradient(160deg, #49242A, #2B1A1D);
    border-radius: 5px;
    padding: 15px;
    margin-bottom: 10px;
    min-height: 112px;
}

.menu-card h3 {
    margin-top: 4px;
    margin-bottom: 6px;
}

.price {
    color: #E7C477;
    font-weight: 700;
    font-size: 18px;
}

.small-muted {
    color: #D6BBA5;
    font-size: 12px;
}

.info-card {
    background: rgba(246,234,212,.07);
    border: 1px solid rgba(214,177,109,.65);
    border-radius: 5px;
    padding: 20px;
    margin: 8px 0;
}

.stButton > button {
    background: #8C3443;
    color: #FFF2DB !important;
    border: 1px solid #D6B16D;
    border-radius: 3px;
    font-weight: 600;
    min-height: 42px;
    transition: .2s ease;
}

.stButton > button:hover {
    background: #D6B16D;
    color: #32121B !important;
    border-color: #F6EAD4;
}

.stButton > button p {
    color: inherit !important;
}

div[data-baseweb="input"] input,
div[data-baseweb="select"] > div,
.stTextArea textarea {
    background: #F6EAD4 !important;
    color: #32121B !important;
    border-radius: 3px !important;
}

[data-testid="stNumberInput"] button {
    background: #8C3443;
}

hr {
    border-color: rgba(214,177,109,.4);
}

.stRadio label, .stCheckbox label {
    color: #F6EAD4 !important;
}

div[data-testid="stMetric"] {
    background: rgba(246,234,212,.07);
    border: 1px solid #AA8052;
    padding: 15px;
    border-radius: 4px;
}

div[data-testid="stMetricLabel"] {
    color: #E6CDA5 !important;
}

div[data-testid="stMetricValue"] {
    color: #F4DCA9 !important;
}

.receipt {
    background: #F6EAD4;
    color: #32121B;
    border: 2px solid #D6B16D;
    border-radius: 4px;
    padding: 22px;
}

.receipt h3, .receipt p, .receipt div {
    color: #32121B !important;
}

div[data-testid="stAlert"] {
    border-radius: 3px;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

@media (max-width: 768px) {
    .hero { padding: 28px 18px; }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 4. THÔNG TIN MENU
# =========================================================

MENU = [
    # ==================== TRÀ SỮA ====================
    {
        "id": "ts01",
        "name": "Trà Sữa Cô Ba Sài Gòn",
        "category": "Trà sữa",
        "price": 35000,
        "desc": "Trà đen đậm vị, sữa thơm béo dịu dàng.",
        "image": "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=700&q=80",
        "emoji": "🧋"
    },
    {
        "id": "ts02",
        "name": "Trà Sữa Tiệm May Xưa",
        "category": "Trà sữa",
        "price": 39000,
        "desc": "Vị trà thanh nhẹ, ngọt ngào như chuyện cũ.",
        "image": "https://images.unsplash.com/photo-1525385133512-2f3bdd039054?auto=format&fit=crop&w=700&q=80",
        "emoji": "🥤"
    },
    {
        "id": "ts03",
        "name": "Trà Sữa Phố Đèn Lồng",
        "category": "Trà sữa",
        "price": 38000,
        "desc": "Hương trà thơm nồng, sữa béo quyện vị.",
        "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=700&q=80",
        "emoji": "🏮"
    },
    {
        "id": "ts04",
        "name": "Trà Sữa Chiều Bên Hiên",
        "category": "Trà sữa",
        "price": 42000,
        "desc": "Ngọt dịu, mềm mại như buổi chiều yên ả.",
        "image": "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=700&q=80",
        "emoji": "🌸"
    },
    {
        "id": "ts05",
        "name": "Trà Sữa Bức Thư Tình",
        "category": "Trà sữa",
        "price": 45000,
        "desc": "Hương vị ngọt ngào gửi trao những nhớ thương.",
        "image": "https://images.unsplash.com/photo-1525385133512-2f3bdd039054?auto=format&fit=crop&w=700&q=80",
        "emoji": "💌"
    },

    # ==================== MATCHA ====================
    {
        "id": "ma01",
        "name": "Matcha Ngọc Bích Đông Dương",
        "category": "Matcha",
        "price": 42000,
        "desc": "Matcha xanh mịn, thanh tao và tinh tế.",
        "image": "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=700&q=80",
        "emoji": "🍵"
    },
    {
        "id": "ma02",
        "name": "Matcha Nắng Qua Rèm",
        "category": "Matcha",
        "price": 45000,
        "desc": "Matcha hòa sữa tươi, dịu dàng như nắng sớm.",
        "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=700&q=80",
        "emoji": "🌿"
    },
    {
        "id": "ma03",
        "name": "Matcha Vườn Ngọc Lan",
        "category": "Matcha",
        "price": 47000,
        "desc": "Vị trà xanh thanh mát gợi nhớ khu vườn xưa.",
        "image": "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=700&q=80",
        "emoji": "🌼"
    },
    {
        "id": "ma04",
        "name": "Matcha Gác Mái Xưa",
        "category": "Matcha",
        "price": 48000,
        "desc": "Matcha đậm vị, béo mịn và đầy lưu luyến.",
        "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=700&q=80",
        "emoji": "🏡"
    },
    {
        "id": "ma05",
        "name": "Matcha Trăng Bên Thềm",
        "category": "Matcha",
        "price": 49000,
        "desc": "Matcha thơm dịu, kết hợp đậu đỏ bùi ngọt.",
        "image": "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=700&q=80",
        "emoji": "🌙"
    },

    # ==================== CÀ PHÊ ====================
    {
        "id": "cf01",
        "name": "Cà Phê Phin Sài Gòn Xưa",
        "category": "Cà phê",
        "price": 29000,
        "desc": "Cà phê phin đậm đà, lưu giữ hương vị phố xưa.",
        "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=700&q=80",
        "emoji": "☕"
    },
    {
        "id": "cf02",
        "name": "Bạc Xỉu Góc Phố",
        "category": "Cà phê",
        "price": 32000,
        "desc": "Sữa thơm béo, cà phê thoảng nhẹ thân quen.",
        "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=700&q=80",
        "emoji": "🥛"
    },
    {
        "id": "cf03",
        "name": "Cà Phê Ban Công Cũ",
        "category": "Cà phê",
        "price": 33000,
        "desc": "Vị cà phê đậm sâu cho những phút giây lắng đọng.",
        "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=700&q=80",
        "emoji": "🏛️"
    },
    {
        "id": "cf04",
        "name": "Cà Phê Đêm Sài Thành",
        "category": "Cà phê",
        "price": 35000,
        "desc": "Đậm đà, mạnh mẽ như nhịp phố khi lên đèn.",
        "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=700&q=80",
        "emoji": "🌃"
    },
    {
        "id": "cf05",
        "name": "Cà Phê Thư Viện Cũ",
        "category": "Cà phê",
        "price": 38000,
        "desc": "Hương cà phê sâu lắng, hợp những ngày hoài niệm.",
        "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=700&q=80",
        "emoji": "📚"
    },
]


TOPPINGS = {
    "Không topping": 0,
    "Trân châu đen": 7000,
    "Trân châu trắng": 8000,
    "Thạch cà phê": 7000,
    "Pudding trứng": 9000,
    "Kem cheese": 10000,
    "Đậu đỏ": 8000,
}

VOUCHERS = {
    "HOAINIEM10": {
        "discount": 0.10,
        "min_order": 50000,
        "description": "Giảm 10% cho đơn từ 50.000đ"
    },
    "TRASUA15": {
        "discount": 0.15,
        "min_order": 100000,
        "description": "Giảm 15% cho đơn từ 100.000đ"
    },
    "DONGDUONG20": {
        "discount": 0.20,
        "min_order": 150000,
        "description": "Giảm 20% cho đơn từ 150.000đ"
    },
}

def money(amount):
    return f"{int(amount):,}".replace(",", ".") + "đ"

def go_to(page):
    st.session_state.page_nav = page

def subtotal():
    return sum(item["unit_price"] * item["quantity"]
               for item in st.session_state.cart)

def discount_amount():
    sub = subtotal()
    code = st.session_state.voucher_code
    voucher = VOUCHERS.get(code)
    if voucher and sub >= voucher["min_order"]:
        return int(sub * voucher["discount"])
    return 0

def total_amount():
    return max(0, subtotal() - discount_amount())

def clear_voucher():
    st.session_state.voucher_code = ""
    st.session_state.voucher_input = ""
    st.session_state.discount = 0

# =========================================================
# 5. SIDEBAR - ĐIỀU HƯỚNG THỐNG NHẤT
# =========================================================
with st.sidebar:
    st.markdown(
        "<div style='text-align:center;font-size:42px'>❖</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h2 style='text-align:center;font-size:25px'>TRÀ QUÁN<br>HOÀI NIỆM</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center;color:#D6B16D;letter-spacing:2px'>EST. 1968</p>",
        unsafe_allow_html=True
    )
    st.divider()

    pages = [
        "Trang chủ",
        "Khám phá thực đơn",
        "Giỏ hàng & thanh toán",
        "Vòng quay may mắn",
        "Đánh giá & phản hồi",
    ]

    st.radio(
        "DANH MỤC",
        pages,
        key="page_nav",
        label_visibility="visible"
    )

    st.divider()
    st.markdown("### 🧾 Đơn hàng của bạn")
    st.metric("Số món", sum(x["quantity"] for x in st.session_state.cart))
    st.metric("Tạm tính", money(subtotal()))

    if st.button("🛍️ Xem giỏ hàng", use_container_width=True):
        go_to("Giỏ hàng & thanh toán")
        st.rerun()

    st.markdown("---")
    st.caption("Một chút hoài niệm, một chút dịu dàng.")
    st.caption("Mở cửa mỗi ngày · 08:00 – 22:00")

# =========================================================
# 6. HEADER CHUNG
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-kicker">✦ Saigon · Indochine · Since 1968 ✦</div>
    <div class="hero-title">Trà Quán Hoài Niệm</div>
    <div class="ornament">❦ ━━━━━━━━━ ❦</div>
    <div class="hero-subtitle">
        Lưu giữ hương vị xưa · Trao gửi những điều thân quen
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 7. TRANG CHỦ
# =========================================================
if st.session_state.page_nav == "Trang chủ":
    st.markdown('<div class="section-label">WELCOME TO OUR TEA HOUSE</div>',
                unsafe_allow_html=True)
    st.title("Chạm vào miền ký ức")
    st.write(
        "Giữa nhịp sống hiện đại, Trà Quán Hoài Niệm mở ra một góc nhỏ "
        "mang hơi thở Đông Dương: màu đỏ trầm, ánh vàng hoài cổ, "
        "những họa tiết xưa và hương trà thân thuộc."
    )

    left, right = st.columns([1.1, 1])
    with left:
        st.image(
            "https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=1000&q=85",
            use_container_width=True
        )
    with right:
        st.markdown("### Câu chuyện của quán")
        st.write(
            "Chúng tôi tin rằng một ly trà ngon không chỉ nằm ở hương vị, "
            "mà còn ở cảm giác bình yên khi bạn ngồi lại, trò chuyện "
            "và dành thời gian cho những người thân yêu."
        )
        st.markdown("""
        <div class="info-card">
            <div class="section-label">OUR PHILOSOPHY</div>
            <h3>Thưởng trà — kể chuyện — nhớ thương</h3>
            <p>Không gian xưa, hương vị mới, sự chăm chút trong từng chiếc ly.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## Ba hương vị đặc trưng")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image(
            "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=600&q=80",
            use_container_width=True
        )
        st.markdown("### Trà sữa")
        st.caption("Béo thơm, ngọt dịu, thân quen.")
    with c2:
        st.image(
            "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=600&q=80",
            use_container_width=True
        )
        st.markdown("### Matcha")
        st.caption("Thanh mát, tinh tế, xanh ngọc.")
    with c3:
        st.image(
            "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=600&q=80",
            use_container_width=True
        )
        st.markdown("### Cà phê")
        st.caption("Đậm đà, sâu lắng, đậm chất Sài Gòn.")

    st.markdown("---")
    st.markdown("### Sẵn sàng cho một cuộc hẹn cùng hương vị xưa?")
    if st.button("✦ KHÁM PHÁ THỰC ĐƠN ✦", use_container_width=True):
        go_to("Khám phá thực đơn")
        st.rerun()

# =========================================================
# 8. THỰC ĐƠN VÀ THÊM MÓN
# =========================================================
elif st.session_state.page_nav == "Khám phá thực đơn":
    st.markdown('<div class="section-label">OUR SIGNATURE MENU</div>',
                unsafe_allow_html=True)
    st.title("Thực đơn hoài cổ")
    st.write("Chọn thức uống, tùy chỉnh theo sở thích và gửi lời nhắn riêng.")

    category = st.selectbox(
        "Chọn nhóm thức uống",
        ["Tất cả", "Trà sữa", "Matcha", "Cà phê"],
        key="menu_category"
    )

    products = [
        p for p in MENU
        if category == "Tất cả" or p["category"] == category
    ]

    for start in range(0, len(products), 2):
        cols = st.columns(2)
        for col, product in zip(cols, products[start:start + 2]):
            with col:
                st.markdown('<div class="menu-card">', unsafe_allow_html=True)
                try:
                    st.image(product["image"], use_container_width=True)
                except Exception:
                    st.markdown(
                        f"<div style='font-size:60px;text-align:center'>{product['emoji']}</div>",
                        unsafe_allow_html=True
                    )
                st.markdown(f"### {product['emoji']} {product['name']}")
                st.markdown(
                    f"<div class='price'>{money(product['price'])}</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<div class='small-muted'>{product['desc']}</div>",
                    unsafe_allow_html=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

                pid = product["id"]

                topping = st.selectbox(
                    "Topping",
                    list(TOPPINGS.keys()),
                    key=f"topping_{pid}"
                )
                sweetness = st.select_slider(
                    "Độ ngọt",
                    options=["0%", "30%", "50%", "70%", "100%"],
                    value="70%",
                    key=f"sweet_{pid}"
                )
                ice = st.selectbox(
                    "Lượng đá",
                    ["Không đá", "Ít đá", "Bình thường", "Nhiều đá"],
                    index=1,
                    key=f"ice_{pid}"
                )
                quantity = st.number_input(
                    "Số lượng",
                    min_value=1,
                    max_value=20,
                    value=1,
                    step=1,
                    key=f"qty_{pid}"
                )
                note = st.text_input(
                    "Lời nhắn riêng",
                    placeholder="Ví dụ: Ghi tên lên ly...",
                    key=f"note_{pid}"
                )

                unit_price = product["price"] + TOPPINGS[topping]
                st.caption(
                    f"Giá mỗi ly đã chọn topping: {money(unit_price)}"
                )

                if st.button(
                    f"＋ Thêm {product['name']}",
                    key=f"add_{pid}",
                    use_container_width=True
                ):
                    # Mỗi cấu hình thức uống có mã riêng để dễ xóa/sửa.
                    cart_item = {
                        "cart_id": str(uuid.uuid4()),
                        "product_id": pid,
                        "name": product["name"],
                        "category": product["category"],
                        "base_price": product["price"],
                        "topping": topping,
                        "topping_price": TOPPINGS[topping],
                        "sweetness": sweetness,
                        "ice": ice,
                        "note": note.strip(),
                        "quantity": int(quantity),
                        "unit_price": unit_price,
                    }
                    st.session_state.cart.append(cart_item)
                    st.success("Đã thêm món vào giỏ hàng!")
                    st.rerun()

    st.markdown("---")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("← Về trang chủ", use_container_width=True):
            go_to("Trang chủ")
            st.rerun()
    with b2:
        if st.button("🛒 Xem giỏ hàng", use_container_width=True):
            go_to("Giỏ hàng & thanh toán")
            st.rerun()

# =========================================================
# 9. GIỎ HÀNG, VOUCHER VÀ HÓA ĐƠN
# =========================================================
elif st.session_state.page_nav == "Giỏ hàng & thanh toán":
    st.markdown('<div class="section-label">YOUR ORDER</div>',
                unsafe_allow_html=True)
    st.title("Giỏ hàng & hóa đơn")

    if not st.session_state.cart:
        st.info("Giỏ hàng đang trống. Hãy chọn món yêu thích của bạn nhé!")
        if st.button("Khám phá thực đơn", use_container_width=True):
            go_to("Khám phá thực đơn")
            st.rerun()
    else:
        st.markdown("### Chi tiết món đã chọn")

        for item in st.session_state.cart[:]:
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                with c1:
                    st.markdown(f"**{item['name']}**")
                    st.caption(
                        f"Topping: {item['topping']} · "
                        f"Ngọt: {item['sweetness']} · Đá: {item['ice']}"
                    )
                    if item["note"]:
                        st.caption(f"Lời nhắn: {item['note']}")
                    st.caption(f"Đơn giá: {money(item['unit_price'])}")
                with c2:
                    st.markdown("**Số lượng**")
                    new_qty = st.number_input(
                        "SL",
                        min_value=1,
                        max_value=20,
                        value=int(item["quantity"]),
                        step=1,
                        key=f"cart_qty_{item['cart_id']}",
                        label_visibility="collapsed"
                    )
                    if int(new_qty) != item["quantity"]:
                        item["quantity"] = int(new_qty)
                        st.rerun()
                with c3:
                    st.markdown("**Thành tiền**")
                    st.write(money(item["unit_price"] * item["quantity"]))
                    if st.button(
                        "🗑️ Xóa",
                        key=f"remove_{item['cart_id']}"
                    ):
                        st.session_state.cart = [
                            x for x in st.session_state.cart
                            if x["cart_id"] != item["cart_id"]
                        ]
                        st.rerun()

        st.markdown("### 🎟️ Mã ưu đãi")
        st.caption(
            "HOAINIEM10 · TRASUA15 · DONGDUONG20"
        )

        with st.form("voucher_form"):
            voucher_input = st.text_input(
                "Nhập mã voucher",
                value=st.session_state.voucher_code,
                placeholder="Ví dụ: HOAINIEM10"
            )
            v1, v2 = st.columns(2)
            with v1:
                apply_voucher = st.form_submit_button(
                    "Áp dụng voucher",
                    use_container_width=True
                )
            with v2:
                remove_voucher = st.form_submit_button(
                    "Bỏ voucher",
                    use_container_width=True
                )

            if apply_voucher:
                code = voucher_input.strip().upper()
                if code not in VOUCHERS:
                    st.session_state.voucher_code = ""
                    st.session_state.discount = 0
                    st.error("Mã voucher không hợp lệ.")
                elif subtotal() < VOUCHERS[code]["min_order"]:
                    st.session_state.voucher_code = ""
                    st.session_state.discount = 0
                    st.error(
                        "Đơn hàng chưa đạt giá trị tối thiểu: "
                        + money(VOUCHERS[code]["min_order"])
                    )
                else:
                    st.session_state.voucher_code = code
                    st.session_state.discount = discount_amount()
                    st.success(
                        f"Áp dụng thành công: "
                        f"{VOUCHERS[code]['description']}"
                    )
                st.rerun()

            if remove_voucher:
                clear_voucher()
                st.rerun()

        # Kiểm tra lại điều kiện voucher sau khi thay đổi số lượng/xóa món.
        current_code = st.session_state.voucher_code
        if current_code:
            if (
                current_code not in VOUCHERS
                or subtotal() < VOUCHERS[current_code]["min_order"]
            ):
                clear_voucher()
                st.warning("Voucher đã được gỡ vì đơn hàng không còn đủ điều kiện.")
                st.rerun()

        sub = subtotal()
        disc = discount_amount()
        total = total_amount()

        st.markdown("---")
        st.markdown("### Hóa đơn tạm tính")

        r1, r2 = st.columns(2)
        with r1:
            st.write("Tạm tính")
            st.write("Giảm giá")
            st.markdown("**TỔNG THANH TOÁN**")
        with r2:
            st.write(money(sub))
            st.write(f"- {money(disc)}")
            st.markdown(
                f"<div class='price' style='font-size:26px'>{money(total)}</div>",
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("### Thông tin nhận đơn")
        customer_name = st.text_input(
            "Tên khách hàng",
            key="customer_name",
            placeholder="Nhập tên của bạn"
        )

        st.markdown("### Phương thức thanh toán")
        payment_method = st.radio(
            "Chọn phương thức",
            ["Tiền mặt tại quán", "Quét mã QR minh họa"],
            horizontal=True,
            key="payment_choice"
        )

        if payment_method == "Quét mã QR minh họa":
            st.info(
                "Đây là QR minh họa cho giao diện demo, "
                "không phải mã thanh toán ngân hàng thực."
            )
            qr_text = (
                f"HOAI NIEM DEMO | "
                f"{customer_name or 'Khach hang'} | {total} VND"
            )
            st.markdown(
                f"""
                <div style="background:#F6EAD4;color:#32121B;
                max-width:360px;padding:20px;text-align:center;
                border:3px solid #D6B16D;margin:10px auto">
                    <div style="font-size:18px;font-weight:bold">
                        TRÀ QUÁN HOÀI NIỆM
                    </div>
                    <div style="font-size:12px;margin:8px">
                        MÃ QR MINH HỌA
                    </div>
                    <div style="font-size:76px;line-height:1.2">▦</div>
                    <div style="font-size:25px;font-weight:bold">
                        {money(total)}
                    </div>
                    <div style="font-size:11px;margin-top:8px">
                        {qr_text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.button(
            "✓ XÁC NHẬN THANH TOÁN",
            use_container_width=True
        ):
            if not customer_name.strip():
                st.error("Vui lòng nhập tên khách hàng trước khi xác nhận.")
            else:
                st.session_state.paid = True
                st.session_state.payment_method = payment_method
                st.session_state.order_id = (
                    "HN" + datetime.now().strftime("%y%m%d%H%M%S")
                )
                st.session_state.last_total = total
                st.session_state.last_subtotal = sub
                st.session_state.last_discount = disc
                st.session_state.last_items = [
                    item.copy() for item in st.session_state.cart
                ]
                st.session_state.cart = []
                clear_voucher()
                st.session_state.feedback_sent = False
                go_to("Đánh giá & phản hồi")
                st.rerun()

        if st.button("← Tiếp tục chọn món", use_container_width=True):
            go_to("Khám phá thực đơn")
            st.rerun()

# =========================================================
# 10. VÒNG QUAY MAY MẮN
# =========================================================
elif st.session_state.page_nav == "Vòng quay may mắn":
    st.markdown('<div class="section-label">A LITTLE GIFT FOR YOU</div>',
                unsafe_allow_html=True)
    st.title("Vòng quay may mắn")
    st.write(
        "Mỗi lượt quay mang đến một bất ngờ nho nhỏ. "
        "Hãy thử vận may của bạn tại Trà Quán Hoài Niệm!"
    )

    prizes = [
        {"name": "Giảm 10% đơn hàng", "code": "HOAINIEM10"},
        {"name": "Giảm 15% đơn từ 100.000đ", "code": "TRASUA15"},
        {"name": "Tặng topping miễn phí", "code": "TOPPINGFREE"},
        {"name": "Giảm 20% đơn từ 150.000đ", "code": "DONGDUONG20"},
        {"name": "Chúc bạn một ngày an lành", "code": "LOICHUC"},
        {"name": "Tặng một lời chúc hoài niệm", "code": "HOAINIEM"},
    ]

    st.markdown("""
    <div class="info-card" style="text-align:center">
        <div style="font-size:82px">🎡</div>
        <h2>Vòng quay ký ức</h2>
        <p>Một chút may mắn — một chút ngọt ngào</p>
        <div class="ornament">❦ ✦ ❦</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎁 QUAY NGAY", use_container_width=True):
        prize = random.choice(prizes)
        st.session_state.spin_result = prize
        st.session_state.spin_history.append({
            "time": datetime.now().strftime("%H:%M:%S %d/%m/%Y"),
            "name": prize["name"],
            "code": prize["code"],
        })
        st.session_state.gift_claimed = False

    if st.session_state.spin_result:
        prize = st.session_state.spin_result
        st.success(f"🎉 Chúc mừng! Bạn nhận được: {prize['name']}")
        st.markdown(
            f"<div class='info-card' style='text-align:center'>"
            f"<div class='section-label'>YOUR GIFT</div>"
            f"<h2>{prize['name']}</h2>"
            f"<p>Mã quà tặng: <b>{prize['code']}</b></p>"
            f"</div>",
            unsafe_allow_html=True
        )

        if prize["code"] in VOUCHERS:
            if st.button("Lưu voucher vào đơn hàng"):
                st.session_state.voucher_code = prize["code"]
                st.session_state.voucher_input = prize["code"]
                st.session_state.gift_claimed = True
                st.success("Đã lưu mã vào phiên đặt hàng hiện tại.")
        elif prize["code"] == "TOPPINGFREE":
            st.info(
                "Quà tặng topping được minh họa trong bản demo. "
                "Khi vận hành thực tế, quán cần xác nhận quà tại quầy."
            )
        else:
            st.info("Hãy lưu lại lời chúc dễ thương này nhé!")

    if st.session_state.spin_history:
        st.markdown("### Lịch sử vòng quay trong phiên hiện tại")
        for result in reversed(st.session_state.spin_history):
            st.write(
                f"🎁 {result['time']} — {result['name']} "
                f"({result['code']})"
            )

    st.caption(
        "Lưu ý: vòng quay và quà tặng hoạt động trong phiên demo; "
        "mỗi lần tải lại phiên hoặc khởi động lại ứng dụng có thể làm "
        "mất lịch sử. Quà không tự động đổi thành tiền mặt."
    )

# =========================================================
# 11. ĐÁNH GIÁ VÀ PHẢN HỒI SAU THANH TOÁN
# =========================================================
elif st.session_state.page_nav == "Đánh giá & phản hồi":
    st.markdown('<div class="section-label">YOUR WORDS MATTER</div>',
                unsafe_allow_html=True)
    st.title("Đánh giá & phản hồi")

    if not st.session_state.paid:
        st.info(
            "Cảm nhận của bạn rất quan trọng. "
            "Sau khi hoàn tất thanh toán, bạn có thể gửi đánh giá tại đây."
        )
        if st.button("← Về trang chủ", use_container_width=True):
            go_to("Trang chủ")
            st.rerun()
    else:
        st.success("Thanh toán đã được xác nhận trong bản demo. Cảm ơn bạn!")

        st.markdown(f"""
        <div class="info-card">
            <div class="section-label">PAYMENT CONFIRMATION</div>
            <h3>Trà Quán Hoài Niệm</h3>
            <p>Mã đơn: <b>{st.session_state.order_id}</b></p>
            <p>Khách hàng: <b>{st.session_state.customer_name}</b></p>
            <p>Phương thức: <b>{st.session_state.payment_method}</b></p>
            <h2>Tổng thanh toán: {money(st.session_state.last_total)}</h2>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.last_items:
            with st.expander("Xem lại hóa đơn đã thanh toán"):
                for item in st.session_state.last_items:
                    st.write(
                        f"**{item['name']}** × {item['quantity']} — "
                        f"{money(item['unit_price'] * item['quantity'])}"
                    )
                    st.caption(
                        f"{item['topping']} · Ngọt {item['sweetness']} · "
                        f"{item['ice']}"
                    )
                st.write(f"Tạm tính: {money(st.session_state.last_subtotal)}")
                st.write(f"Giảm giá: {money(st.session_state.last_discount)}")
                st.write(f"Tổng cộng: {money(st.session_state.last_total)}")

        if not st.session_state.feedback_sent:
            st.markdown("### 🌸 Một vài lời gửi đến quán")
            st.write("Trải nghiệm của bạn hôm nay như thế nào?")

            rating = st.select_slider(
                "Bạn chấm quán bao nhiêu sao?",
                options=[1, 2, 3, 4, 5],
                value=st.session_state.rating,
                format_func=lambda x: "⭐" * x,
                key="feedback_rating"
            )
            feedback = st.text_area(
                "Lời nhắn dành cho chúng mình",
                placeholder="Hương vị, dịch vụ, không gian... "
                            "Bạn cứ chia sẻ thật lòng nhé!",
                key="feedback_message"
            )

            if st.button("GỬI ĐÁNH GIÁ", use_container_width=True):
                st.session_state.rating = rating
                st.session_state.feedback = feedback.strip()
                st.session_state.feedback_sent = True
                st.session_state.paid = False
                st.rerun()
        else:
            st.success(
                f"Cảm ơn bạn đã đánh giá "
                f"{'⭐' * st.session_state.rating}!"
            )
            if st.session_state.feedback:
                st.markdown(
                    f"<div class='info-card'>"
                    f"<div class='section-label'>LỜI NHẮN CỦA BẠN</div>"
                    f"<p>{st.session_state.feedback}</p>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            st.caption(
                "Đánh giá đang được lưu trong phiên ứng dụng hiện tại. "
                "Để lưu lâu dài, cần tích hợp cơ sở dữ liệu."
            )

        if st.button("🏠 Trở về trang chủ", use_container_width=True):
            go_to("Trang chủ")
            st.rerun()

# =========================================================
# 12. CHÂN TRANG
# =========================================================
st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:10px 0 20px 0">
    <div style="color:#D6B16D;letter-spacing:4px">❦ HOÀI NIỆM ❦</div>
    <p style="color:#D6BBA5;font-size:12px">
        Trà Quán Hoài Niệm · Indochine Tea House
    </p>
    <p style="color:#D6BBA5;font-size:11px">
        Một tách trà — ngàn câu chuyện.
    </p>
</div>
""", unsafe_allow_html=True)
