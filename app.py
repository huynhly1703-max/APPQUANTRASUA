import streamlit as st
import random
import uuid
import html
from datetime import datetime

st.set_page_config(page_title="Trà Quán Hoài Niệm", page_icon="🍵", layout="wide")

# -------------------- SESSION STATE --------------------
DEFAULTS = {
    "page": "Trang chủ",
    "cart": [],
    "voucher": "",
    "paid": False,
    "order_id": "",
    "last_order": [],
    "last_subtotal": 0,
    "last_discount": 0,
    "last_total": 0,
    "last_payment": "",
    "last_customer": "",
    "feedback_sent": False,
    "feedback_rating": 5,
    "feedback_text": "",
    "spin_result": None,
    "spin_history": [],
    "nav_radio": "Trang chủ",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -------------------- INDOCHINE DESIGN --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700;800&display=swap');
:root {
 --cream:#F3E4C5; --paper:#E8D2A6; --green:#123D35; --green2:#1B5146;
 --wine:#76252B; --wine2:#9B3B37; --gold:#C69B50; --ink:#2B2119;
}
.stApp {background:#E9D6B0;color:var(--ink);font-family:'Be Vietnam Pro',sans-serif;}
[data-testid="stHeader"]{background:rgba(232,210,166,.94);}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#123D35,#0D2D28);border-right:3px solid var(--gold);}
[data-testid="stSidebar"] *{color:var(--cream);}
h1,h2,h3{font-family:'Playfair Display',Georgia,serif!important;color:var(--green)!important;}
p, label, .stMarkdown{color:var(--ink);}
div[data-testid="stVerticalBlockBorderWrapper"]{border-color:#B58A49!important;}
.stButton>button{background:var(--wine);color:#FFF1D6!important;border:1px solid var(--gold);border-radius:2px;font-weight:700;min-height:40px;}
.stButton>button:hover{background:var(--green);color:#FFF1D6!important;border-color:#E7C77D;}
.stButton>button p{color:inherit!important;}
div[data-baseweb="input"] input,div[data-baseweb="select"]>div,.stTextArea textarea{
 background:#FFF4D9!important;color:#2B2119!important;border:1px solid #B58A49!important;border-radius:2px!important;
}
div[data-testid="stNumberInput"] button{background:#76252B;color:#fff;}
.stRadio label,.stCheckbox label{color:#2B2119!important;}
[data-testid="stSidebar"] .stRadio label{color:#F3E4C5!important;}
hr{border-color:#B58A49!important;}
.poster-banner{
 position:relative;text-align:center;padding:25px 18px 22px;margin:0 0 16px;
 color:#F3E4C5;background:
 radial-gradient(circle at 8% 20%,#C69B5030 0 2px,transparent 3px),
 radial-gradient(circle at 90% 80%,#C69B5030 0 2px,transparent 3px),
 linear-gradient(110deg,#123D35,#19483D 50%,#76252B);
 border:3px double #D8B66E;outline:1px solid #123D35;outline-offset:-8px;
}
.poster-kicker{font-size:11px;letter-spacing:5px;color:#E8C77F;text-transform:uppercase;}
.poster-title{font-family:'Playfair Display',Georgia,serif;font-size:clamp(30px,4vw,54px);font-weight:800;line-height:1.05;color:#F6E8C9;letter-spacing:2px;margin:8px 0;}
.poster-sub{color:#E8D2A6;letter-spacing:2px;font-size:12px;}
.cornerline{color:#D8B66E;letter-spacing:8px;font-size:13px;margin:7px;}
.poster-card{background:#F6E8C9;border:2px solid #9B773F;outline:1px solid #D6B66E;outline-offset:-6px;padding:8px;border-radius:2px;text-align:center;box-shadow:2px 4px 0 #6D4C2C22;margin-bottom:8px;}
.poster-card .category{font-size:10px;letter-spacing:2px;font-weight:800;color:#F3E4C5;background:#123D35;padding:5px;margin:1px 0 7px;}
.poster-card .name{font-family:'Playfair Display',Georgia,serif;color:#30241A;font-size:18px;font-weight:800;line-height:1.15;min-height:44px;margin:7px 0 5px;}
.poster-card .desc{font-size:11px;line-height:1.5;color:#4D3B2A;min-height:34px;}
.poster-card .price{display:inline-block;background:#123D35;color:#F8E7BF;border:1px solid #C69B50;border-radius:20px;padding:4px 14px;font-weight:800;font-size:13px;margin:7px 0 2px;}
.poster-card .orn{font-size:14px;color:#9B773F;letter-spacing:3px;}
.section-ribbon{background:#123D35;color:#F3E4C5;border:2px double #C69B50;padding:10px 14px;font-family:'Playfair Display',Georgia,serif;font-size:22px;margin:18px 0 12px;}
.section-ribbon span{color:#E8C77F;font-size:11px;letter-spacing:2px;float:right;padding-top:8px;}
.paperbox{background:#F6E8C9;border:2px solid #B58A49;padding:15px;color:#2B2119;}
.paperbox h3{color:#123D35!important;}
.muted{font-size:12px;color:#755E43;}
.price-big{font-family:'Playfair Display',Georgia,serif;color:#76252B;font-size:24px;font-weight:800;}
.receipt{background:#FFF4D9;color:#2B2119;border:2px dashed #B58A49;padding:16px;}
.receipt *{color:#2B2119!important;}
div[data-testid="stMetric"]{background:#F6E8C9;border:1px solid #B58A49;padding:12px;}
div[data-testid="stMetricLabel"]{color:#4D3B2A!important;}
div[data-testid="stMetricValue"]{color:#76252B!important;}
footer,#MainMenu{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

MENU = [
    # Trà sữa
    {"id":"ts01","name":"Trà Sữa Cô Ba Sài Gòn","category":"Trà sữa","price":35000,"desc":"Trà đen đậm vị, sữa thơm béo dịu dàng.","emoji":"🧋","color":"wine"},
    {"id":"ts02","name":"Trà Sữa Tiệm May Xưa","category":"Trà sữa","price":39000,"desc":"Vị trà thanh nhẹ, ngọt ngào như chuyện cũ.","emoji":"🥤","color":"green"},
    {"id":"ts03","name":"Trà Sữa Phố Đèn Lồng","category":"Trà sữa","price":38000,"desc":"Hương trà thơm nồng, sữa béo quyện vị.","emoji":"🏮","color":"wine"},
    {"id":"ts04","name":"Trà Sữa Chiều Bên Hiên","category":"Trà sữa","price":42000,"desc":"Ngọt dịu, mềm mại như buổi chiều yên ả.","emoji":"🌸","color":"green"},
    {"id":"ts05","name":"Trà Sữa Bức Thư Tình","category":"Trà sữa","price":45000,"desc":"Hương vị ngọt ngào gửi trao những nhớ thương.","emoji":"💌","color":"wine"},
    # Matcha
    {"id":"ma01","name":"Matcha Ngọc Bích Đông Dương","category":"Matcha","price":42000,"desc":"Matcha xanh mịn, thanh tao và tinh tế.","emoji":"🍵","color":"green"},
    {"id":"ma02","name":"Matcha Nắng Qua Rèm","category":"Matcha","price":45000,"desc":"Matcha hòa sữa tươi, dịu dàng như nắng sớm.","emoji":"🌿","color":"green"},
    {"id":"ma03","name":"Matcha Vườn Ngọc Lan","category":"Matcha","price":47000,"desc":"Vị trà xanh thanh mát gợi nhớ khu vườn xưa.","emoji":"🌼","color":"green"},
    {"id":"ma04","name":"Matcha Gác Mái Xưa","category":"Matcha","price":48000,"desc":"Matcha đậm vị, béo mịn và đầy lưu luyến.","emoji":"🏡","color":"green"},
    {"id":"ma05","name":"Matcha Trăng Bên Thềm","category":"Matcha","price":49000,"desc":"Matcha thơm dịu, kết hợp đậu đỏ bùi ngọt.","emoji":"🌙","color":"green"},
    # Cà phê
    {"id":"cf01","name":"Cà Phê Phin Sài Gòn Xưa","category":"Cà phê","price":29000,"desc":"Cà phê phin đậm đà, lưu giữ hương vị phố xưa.","emoji":"☕","color":"wine"},
    {"id":"cf02","name":"Bạc Xỉu Góc Phố","category":"Cà phê","price":32000,"desc":"Sữa thơm béo, cà phê thoảng nhẹ thân quen.","emoji":"🥛","color":"wine"},
    {"id":"cf03","name":"Cà Phê Ban Công Cũ","category":"Cà phê","price":33000,"desc":"Vị cà phê đậm sâu cho những phút giây lắng đọng.","emoji":"🏛️","color":"green"},
    {"id":"cf04","name":"Cà Phê Đêm Sài Thành","category":"Cà phê","price":35000,"desc":"Đậm đà, mạnh mẽ như nhịp phố khi lên đèn.","emoji":"🌃","color":"wine"},
    {"id":"cf05","name":"Cà Phê Thư Viện Cũ","category":"Cà phê","price":38000,"desc":"Hương cà phê sâu lắng, hợp những ngày hoài niệm.","emoji":"📚","color":"wine"},
]

TOPPINGS = {"Không topping":0,"Trân châu đen":7000,"Trân châu trắng":8000,"Thạch cà phê":7000,"Pudding trứng":9000,"Kem cheese":10000,"Đậu đỏ":8000}
VOUCHERS = {
    "HOAINIEM10":{"rate":.10,"min":50000,"desc":"Giảm 10% cho đơn từ 50.000đ"},
    "TRASUA15":{"rate":.15,"min":100000,"desc":"Giảm 15% cho đơn từ 100.000đ"},
    "DONGDUONG20":{"rate":.20,"min":150000,"desc":"Giảm 20% cho đơn từ 150.000đ"},
}
PRIZES = [
    {"name":"Giảm 10% đơn hàng","code":"HOAINIEM10"},
    {"name":"Giảm 15% đơn từ 100.000đ","code":"TRASUA15"},
    {"name":"Tặng topping miễn phí","code":"TOPPINGFREE"},
    {"name":"Giảm 20% đơn từ 150.000đ","code":"DONGDUONG20"},
    {"name":"Một lời chúc an lành","code":"LOICHUC"},
    {"name":"Lời chúc từ Sài Gòn xưa","code":"HOAINIEM"},
]

def money(n):
    return f"{int(n):,}".replace(",", ".") + "đ"

def nav(page):
    st.session_state.page = page
    st.session_state.nav_radio = page

def subtotal():
    return sum(x["unit_price"] * x["quantity"] for x in st.session_state.cart)

def discount():
    code = st.session_state.voucher
    voucher = VOUCHERS.get(code)
    if voucher and subtotal() >= voucher["min"]:
        return int(subtotal() * voucher["rate"])
    return 0

def total():
    return max(0, subtotal() - discount())

def safe(text):
    return html.escape(str(text))

# -------------------- SIDEBAR --------------------
PAGES = ["Trang chủ","Thực đơn","Giỏ hàng & thanh toán","Vòng quay may mắn","Đánh giá & phản hồi"]
with st.sidebar:
    st.markdown("<div style='text-align:center;font-size:40px;color:#D8B66E'>❦</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;color:#F3E4C5!important;font-size:26px'>TRÀ QUÁN<br>HOÀI NIỆM</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#D8B66E;letter-spacing:2px'>HƯƠNG VỊ XƯA · CẢM XÚC MỚI</p>", unsafe_allow_html=True)
    st.divider()
    # Một nguồn trạng thái duy nhất cho radio; các nút gọi nav() rồi rerun.
    st.radio(
    "ĐIỀU HƯỚNG",
    PAGES,
    key="nav_radio",
    label_visibility="collapsed",
    on_change=lambda: st.session_state.update(
        page=st.session_state.nav_radio
    )
)
    st.divider()
    st.markdown("### 🛒 Giỏ hàng")
    st.metric("Số lượng ly", sum(x["quantity"] for x in st.session_state.cart))
    st.metric("Tạm tính", money(subtotal()))
    if st.button("Mở giỏ hàng", use_container_width=True):
        nav("Giỏ hàng & thanh toán")
        st.rerun()
    st.markdown("---")
    st.markdown("<div style='color:#D8B66E;font-family:serif;font-style:italic;font-size:20px'>Sài Gòn xưa còn đó...<br>trong từng ly trà.</div>", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("""
<div class="poster-banner">
 <div class="poster-kicker">✦ Saigon · Indochine · Since 1968 ✦</div>
 <div class="cornerline">❦ ━━━━━━━━━━━━━━━━━━━━━ ❦</div>
 <div class="poster-title">TRÀ QUÁN HOÀI NIỆM</div>
 <div class="poster-sub">HƯƠNG VỊ XƯA — CẢM XÚC MỚI</div>
 <div class="cornerline">✦ Một ly trà · Một chút ký ức ✦</div>
</div>
""", unsafe_allow_html=True)

# -------------------- HOME --------------------
if st.session_state.page == "Trang chủ":
    st.markdown('<div class="section-ribbon">Chạm vào miền ký ức <span>WELCOME TO OUR TEA HOUSE</span></div>', unsafe_allow_html=True)
    left, right = st.columns([1.1,1])
    with left:
        st.markdown("""
        <div class="paperbox">
          <div style="font-size:12px;letter-spacing:3px;color:#8B642F">CÂU CHUYỆN CỦA QUÁN</div>
          <h2 style="font-family:Georgia,serif;color:#123D35">Một góc Sài Gòn xưa giữa nhịp sống mới</h2>
          <p>Trà Quán Hoài Niệm lấy cảm hứng từ kiến trúc Đông Dương, những tấm áp phích quảng cáo xưa và nét duyên của phố Sài Gòn thập niên 1960–1980.</p>
          <p>Mỗi thức uống là một câu chuyện nhỏ — từ ly trà sữa ngọt dịu, matcha xanh thanh đến cà phê phin đậm đà.</p>
          <div style="text-align:center;color:#8B642F;font-size:20px">❦ ✦ ❦</div>
        </div>
        """, unsafe_allow_html=True)
    with right:
        st.markdown("""
        <div class="paperbox" style="background:#123D35;color:#F3E4C5">
          <div style="font-size:12px;letter-spacing:3px;color:#D8B66E">THE INDOCHINE SPIRIT</div>
          <h2 style="color:#F3E4C5!important">Thưởng trà — kể chuyện — nhớ thương</h2>
          <p style="color:#F3E4C5">Tông xanh cổ vịt, đỏ rượu vang, giấy ngả màu thời gian và họa tiết hoa lá tạo nên không gian hoài cổ mà gần gũi.</p>
          <p style="color:#E8D2A6">Mở cửa: 08:00 – 22:00</p>
          <div style="color:#D8B66E;font-size:22px">❧ ━ ❧ ━ ❧</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('<div class="section-ribbon">Ba hương vị đặc trưng <span>OUR SIGNATURES</span></div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for col, emoji, title, desc in zip(cols, ["🧋","🍵","☕"], ["Trà sữa","Matcha","Cà phê"], ["Béo thơm, ngọt dịu, thân quen.","Thanh mát, tinh tế, xanh ngọc.","Đậm đà, sâu lắng, phong vị Sài Gòn."]):
        with col:
            st.markdown(f'<div class="paperbox" style="text-align:center"><div style="font-size:42px">{emoji}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
    if st.button("✦ KHÁM PHÁ THỰC ĐƠN ✦", use_container_width=True):
        nav("Thực đơn")
        st.rerun()

# -------------------- MENU --------------------
elif st.session_state.page == "Thực đơn":
    st.markdown('<div class="section-ribbon">Thực đơn áp phích <span>THE VINTAGE COLLECTION</span></div>', unsafe_allow_html=True)
    st.write("Mỗi món là một tấm áp phích nhỏ lấy cảm hứng từ bảng màu và họa tiết Đông Dương.")
    category = st.radio("Chọn bộ sưu tập", ["Tất cả","Trà sữa","Matcha","Cà phê"], horizontal=True, key="menu_filter")
    products = [p for p in MENU if category == "Tất cả" or p["category"] == category]
    for cat in (["Trà sữa","Matcha","Cà phê"] if category == "Tất cả" else [category]):
        group = [p for p in products if p["category"] == cat]
        if not group:
            continue
        st.markdown(f'<div class="section-ribbon">{cat}<span>❦ BỘ SƯU TẬP ❦</span></div>', unsafe_allow_html=True)
        for start in range(0, len(group), 5):
            cards = st.columns(5)
            for col, p in zip(cards, group[start:start+5]):
                with col:
                    theme = "#76252B" if p["color"] == "wine" else "#123D35"
                    st.markdown(f"""
                    <div class="poster-card">
                      <div class="orn">❦ ✦ ❦</div>
                      <div class="category" style="background:{theme}">{safe(p["category"].upper())}</div>
                      <div style="background:linear-gradient(145deg,{theme},#D6B66E);padding:12px 3px;border:1px solid #B58A49">
                        <div style="font-size:57px;line-height:1.25">{p["emoji"]}</div>
                        <div style="font-size:10px;color:#FFF0D2;letter-spacing:2px">HOÀI NIỆM · 1968</div>
                      </div>
                      <div class="name">{safe(p["name"])}</div>
                      <div class="desc">{safe(p["desc"])}</div>
                      <div class="price">{money(p["price"])}</div>
                      <div class="orn">❧ ━ ❧</div>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.expander("Tùy chỉnh & đặt món"):
                        topping = st.selectbox("Topping", list(TOPPINGS), key=f"top_{p['id']}")
                        sweetness = st.select_slider("Độ ngọt", ["0%","30%","50%","70%","100%"], value="70%", key=f"sweet_{p['id']}")
                        ice = st.selectbox("Lượng đá", ["Không đá","Ít đá","Bình thường","Nhiều đá"], index=1, key=f"ice_{p['id']}")
                        qty = st.number_input("Số lượng", min_value=1, max_value=20, value=1, key=f"qty_{p['id']}")
                        note = st.text_input("Lời nhắn riêng", placeholder="Ví dụ: Ghi tên lên ly...", key=f"note_{p['id']}")
                        st.caption(f"Đơn giá: {money(p['price'] + TOPPINGS[topping])}")
                        if st.button("＋ Thêm vào giỏ", key=f"add_{p['id']}", use_container_width=True):
                            st.session_state.cart.append({
                                "cart_id":str(uuid.uuid4()), "product_id":p["id"],
                                "name":p["name"], "category":p["category"],
                                "base_price":p["price"], "topping":topping,
                                "topping_price":TOPPINGS[topping], "sweetness":sweetness,
                                "ice":ice, "note":note.strip(), "quantity":int(qty),
                                "unit_price":p["price"] + TOPPINGS[topping]
                            })
                            st.success("Đã thêm món vào giỏ!")
                            st.rerun()
    a, b = st.columns(2)
    with a:
        if st.button("← Trang chủ", use_container_width=True):
            nav("Trang chủ")
            st.rerun()
    with b:
        if st.button("Xem giỏ hàng →", use_container_width=True):
            nav("Giỏ hàng & thanh toán")
            st.rerun()

# -------------------- CART / CHECKOUT --------------------
elif st.session_state.page == "Giỏ hàng & thanh toán":
    st.markdown('<div class="section-ribbon">Giỏ hàng & hóa đơn <span>YOUR ORDER</span></div>', unsafe_allow_html=True)
    if not st.session_state.cart:
        st.info("Giỏ hàng đang trống. Hãy chọn một thức uống từ thực đơn.")
        if st.button("Khám phá thực đơn", use_container_width=True):
            nav("Thực đơn")
            st.rerun()
    else:
        for item in st.session_state.cart[:]:
            with st.container(border=True):
                c1,c2,c3 = st.columns([3,1,1])
                with c1:
                    st.markdown(f"**{item['name']}**")
                    st.caption(f"{item['topping']} · Ngọt {item['sweetness']} · {item['ice']}")
                    if item["note"]:
                        st.caption("Lời nhắn: " + item["note"])
                    st.write(f"Đơn giá: {money(item['unit_price'])}")
                with c2:
                    q = st.number_input("SL", min_value=1, max_value=20, value=int(item["quantity"]), key=f"cartqty_{item['cart_id']}")
                    if q != item["quantity"]:
                        item["quantity"] = int(q)
                        st.rerun()
                with c3:
                    st.markdown(f"**{money(item['unit_price']*item['quantity'])}**")
                    if st.button("🗑️ Xóa", key=f"del_{item['cart_id']}"):
                        st.session_state.cart = [x for x in st.session_state.cart if x["cart_id"] != item["cart_id"]]
                        st.rerun()

        st.markdown("### 🎟️ Voucher ưu đãi")
        st.caption("HOAINIEM10 · TRASUA15 · DONGDUONG20")
        vc1,vc2,vc3 = st.columns([3,1,1])
        with vc1:
            voucher_text = st.text_input("Mã voucher", value=st.session_state.voucher, placeholder="Nhập mã voucher", key="voucher_entry")
        with vc2:
            if st.button("Áp dụng", use_container_width=True):
                code = voucher_text.strip().upper()
                if code not in VOUCHERS:
                    st.error("Mã voucher không hợp lệ.")
                elif subtotal() < VOUCHERS[code]["min"]:
                    st.error(f"Đơn chưa đạt mức tối thiểu {money(VOUCHERS[code]['min'])}.")
                else:
                    st.session_state.voucher = code
                    st.success(VOUCHERS[code]["desc"])
                    st.rerun()
        with vc3:
            if st.button("Bỏ mã", use_container_width=True):
                st.session_state.voucher = ""
                st.rerun()

        if st.session_state.voucher and subtotal() < VOUCHERS[st.session_state.voucher]["min"]:
            st.session_state.voucher = ""
            st.warning("Voucher đã được gỡ vì đơn hàng không còn đủ điều kiện.")
            st.rerun()

        sub, disc, grand = subtotal(), discount(), total()
        st.markdown('<div class="receipt">', unsafe_allow_html=True)
        st.markdown("### TRÀ QUÁN HOÀI NIỆM")
        st.write("HÓA ĐƠN TẠM TÍNH")
        st.write(f"Tạm tính: **{money(sub)}**")
        st.write(f"Voucher giảm giá: **- {money(disc)}**")
        st.markdown(f'<div class="price-big">TỔNG THANH TOÁN: {money(grand)}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("### Thông tin khách hàng")
        customer = st.text_input("Tên khách hàng", key="checkout_customer", placeholder="Nhập tên của bạn")
        payment = st.radio("Phương thức thanh toán", ["Tiền mặt tại quán","Quét mã QR minh họa"], horizontal=True, key="checkout_payment")
        if payment == "Quét mã QR minh họa":
            st.markdown(f"""
            <div style="background:#FFF4D9;color:#2B2119;border:3px double #B58A49;max-width:320px;margin:auto;padding:18px;text-align:center">
              <div style="font-family:Georgia;font-size:19px;font-weight:bold">TRÀ QUÁN HOÀI NIỆM</div>
              <div style="font-size:12px;margin:8px">MÃ QR MINH HỌA — KHÔNG PHẢI QR NGÂN HÀNG</div>
              <div style="font-size:90px;line-height:1.1">▦</div>
              <div style="font-size:26px;font-weight:bold">{money(grand)}</div>
              <div style="font-size:12px">{safe(customer or "Khách hàng")} · DEMO</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("QR chỉ minh họa giao diện; không thể nhận hoặc xác minh chuyển khoản thật.")
        if st.button("✓ XÁC NHẬN THANH TOÁN", use_container_width=True):
            if not customer.strip():
                st.error("Vui lòng nhập tên khách hàng.")
            else:
                st.session_state.paid = True
                st.session_state.order_id = "HN" + datetime.now().strftime("%y%m%d%H%M%S")
                st.session_state.last_order = [x.copy() for x in st.session_state.cart]
                st.session_state.last_subtotal = sub
                st.session_state.last_discount = disc
                st.session_state.last_total = grand
                st.session_state.last_payment = payment
                st.session_state.last_customer = customer.strip()
                st.session_state.cart = []
                st.session_state.voucher = ""
                st.session_state.feedback_sent = False
                nav("Đánh giá & phản hồi")
                st.rerun()
        if st.button("← Tiếp tục chọn món", use_container_width=True):
            nav("Thực đơn")
            st.rerun()

# -------------------- LUCKY WHEEL --------------------
elif st.session_state.page == "Vòng quay may mắn":
    st.markdown('<div class="section-ribbon">Vòng quay may mắn <span>A LITTLE GIFT FOR YOU</span></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="paperbox" style="text-align:center;background:#123D35;color:#F3E4C5">
      <div style="font-size:82px">🎡</div>
      <h2 style="color:#F3E4C5!important">Vòng quay ký ức</h2>
      <p style="color:#E8D2A6">Một chút may mắn — một chút ngọt ngào</p>
      <div style="font-size:22px;color:#D8B66E">❦ ✦ ❦</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🎁 QUAY NGAY", use_container_width=True):
        prize = random.choice(PRIZES)
        st.session_state.spin_result = prize
        st.session_state.spin_history.append({"time":datetime.now().strftime("%H:%M:%S %d/%m/%Y"), **prize})
        st.rerun()
    if st.session_state.spin_result:
        prize = st.session_state.spin_result
        st.success(f"🎉 Bạn nhận được: {prize['name']}")
        st.markdown(f'<div class="paperbox" style="text-align:center"><h2>{safe(prize["name"])}</h2><p>Mã quà: <b>{safe(prize["code"])}</b></p></div>', unsafe_allow_html=True)
        if prize["code"] in VOUCHERS:
            if st.button("Lưu voucher vào phiên đặt hàng"):
                st.session_state.voucher = prize["code"]
                st.success("Đã lưu voucher cho đơn hàng tiếp theo.")
        elif prize["code"] == "TOPPINGFREE":
            st.info("Quà topping là minh họa; vui lòng xác nhận với nhân viên khi vận hành thực tế.")
        else:
            st.info("Một lời chúc hoài niệm dành riêng cho bạn!")
    if st.session_state.spin_history:
        st.markdown("### Lịch sử quay trong phiên")
        for x in reversed(st.session_state.spin_history):
            st.write(f"🎁 {x['time']} — {x['name']} ({x['code']})")

# -------------------- FEEDBACK --------------------
elif st.session_state.page == "Đánh giá & phản hồi":
    st.markdown('<div class="section-ribbon">Đánh giá & phản hồi <span>YOUR WORDS MATTER</span></div>', unsafe_allow_html=True)
    if not st.session_state.paid and not st.session_state.feedback_sent:
        st.info("Biểu mẫu đánh giá sẽ xuất hiện sau khi bạn xác nhận thanh toán.")
        if st.button("← Về trang chủ", use_container_width=True):
            nav("Trang chủ")
            st.rerun()
    else:
        st.markdown(f"""
        <div class="paperbox">
          <div style="font-size:11px;letter-spacing:3px;color:#8B642F">PAYMENT CONFIRMATION</div>
          <h2>Trà Quán Hoài Niệm</h2>
          <p>Mã đơn: <b>{safe(st.session_state.order_id)}</b></p>
          <p>Khách hàng: <b>{safe(st.session_state.last_customer)}</b></p>
          <p>Phương thức: <b>{safe(st.session_state.last_payment)}</b></p>
          <div class="price-big">Tổng thanh toán: {money(st.session_state.last_total)}</div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Xem lại hóa đơn"):
            for item in st.session_state.last_order:
                st.write(f"{item['name']} × {item['quantity']} — {money(item['unit_price']*item['quantity'])}")
            st.write(f"Tạm tính: {money(st.session_state.last_subtotal)}")
            st.write(f"Giảm giá: {money(st.session_state.last_discount)}")
            st.write(f"Tổng cộng: {money(st.session_state.last_total)}")

        if not st.session_state.feedback_sent:
            st.markdown("### 🌸 Một vài lời gửi đến quán")
            rating = st.select_slider("Bạn chấm quán bao nhiêu sao?", options=[1,2,3,4,5], value=5, format_func=lambda x: "⭐" * x, key="rating_input")
            feedback = st.text_area("Lời nhắn dành cho chúng mình", placeholder="Hương vị, dịch vụ, không gian... Bạn cứ chia sẻ thật lòng nhé!", key="feedback_input")
            if st.button("GỬI ĐÁNH GIÁ", use_container_width=True):
                st.session_state.feedback_rating = rating
                st.session_state.feedback_text = feedback.strip()
                st.session_state.feedback_sent = True
                st.session_state.paid = False
                st.rerun()
        else:
            st.success(f"Cảm ơn bạn đã đánh giá {'⭐' * st.session_state.feedback_rating}!")
            if st.session_state.feedback_text:
                st.markdown(f'<div class="paperbox"><b>LỜI NHẮN CỦA BẠN</b><p>{safe(st.session_state.feedback_text)}</p></div>', unsafe_allow_html=True)
            st.caption("Đánh giá hiện được lưu trong phiên ứng dụng. Có thể tích hợp cơ sở dữ liệu để lưu lâu dài.")
        if st.button("🏠 Trở về trang chủ", use_container_width=True):
            nav("Trang chủ")
            st.rerun()

# -------------------- FOOTER --------------------
st.markdown("""
<div style="margin-top:25px;background:#123D35;border:2px double #C69B50;text-align:center;padding:14px;color:#F3E4C5">
 <div style="color:#D8B66E;letter-spacing:5px">❦ HOÀI NIỆM ❦</div>
 <div style="font-family:Georgia,serif;font-size:16px;margin:6px">Hơn cả một ly trà, đó là ký ức!</div>
 <div style="font-size:10px;letter-spacing:2px;color:#E8D2A6">INDOCHINE TEA HOUSE · SAIGON</div>
</div>
""", unsafe_allow_html=True)

