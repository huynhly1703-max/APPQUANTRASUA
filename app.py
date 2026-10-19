
import streamlit as st
from datetime import datetime
from urllib.parse import quote

# ==================================================
# CẤU HÌNH ỨNG DỤNG
# ==================================================

st.set_page_config(
    page_title="Milk Tea Order",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bảng giá đồ uống (VNĐ)
MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa trân châu đường đen": 35000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà đào cam sả": 30000,
    "Trà vải": 30000,
    "Trà ô long": 25000,
    "Trà chanh": 20000,
    "Matcha latte": 40000,
    "Sữa tươi trân châu đường đen": 40000,
}

# Giá topping (VNĐ/phần)
TOPPINGS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
    "Thạch cà phê": 5000,
    "Không topping": 0,
}

# ==================================================
# THÔNG TIN THANH TOÁN QR
# THAY BẰNG THÔNG TIN TÀI KHOẢN THẬT CỦA QUÁN
# ==================================================

BANK_ID = "MB"
ACCOUNT_NO = "0123456789"
ACCOUNT_NAME = "TEN CHU TAI KHOAN"
QR_TEMPLATE = "compact2"

# ==================================================
# GIAO DIỆN
# ==================================================

st.markdown("""
<style>
    .stApp {
        background-color: #fffaf5;
    }

    .main-title {
        text-align: center;
        color: #8b4513;
        font-size: 38px;
        font-weight: bold;
        padding: 10px;
    }

    .sub-title {
        text-align: center;
        color: #9b7653;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .bill {
        background-color: white;
        border: 2px dashed #c49a6c;
        border-radius: 15px;
        padding: 22px;
        color: #333333;
    }

    .total {
        color: #b45309;
        font-size: 26px;
        font-weight: bold;
        text-align: right;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: bold;
        min-height: 42px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">🧋 MILK TEA HOUSE</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-title">Ngọt ngào trong từng giọt trà!</div>',
    unsafe_allow_html=True
)

# ==================================================
# KHỞI TẠO GIỎ HÀNG
# ==================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "order_no" not in st.session_state:
    st.session_state.order_no = 1

if "last_order" not in st.session_state:
    st.session_state.last_order = None

# ==================================================
# HÀM ĐỊNH DẠNG TIỀN
# ==================================================

def money(amount):
    return f"{amount:,.0f} đ".replace(",", ".")


# ==================================================
# THANH BÊN: GIỎ HÀNG
# ==================================================

with st.sidebar:
    st.header("🛒 Giỏ hàng")
    st.write(f"Số loại đồ uống: **{len(st.session_state.cart)}**")

    if st.session_state.cart:
        total_sidebar = sum(
            item["subtotal"] for item in st.session_state.cart
        )
        st.metric("Tạm tính", money(total_sidebar))

        if st.button("🗑️ Xóa toàn bộ giỏ hàng", use_container_width=True):
            st.session_state.cart = []
            st.rerun()
    else:
        st.info("Giỏ hàng đang trống.")

    st.divider()
    st.caption("Giá bán được tính bằng VNĐ.")

# ==================================================
# BỐ CỤC CHÍNH
# ==================================================

tab_order, tab_bill = st.tabs([
    "🧋 ĐẶT ĐỒ UỐNG",
    "🧾 HÓA ĐƠN"
])

# ==================================================
# TAB 1: ĐẶT ĐỒ UỐNG
# ==================================================

with tab_order:
    st.header("1. Chọn đồ uống")

    col1, col2 = st.columns(2)

    with col1:
        drink = st.selectbox(
            "Loại đồ uống",
            options=list(MENU.keys()),
            format_func=lambda x: f"{x} — {money(MENU[x])}"
        )

        quantity = st.number_input(
            "Số lượng",
            min_value=1,
            max_value=100,
            value=1,
            step=1
        )

        sweetness = st.selectbox(
            "Độ ngọt",
            ["0% - Không đường", "30% - Ít ngọt",
             "50% - Ngọt vừa", "70% - Ngọt",
             "100% - Ngọt bình thường"]
        )

    with col2:
        toppings = st.multiselect(
            "Chọn topping (có thể chọn nhiều)",
            options=list(TOPPINGS.keys()),
            default=[]
        )

        ice = st.radio(
            "Lượng đá",
            ["100% đá", "50% đá", "Ít đá", "Không đá"],
            horizontal=True
        )

        st.info(
            f"Giá đồ uống: **{money(MENU[drink])}**\n\n"
            f"Topping mỗi ly: **{money(sum(TOPPINGS[t] for t in toppings))}**"
        )

    drink_price = MENU[drink]
    topping_price = sum(TOPPINGS[t] for t in toppings)
    unit_price = drink_price + topping_price
    subtotal = unit_price * quantity

    st.divider()

    st.subheader("2. Kiểm tra giá")

    price_col1, price_col2, price_col3 = st.columns(3)

    price_col1.metric("Giá một ly", money(unit_price))
    price_col2.metric("Số lượng", quantity)
    price_col3.metric("Thành tiền", money(subtotal))

    if st.button(
        "➕ THÊM VÀO GIỎ HÀNG",
        type="primary",
        use_container_width=True
    ):
        item = {
            "name": drink,
            "drink_price": drink_price,
            "toppings": toppings.copy(),
            "topping_price": topping_price,
            "sweetness": sweetness,
            "ice": ice,
            "quantity": int(quantity),
            "unit_price": unit_price,
            "subtotal": subtotal,
        }

        st.session_state.cart.append(item)
        st.success(f"Đã thêm {quantity} ly {drink} vào giỏ hàng!")
        st.rerun()

    # Giỏ hàng chi tiết
    st.divider()
    st.header("3. Danh sách món đã chọn")

    if not st.session_state.cart:
        st.info("Bạn chưa thêm món nào.")
    else:
        for i, item in enumerate(st.session_state.cart):
            with st.container(border=True):
                c1, c2 = st.columns([5, 1])

                with c1:
                    st.markdown(f"**{i + 1}. {item['name']}**")
                    st.write(f"Số lượng: {item['quantity']} ly")
                    st.write(
                        "Topping: "
                        + (", ".join(item["toppings"]) or "Không")
                    )
                    st.caption(
                        f"Độ ngọt: {item['sweetness']} | Đá: {item['ice']}"
                    )
                    st.write(f"Thành tiền: **{money(item['subtotal'])}**")

                with c2:
                    if st.button("❌", key=f"remove_{i}"):
                        st.session_state.cart.pop(i)
                        st.rerun()

        total = sum(
            item["subtotal"] for item in st.session_state.cart
        )

        st.markdown(f"### Tổng tiền: {money(total)}")

        if st.button(
            "➡️ TIẾN HÀNH THANH TOÁN",
            type="primary",
            use_container_width=True
        ):
            st.session_state.go_to_bill = True
            st.rerun()

# ==================================================
# TAB 2: HÓA ĐƠN VÀ THANH TOÁN
# ==================================================

with tab_bill:
    st.header("🧾 Hóa đơn thanh toán")

    if not st.session_state.cart:
        st.info("Vui lòng thêm đồ uống vào giỏ hàng trước.")
    else:
        total = sum(
            item["subtotal"] for item in st.session_state.cart
        )

        st.subheader("4. Chọn phương thức thanh toán")

        payment = st.radio(
            "Bạn muốn thanh toán bằng cách nào?",
            ["💵 Tiền mặt", "📱 Chuyển khoản bằng mã QR"],
            horizontal=True,
            key="payment_method"
        )

        st.divider()

        # Hiển thị hóa đơn
        st.markdown(
            '<div class="bill">',
            unsafe_allow_html=True
        )

        st.markdown(
            "<h2 style='text-align:center;color:#8b4513;'>"
            "MILK TEA HOUSE</h2>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align:center;'>HÓA ĐƠN THANH TOÁN</p>",
            unsafe_allow_html=True
        )

        st.write(f"**Mã đơn:** MT{st.session_state.order_no:04d}")
        st.write(
            f"**Thời gian:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        )

        st.divider()

        # Bảng chi tiết món
        for i, item in enumerate(st.session_state.cart, start=1):
            st.markdown(f"**{i}. {item['name']}**")
            st.write(
                f"{money(item['drink_price'])} × {item['quantity']} ly"
            )

            if item["toppings"]:
                st.write(
                    "Topping: " + ", ".join(item["toppings"])
                )
                st.write(
                    f"Phụ thu topping: "
                    f"{money(item['topping_price'] * item['quantity'])}"
                )

            st.caption(
                f"Độ ngọt: {item['sweetness']} | Đá: {item['ice']}"
            )
            st.markdown(
                f"**Thành tiền: {money(item['subtotal'])}**"
            )
            st.divider()

        st.markdown(
            f"<div class='total'>TỔNG CỘNG: {money(total)}</div>",
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()

        # Thông tin thanh toán
        if payment == "💵 Tiền mặt":
            st.success("Phương thức: Thanh toán bằng tiền mặt")
            cash_received = st.number_input(
                "Số tiền khách đưa (VNĐ)",
                min_value=0,
                value=int(total),
                step=10000,
                key="cash_received"
            )

            change = cash_received - total

            if change >= 0:
                st.metric("Tiền thối lại", money(change))
            else:
                st.warning(
                    f"Khách cần đưa thêm {money(-change)}."
                )

        else:
            st.subheader("📱 Quét mã QR để thanh toán")

            st.warning(
                "Hãy cập nhật BANK_ID, ACCOUNT_NO và ACCOUNT_NAME "
                "ở đầu file bằng thông tin tài khoản thật của quán "
                "trước khi sử dụng."
            )

            if (
                ACCOUNT_NO != "0123456789"
                and ACCOUNT_NAME != "TEN CHU TAI KHOAN"
            ):
                qr_url = (
                    f"https://img.vietqr.io/image/"
                    f"{BANK_ID}-{ACCOUNT_NO}-{QR_TEMPLATE}.png"
                    f"?amount={int(total)}"
                    f"&addInfo={quote('Thanh toan MT' + str(st.session_state.order_no).zfill(4))}"
                    f"&accountName={quote(ACCOUNT_NAME)}"
                )

                st.image(
                    qr_url,
                    caption=f"Số tiền cần thanh toán: {money(total)}",
                    width=300
                )

                st.caption(
                    "Mã QR được tạo từ dịch vụ VietQR. "
                    "Cần có kết nối internet để tải hình ảnh."
                )
            else:
                st.error(
                    "Chưa cấu hình tài khoản ngân hàng thật. "
                    "Vui lòng sửa thông tin QR ở đầu file."
                )

        st.divider()

        # Hoàn tất đơn
        if st.button(
            "✅ XÁC NHẬN HOÀN TẤT ĐƠN",
            type="primary",
            use_container_width=True
        ):
            if (
                payment == "💵 Tiền mặt"
                and st.session_state.cash_received < total
            ):
                st.error("Số tiền khách đưa chưa đủ để thanh toán.")
            else:
                st.session_state.last_order = {
                    "order_no": st.session_state.order_no,
                    "items": st.session_state.cart.copy(),
                    "total": total,
                    "payment": payment,
                    "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                }

                st.session_state.order_no += 1
                st.session_state.cart = []
                st.session_state.pop("cash_received", None)
                st.success(
                    "Đã ghi nhận đơn hàng trên ứng dụng!"
                )
                st.rerun()

    # Hiển thị đơn vừa hoàn tất
    if st.session_state.last_order:
        order = st.session_state.last_order

        st.divider()
        st.subheader("📋 Đơn hàng vừa hoàn tất")
        st.write(f"Mã đơn: MT{order['order_no']:04d}")
        st.write(f"Thời gian: {order['time']}")
        st.write(f"Thanh toán: {order['payment']}")
        st.write(f"Tổng cộng: **{money(order['total'])}**")

        if st.button("🆕 TẠO ĐƠN HÀNG MỚI", use_container_width=True):
            st.session_state.last_order = None
            st.session_state.cart = []
            st.rerun()

st.divider()
st.caption("🧋 MILK TEA HOUSE | Cảm ơn quý khách và hẹn gặp lại!")
