import streamlit as st
import random
import time

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & GIAO DIỆN PHONG CÁCH ĐÔNG DƯƠNG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Trà Quán Hoài Niệm - Sài Gòn Xưa",
    page_icon="🍵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tùy chỉnh CSS: Tone màu đỏ đô, xanh rêu đậm, vàng kem, hoa văn cổ điển Đông Dương
st.markdown("""
    <style>
    /* Tổng thể ứng dụng */
    .stApp {
        background-color: #F3EBDD;
        color: #2D241E;
        font-family: 'Times New Roman', 'Georgia', serif;
    }

    /* Sidebar - Menu bên trái */
    [data-testid="stSidebar"] {
        background-color: #1A382B;
        border-right: 3px solid #C5A059;
    }
    
    [data-testid="stSidebar"] * {
        color: #F3EBDD !important;
    }

    /* Tiêu đề phong cách Indochine */
    .title-indochine {
        text-align: center;
        color: #8B1A1A;
        font-family: 'Georgia', serif;
        font-weight: bold;
        text-transform: uppercase;
        border-bottom: 2px solid #C5A059;
        padding-bottom: 8px;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }

    /* Khung món ăn (Card) */
    .menu-card {
        background-color: #FAF6ED;
        border: 2px solid #C5A059;
        border-radius: 6px;
        padding: 12px;
        text-align: center;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.12);
        margin-bottom: 12px;
    }

    .price-tag {
        background-color: #8B1A1A;
        color: #F3EBDD;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: bold;
        display: inline-block;
        margin-top: 6px;
        font-size: 0.95em;
    }

    /* Nút bấm đồng bộ phong cách */
    .stButton>button {
        background-color: #8B1A1A !important;
        color: #FFFFFF !important;
        border-radius: 4px !important;
        border: 1px solid #C5A059 !important;
        font-weight: bold !important;
        width: 100%;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #1A382B !important;
        color: #F3EBDD !important;
        border-color: #F3EBDD !important;
    }

    /* Khung giỏ hàng & hóa đơn */
    .bill-box {
        background-color: #FAF6ED;
        border: 2px dashed #C5A059;
        padding: 15px;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. KHỞI TẠO SESSION STATE (QUẢN LÝ TRẠNG THÁI KHÔNG XUNG ĐỘT)
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
if "won_voucher" not in st.session_state:
    st.session_state.won_voucher = None

# Dữ liệu thực đơn chuẩn theo hình ảnh đính kèm
MENU = {
    "Trà sữa": [
        {
            "id": 1, "name": "Trà Sữa Cô Ba Sài Gòn", "price": 35000, 
            "desc": "Trà đậm vị, sữa thơm béo dịu dàng.", 
            "msg": "💌 Lời nhắn: 'Dành cho người yêu thích nét béo ngậy truyền thống Sài Gòn xưa.'",
            "img": "https://picsum.photos/seed/trasua_coba/300/220"
        },
        {
            "id": 2, "name": "Trà Sữa Tiệm May Xưa", "price": 39000, 
            "desc": "Vị trà thanh nhẹ, ngọt ngào như chuyện cũ.", 
            "msg": "💌 Lời nhắn: 'Nhẹ nhàng thanh tao như tà áo dài lụa Tân Châu.'",
            "img": "https://picsum.photos/seed/trasua_tiemmay/300/220"
        },
        {
            "id": 3, "name": "Trà Sữa Phố Đèn Lồng", "price": 38000, 
            "desc": "Hương trà thơm nồng, sữa béo quyện vị.", 
            "msg": "💌 Lời nhắn: 'Ấm áp lung linh như góc phố Chợ Lớn đêm Rằm.'",
            "img": "https://picsum.photos/seed/trasua_phodenlong/300/220"
        },
        {
            "id": 4, "name": "Trà Sữa Chiều Bên Hiên", "price": 42000, 
            "desc": "Ngọt dịu, mềm mại như buổi chiều yên ả.", 
            "msg": "💌 Lời nhắn: 'Thích hợp lắng nghe tiếng mưa rào trên mái ngói cũ.'",
            "img": "https://picsum.photos/seed/trasua_chieubenhien/300/220"
        },
        {
            "id": 5, "name": "Trà Sữa Bức Thư Tình", "price": 45000, 
            "desc": "Hương vị ngọt ngào gửi trao những nhớ thương.", 
            "msg": "💌 Lời nhắn: 'Gửi chút hương ngọt cho người phương xa.'",
            "img": "https://picsum.photos/seed/trasua_bucthutinh/300/220"
        }
    ],
    "Matcha": [
        {
            "id": 6, "name": "Matcha Ngọc Bích Đông Dương", "price": 42000, 
            "desc": "Matcha xanh mịn, thanh mát và tinh tế.", 
            "msg": "💌 Lời nhắn: 'Xanh trong tựa viên ngọc bích thời Đông Dương.'",
            "img": "https://picsum.photos/seed/matcha_ngocbich/300/220"
        },
        {
            "id": 7, "name": "Matcha Nắng Qua Rèm", "price": 45000, 
            "desc": "Matcha hòa sữa tươi, dịu dàng như nắng sớm.", 
            "msg": "💌 Lời nhắn: 'Chút nắng vệt qua rèm cửa gỗ măng-sơ.'",
            "img": "https://picsum.photos/seed/matcha_nangquarem/300/220"
        },
        {
            "id": 8, "name": "Matcha Vườn Ngọc Lan", "price": 47000, 
            "desc": "Vị trà xanh thanh mát gợi nhớ khu vườn xưa.", 
            "msg": "💌 Lời nhắn: 'Thơm thoảng như hương hoa ngọc lan trước sân.'",
            "img": "https://picsum.photos/seed/matcha_vuonngoclan/300/220"
        },
        {
            "id": 9, "name": "Matcha Gác Mái Xưa", "price": 48000, 
            "desc": "Matcha đậm vị, béo mịn và đầy lưu quyến.", 
            "msg": "💌 Lời nhắn: 'Khoảng tĩnh lặng trên căn gác gỗ phủ màu thời gian.'",
            "img": "https://picsum.photos/seed/matcha_gacmaixua/300/220"
        },
        {
            "id": 10, "name": "Matcha Trăng Bên Thềm", "price": 49000, 
            "desc": "Matcha thơm dịu, kết hợp đậm đà hài hòa.", 
            "msg": "💌 Lời nhắn: 'Ánh trăng huyền ảo rọi thềm nhà cổ.'",
            "img": "https://picsum.photos/seed/matcha_trangbenthem/300/220"
        }
    ],
    "Cà phê": [
        {
            "id": 11, "name": "Cà Phê Phin Sài Gòn Xưa", "price": 29000, 
            "desc": "Cà phê phin đậm đà, lưu giữ hương vị hoài niệm.", 
            "msg": "💌 Lời nhắn: 'Từng giọt đắng ngắt đọng lại vị ngọt hoài niệm.'",
            "img": "https://picsum.photos/seed/caphe_phin/300/220"
        },
        {
            "id": 12, "name": "Bạc Xỉu Góc Phố", "price": 32000, 
            "desc": "Sữa thơm béo, cà phê thoáng nhẹ thân quen.", 
            "msg": "💌 Lời nhắn: 'Đã thèm vị ngọt béo nơi quán quen góc đường.'",
            "img": "https://picsum.photos/seed/caphe_bacxiu/300/220"
        },
        {
            "id": 13, "name": "Cà Phê Ban Công Cũ", "price": 33000, 
            "desc": "Vị cà phê đậm vừa cho những phút giây lắng đọng.", 
            "msg": "💌 Lời nhắn: 'Ngắm nhìn dòng người qua lại trên chiếc ban công cũ.'",
            "img": "https://picsum.photos/seed/caphe_bancong/300/220"
        },
        {
            "id": 14, "name": "Cà Phê Đêm Sài Thành", "price": 35000, 
            "desc": "Đậm đà, mạnh mẽ như nhịp sống khi lên đèn.", 
            "msg": "💌 Lời nhắn: 'Thức cùng vẻ đẹp lung linh của đêm Sài Thành.'",
            "img": "https://picsum.photos/seed/caphe_demsaithanh/300/220"
        },
        {
            "id": 15, "name": "Cà Phê Thư Viện Cổ", "price": 38000, 
            "desc": "Hương vị cà phê sâu lắng, hợp những ngày hoài niệm.", 
            "msg": "💌 Lời nhắn: 'Trầm lắng bên sách cũ và tách cà phê đượm nồng.'",
            "img": "https://picsum.photos/seed/caphe_thuvien/300/220"
        }
    ]
}

VOUCHERS = {
    "HOAINIEM10": 10,
    "SAIGON20": 20,
    "MAYMAN15": 15
}

# ---------------------------------------------------------
# 3. ĐIỀU HƯỚNG MENU BÊN TRÁI (SIDEBAR)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #C5A059;'>TRÀ QUÁN HOÀI NIỆM</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic; font-size: 0.9em;'>HƯƠNG VỊ XƯA - CẢM XÚC MỚI</p>", unsafe_allow_html=True)
    st.divider()

    pages = ["Trang chủ", "Thực đơn", "Giỏ hàng", "Vòng quay may mắn", "Thanh toán", "Đánh giá & Phản hồi"]
    
    # Đồng bộ lựa chọn chuyển trang không gây xung đột state
    selected_page = st.radio(
        "Danh mục menu:",
        pages,
        index=pages.index(st.session_state.current_page)
    )
    
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        st.rerun()

    st.divider()
    st.markdown("🏮 **Sài Gòn xưa còn đó... trong từng ly trà!**")
    st.caption("📍 Địa chỉ: 12 Bùi Viện, Q.1, TP.HCM\n📞 ĐT: 0908 123 456")

# ---------------------------------------------------------
# 4. NỘI DUNG CÁC TRANG
# ---------------------------------------------------------

# --- TRANG 1: TRANG CHỦ & GIỚI THIỆU ---
if st.session_state.current_page == "Trang chủ":
    st.markdown("<h1 class='title-indochine'>TRÀ QUÁN HOÀI NIỆM</h1>", unsafe_allow_html=True)
    st.image("https://picsum.photos/seed/indochine_banner/1000/320", use_container_width=True)
    
    st.markdown("### 🏮 Giới Thiệu Về Quán")
    st.write("""
        **Trà Quán Hoài Niệm** tái hiện lại nét đẹp kiêu kỳ và hoài cổ của **Sài Gòn Xưa** thập niên 60-70. 
        Từng góc nhỏ tại quán đều mang đậm dấu ấn phong cách kiến trúc **Đông Dương (Indochine)** với màu gạch bông cổ điển, 
        đèn lồng đỏ và nhịp xích lô chậm rãi.

        Đến với chúng tôi, quý khách không chỉ thưởng thức những ly trà sữa béo thơm, tách cà phê phin đậm đà hay抹茶 thanh mát, 
        mà còn tìm lại chút lắng đọng và những ký ức ngọt ngào gửi gắm trong từng ly trà.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍵 Thưởng Thức Thực Đơn Ngay"):
            st.session_state.current_page = "Thực đơn"
            st.rerun()
    with col2:
        if st.button("🎡 Thử May Mắn Nhận Voucher"):
            st.session_state.current_page = "Vòng quay may mắn"
            st.rerun()

# --- TRANG 2: THỰC ĐƠN ---
elif st.session_state.current_page == "Thực đơn":
    st.markdown("<h1 class='title-indochine'>THỰC ĐƠN TRÀ QUÁN</h1>", unsafe_allow_html=True)
    
    tabs = st.tabs(["🧋 Trà Sữa", "🍵 Matcha", "☕ Cà Phê"])
    
    def render_menu_category(item_list):
        cols = st.columns(3)
        for idx, item in enumerate(item_list):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class='menu-card'>
                        <img src="{item['img']}" width="100%" height="150px" style="border-radius:4px; object-fit:cover;">
                        <h4 style="color:#8B1A1A; margin: 8px 0 4px 0;">{item['name']}</h4>
                        <p style="font-size:0.85em; color:#555; height:36px;">{item['desc']}</p>
                        <p style="font-size:0.8em; font-style:italic; color:#1A382B;">{item['msg']}</p>
                        <span class='price-tag'>{item['price']:,} VNĐ</span>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.expander(f"⚙️ Tùy chỉnh: {item['name']}"):
                    sweet = st.select_slider("Độ ngọt", options=["0%", "30%", "50%", "70%", "100%"], value="100%", key=f"sw_{item['id']}")
                    ice = st.select_slider("Lượng đá", options=["0%", "30%", "50%", "70%", "100%"], value="100%", key=f"ice_{item['id']}")
                    toppings = st.multiselect("Topping (+5,000đ/món)", ["Trân châu đen", "Thạch củ năng", "Pudding trứng", "Kem Cheese"], key=f"top_{item['id']}")
                    user_note = st.text_input("Lời nhắn gửi riêng:", placeholder="Ví dụ: Lấy ít đá, giao đúng giờ...", key=f"note_{item['id']}")
                    
                    if st.button("➕ Thêm vào giỏ hàng", key=f"btn_add_{item['id']}"):
                        extra_price = len(toppings) * 5000
                        cart_item = {
                            "id": item["id"],
                            "name": item["name"],
                            "base_price": item["price"],
                            "price": item["price"] + extra_price,
                            "sweetness": sweet,
                            "ice": ice,
                            "toppings": toppings,
                            "user_note": user_note,
                            "msg": item["msg"]
                        }
                        st.session_state.cart.append(cart_item)
                        st.toast(f"Đã thêm '{item['name']}' vào giỏ hàng!", icon="✅")

    with tabs[0]:
        render_menu_category(MENU["Trà sữa"])
    with tabs[1]:
        render_menu_category(MENU["Matcha"])
    with tabs[2]:
        render_menu_category(MENU["Cà phê"])

# --- TRANG 3: GIỎ HÀNG & HÓA ĐƠN ---
elif st.session_state.current_page == "Giỏ hàng":
    st.markdown("<h1 class='title-indochine'>GIỎ HÀNG & HÓA ĐƠN DETAILED</h1>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.info("🛒 Giỏ hàng của bạn đang trống! Hãy quay lại **Thực đơn** để chọn đồ uống yêu thích.")
    else:
        col_list, col_bill = st.columns([2, 1])
        
        with col_list:
            st.subheader("📋 Món đã chọn")
            total_raw = 0
            
            # Liệt kê món trong giỏ
            items_to_remove = []
            for idx, item in enumerate(st.session_state.cart):
                total_raw += item["price"]
                with st.container():
                    c1, c2, c3 = st.columns([3, 1, 1])
                    with c1:
                        st.markdown(f"**{item['name']}**")
                        st.caption(f"Độ ngọt: {item['sweetness']} | Đá: {item['ice']}")
                        if item["toppings"]:
                            st.caption(f"Topping: {', '.join(item['toppings'])}")
                        if item["user_note"]:
                            st.caption(f"📝 Lời nhắn của bạn: {item['user_note']}")
                        st.caption(f"✨ *{item['msg']}*")
                    with c2:
                        st.write(f"**{item['price']:,}đ**")
                    with c3:
                        if st.button("🗑️ Xóa", key=f"del_{idx}"):
                            items_to_remove.append(idx)
                st.divider()

            if items_to_remove:
                for idx in reversed(items_to_remove):
                    st.session_state.cart.pop(idx)
                st.rerun()

        with col_bill:
            st.markdown("<div class='bill-box'>", unsafe_allow_html=True)
            st.subheader("🧾 Hóa Đơn Tạm Tính")
            
            # Nhập Voucher
            v_input = st.text_input("Nhập mã Voucher:", value=st.session_state.applied_voucher)
            if st.button("Áp dụng Voucher"):
                if v_input.upper() in VOUCHERS:
                    st.session_state.voucher_discount = VOUCHERS[v_input.upper()]
                    st.session_state.applied_voucher = v_input.upper()
                    st.success(f"Đã giảm {st.session_state.voucher_discount}%!")
                else:
                    st.error("Mã Voucher không chính xác!")
            
            discount_val = total_raw * (st.session_state.voucher_discount / 100)
            final_total = total_raw - discount_val
            
            st.write(f"Tổng tiền món: **{total_raw:,} VNĐ**")
            st.write(f"Voucher giảm giá ({st.session_state.voucher_discount}%): **-{discount_val:,.0f} VNĐ**")
            st.markdown(f"### Tổng thanh toán:\n<h2 style='color:#8B1A1A;'>{final_total:,.0f} VNĐ</h2>", unsafe_allow_html=True)
            
            if st.button("💳 Đến Thanh Toán"):
                st.session_state.current_page = "Thanh toán"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# --- TRANG 4: VÒNG QUAY MAY MẮN ---
elif st.session_state.current_page == "Vòng quay may mắn":
    st.markdown("<h1 class='title-indochine'>🎡 VÒNG QUAY MAY MẮN HOÀI NIỆM</h1>", unsafe_allow_html=True)
    st.write("Quay ngay để nhận Voucher ưu đãi độc quyền dành cho khách hàng!")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://picsum.photos/seed/vintage_wheel/400/400", caption="Vòng Quay May Mắn Sài Gòn Xưa", use_container_width=True)
        
        if st.button("🎯 QUAY VÒNG MAY MẮN"):
            with st.spinner("Vòng quay đang quay..."):
                time.sleep(1.5)
                outcomes = [
                    ("Voucher SAIGON20 - Giảm 20%", "SAIGON20"),
                    ("Voucher HOAINIEM10 - Giảm 10%", "HOAINIEM10"),
