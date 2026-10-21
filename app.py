
import streamlit as st
import random
import qrcode
from io import BytesIO
from datetime import datetime

# =========================================================
# 1. CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="Trà Quán Hoài Niệm",
    page_icon="🍵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. BẢNG MÀU VÀ GIAO DIỆN
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap');

.stApp {
    background: #f6f0e5;
    color: #453a2d;
    font-family: 'Be Vietnam Pro', sans-serif;
}
[data-testid="stSidebar"] {
    background: #e8ddc9;
    border-right: 1px solid #c9b89b;
}
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #4d3b29 !important;
}
p, label, span {
    color: #514536;
}
.hero {
    padding: 36px 30px;
    border-radius: 14px;
    background: linear-gradient(120deg, #4d3b29, #796344);
    color: #fff8e9;
    margin-bottom: 22px;
}
.hero h1, .hero h2, .hero p {
    color: #fff8e9 !important;
}
.hero h1 {
    font-size: 42px;
    margin-bottom: 8px;
}
.subtitle {
    color: #e8d9bc !important;
    font-size: 15px;
}
.section-label {
    color: #8a6c43;
    letter-spacing: 3px;
    font-size: 12px;
    font-weight: 700;
}
.menu-card {
    padding: 15px;
    background: #fffaf1;
    border: 1px solid #e1d2ba;
    border-radius: 12px;
    margin-bottom: 12px;
}
.price {
    color: #7a4e25;
    font-size: 20px;
    font-weight: 700;
}
.note {
    padding: 12px 16px;
    background: #ece4d2;
    border-left: 4px solid #8c754c;
    border-radius: 5px;
    margin: 10px 0;
}
.bill {
    padding: 22px;
    background: #fffaf1;
    border: 1px dashed #9c835e;
    border-radius: 10px;
}
.small-muted {
    color: #887b67;
    font-size: 12px;
}
div.stButton > button {
    background: #5a4934;
    color: #fff9eb;
    border: 1px solid #5a4934;
    border-radius: 8px;
    min-height: 42px;
}
div.stButton > button:hover {
    background: #826747;
    color: white;
    border-color: #826747;
}
div[data-testid="stFormSubmitButton"] button {
    background: #5a4934;
    color: white;
}
hr {
    border-color: #d9cbb4;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. THỰC ĐƠN
# =========================================================
MENU = {
    "Trà sữa": [
        {
            "name": "Trà Sữa Cô Ba",
            "price": 35000,
            "image": "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=700&q=80",
            "description": "Trà đen thơm dịu, sữa béo vừa, ngọt ngào như ký ức.",
            "message": "Cô Ba gửi bạn một chút ngọt ngào của những ngày xưa cũ!"
        },
        {
            "name": "Trà Sữa Gánh Hàng Rong",
            "price": 39000,
            "image": "https://images.unsplash.com/photo-1525385133512-2f3bdd039054?auto=format&fit=crop&w=700&q=80",
            "description": "Vị trà đậm đà, sữa thơm, lưu giữ nét thân quen của phố xưa.",
            "message": "Mời bạn nhâm nhi một ly trà, nghe phố kể chuyện ngày xưa."
        },
        {
            "name": "Trà Sữa Phố Hội",
            "price": 42000,
            "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=700&q=80",
            "description": "Trà sữa thơm mượt, lấy cảm hứng từ nét trầm mặc phố cổ.",
            "message": "Chúc bạn có một chuyến dạo chơi thật an yên tại Phố Hội!"
        },
        {
            "name": "Trà Sữa Mợ Hai",
            "price": 40000,
            "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=700&q=80",
            "description": "Vị trà thanh, sữa dịu, nhẹ nhàng và tinh tế.",
            "message": "Mợ Hai chúc bạn hôm nay gặp toàn điều dễ thương!"
        }
    ],
    "Matcha": [
        {
            "name": "Matcha Ngọc Bích",
            "price": 42000,
            "image": "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=700&q=80",
            "description": "Matcha xanh mịn, thơm dịu, hòa cùng sữa tươi.",
            "message": "Một chút xanh bình yên, mong ngày của bạn dịu dàng hơn."
        },
        {
            "name": "Matcha Sữa Cô Tư",
            "price": 45000,
            "image": "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&w=700&q=80",
            "description": "Matcha đậm vị, sữa béo nhẹ, hậu vị thanh.",
            "message": "Cô Tư mời bạn một ly xanh mát, uống là thấy thương!"
        },
        {
            "name": "Matcha Đêm Trăng",
            "price": 47000,
            "image": "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=700&q=80",
            "description": "Matcha sữa mềm mượt, cảm hứng từ đêm trăng tĩnh lặng.",
            "message": "Chúc tâm hồn bạn nhẹ như ánh trăng đêm nay."
        }
    ]
}

TOPPINGS = {
    "Không topping": 0,
    "Trân châu đen": 7000,
    "Trân châu trắng": 8000,
    "Thạch củ năng": 8000,
    "Pudding trứng": 10000,
    "Kem cheese": 12000
}

SWEETNESS = ["0%", "30%", "50%", "70%", "100%"]
ICE = ["Có đá", "Ít đá", "Không đá"]

VOUCHERS = {
    "HOAINIEM10": 0.10,
    "COBA15": 0.15,
    "TRAXUA20": 0.20
}

# =========================================================
# 4. KHỞI TẠO TRẠNG THÁI
# =========================================================
if "cart" not in st.session_state:
    st.session_state.cart = []

if "page" not in st.session_state:
    st.session_state.page = "Trang chủ"

if "voucher" not in st.session_state:
    st.session_state.voucher = ""

if "voucher_applied" not in st.session_state:
    st.session_state.voucher_applied = ""

if "spin_result" not in st.session_state:
    st.session_state.spin_result = None

if "used_spin" not in st.session_state:
    st.session_state.used_spin = False

if "payment_method" not in st.session_state:
    st.session_state.payment_method = "Tiền mặt"

# =========================================================
# 5. HÀM HỖ TRỢ
# =========================================================
def money(value):
    return f"{int(value):,}".replace(",", ".") + " đ"

def go_to(page):
    st.session_state.page = page

def add_to_cart(product, quantity, topping, sweetness, ice):
    unit_price = product["price"] + TOPPINGS[topping]

    st.session_state.cart.append({
        "name": product["name"],
        "base_price": product["price"],
        "topping": topping,
        "topping_price": TOPPINGS[topping],
        "sweetness": sweetness,
        "ice": ice,
        "quantity": quantity,
        "unit_price": unit_price,
        "subtotal": unit_price * quantity,
        "message": product["message"]
    })

def cart_subtotal():
    return sum(item["subtotal"] for item in st.session_state.cart)

def discount_rate():
    code = st.session_state.voucher_applied
    return VOUCHERS.get(code, 0)

def discount_amount():
    return int(cart_subtotal() * discount_rate())

def grand_total():
    return max(0, cart_subtotal() - discount_amount())

def show_product_image(url, caption):
    try:
        st.image(url, use_container_width=True, caption=caption)
    except Exception:
        st.info("Chưa tải được ảnh. Vui lòng kiểm tra kết nối Internet.")

def create_demo_qr(amount):
    # QR này chỉ chứa nội dung minh họa, chưa phải QR chuyển khoản ngân hàng.
    content = (
        "TRA QUAN HOAI NIEM - MA THANH TOAN MINH HOA\n"
        f"So tien: {amount} VND\n"
        "Vui long thay bang QR ngan hang cua quan truoc khi su dung."
    )
    qr = qrcode.QRCode(box_size=7, border=3)
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#4d3b29", back_color="#fffaf1")
    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output

def clear_voucher():
    st.session_state.voucher_applied = ""
    st.session_state.voucher = ""

# =========================================================
# 6. THANH ĐIỀU HƯỚNG
# =========================================================
with st.sidebar:
    st.markdown("## 🍵 Trà Quán")
    st.caption("HOÀI NIỆM • HƯƠNG XƯA • VỊ CŨ")
    st.divider()

    pages = [
        "Trang chủ",
        "Khám phá thực đơn",
        "Giỏ hàng & thanh toán",
        "Vòng quay may mắn",
        "Về chúng tôi"
    ]

    current_index = (
        pages.index(st.session_state.page)
        if st.session_state.page in pages else 0
    )

selected_page = st.radio(
    "MENU",
    pages,
    index=None,
    key="main_navigation"
)

if selected_page is not None:
    st.session_state.page = selected_page

    st.divider()
    st.markdown("### 🧺 Giỏ hàng")
    st.write(f"**{len(st.session_state.cart)}** lượt chọn món")

    if st.session_state.cart:
        st.write("Tạm tính:", money(cart_subtotal()))

    if st.button("🛍️ Xem giỏ hàng", use_container_width=True):
        go_to("Giỏ hàng & thanh toán")
        st.rerun()

    st.markdown("---")
    st.caption("Một góc nhỏ lưu giữ hương vị xưa.")

# =========================================================
# 7. TRANG CHỦ
# =========================================================
if st.session_state.page == "Trang chủ":
    st.markdown("""
    <div class="hero">
        <div class="section-label" style="color:#e4cda7">
            CHÀO MỪNG BẠN GHÉ THĂM
        </div>
        <h1>Trà Quán Hoài Niệm</h1>
        <p class="subtitle">
            Một chút hương xưa · Một chút vị trà · Một khoảng bình yên
        </p>
        <p>
            Giữa nhịp sống vội vàng, hãy dừng chân để thưởng thức
            một ly trà mang hương vị thân quen.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 1])

    with col1:
        st.markdown("### Nơi ký ức được pha thành vị")
        st.write("""
        Lấy cảm hứng từ những con phố cũ, quán nước ven đường,
        chiếc radio xưa và những câu chuyện bên tách trà,
        Trà Quán Hoài Niệm mong muốn đem đến trải nghiệm gần gũi
        nhưng vẫn thật đặc biệt.

        Mỗi thức uống là một câu chuyện nhỏ. Mỗi lần ghé thăm
        là một lần bạn có thể sống chậm lại, tận hưởng khoảnh khắc
        của riêng mình.
        """)
        if st.button("📜 Khám phá thực đơn", use_container_width=True):
            go_to("Khám phá thực đơn")
            st.rerun()

    with col2:
        show_product_image(
            "https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=1000&q=85",
            "Một góc trà mang phong vị hoài cổ"
        )

    st.markdown("---")
    st.markdown("### ✨ Những điều nhỏ xinh tại quán")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 🍃")
        st.markdown("**Hương vị thân quen**")
        st.write("Trà sữa và matcha được đặt tên theo những câu chuyện xưa.")
    with c2:
        st.markdown("#### 🎁")
        st.markdown("**Quà tặng bất ngờ**")
        st.write("Thử vận may để nhận voucher hoặc món quà nhỏ.")
    with c3:
        st.markdown("#### 🧾")
        st.markdown("**Đặt món tiện lợi**")
        st.write("Tùy chỉnh thức uống, topping và xem hóa đơn ngay.")

# =========================================================
# 8. KHÁM PHÁ THỰC ĐƠN
# =========================================================
elif st.session_state.page == "Khám phá thực đơn":
    st.markdown("""
    <div class="hero">
        <div class="section-label" style="color:#e4cda7">MENU • 01</div>
        <h1>Thực đơn nhà trà</h1>
        <p class="subtitle">
            Chọn một hương vị, gửi gắm một tâm tình.
        </p>
    </div>
    """, unsafe_allow_html=True)

    category = st.radio(
        "Chọn nhóm thức uống",
        ["Trà sữa", "Matcha"],
        horizontal=True,
        key="drink_category"
    )

    st.caption("Giá tính bằng VNĐ. Topping được tính thêm vào giá món.")

    products = MENU[category]

    for idx, product in enumerate(products):
        with st.container(border=True):
            image_col, detail_col = st.columns([0.9, 1.3])

            with image_col:
                show_product_image(product["image"], product["name"])

            with detail_col:
                st.markdown(f"### {product['name']}")
                st.markdown(
                    f'<div class="price">{money(product["price"])}</div>',
                    unsafe_allow_html=True
                )
                st.write(product["description"])
                st.markdown(
                    f'<div class="note">💌 {product["message"]}</div>',
                    unsafe_allow_html=True
                )

                with st.form(key=f"form_{category}_{idx}"):
                    st.markdown("**Tùy chỉnh ly của bạn**")

                    quantity = st.number_input(
                        "Số lượng",
                        min_value=1,
                        max_value=20,
                        value=1,
                        step=1,
                        key=f"qty_{category}_{idx}"
                    )

                    topping = st.selectbox(
                        "Topping",
                        list(TOPPINGS.keys()),
                        key=f"top_{category}_{idx}"
                    )

                    sweetness = st.select_slider(
                        "Độ ngọt",
                        options=SWEETNESS,
                        value="50%",
                        key=f"sweet_{category}_{idx}"
                    )

                    ice = st.radio(
                        "Lượng đá",
                        ICE,
                        horizontal=True,
                        key=f"ice_{category}_{idx}"
                    )

                    unit = product["price"] + TOPPINGS[topping]
                    st.write("Giá mỗi ly:", money(unit))
                    st.write("Thành tiền:", money(unit * quantity))

                    submitted = st.form_submit_button(
                        "➕ Thêm vào giỏ hàng",
                        use_container_width=True
                    )

                    if submitted:
                        add_to_cart(
                            product,
                            quantity,
                            topping,
                            sweetness,
                            ice
                        )
                        st.session_state[
                            f"notice_{category}_{idx}"
                        ] = product["message"]
                        st.session_state[
                            f"added_{category}_{idx}"
                        ] = True

                if st.session_state.get(f"added_{category}_{idx}", False):
                    st.success("Đã thêm món vào giỏ hàng!")
                    st.info(
                        st.session_state.get(
                            f"notice_{category}_{idx}", product["message"]
                        )
                    )

    st.divider()
    left, right = st.columns(2)

    with left:
        if st.button("🏠 Về trang chủ", use_container_width=True):
            go_to("Trang chủ")
            st.rerun()

    with right:
        if st.button("🧺 Sang giỏ hàng", use_container_width=True):
            go_to("Giỏ hàng & thanh toán")
            st.rerun()

# =========================================================
# 9. GIỎ HÀNG VÀ THANH TOÁN
# =========================================================
elif st.session_state.page == "Giỏ hàng & thanh toán":
    st.markdown("""
    <div class="hero">
        <div class="section-label" style="color:#e4cda7">ORDER • 02</div>
        <h1>Giỏ hàng & thanh toán</h1>
        <p class="subtitle">
            Kiểm tra món đã chọn trước khi hoàn tất đơn hàng.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.cart:
        st.info("Giỏ hàng đang trống. Mời bạn chọn thức uống yêu thích!")
        if st.button("📜 Khám phá thực đơn", use_container_width=True):
            go_to("Khám phá thực đơn")
            st.rerun()
    else:
        st.markdown("### 🧺 Các món đã chọn")

        for i, item in enumerate(st.session_state.cart):
            with st.container(border=True):
                a, b, c = st.columns([3, 1.2, 0.8])

                with a:
                    st.markdown(f"**{item['name']}**")
                    st.caption(
                        f"Topping: {item['topping']} | "
                        f"Ngọt: {item['sweetness']} | "
                        f"{item['ice']}"
                    )
                    st.caption(
                        f"{money(item['base_price'])} + "
                        f"{money(item['topping_price'])}/ly"
                    )

                with b:
                    st.write(f"Số lượng: **{item['quantity']}**")
                    st.write(money(item["subtotal"]))

                with c:
                    if st.button("🗑️ Xóa", key=f"delete_{i}"):
                        st.session_state.cart.pop(i)
                        st.rerun()

        st.divider()
        st.markdown("### 🎟️ Mã ưu đãi")

        voucher_col, apply_col = st.columns([2, 1])

        with voucher_col:
            voucher_input = st.text_input(
                "Nhập mã voucher",
                value=st.session_state.voucher,
                placeholder="Ví dụ: HOAINIEM10",
                key="voucher_input_box"
            )

        with apply_col:
            st.write("")
            st.write("")
            if st.button("Áp dụng mã", use_container_width=True):
                code = voucher_input.strip().upper()

                if code in VOUCHERS:
                    st.session_state.voucher = code
                    st.session_state.voucher_applied = code
                    st.success(
                        f"Áp dụng thành công: giảm "
                        f"{int(VOUCHERS[code] * 100)}%!"
                    )
                else:
                    st.session_state.voucher = voucher_input.strip()
                    st.session_state.voucher_applied = ""
                    st.error("Mã không hợp lệ. Vui lòng kiểm tra lại.")

        if st.session_state.voucher_applied:
            st.success(
                f"Đang dùng mã {st.session_state.voucher_applied} "
                f"(-{int(discount_rate() * 100)}%)."
            )
            if st.button("Bỏ voucher"):
                clear_voucher()
                st.rerun()

        st.divider()
        st.markdown("### 🧾 Hóa đơn tạm tính")

        st.markdown('<div class="bill">', unsafe_allow_html=True)
        st.markdown("#### TRÀ QUÁN HOÀI NIỆM")
        st.caption(
            "Thời gian: " + datetime.now().strftime("%d/%m/%Y %H:%M")
        )
        st.caption("HÓA ĐƠN ĐẶT MÓN")

        for item in st.session_state.cart:
            st.write(
                f"**{item['name']}** — "
                f"{item['quantity']} × {money(item['unit_price'])} "
                f"= **{money(item['subtotal'])}**"
            )

        st.markdown("---")
        st.write(f"Tạm tính: **{money(cart_subtotal())}**")
        st.write(f"Giảm giá: **- {money(discount_amount())}**")
        st.markdown(
            f"## Tổng cộng: {money(grand_total())}"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()
        st.markdown("### 💳 Phương thức thanh toán")

        payment = st.radio(
            "Bạn muốn thanh toán bằng cách nào?",
            ["Tiền mặt", "Quét mã QR"],
            horizontal=True,
            key="payment_choice"
        )
        st.session_state.payment_method = payment

        if payment == "Tiền mặt":
            st.info(
                "Bạn chọn thanh toán tiền mặt. Vui lòng thanh toán "
                "cho nhân viên khi nhận món."
            )
        else:
            st.warning(
                "QR bên dưới là mã minh họa, KHÔNG phải QR nhận tiền thật. "
                "Chủ quán cần thay bằng QR ngân hàng của mình trước khi sử dụng."
            )
            qr_col1, qr_col2 = st.columns([1, 1.4])

            with qr_col1:
                st.image(
                    create_demo_qr(grand_total()),
                    caption="QR minh họa — chưa thể chuyển khoản",
                    width=230
                )

            with qr_col2:
                st.markdown("#### Thông tin thanh toán")
                st.write("Đơn vị: Trà Quán Hoài Niệm")
                st.write("Số tiền:", money(grand_total()))
                st.write("Nội dung: TRAQUAN HOAINIEM")
                st.caption(
                    "Khi triển khai thật, hãy dùng QR thanh toán do ngân hàng "
                    "hoặc nhà cung cấp thanh toán của quán tạo ra."
                )

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("➕ Chọn thêm món", use_container_width=True):
                go_to("Khám phá thực đơn")
                st.rerun()

        with col2:
            if st.button("🧹 Xóa toàn bộ", use_container_width=True):
                st.session_state.cart = []
                clear_voucher()
                st.rerun()

        with col3:
            if st.button("✅ Xác nhận đặt món", use_container_width=True):
                st.session_state.order_confirmation = {
                    "items": [item.copy() for item in st.session_state.cart],
                    "subtotal": cart_subtotal(),
                    "discount": discount_amount(),
                    "total": grand_total(),
                    "payment": st.session_state.payment_method,
                    "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }
                go_to("Đơn hàng đã xác nhận")
                st.rerun()

# =========================================================
# 10. KẾT QUẢ ĐẶT MÓN
# =========================================================
elif st.session_state.page == "Đơn hàng đã xác nhận":
    order = st.session_state.get("order_confirmation")

    st.markdown("""
    <div class="hero">
        <div class="section-label" style="color:#e4cda7">THANK YOU</div>
        <h1>Cảm ơn bạn đã ghé quán!</h1>
        <p class="subtitle">Một ly trà, một niềm vui nho nhỏ.</p>
    </div>
    """, unsafe_allow_html=True)

    if order:
        st.success("Đơn hàng đã được ghi nhận trên ứng dụng demo.")
        st.caption(f"Thời gian: {order['time']}")

        st.markdown("### 🧾 Hóa đơn")
        for item in order["items"]:
            st.write(
                f"- **{item['name']}** × {item['quantity']} — "
                f"{money(item['subtotal'])}"
            )
            st.caption(
                f"Topping: {item['topping']} | "
                f"Độ ngọt: {item['sweetness']} | {item['ice']}"
            )

        st.write(f"Tạm tính: {money(order['subtotal'])}")
        st.write(f"Giảm giá: -{money(order['discount'])}")
        st.markdown(f"## Tổng thanh toán: {money(order['total'])}")
        st.write(f"Phương thức: **{order['payment']}**")

        if order["payment"] == "Quét mã QR":
            st.warning(
                "Đây là bản demo, ứng dụng chưa xác minh giao dịch ngân hàng."
            )
        else:
            st.info(
                "Đơn hàng tiền mặt đã được ghi nhận trên giao diện demo. "
                "Vui lòng thanh toán cho nhân viên."
            )

        st.markdown("---")
        if st.button("🏠 Về trang chủ", use_container_width=True):
            go_to("Trang chủ")
            st.rerun()

        if st.button("🛍️ Đặt đơn mới", use_container_width=True):
            st.session_state.cart = []
            clear_voucher()
            st.session_state.order_confirmation = None
            go_to("Khám phá thực đơn")
            st.rerun()
    else:
        st.info("Chưa có đơn hàng nào được xác nhận.")
        if st.button("Đến giỏ hàng"):
            go_to("Giỏ hàng & thanh toán")
            st.rerun()

# =========================================================
# 11. VÒNG QUAY MAY MẮN
# =========================================================
elif st.session_state.page == "Vòng quay may mắn":
    st.markdown("""
    <div class="hero">
        <div class="section-label" style="color:#e4cda7">LUCKY CORNER • 03</div>
        <h1>Vòng quay may mắn</h1>
        <p class="subtitle">
            Ghé quán một chút, mang về niềm vui.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write(
        "Mỗi lượt chơi nhận một phần quà. Hãy nhấn nút để thử vận may nhé!"
    )

    prizes = [
        {"name": "Giảm 10%", "code": "HOAINIEM10", "type": "voucher"},
        {"name": "Giảm 15%", "code": "COBA15", "type": "voucher"},
        {"name": "Giảm 20%", "code": "TRAXUA20", "type": "voucher"},
        {"name": "Tặng topping", "code": None, "type": "gift"},
        {"name": "Một lời chúc an yên", "code": None, "type": "message"},
    ]

    st.markdown("""
    <div style="background:#fffaf1;border:2px dashed #a58a60;
    border-radius:50%;width:250px;height:250px;margin:20px auto;
    display:flex;align-items:center;justify-content:center;
    text-align:center;">
        <div>
            <div style="font-size:55px">🎡</div>
            <div style="font-size:20px;font-weight:bold;color:#5a4934">
                VÒNG QUAY<br/>HOÀI NIỆM
            </div>
            <div style="color:#8b7655">Thử vận may của bạn</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎁 Các phần quà")
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("**🎟️ Voucher**")
        st.write("Giảm 10%, 15% hoặc 20%.")
    with p2:
        st.markdown("**🧋 Quà nhỏ**")
        st.write("Một topping miễn phí.")
    with p3:
        st.markdown("**💌 Lời chúc**")
        st.write("Một lời chúc dễ thương.")

    if st.session_state.used_spin:
        st.info("Bạn đã sử dụng lượt quay trong phiên này.")
        result = st.session_state.spin_result
        if result:
            st.markdown(f"### 🎉 Bạn nhận được: {result['name']}")
            if result["code"]:
                st.code(result["code"])
                if st.button("Dùng voucher này"):
                    st.session_state.voucher = result["code"]
                    st.session_state.voucher_applied = result["code"]
                    go_to("Giỏ hàng & thanh toán")
                    st.rerun()
            elif result["type"] == "gift":
                st.success(
                    "Bạn đã nhận quà tặng topping. Khi dùng thật, nhân viên "
                    "cần xác nhận và áp dụng phần quà vào đơn hàng."
                )
            else:
                st.success(
                    "Chúc bạn luôn giữ được sự bình yên và tìm thấy niềm vui "
                    "trong những điều giản dị."
                )
    else:
        if st.button("🎡 QUAY NGAY", use_container_width=True):
            result = random.choice(prizes)
            st.session_state.spin_result = result
            st.session_state.used_spin = True
            st.rerun()

    st.caption(
        "Lưu ý: vòng quay là tính năng demo trong phiên ứng dụng. "
        "Nếu triển khai kinh doanh, hãy thiết lập thể lệ, hạn sử dụng, "
        "điều kiện áp dụng voucher và cơ chế lưu lượt quay phù hợp."
    )

# =========================================================
# 12. GIỚI THIỆU QUÁN
# =========================================================
elif st.session_state.page == "Về chúng tôi":
    st.markdown("""
    <div class="hero">
        <div class="section-label" style="color:#e4cda7">OUR STORY</div>
        <h1>Câu chuyện của Trà Quán</h1>
        <p class="subtitle">Giữ chút hương xưa giữa nhịp sống hiện đại.</p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1])

    with left:
        show_product_image(
            "https://images.unsplash.com/photo-1498804103079-a6351b050096?auto=format&fit=crop&w=1000&q=85",
            "Không gian thưởng trà đầy hoài niệm"
        )

    with right:
        st.markdown("### Khởi nguồn từ những điều bình dị")
        st.write("""
        Trà Quán Hoài Niệm được xây dựng từ mong muốn lưu giữ những
        hình ảnh thân thuộc của Việt Nam xưa: chiếc bàn gỗ, tách trà,
        con phố nhỏ và những lời hỏi thăm chân thành.

        Chúng tôi tin rằng một thức uống ngon không chỉ nằm ở hương vị,
        mà còn ở cảm xúc mà nó mang lại. Bởi vậy, mỗi món trong thực đơn
        đều được đặt một cái tên gợi nhớ đến những nhân vật, góc phố
        và khoảnh khắc bình dị.

        Hãy ghé quán, chọn một ly trà và dành cho mình một khoảng nghỉ.
        """)

    st.divider()
    st.markdown("### 🌿 Điều quán luôn hướng đến")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### Chân thành")
        st.write("Tạo trải nghiệm thân thiện và gần gũi.")
    with c2:
        st.markdown("#### Chất riêng")
        st.write("Kết hợp thức uống hiện đại với cảm hứng xưa.")
    with c3:
        st.markdown("#### Bình yên")
        st.write("Để mỗi lần ghé quán là một lần sống chậm.")

    st.markdown("---")
    st.markdown("### 📮 Thông tin liên hệ")
    st.write("Tên quán: Trà Quán Hoài Niệm")
    st.write("Phong cách: Trà sữa và matcha hoài cổ")
    st.write("Địa chỉ: Bổ sung địa chỉ thật của quán tại đây")
    st.write("Fanpage: Bổ sung đường dẫn fanpage tại đây")

    if st.button("📜 Xem thực đơn ngay", use_container_width=True):
        go_to("Khám phá thực đơn")
        st.rerun()

# =========================================================
# 13. CHÂN TRANG
# =========================================================
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#887b67;font-size:12px'>"
    "TRÀ QUÁN HOÀI NIỆM · HƯƠNG XƯA VỊ CŨ · "
    "Cảm ơn bạn đã ghé thăm"
    "</div>",
    unsafe_allow_html=True
)
