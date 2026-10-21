import streamlit as st
import random
import time

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG VÀ STYLESHEET (PHONG CÁCH ĐÔNG DƯƠNG)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Trà Quán Hoài Niệm",
    page_icon="🍵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho phong cách Đông Dương: Tone vàng kem, xạnh rêu đậm, đỏ đô, hoa văn hoài cổ
st.markdown("""
    <style>
    /* Màu nền chính */
    .stApp {
        background-color: #F7F3E9;
        color: #2C3E35;
        font-family: 'Georgia', 'Times New Roman', serif;
    }
    
    /* Sidebar phong cách Đông Dương */
    [data-testid="stSidebar"] {
        background-color: #1B3B2B;
        border-right: 3px solid #C5A059;
    }
    
    [data-testid="stSidebar"] * {
        color: #F7F3E9 !important;
    }

    /* Tiêu đề chính */
    .title-indochine {
        text-align: center;
        color: #8B0000;
        font-family: 'Playfair Display', serif;
        font-weight: bold;
        border-bottom: 2px solid #C5A059;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Card món ăn */
    .menu-card {
        background-color: #FFFDF9;
        border: 2px solid #C5A059;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    
    .menu-card img {
        border-radius: 5px;
        object-fit: cover;
    }

    .price-tag {
        background-color: #1B3B2B;
        color: #F7F3E9;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: bold;
        display: inline-block;
        margin-top: 5px;
    }

    /* Button chung */
    .stButton>button {
        background-color: #8B0000;
        color: #FFFFFF !important;
        border-radius: 5px;
        border: 1px solid #C5A059;
        font-weight: bold;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #1B3B2B;
        color: #F7F3E9 !important;
    }
    
    /* Khung giỏ hàng & hóa đơn */
    .cart-box {
        background-color: #FFFDF9;
        border: 2px dashed #C5A059;
        padding: 15px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. KHỞI TẠO SESSION STATE (TRÁNH XUNG ĐỘT TRẠNG THÁI)
# ---------------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []
if "voucher_discount" not in st.session_state:
    st.session_state.voucher_discount = 0
if "applied_voucher" not in st.session_state:
    st.session_state.applied_voucher = ""
if "order_completed" not in st.session_state:
    st.session_state.order_completed = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Trang chủ"

# Dữ liệu thực đơn
MENU = {
    "Trà sữa": [
        {"id": 1, "name": "Trà Sữa Cô Ba Sài Gòn", "price": 35000, "desc": "Trà đậm vị, sữa thơm béo dịu dàng.", "img": "https://picsum.photos/seed/trasua1/300/200"},
        {"id": 2, "name": "Trà Sữa Tiệm May Xưa", "price": 39000, "desc": "Vị trà thanh nhẹ, ngọt ngào như chuyện cũ.", "img": "https://picsum.photos/seed/trasua2/300/200"},
        {"id": 3, "name": "Trà Sữa Phố Đèn Lồng", "price": 38000, "desc": "Hương trà thơm nồng, sữa béo quyện vị.", "img": "https://picsum.photos/seed/trasua3/300/200"},
        {"id": 4, "name": "Trà Sữa Chiều Bên Hiên", "price": 42000, "desc": "Ngọt dịu, mềm mại như buổi chiều yên ả.", "img": "https://picsum.photos/seed/trasua4/300/200"}
    ],
    "Matcha": [
        {"id": 5, "name": "Matcha Ngọc Bích Đông Dương", "price": 42000, "desc": "Matcha xanh mịn, thanh mát và tinh tế.", "img": "https://picsum.photos/seed/matcha1/300/200"},
        {"id": 6, "name": "Matcha Nắng Qua Rèm", "price": 45000, "desc": "Matcha hòa sữa tươi, dịu dàng như nắng sớm.", "img": "https://picsum.photos/seed/matcha2/300/200"},
        {"id": 7, "name": "Matcha Vườn Ngọc Lan", "price": 47000, "desc": "Vị trà xanh thanh mát gợi nhớ khu vườn xưa.", "img": "https://picsum.photos/seed/matcha3/300/200"}
    ],
    "Cà phê": [
        {"id": 8, "name": "Cà Phê Phin Sài Gòn Xưa", "price": 29000, "desc": "Cà phê phin đậm đà, lưu giữ hương vị hoài niệm.", "img": "https://picsum.photos/seed/caphe1/300/200"},
        {"id": 9, "name": "Bạc Xỉu Góc Phố", "price": 32000, "desc": "Sữa thơm béo, cà phê thoáng nhẹ thân quen.", "img": "https://picsum.photos/seed/caphe2/300/200"},
        {"id": 10, "name": "Cà Phê Ban Công Cũ", "price": 33000, "desc": "Vị cà phê đậm vừa cho những phút giây lắng đọng.", "img": "https://picsum.photos/seed/caphe3/300/200"}
    ]
}

VOUCHERS = {
    "HOAINIEM10": 10,
    "INDOCINE20": 20,
    "MAYMAN15": 15
}

# ---------------------------------------------------------
# 3. SIDEBAR ĐIỀU HƯỚNG
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #C5A059;'>TRÀ QUÁN HOÀI NIỆM</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic;'>Hương vị xưa - Cảm xúc mới</p>", unsafe_allow_html=True)
    st.divider()

    pages = ["Trang chủ", "Thực đơn", "Giỏ hàng & Hóa đơn", "Vòng quay may mắn", "Thanh toán & Đánh giá"]
    page_choice = st.radio("Chuyển mục", pages, index=pages.index(st.session_state.current_page))
    st.session_state.current_page = page_choice

    st.divider()
    st.markdown("📍 **Địa chỉ**: 123 Đường Đông Dương, Sài Gòn\n☎️ **Hotline**: 0909 123 456")

# ---------------------------------------------------------
# 4. GIAO DIỆN CÁC TRANG
# ---------------------------------------------------------

# ----- TRANG 1: TRANG CHỦ -----
if st.session_state.current_page == "Trang chủ":
    st.markdown("<h1 class='title-indochine'>TRÀ QUÁN HOÀI NIỆM</h1>", unsafe_allow_html=True)
    st.image("https://picsum.photos/seed/indochine_banner/1000/350", use_container_width=True)
    
    st.markdown("### 🏮 Lời Giới Thiệu")
    st.write("""
        Chào mừng quý khách đến với **Trà Quán Hoài Niệm** - nơi tìm lại những ký ức xưa cũ qua từng ngụm trà đậm đà. 
        Được thiết kế theo phong cách Đông Dương giao thoa giữa nét cổ kính Á Đông và sự lãng mạn nước Pháp, 
        quán đem tới cho bạn không gian thư thái tuyệt đối cùng menu trà sữa, matcha, cà phê truyền thống tinh tế.
    """)
    
    st.info("💡 **Gợi ý**: Hãy thử quay **Vòng quay may mắn** ở menu bên trái để nhận Voucher ưu đãi trước khi đặt hàng nhé!")
    
    if st.button("Khám phá Thực Đơn ngay"):
        st.session_state.current_page = "Thực đơn"
        st.rerun()

# ----- TRANG 2: THỰC ĐƠN -----
elif st.session_state.current_page == "Thực đơn":
    st.markdown("<h1 class='title-indochine'>THỰC ĐƠN TRÀ QUÁN</h1>", unsafe_allow_html=True)
    
    category = st.tabs(["🧋 Trà Sữa", "🍵 Matcha", "☕ Cà Phê"])
    
    def render_items(item_list):
        cols = st.columns(3)
        for idx, item in enumerate(item_list):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class='menu-card'>
                        <img src="{item['img']}" width="100%" height="150px">
                        <h4>{item['name']}</h4>
                        <p style='font-size: 0.85em; color: #555;'>{item['desc']}</p>
                        <span class='price-tag'>{item['price']:,} VNĐ</span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Tùy chỉnh đơn hàng
                with st.expander(f"⚙️ Tùy chỉnh món: {item['name']}"):
                    sweetness = st.select_slider("Độ ngọt", options=["0%", "30%", "50%", "70%", "100%"], value="100%", key=f"sweet_{item['id']}")
                    ice = st.select_slider("Lượng đá", options=["0%", "30%", "50%", "70%", "100%"], value="100%", key=f"ice_{item['id']}")
                    toppings = st.multiselect("Thêm Topping (+5,000đ/món)", ["Trân châu đen", "Thạch trái cây", "Pudding trứng", "Kem Cheese"], key=f"top_{item['id']}")
                    note = st.text_input("Lời nhắn gửi quán", placeholder="Ví dụ: Ít đắng, giao tận tay...", key=f"note_{item['id']}")
                    
                    if st.button("➕ Thêm vào giỏ", key=f"add_{item['id']}"):
                        extra_price = len(toppings) * 5000
                        cart_item = {
                            "id": item["id"],
                            "name": item["name"],
                            "price": item["price"] + extra_price,
                            "sweetness": sweetness,
                            "ice": ice,
                            "toppings": toppings,
                            "note": note
                        }
                        st.session_state.cart.append(cart_item)
                        st.toast(f"Đã thêm **{item['name']}** vào giỏ hàng!", icon="✅")

    with category[0]:
        render_items(MENU["Trà sữa"])
    with category[1]:
        render_items(MENU["Matcha"])
    with category[2]:
        render_items(MENU["Cà phê"])

# ----- TRANG 3: GIỎ HÀNG & HÓA ĐƠN -----
elif st.session_state.current_page == "Giỏ hàng & Hóa đơn":
    st.markdown("<h1 class='title-indochine'>GIỎ HÀNG & HÓA ĐƠN</h1>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.warning("🛒 Giỏ hàng của bạn đang trống! Hãy chọn món từ **Thực đơn**.")
    else:
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.subheader("Chi tiết danh sách món đã chọn")
            total_raw = 0
            for idx, item in enumerate(st.session_state.cart):
                total_raw += item["price"]
                with st.container():
                    c1, c2, c3 = st.columns([3, 2, 1])
                    with c1:
                        st.markdown(f"**{item['name']}**")
                        st.caption(f"Ngọt: {item['sweetness']} | Đá: {item['ice']} | Topping: {', '.join(item['toppings']) if item['toppings'] else 'Không'}")
                        if item["note"]:
                            st.caption(f"📝 Ghi chú: {item['note']}")
                    with c2:
                        st.write(f"**{item['price']:,} VNĐ**")
                    with c3:
                        if st.button("❌ Xóa", key=f"del_{idx}"):
                            st.session_state.cart.pop(idx)
                            st.rerun()
                st.divider()

        with col_right:
            st.markdown("<div class='cart-box'>", unsafe_allow_html=True)
            st.subheader("🧾 Tổng Hóa Đơn")
            
            # Mã giảm giá
            v_code = st.text_input("Nhập mã Voucher giảm giá:", value=st.session_state.applied_voucher)
            if st.button("Áp dụng mã"):
                if v_code.upper() in VOUCHERS:
                    st.session_state.voucher_discount = VOUCHERS[v_code.upper()]
                    st.session_state.applied_voucher = v_code.upper()
                    st.success(f"Đã áp dụng mã **{v_code.upper()}** (Giảm {st.session_state.voucher_discount}%)")
                else:
                    st.error("Mã giảm giá không hợp lệ!")
            
            discount_amount = total_raw * (st.session_state.voucher_discount / 100)
            final_total = total_raw - discount_amount
            
            st.write(f"Tạm tính: **{total_raw:,} VNĐ**")
            st.write(f"Giảm giá ({st.session_state.voucher_discount}%): **-{discount_amount:,.0f} VNĐ**")
            st.markdown(f"### Tổng thanh toán:\n<h2 style='color:#8B0000;'>{final_total:,.0f} VNĐ</h2>", unsafe_allow_html=True)
            
            if st.button("💳 Tiến hành Thanh toán"):
                st.session_state.current_page = "Thanh toán & Đánh giá"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ----- TRANG 4: VÒNG QUAY MAY MẮN -----
elif st.session_state.current_page == "Vòng quay may mắn":
    st.markdown("<h1 class='title-indochine'>🎯 VÒNG QUAY MAY MẮN</h1>", unsafe_allow_html=True)
    st.write("Thử vận may của bạn để nhận Voucher ưu đãi đặc biệt từ Trà Quán Hoài Niệm!")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://picsum.photos/seed/wheel/400/400", caption="Vòng quay Hoài Niệm", use_container_width=True)
        if st.button("🎰 QUAY NGAY"):
            with st.spinner("Đang quay... Chờ chút nhé!"):
                time.sleep(2)
                prizes = [
                    ("Voucher HOAINIEM10 (Giảm 10%)", "HOAINIEM10"),
                    ("Voucher INDOCINE20 (Giảm 20%)", "INDOCINE20"),
                    ("Voucher MAYMAN15 (Giảm 15%)", "MAYMAN15"),
                    ("Chúc bạn may mắn lần sau!", None)
                ]
                res_name, res_code = random.choice(prizes)
                
                if res_code:
                    st.balloons()
                    st.success(f"🎉 Chúc mừng bạn đã trúng: **{res_name}**")
                    st.info(f"Mã của bạn là: **{res_code}**. Hãy sao chép mã này vào trang Giỏ hàng!")
                else:
                    st.warning("😅 Rất tiếc, chúc bạn may mắn lần sau!")

# ----- TRANG 5: THANH TOÁN & ĐÁNH GIÁ -----
elif st.session_state.current_page == "Thanh toán & Đánh giá":
    st.markdown("<h1 class='title-indochine'>THANH TOÁN & PHẢN HỒI</h1>", unsafe_allow_html=True)
    
    if not st.session_state.cart and not st.session_state.order_completed:
        st.warning("Chưa có đơn hàng nào cần thanh toán!")
    else:
        if not st.session_state.order_completed:
            st.subheader("1. Chọn phương thức thanh toán")
            pay_method = st.radio("Phương thức thanh toán", ["💵 Tiền mặt khi nhận hàng", "📱 Chuyển khoản QR Code"])
            
            if pay_method == "📱 Chuyển khoản QR Code":
                st.image("https://picsum.photos/seed/qrcode/250/250", caption="Quét mã QR VietQR để thanh toán")
                st.info("Nội dung chuyển khoản: HOAINIEM_SĐT_CUA_BAN")
            
            if st.button("✅ Xác nhận đã thanh toán"):
                st.session_state.order_completed = True
                st.success("Thanh toán thành công! Quán đang chuẩn bị đồ uống cho bạn.")
                st.rerun()
        else:
            st.success("🎉 Đơn hàng của bạn đã hoàn tất!")
            st.subheader("2. Đánh giá & Phản hồi dịch vụ")
            st.write("Cảm ơn bạn đã thưởng thức trà tại quán. Hãy để lại nhận xét để quán phục vụ tốt hơn nhé!")
            
            rating = st.feedback("stars")
            feedback = st.text_area("Lời nhắn/Đóng góp ý kiến gửi tới quán:")
            
            if st.button("📩 Gửi phản hồi"):
                st.toast("Cảm ơn những lời góp ý quý báu của quý khách!", icon="💌")
                st.balloons()
                # Clear session
                st.session_state.cart = []
                st.session_state.voucher_discount = 0
                st.session_state.applied_voucher = ""
                st.session_state.order_completed = False
