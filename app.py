
import streamlit as st
import random
import qrcode
from io import BytesIO
from datetime import datetime

# =====================================================
# 1. CẤU HÌNH TRANG
# =====================================================
st.set_page_config(
    page_title="Trà Quán Hoài Niệm",
    page_icon="🫖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. THÔNG TIN QUÁN - CÓ THỂ TÙY CHỈNH
# =====================================================
TEN_QUAN = "TRÀ QUÁN HOÀI NIỆM"
SLOGAN = "Một ngụm trà xưa, một miền ký ức."

# Thông tin chuyển khoản DEMO.
# Hãy thay bằng thông tin tài khoản thật của quán trước khi sử dụng.
NGAN_HANG = "MB"
SO_TAI_KHOAN = "0123456789"
TEN_TAI_KHOAN = "TRA QUAN HOAI NIEM"

# =====================================================
# 3. GIAO DIỆN VINTAGE
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap');

.stApp {
    background-color: #F7F0E4;
    color: #4A3024;
    font-family: 'Be Vietnam Pro', sans-serif;
}
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #6B3025 !important;
}
header[data-testid="stHeader"] {
    background-color: rgba(247,240,228,0.9);
}
section[data-testid="stSidebar"] {
    background-color: #E9D8BF;
}
section[data-testid="stSidebar"] * {
    color: #4A3024;
}
div.stButton > button {
    background-color: #783D2C;
    color: #FFF7E9;
    border: 1px solid #783D2C;
    border-radius: 8px;
    font-weight: 600;
    transition: 0.2s;
}
div.stButton > button:hover {
    background-color: #A46C43;
    color: white;
    border-color: #A46C43;
}
div[data-testid="stMetric"] {
    background: #EFE0C9;
    border: 1px solid #D5B895;
    padding: 15px;
    border-radius: 12px;
}
.vintage-banner {
    background: linear-gradient(120deg, #4B2921, #874A35);
    color: #FFF2DA;
    padding: 35px 25px;
    border-radius: 16px;
    text-align: center;
    border: 3px double #D7B77D;
    margin-bottom: 20px;
}
.vintage-banner h1 {
    color: #F5D9A6 !important;
    font-size: 40px;
}
.vintage-banner p {
    color: #FFF2DA;
    font-size: 17px;
}
.menu-card {
    background: #FFF9EF;
    border: 1px solid #DCC5A5;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 8px;
}
.price {
    color: #8C3D2B;
    font-weight: 700;
    font-size: 19px;
}
.small-note {
    color: #806653;
    font-size: 13px;
}
hr {
    border-color: #DCC5A5;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 4. MENU ĐỒ UỐNG
# =====================================================
MENU = {
    "Trà sữa": {
        "Sữa Tươi Cổng Làng": {
            "price": 35000,
            "image": "https://images.unsplash.com/photo-1558857563-b371033873b8?w=700",
            "description": "Trà sữa dịu nhẹ, béo thơm, gợi nhớ góc phố thân quen."
        },
        "Hồng Trà Bến Xưa": {
            "price": 32000,
            "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=700",
            "description": "Hồng trà đậm vị hòa quyện cùng sữa thơm."
        },
        "Trà Sữa Hiên Nhà": {
            "price": 38000,
            "image": "https://images.unsplash.com/photo-1525385133512-2f3bdd039054?w=700",
            "description": "Vị trà sữa ngọt ngào như những buổi chiều xưa."
        },
        "Ô Long Phố Cũ": {
            "price": 36000,
            "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=700",
            "description": "Ô long thơm thanh, hậu vị dịu dàng."
        },
    },
    "Matcha": {
        "Matcha Vườn Ngọc": {
            "price": 39000,
            "image": "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?w=700",
            "description": "Matcha xanh mướt, thơm dịu, vị trà đặc trưng."
        },
        "Matcha Sữa Hoài Phố": {
            "price": 42000,
            "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=700",
            "description": "Matcha hòa quyện sữa béo, mịn màng."
        },
        "Matcha Đậu Đỏ Ký Ức": {
            "price": 45000,
            "image": "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?w=700",
            "description": "Matcha kết hợp đậu đỏ bùi ngọt."
        },
    },
    "Trà trái cây": {
        "Trà Đào Ga Xưa": {
            "price": 35000,
            "image": "https://images.unsplash.com/photo-1499638673689-79a0b5115d87?w=700",
            "description": "Trà đào thơm mát, ngọt dịu và tươi mới."
        },
        "Trà Vải Ngõ Nhỏ": {
            "price": 36000,
            "image": "https://images.unsplash.com/photo-1513558161293-cdaf765edfd7?w=700",
            "description": "Vị vải thanh ngọt cùng hương trà nhẹ nhàng."
        },
        "Trà Chanh Phố Hội": {
            "price": 29000,
            "image": "https://images.unsplash.com/photo-1513558161293-cdaf765edfd7?w=700",
            "description": "Chua ngọt hài hòa, giải khát sảng khoái."
        },
        "Trà Dâu Tháng Tư": {
            "price": 37000,
            "image": "https://images.unsplash.com/photo-1546173159-315724a31696?w=700",
            "description": "Dâu thơm dịu, sắc hồng ngọt ngào."
        },
    },
}

TOPPINGS = {
    "Trân châu đen": 7000,
    "Trân châu trắng": 8000,
    "Thạch củ năng": 7000,
    "Pudding trứng": 9000,
    "Kem cheese": 12000,
    "Đậu đỏ": 8000,
}

# =====================================================
# 5. VOUCHER
# =====================================================
VOUCHERS = {
    "HOAI_NIEM10": {
        "type": "percent",
        "value": 10,
        "description": "Giảm 10% tổng hóa đơn."
    },
    "PHOXUA15": {
        "type": "percent",
        "value": 15,
        "description": "Giảm 15% tổng hóa đơn."
    },
    "GIAM20K": {
        "type": "fixed",
        "value": 20000,
        "description": "Giảm 20.000đ cho hóa đơn."
    },
    "TANGTOPPING": {
        "type": "topping",
        "value": 0,
        "description": "Tặng một phần topping trị giá tối đa 9.000đ."
    },
}

# =====================================================
# 6. KHỞI TẠO SESSION STATE
# =====================================================
defaults = {
    "cart": [],
    "voucher": "",
    "wheel_result": None,
    "wheel_spun": False,
    "order_done": False,
    "order_number": 1001,
    "payment_method": "Tiền mặt",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =====================================================
# 7. HÀM HỖ TRỢ
# =====================================================
def money(amount):
    return f"{int(amount):,}".replace(",", ".") + "đ"


def subtotal_cart():
    return sum(item["total"] for item in st.session_state.cart)


def calculate_discount(subtotal, voucher_code):
    """Trả về (tiền giảm, mô tả giảm giá)."""
    code = voucher_code.strip().upper()

    if not code or code not in VOUCHERS:
        return 0, ""

    voucher = VOUCHERS[code]

    if voucher["type"] == "percent":
        discount = round(subtotal * voucher["value"] / 100)
        return min(discount, subtotal), voucher["description"]

    if voucher["type"] == "fixed":
        return min(voucher["value"], subtotal), voucher["description"]

    if voucher["type"] == "topping":
        return min(9000, subtotal), voucher["description"]

    return 0, ""


def make_qr():
    """Tạo QR chứa thông tin chuyển khoản dạng văn bản.
    Đây là QR minh họa, không phải QR thanh toán ngân hàng VietQR chuẩn.
    """
    amount = max(0, subtotal_cart() -
                 calculate_discount(
                     subtotal_cart(), st.session_state.voucher
                 )[0])

    content = (
        f"THANH TOAN {TEN_QUAN}\n"
        f"NGAN HANG: {NGAN_HANG}\n"
        f"SO TAI KHOAN: {SO_TAI_KHOAN}\n"
        f"CHU TAI KHOAN: {TEN_TAI_KHOAN}\n"
        f"SO TIEN: {amount}\n"
        f"NOI DUNG: DON {st.session_state.order_number}"
    )

    qr = qrcode.QRCode(box_size=8, border=3)
    qr.add_data(content)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#4B2921", back_color="#FFF9EF")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def reset_order():
    st.session_state.cart = []
    st.session_state.voucher = ""
    st.session_state.wheel_result = None
    st.session_state.wheel_spun = False
    st.session_state.order_done = False
    st.session_state.order_number += 1


# =====================================================
# 8. THANH ĐIỀU HƯỚNG
# =====================================================
with st.sidebar:
    st.markdown("## 🫖 Hoài Niệm")
    st.caption("Hương trà xưa - Vị thân quen")
    st.divider()

    page = st.radio(
        "DANH MỤC",
        [
            "🏮 Giới thiệu quán",
            "📜 Thực đơn & Đặt món",
            "🎡 Vòng quay may mắn",
            "🧾 Hóa đơn & Thanh toán",
        ],
    )

    st.divider()
    st.markdown("**Giờ mở cửa**")
    st.write("08:00 – 22:00 hằng ngày")
    st.markdown("**Phong cách**")
    st.write("Vintage • Hoài cổ • Ấm áp")
    st.caption("Một ngụm trà xưa, một miền ký ức.")

# =====================================================
# 9. TRANG GIỚI THIỆU
# =====================================================
if page == "🏮 Giới thiệu quán":
    st.markdown(f"""
    <div class="vintage-banner">
        <h1>🫖 {TEN_QUAN}</h1>
        <p><i>{SLOGAN}</i></p>
        <p>Hương vị thân quen, lưu giữ nét đẹp của những ngày xưa cũ.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 1])

    with col1:
        st.subheader("Câu chuyện của chúng mình")
        st.write("""
        Giữa nhịp sống hiện đại, Trà Quán Hoài Niệm là một góc nhỏ
        dành cho những ai muốn chậm lại, nhâm nhi một ly trà và
        tìm về những ký ức bình dị.

        Lấy cảm hứng từ những con phố xưa, mái hiên cũ và nét đẹp
        Việt Nam truyền thống, quán mang đến không gian ấm áp với
        sắc nâu gỗ, giấy ngả vàng và những thức uống được đặt tên
        bằng tất cả sự hoài niệm.

        Mỗi ly trà không chỉ là một thức uống, mà còn là lời mời
        gọi bạn tận hưởng những khoảnh khắc bình yên.
        """)

        st.markdown("### Giá trị của quán")
        st.write("🌿 Nguyên liệu được lựa chọn cẩn thận.")
        st.write("🫖 Hương vị hài hòa, phù hợp nhiều sở thích.")
        st.write("🏮 Không gian và trải nghiệm mang phong cách xưa.")

    with col2:
        st.image(
            "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1000",
            caption="Một góc nhỏ bình yên giữa phố thị",
            use_container_width=True,
        )

    st.divider()
    st.subheader("Ba miền hương vị")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.image(
            "https://images.unsplash.com/photo-1558857563-b371033873b8?w=600",
            use_container_width=True
        )
        st.markdown("**Trà sữa – Ngọt ngào ký ức**")
        st.caption("Béo thơm, đậm vị, thân quen.")

    with c2:
        st.image(
            "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?w=600",
            use_container_width=True
        )
        st.markdown("**Matcha – Sắc xanh thanh nhã**")
        st.caption("Thơm dịu, tinh tế, nhẹ nhàng.")

    with c3:
        st.image(
            "https://images.unsplash.com/photo-1513558161293-cdaf765edfd7?w=600",
            use_container_width=True
        )
        st.markdown("**Trà trái cây – Tươi mát phố xưa**")
        st.caption("Thanh mát, tươi mới, đầy sức sống.")

if st.button("📜 Khám phá thực đơn", use_container_width=True):
    st.session_state["selected_page"] = "📜 Thực đơn & Đặt món"
    st.rerun()

# =====================================================
# 10. TRANG MENU VÀ ĐẶT MÓN
# =====================================================
elif page == "📜 Thực đơn & Đặt món":
    st.markdown(f"""
    <div class="vintage-banner">
        <h1>Thực đơn Hoài Niệm</h1>
        <p>Chọn một thức uống, gửi gắm một chút thương nhớ.</p>
    </div>
    """, unsafe_allow_html=True)

    category = st.selectbox(
        "Chọn nhóm đồ uống",
        list(MENU.keys())
    )

    drinks = MENU[category]
    drink_name = st.selectbox("Tên thức uống", list(drinks.keys()))
    drink = drinks[drink_name]

    col_img, col_detail = st.columns([1, 1.2])

    with col_img:
        st.image(
            drink["image"],
            caption=drink_name,
            use_container_width=True
        )

    with col_detail:
        st.subheader(drink_name)
        st.markdown(
            f'<div class="price">{money(drink["price"])}</div>',
            unsafe_allow_html=True
        )
        st.write(drink["description"])
        st.caption("Hình ảnh mang tính minh họa; ảnh cần có kết nối Internet.")

    st.divider()
    st.subheader("✨ Tùy chỉnh thức uống")

    with st.form("order_form", clear_on_submit=False):
        quantity = st.number_input(
            "Số lượng ly",
            min_value=1,
            max_value=50,
            value=1,
            step=1
        )

        toppings = st.multiselect(
            "Chọn topping kèm",
            options=list(TOPPINGS.keys()),
            help="Có thể chọn nhiều topping. Giá topping được tính cho mỗi ly."
        )

        sweetness = st.radio(
            "Độ ngọt",
            ["0% - Không đường", "30% - Ít ngọt", "50% - Vừa", "70% - Ngọt", "100% - Ngọt đậm"],
            index=2,
            horizontal=True
        )

        ice = st.radio(
            "Lượng đá",
            ["Có đá", "Ít đá", "Không đá"],
            horizontal=True
        )

        note = st.text_input(
            "Ghi chú riêng (nếu có)",
            placeholder="Ví dụ: ít trà, để riêng topping..."
        )

        topping_price = sum(TOPPINGS[t] for t in toppings)
        unit_price = drink["price"] + topping_price
        item_total = unit_price * quantity

        st.markdown(f"**Giá mỗi ly:** {money(unit_price)}")
        st.markdown(f"**Thành tiền:** {money(item_total)}")

        submitted = st.form_submit_button(
            "➕ Thêm vào giỏ hàng",
            use_container_width=True
        )

        if submitted:
            st.session_state.cart.append({
                "name": drink_name,
                "category": category,
                "price": drink["price"],
                "toppings": toppings.copy(),
                "topping_price": topping_price,
                "sweetness": sweetness,
                "ice": ice,
                "note": note.strip(),
                "quantity": int(quantity),
                "unit_price": unit_price,
                "total": item_total,
            })
            st.session_state.order_done = False
            st.success(f"Đã thêm {quantity} ly {drink_name} vào giỏ hàng!")

    st.divider()
    st.subheader("🛍️ Giỏ hàng của bạn")

    if not st.session_state.cart:
        st.info("Giỏ hàng đang trống. Hãy chọn món bạn yêu thích nhé!")
    else:
        for i, item in enumerate(st.session_state.cart):
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 2, 1])

                with c1:
                    st.markdown(f"**{i + 1}. {item['name']}**")
                    st.caption(f"Nhóm: {item['category']}")
                    st.caption(
                        f"Đường: {item['sweetness']} | Đá: {item['ice']}"
                    )
                    st.caption(
                        "Topping: " + (
                            ", ".join(item["toppings"])
                            if item["toppings"] else "Không"
                        )
                    )
                    if item["note"]:
                        st.caption("Ghi chú: " + item["note"])

                with c2:
                    st.write(f"Số lượng: {item['quantity']}")
                    st.write(f"Đơn giá: {money(item['unit_price'])}")
                    st.markdown(f"**{money(item['total'])}**")

                with c3:
                    if st.button("🗑️ Xóa", key=f"remove_{i}"):
                        st.session_state.cart.pop(i)
                        st.session_state.order_done = False
                        st.rerun()

        st.markdown(
            f"### Tổng tiền hàng: {money(subtotal_cart())}"
        )

        if st.button("🧹 Xóa toàn bộ giỏ hàng"):
            st.session_state.cart = []
            st.session_state.voucher = ""
            st.session_state.order_done = False
            st.rerun()

    st.info("Muốn thanh toán hoặc nhập voucher? Mở mục 'Hóa đơn & Thanh toán' ở thanh bên.")

# =====================================================
# 11. VÒNG QUAY MAY MẮN
# =====================================================
elif page == "🎡 Vòng quay may mắn":
    st.markdown("""
    <div class="vintage-banner">
        <h1>🎡 Vòng Quay May Mắn</h1>
        <p>Thử vận may, nhận lộc nhỏ, vui cả ngày!</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("""
    Mỗi khách hàng được quay một lần trong phiên sử dụng này.
    Phần thưởng có thể là mã giảm giá hoặc một món quà nhỏ.
    """)

    # Mỗi phần thưởng có xác suất như nhau trong danh sách.
    prizes = [
        {
            "name": "Giảm 10% hóa đơn",
            "voucher": "HOAI_NIEM10",
            "message": "Bạn nhận được mã HOAI_NIEM10!"
        },
        {
            "name": "Giảm 15% hóa đơn",
            "voucher": "PHOXUA15",
            "message": "Bạn nhận được mã PHOXUA15!"
        },
        {
            "name": "Giảm 20.000đ",
            "voucher": "GIAM20K",
            "message": "Bạn nhận được mã GIAM20K!"
        },
        {
            "name": "Tặng topping",
            "voucher": "TANGTOPPING",
            "message": "Bạn nhận được mã TANGTOPPING!"
        },
        {
            "name": "Quà nhỏ bí mật 🎁",
            "voucher": None,
            "message": "Bạn nhận được một phần quà nhỏ! Hãy đưa màn hình này cho nhân viên."
        },
    ]

    st.markdown("### Các phần quà đang chờ bạn")
    prize_cols = st.columns(5)

    for col, prize in zip(prize_cols, prizes):
        with col:
            st.markdown(
                f"""
                <div class="menu-card" style="text-align:center; min-height:120px">
                    <div style="font-size:30px">🎁</div>
                    <b>{prize['name']}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.caption(
        "Lưu ý: Đây là vòng quay ngẫu nhiên mô phỏng. "
        "Xác suất của mỗi phần thưởng hiện bằng nhau."
    )

    if not st.session_state.wheel_spun:
        if st.button("🎡 QUAY NGAY!", use_container_width=True):
            prize = random.choice(prizes)
            st.session_state.wheel_result = prize
            st.session_state.wheel_spun = True
            st.rerun()

    if st.session_state.wheel_spun:
        result = st.session_state.wheel_result

        st.balloons()
        st.success("🎉 Chúc mừng bạn!")

        st.markdown(
            f"""
            <div class="vintage-banner">
                <h1>🎁 {result['name']}</h1>
                <p>{result['message']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if result["voucher"]:
            st.code(result["voucher"], language=None)

            if st.button("🎟️ Dùng mã này cho hóa đơn"):
                st.session_state.voucher = result["voucher"]
                st.success("Đã lưu mã. Hãy sang trang thanh toán để kiểm tra mức giảm.")

        else:
            st.info(
                "Phần quà nhỏ được nhận trực tiếp tại quán. "
                "Nhân viên cần xác nhận phần thưởng khi khách nhận quà."
            )

        if st.button("🔄 Đặt lại vòng quay (chỉ dùng thử nghiệm)"):
            st.session_state.wheel_spun = False
            st.session_state.wheel_result = None
            st.rerun()

# =====================================================
# 12. HÓA ĐƠN VÀ THANH TOÁN
# =====================================================
elif page == "🧾 Hóa đơn & Thanh toán":
    st.markdown("""
    <div class="vintage-banner">
        <h1>🧾 Hóa đơn Hoài Niệm</h1>
        <p>Cảm ơn bạn đã ghé thăm góc trà nhỏ của chúng mình.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.cart:
        st.warning("Bạn chưa có món nào trong giỏ hàng.")
        st.info("Hãy vào mục 'Thực đơn & Đặt món' để chọn thức uống.")
        st.stop()

    st.markdown(f"**Mã đơn hàng:** HD{st.session_state.order_number}")
    st.markdown(
        f"**Thời gian lập hóa đơn:** {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

    st.divider()
    st.subheader("Chi tiết đơn hàng")

    # Bảng chi tiết, hiển thị từng món và thành tiền.
    for index, item in enumerate(st.session_state.cart, start=1):
        with st.container(border=True):
            st.markdown(f"**{index}. {item['name']}**")
            st.write(
                f"Đơn giá gốc: {money(item['price'])} | "
                f"Topping mỗi ly: {money(item['topping_price'])}"
            )
            st.write(
                f"Số lượng: {item['quantity']} | "
                f"Đơn giá sau topping: {money(item['unit_price'])}"
            )
            st.write(
                f"Độ ngọt: {item['sweetness']} | "
                f"Lượng đá: {item['ice']}"
            )
            if item["toppings"]:
                st.write("Topping: " + ", ".join(item["toppings"]))
            if item["note"]:
                st.write("Ghi chú: " + item["note"])

            st.markdown(
                f"**Thành tiền: {money(item['total'])}**"
            )

    subtotal = subtotal_cart()

    st.divider()
    st.subheader("🎟️ Mã giảm giá")

    with st.form("voucher_form"):
        voucher_input = st.text_input(
            "Nhập mã voucher",
            value=st.session_state.voucher,
            placeholder="Ví dụ: HOAI_NIEM10"
        ).strip().upper()

        voucher_submit = st.form_submit_button("Áp dụng voucher")

        if voucher_submit:
            if not voucher_input:
                st.session_state.voucher = ""
                st.success("Đã bỏ mã voucher.")
            elif voucher_input in VOUCHERS:
                st.session_state.voucher = voucher_input
                st.success(
                    f"Áp dụng thành công: {VOUCHERS[voucher_input]['description']}"
                )
            else:
                st.error("Mã voucher không hợp lệ. Vui lòng thử lại.")

    active_code = st.session_state.voucher
    discount, discount_description = calculate_discount(subtotal, active_code)

    if active_code and active_code in VOUCHERS:
        st.caption(f"Mã đang dùng: {active_code} — {discount_description}")
        st.caption(
            "Lưu ý: Voucher TANGTOPPING hiện được quy đổi thành "
            "khoản giảm tối đa 9.000đ trên hóa đơn; nhân viên có thể "
            "tặng topping trực tiếp để đúng chương trình khuyến mãi."
        )

    total = max(0, subtotal - discount)

    m1, m2, m3 = st.columns(3)
    m1.metric("Tiền hàng", money(subtotal))
    m2.metric("Giảm giá", money(discount))
    m3.metric("Tổng thanh toán", money(total))

    st.divider()
    st.subheader("💳 Phương thức thanh toán")

    payment = st.radio(
        "Chọn cách thanh toán",
        ["Tiền mặt", "Mã QR chuyển khoản"],
        horizontal=True,
        index=0 if st.session_state.payment_method == "Tiền mặt" else 1
    )

    st.session_state.payment_method = payment

    if payment == "Tiền mặt":
        st.info(
            f"Khách thanh toán tại quầy: **{money(total)}**. "
            "Nhân viên nhận tiền và xác nhận đơn hàng."
        )
    else:
        st.warning(
            "QR dưới đây chỉ chứa thông tin chuyển khoản dạng văn bản, "
            "không phải mã QR ngân hàng VietQR chuẩn. "
            "Không sử dụng mã này để xác nhận chuyển khoản thực tế."
        )

        st.image(
            make_qr(),
            caption="QR minh họa — cần tích hợp QR thanh toán thật trước khi sử dụng",
            width=260
        )

        st.markdown(f"**Ngân hàng:** {NGAN_HANG}")
        st.markdown(f"**Số tài khoản:** {SO_TAI_KHOAN}")
        st.markdown(f"**Chủ tài khoản:** {TEN_TAI_KHOAN}")
        st.markdown(f"**Số tiền cần chuyển:** {money(total)}")
        st.markdown(f"**Nội dung chuyển khoản:** DON {st.session_state.order_number}")

    st.divider()

    if not st.session_state.order_done:
        if st.button("✅ XÁC NHẬN ĐƠN HÀNG", use_container_width=True):
            st.session_state.order_done = True
            st.rerun()
    else:
        st.success("Đơn hàng đã được ghi nhận trong phiên ứng dụng.")
        st.markdown(f"### Tổng thanh toán: {money(total)}")
        st.write(f"Phương thức thanh toán: {payment}")

        st.warning(
            "Đây là xác nhận trên giao diện, không phải xác nhận tiền đã nhận. "
            "Nhân viên cần kiểm tra thanh toán thực tế trước khi giao món."
        )

        if st.button("🖨️ In / Lưu hóa đơn"):
            receipt = [
                f"{TEN_QUAN}",
                SLOGAN,
                f"Mã đơn: HD{st.session_state.order_number}",
                f"Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                "-" * 36,
            ]

            for item in st.session_state.cart:
                receipt.append(item["name"])
                receipt.append(
                    f"  {item['quantity']} x {money(item['unit_price'])}"
                    f" = {money(item['total'])}"
                )
                receipt.append(
                    f"  Đường: {item['sweetness']} | Đá: {item['ice']}"
                )
                if item["toppings"]:
                    receipt.append("  Topping: " + ", ".join(item["toppings"]))

            receipt.extend([
                "-" * 36,
                f"Tiền hàng: {money(subtotal)}",
                f"Giảm giá: {money(discount)}",
                f"TỔNG CỘNG: {money(total)}",
                f"Thanh toán: {payment}",
                "",
                "Xin cảm ơn và hẹn gặp lại!",
            ])

            st.download_button(
                "⬇️ Tải hóa đơn dạng TXT",
                data="\n".join(receipt),
                file_name=f"hoa_don_{st.session_state.order_number}.txt",
                mime="text/plain",
                use_container_width=True
            )

        if st.button("🛒 Tạo đơn hàng mới", use_container_width=True):
            reset_order()
            st.rerun()

# =====================================================
# 13. CHÂN TRANG
# =====================================================
st.markdown("---")
st.markdown(
    f"""
    <div style="text-align:center; color:#806653; padding:10px">
        <b>{TEN_QUAN}</b><br>
        <i>{SLOGAN}</i><br>
        © 2026 - Gìn giữ hương vị, trân trọng ký ức.
    </div>
    """,
    unsafe_allow_html=True
)
