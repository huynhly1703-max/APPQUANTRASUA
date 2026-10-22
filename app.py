import streamlit as st
import random
import qrcode
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Trà Quán Hoài Niệm", page_icon="🍵", layout="wide", initial_sidebar_state="expanded")

# Bảng màu Đông Dương: xanh rêu, vàng nghệ, đỏ gạch, kem giấy
MOSS = "#203F32"
MOSS_LIGHT = "#315847"
TURMERIC = "#E4B548"
BRICK = "#B74735"
PAPER = "#F7EEDB"
PAPER_DARK = "#E8D8B9"
INK = "#2C3026"
MUTED = "#766B58"
WHITE = "#FFF9ED"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&family=Playfair+Display:wght@500;600;700;800&display=swap');
:root{--moss:#203F32;--moss-light:#315847;--turmeric:#E4B548;--brick:#B74735;--paper:#F7EEDB;--paper-dark:#E8D8B9;--ink:#2C3026;--muted:#766B58;--white:#FFF9ED}
.stApp{background:radial-gradient(ellipse at 4% 3%,rgba(228,181,72,.13),transparent 25%),radial-gradient(ellipse at 96% 96%,rgba(183,71,53,.08),transparent 28%),var(--paper);color:var(--ink);font-family:'Be Vietnam Pro',sans-serif}
[data-testid="stHeader"]{background:rgba(247,238,219,.92)}
[data-testid="stSidebar"]{background:var(--moss);border-right:4px solid var(--turmeric)}
[data-testid="stSidebar"] *{color:var(--paper)}
[data-testid="stSidebar"] [data-testid="stButton"] button{background:var(--moss-light);border:1px solid rgba(247,238,219,.25);text-align:left}
[data-testid="stSidebar"] [data-testid="stButton"] button:hover{background:var(--turmeric);color:var(--moss);border-color:var(--turmeric)}
h1,h2,h3,h4{font-family:'Playfair Display',Georgia,serif!important;color:var(--moss)!important;letter-spacing:-.3px}
p,label,li{color:var(--ink)} hr{border-color:#D7C5A2!important}
[data-testid="stCaptionContainer"]{color:var(--muted)!important}
.hero{position:relative;overflow:hidden;background:var(--moss);color:var(--paper);border:2px solid var(--turmeric);border-radius:18px;padding:34px;margin:4px 0 24px;box-shadow:0 8px 0 rgba(32,63,50,.09)}
.hero:before{content:'❖  ✦  ❖';position:absolute;right:22px;top:12px;color:var(--turmeric);font-size:27px;letter-spacing:8px}
.hero:after{content:'✦';position:absolute;right:30px;bottom:-55px;color:rgba(228,181,72,.15);font-size:180px;line-height:1}
.hero h1{color:var(--paper)!important;font-size:clamp(2.1rem,5vw,3.5rem)!important;line-height:1.08;margin:8px 0 12px;position:relative;z-index:1}
.hero p{color:#F5E5C5!important;position:relative;z-index:1;max-width:760px}.kicker{color:var(--turmeric);font-size:11px;font-weight:800;letter-spacing:4px;position:relative;z-index:1}
.section-heading{border-left:5px solid var(--brick);padding-left:13px;margin:22px 0 12px}.section-heading h2{margin-bottom:3px}
.paper-card{background:var(--white);border:1px solid #D8C6A5;border-radius:14px;padding:16px;box-shadow:0 4px 0 rgba(32,63,50,.06);margin-bottom:12px}
.price-tag{display:inline-block;background:var(--turmeric);color:var(--moss);font-weight:800;font-size:18px;padding:5px 11px;border-radius:4px}
.message-box{background:#F2E5C8;border-left:4px solid var(--brick);border-radius:5px;padding:11px 13px;color:#4C4030;margin:10px 0}
.info-strip{background:var(--paper-dark);border:1px solid #D4BD93;border-radius:10px;padding:13px 16px}
.bill-box{background:var(--white);border:2px dashed #A48B60;border-radius:12px;padding:20px}
.big-total{color:var(--brick);font-family:'Playfair Display',Georgia,serif;font-weight:800;font-size:27px}
div.stButton>button,div.stFormSubmitButton>button{background:var(--brick);color:#FFF9ED;border:1px solid var(--brick);border-radius:8px;min-height:42px;font-weight:700;transition:.15s ease-in-out}
div.stButton>button:hover,div.stFormSubmitButton>button:hover{background:var(--turmeric);color:var(--moss);border-color:var(--turmeric);transform:translateY(-1px)}
.stTextInput input,.stNumberInput input,.stSelectbox [data-baseweb="select"]>div{background:var(--white);border-color:#CDB994;border-radius:8px}
div[data-testid="stExpander"]{background:rgba(255,249,237,.75);border:1px solid #D8C6A5;border-radius:10px}
div[data-testid="stAlert"]{border-radius:10px}div[data-testid="stImage"] img{border-radius:10px}
.footer{text-align:center;color:var(--muted);font-size:12px;letter-spacing:1px;padding:14px 0 4px}\n[data-testid="stForm"]{background:rgba(255,249,237,.72);border:1px solid #D8C6A5;border-radius:12px;padding:16px}
@media(max-width:700px){.hero{padding:25px 20px}.hero:before{font-size:18px;right:10px}}
</style>
""", unsafe_allow_html=True)

MENU = {
    "Trà sữa": [
        {"name":"Trà Sữa Cô Ba","price":35000,"image":"https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=900&q=85","description":"Trà đen thơm dịu, sữa béo vừa, ngọt ngào như ký ức.","message":"Cô Ba gửi bạn một chút ngọt ngào của những ngày xưa cũ!"},
        {"name":"Trà Sữa Gánh Hàng Rong","price":39000,"image":"https://images.unsplash.com/photo-1525385133512-2f3bdd039054?auto=format&fit=crop&w=900&q=85","description":"Vị trà đậm đà, sữa thơm, gợi nhớ những con phố thân quen.","message":"Mời bạn nhâm nhi một ly trà, nghe phố kể chuyện ngày xưa."},
        {"name":"Trà Sữa Phố Hội","price":42000,"image":"https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=900&q=85","description":"Trà sữa thơm mượt, lấy cảm hứng từ nét trầm mặc phố cổ.","message":"Chúc bạn có một chuyến dạo chơi thật an yên tại Phố Hội!"},
        {"name":"Trà Sữa Mợ Hai","price":40000,"image":"https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=900&q=85","description":"Vị trà thanh, sữa dịu, nhẹ nhàng và tinh tế.","message":"Mợ Hai chúc bạn hôm nay gặp toàn điều dễ thương!"},
    ],
    "Matcha": [
        {"name":"Matcha Ngọc Bích","price":42000,"image":"https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=900&q=85","description":"Matcha xanh mịn, thơm dịu, hòa cùng sữa tươi.","message":"Một chút xanh bình yên, mong ngày của bạn dịu dàng hơn."},
        {"name":"Matcha Sữa Cô Tư","price":45000,"image":"https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&w=900&q=85","description":"Matcha đậm vị, sữa béo nhẹ, hậu vị thanh.","message":"Cô Tư mời bạn một ly xanh mát, uống là thấy thương!"},
        {"name":"Matcha Đêm Trăng","price":47000,"image":"https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=900&q=85","description":"Matcha sữa mềm mượt, cảm hứng từ đêm trăng tĩnh lặng.","message":"Chúc tâm hồn bạn nhẹ như ánh trăng đêm nay."},
    ],
    "Cà phê": [
        {"name":"Matcha Ngọc Bích","price":42000,"image":"https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=900&q=85","description":"Matcha xanh mịn, thơm dịu, hòa cùng sữa tươi.","message":"Một chút xanh bình yên, mong ngày của bạn dịu dàng hơn."},
        {"name":"Matcha Sữa Cô Tư","price":45000,"image":"https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&w=900&q=85","description":"Matcha đậm vị, sữa béo nhẹ, hậu vị thanh.","message":"Cô Tư mời bạn một ly xanh mát, uống là thấy thương!"},
        {"name":"Matcha Đêm Trăng","price":47000,"image":"https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=900&q=85","description":"Matcha sữa mềm mượt, cảm hứng từ đêm trăng tĩnh lặng.","message":"Chúc tâm hồn bạn nhẹ như ánh trăng đêm nay."},
    ],        
}
TOPPINGS={"Không topping":0,"Trân châu đen":7000,"Trân châu trắng":8000,"Thạch củ năng":8000,"Pudding trứng":10000,"Kem cheese":12000}
SWEETNESS=["0%","30%","50%","70%","100%"]
ICE=["Có đá","Ít đá","Không đá"]
VOUCHERS={"HOAINIEM10":0.10,"COBA15":0.15,"TRAXUA20":0.20}
PAGES=["Trang chủ","Khám phá thực đơn","Giỏ hàng & thanh toán","Vòng quay may mắn","Về chúng tôi","Đơn hàng đã xác nhận"]

# State is preserved across Streamlit reruns.
for key, value in {"cart":[],"page":"Trang chủ","voucher":"","voucher_applied":"","spin_result":None,"used_spin":False,"order_confirmation":None,"feedbacks":[]}.items():
    if key not in st.session_state: st.session_state[key]=value

def money(value): return f"{int(value):,}".replace(",",".")+" đ"
def subtotal(): return sum(item["subtotal"] for item in st.session_state.cart)
def rate(): return VOUCHERS.get(st.session_state.voucher_applied,0)
def discount(): return int(subtotal()*rate())
def total(): return max(0,subtotal()-discount())
def navigate(page):
    st.session_state.page=page
    st.rerun()
def add_item(product, quantity, topping, sweetness, ice):
    unit=product["price"]+TOPPINGS[topping]
    st.session_state.cart.append({"name":product["name"],"base_price":product["price"],"topping":topping,"topping_price":TOPPINGS[topping],"sweetness":sweetness,"ice":ice,"quantity":int(quantity),"unit_price":unit,"subtotal":unit*int(quantity),"message":product["message"]})
def make_qr(amount):
    # QR demo only; replace with a real bank/provider QR before accepting payments.
    content=f"TRA QUAN HOAI NIEM - QR MINH HOA | So tien: {amount} VND | Thay bang QR ngan hang cua quan"
    qr=qrcode.QRCode(box_size=7,border=3); qr.add_data(content); qr.make(fit=True)
    img=qr.make_image(fill_color=MOSS,back_color=WHITE); out=BytesIO(); img.save(out,format="PNG"); out.seek(0); return out
def hero(kicker,title,subtitle):
    st.markdown(f'<div class="hero"><div class="kicker">{kicker}</div><h1>{title}</h1><p>{subtitle}</p></div>',unsafe_allow_html=True)
def section(title, subtitle=None):
    st.markdown(f'<div class="section-heading"><h2>{title}</h2></div>',unsafe_allow_html=True)
    if subtitle: st.caption(subtitle)
def show_image(url,caption): st.image(url,use_container_width=True,caption=caption)

# Sidebar uses buttons instead of a radio widget so navigation buttons never conflict with widget state.
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:14px 0 8px'><div style='font-size:42px'>🍵</div><div style='font-family:Georgia,serif;font-size:25px;font-weight:700;color:#E4B548'>TRÀ QUÁN</div><div style='font-size:11px;letter-spacing:3px'>HOÀI NIỆM</div><div style='color:#E4B548;font-size:18px;margin-top:8px'>❖ ── ✦ ── ❖</div></div>",unsafe_allow_html=True)
    st.markdown("---")
    st.caption("DANH MỤC")
    for p in PAGES:
        label=("➤  " if st.session_state.page==p else "　 ")+p
        if st.button(label,key="nav_"+p,use_container_width=True):
            st.session_state.page=p
            st.rerun()
    st.markdown("---")
    st.markdown("**🧺 Giỏ hàng của bạn**")
    st.write(f"{len(st.session_state.cart)} dòng món")
    st.markdown(f"<div style='background:#315847;border:1px solid #E4B548;padding:10px;border-radius:8px'>Tạm tính<br><span style='font-size:22px;font-weight:800;color:#E4B548'>{money(subtotal())}</span></div>",unsafe_allow_html=True)
    if st.button("Mở giỏ hàng →",key="sidebar_cart",use_container_width=True): navigate("Giỏ hàng & thanh toán")
    st.markdown("<div style='padding-top:18px;font-size:11px;line-height:1.8;color:#DCCBA9'>HƯƠNG XƯA · VỊ CŨ<br>Chậm một nhịp, thương một đời.</div>",unsafe_allow_html=True)

page=st.session_state.page

if page=="Trang chủ":
    hero("❖ CHÀO MỪNG BẠN GHÉ THĂM ❖","Trà Quán Hoài Niệm","Một chút hương xưa · Một chút vị trà · Một khoảng bình yên.")
    left,right=st.columns([1.05,1],gap="large")
    with left:
        st.markdown('<div style="color:#B74735;font-weight:800;letter-spacing:3px">✦ HƯƠNG XƯA VỊ CŨ ✦</div>',unsafe_allow_html=True)
        st.markdown("## Nơi ký ức được pha thành vị")
        st.write("Giữa nhịp sống vội vàng, hãy dừng chân để thưởng thức một ly trà mang hương vị thân quen. Lấy cảm hứng từ những con phố cũ, quán nước ven đường và câu chuyện bên tách trà, Trà Quán Hoài Niệm mong muốn mang đến một khoảng nghỉ nhỏ giữa ngày bận rộn.")
        st.markdown('<div class="message-box">“Có những điều xưa cũ, chỉ cần nhấp một ngụm là thấy lòng dịu lại.”</div>',unsafe_allow_html=True)
        if st.button("📜 Khám phá thực đơn",key="home_explore",use_container_width=True): navigate("Khám phá thực đơn")
    with right: show_image("https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=1200&q=85","Một góc trà mang phong vị hoài cổ")
    section("DẤU ẤN CỦA QUÁN","Ba điều nhỏ tạo nên trải nghiệm riêng.")
    a,b,c=st.columns(3)
    for col,emoji,title,desc in [(a,"🍃","Hương vị thân quen","Trà sữa và matcha mang tên gọi gợi nhớ những câu chuyện xưa."),(b,"🎁","Quà tặng bất ngờ","Thử vận may với voucher hoặc một món quà nhỏ từ quán."),(c,"🧾","Đặt món dễ dàng","Tùy chỉnh thức uống và xem hóa đơn ngay trên ứng dụng.")]:
        with col: st.markdown(f'<div class="paper-card"><div style="font-size:30px">{emoji}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)

elif page=="Khám phá thực đơn":
    hero("❖ MENU NHÀ TRÀ ❖","Thực đơn nhà trà","Chọn một hương vị, gửi gắm một tâm tình.")
    category=st.radio("Chọn nhóm thức uống",["Trà sữa","Matcha"],horizontal=True,key="drink_category")
    st.markdown('<div class="info-strip">✦ Giá tính bằng VNĐ. Topping được tính thêm vào giá món. Mỗi thức uống đều có lời nhắn riêng dành cho bạn.</div>',unsafe_allow_html=True)
    st.write("")
    for idx,product in enumerate(MENU[category]):
        with st.container(border=True):
            image_col,detail_col=st.columns([.85,1.3],gap="large")
            with image_col: show_image(product["image"],product["name"])
            with detail_col:
                st.markdown(f"### {product['name']}")
                st.markdown(f'<span class="price-tag">{money(product["price"])}</span>',unsafe_allow_html=True)
                st.write(product["description"])
                st.markdown(f'<div class="message-box">💌 {product["message"]}</div>',unsafe_allow_html=True)
                with st.form(key=f"form_{category}_{idx}"):
                    st.markdown("**Tùy chỉnh ly của bạn**")
                    qty=st.number_input("Số lượng",min_value=1,max_value=20,value=1,step=1,key=f"qty_{category}_{idx}")
                    topping=st.selectbox("Topping",list(TOPPINGS),key=f"top_{category}_{idx}")
                    sweet=st.select_slider("Độ ngọt",options=SWEETNESS,value="50%",key=f"sweet_{category}_{idx}")
                    ice=st.radio("Lượng đá",ICE,horizontal=True,key=f"ice_{category}_{idx}")
                    unit=product["price"]+TOPPINGS[topping]
                    st.markdown(f"**Giá mỗi ly:** {money(unit)}　·　**Thành tiền:** {money(unit*qty)}")
                    submitted=st.form_submit_button("＋ Thêm vào giỏ hàng",use_container_width=True)
                    if submitted:
                        add_item(product,qty,topping,sweet,ice)
                        st.session_state[f"notice_{category}_{idx}"]=product["message"]
                        st.session_state[f"added_{category}_{idx}"]=True
                        st.rerun()
                if st.session_state.get(f"added_{category}_{idx}",False):
                    st.success("Đã thêm món vào giỏ hàng!")
                    st.info(st.session_state.get(f"notice_{category}_{idx}",product["message"]))
    st.divider(); x,y=st.columns(2)
    with x:
        if st.button("← Về trang chủ",use_container_width=True): navigate("Trang chủ")
    with y:
        if st.button("Sang giỏ hàng →",use_container_width=True): navigate("Giỏ hàng & thanh toán")

elif page=="Giỏ hàng & thanh toán":
    hero("❖ ORDER & CHECKOUT ❖","Giỏ hàng & thanh toán","Kiểm tra món đã chọn trước khi hoàn tất đơn hàng.")
    if not st.session_state.cart:
        st.markdown('<div class="info-strip">🧺 Giỏ hàng đang trống. Mời bạn chọn thức uống yêu thích!</div>',unsafe_allow_html=True)
        if st.button("📜 Khám phá thực đơn",use_container_width=True): navigate("Khám phá thực đơn")
    else:
        section("CÁC MÓN ĐÃ CHỌN")
        for i,item in enumerate(st.session_state.cart):
            with st.container(border=True):
                a,b,c=st.columns([3,1.2,.8])
                with a:
                    st.markdown(f"**{item['name']}**")
                    st.caption(f"Topping: {item['topping']} · Độ ngọt: {item['sweetness']} · {item['ice']}")
                    st.caption(f"{money(item['base_price'])} + {money(item['topping_price'])} topping/ly")
                with b:
                    st.write(f"Số lượng: **{item['quantity']}**")
                    st.write(f"**{money(item['subtotal'])}**")
                with c:
                    if st.button("🗑️ Xóa",key=f"delete_{i}"): st.session_state.cart.pop(i); st.rerun()
        st.divider(); section("VOUCHER ƯU ĐÃI","Mã dùng thử: HOAINIEM10, COBA15, TRAXUA20.")
        vc,bc=st.columns([2,1])
        with vc: voucher_input=st.text_input("Mã voucher",value=st.session_state.voucher,placeholder="Nhập mã ưu đãi",key="voucher_input_box")
        with bc:
            st.write(""); st.write("")
            if st.button("Áp dụng mã",use_container_width=True):
                code=voucher_input.strip().upper(); st.session_state.voucher=voucher_input.strip()
                if code in VOUCHERS:
                    st.session_state.voucher_applied=code; st.success(f"Đã áp dụng {code} — giảm {int(VOUCHERS[code]*100)}%.")
                else: st.session_state.voucher_applied=""; st.error("Mã không hợp lệ. Vui lòng kiểm tra lại.")
        if st.session_state.voucher_applied:
            st.info(f"Voucher đang dùng: {st.session_state.voucher_applied} (−{int(rate()*100)}%).")
            if st.button("Bỏ voucher"): st.session_state.voucher_applied=""; st.session_state.voucher=""; st.rerun()
        st.divider(); section("HÓA ĐƠN TẠM TÍNH")
        st.markdown('<div class="bill-box">',unsafe_allow_html=True)
        st.markdown("#### TRÀ QUÁN HOÀI NIỆM"); st.caption("Thời gian: "+datetime.now().strftime("%d/%m/%Y %H:%M")); st.caption("HÓA ĐƠN ĐẶT MÓN")
        for item in st.session_state.cart:
            st.write(f"**{item['name']}** — {item['quantity']} × {money(item['unit_price'])} = **{money(item['subtotal'])}**")
            st.caption(f"{item['topping']} · Ngọt {item['sweetness']} · {item['ice']}")
        st.markdown("---"); st.write(f"Tạm tính: **{money(subtotal())}**"); st.write(f"Giảm giá: **− {money(discount())}**")
        st.markdown(f'<div class="big-total">TỔNG CỘNG: {money(total())}</div>',unsafe_allow_html=True); st.markdown("</div>",unsafe_allow_html=True)
        st.divider(); section("PHƯƠNG THỨC THANH TOÁN")
        payment=st.radio("Bạn muốn thanh toán bằng cách nào?",["Tiền mặt","Quét mã QR"],horizontal=True,key="payment_choice")
        if payment=="Tiền mặt": st.markdown('<div class="info-strip">💵 Bạn chọn thanh toán tiền mặt. Vui lòng thanh toán cho nhân viên khi nhận món.</div>',unsafe_allow_html=True)
        else:
            st.warning("QR bên dưới chỉ là mã minh họa, KHÔNG phải QR chuyển khoản ngân hàng thật.")
            q1,q2=st.columns([1,1.4])
            with q1: st.image(make_qr(total()),caption="QR minh họa — chưa thể chuyển khoản",width=230)
            with q2:
                st.markdown("#### Thông tin thanh toán"); st.write("Đơn vị: Trà Quán Hoài Niệm"); st.write("Số tiền:",money(total())); st.write("Nội dung: TRAQUANHOAINIEM")
                st.caption("Khi triển khai thật, thay bằng QR ngân hàng hoặc nhà cung cấp thanh toán của quán.")
        st.divider(); c1,c2,c3=st.columns(3)
        with c1:
            if st.button("＋ Chọn thêm món",use_container_width=True): navigate("Khám phá thực đơn")
        with c2:
            if st.button("Xóa toàn bộ",use_container_width=True): st.session_state.cart=[]; st.session_state.voucher=""; st.session_state.voucher_applied=""; st.rerun()
        with c3:
            if st.button("✓ Xác nhận đặt món",use_container_width=True):
                st.session_state.order_confirmation={"items":[i.copy() for i in st.session_state.cart],"subtotal":subtotal(),"discount":discount(),"total":total(),"payment":payment,"time":datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
                navigate("Đơn hàng đã xác nhận")

elif page=="Đơn hàng đã xác nhận":
    hero("❖ THANK YOU ❖","Cảm ơn bạn đã ghé quán!","Một ly trà, một niềm vui nho nhỏ.")
    order=st.session_state.order_confirmation
    if order:
        st.success("Đơn hàng đã được ghi nhận trên ứng dụng demo."); st.caption("Thời gian: "+order["time"]); section("HÓA ĐƠN CỦA BẠN")
        for item in order["items"]:
            st.write(f"• **{item['name']}** × {item['quantity']} — **{money(item['subtotal'])}**")
            st.caption(f"Topping: {item['topping']} · Độ ngọt: {item['sweetness']} · {item['ice']}")
        st.write(f"Tạm tính: {money(order['subtotal'])}"); st.write(f"Giảm giá: −{money(order['discount'])}")
        st.markdown(f'<div class="big-total">TỔNG THANH TOÁN: {money(order["total"])}</div>',unsafe_allow_html=True); st.write(f"Phương thức: **{order['payment']}**")
        if order["payment"]=="Quét mã QR":
            st.warning("Bản demo chưa xác minh giao dịch ngân hàng. Chỉ xác nhận thanh toán sau khi kiểm tra giao dịch thực tế.")
        else:
            st.info("Đơn hàng tiền mặt đã được ghi nhận trên giao diện demo. Vui lòng thanh toán cho nhân viên.")

        # Feedback form shown on the order confirmation page.
        st.divider()
        section("ĐÁNH GIÁ & PHẢN HỒI", "Ý kiến của bạn giúp Trà Quán Hoài Niệm phục vụ tốt hơn.")
        feedback_key = "feedback_submitted_" + order["time"].replace("/", "_").replace(":", "_").replace(" ", "_")
        if st.session_state.get(feedback_key, False):
            st.success("Cảm ơn bạn đã dành thời gian đánh giá và gửi lời nhắn cho quán! 🌿")
            saved_feedback = next(
                (f for f in st.session_state.feedbacks if f.get("order_time") == order["time"]),
                None
            )
            if saved_feedback:
                st.write(f"Đánh giá của bạn: {'⭐' * saved_feedback['rating']}")
                if saved_feedback["message"]:
                    st.caption("Lời nhắn: " + saved_feedback["message"])
        else:
            with st.form(key="feedback_form_" + order["time"].replace("/", "_").replace(":", "_").replace(" ", "_")):
                rating = st.select_slider(
                    "Bạn hài lòng với trải nghiệm tại quán ở mức nào?",
                    options=[1, 2, 3, 4, 5],
                    value=5,
                    format_func=lambda x: "⭐" * x + f"  ({x}/5)"
                )
                feedback_message = st.text_area(
                    "Lời nhắn dành cho quán (không bắt buộc)",
                    placeholder="Chia sẻ cảm nhận của bạn về đồ uống hoặc trải nghiệm đặt món...",
                    max_chars=500
                )
                feedback_submit = st.form_submit_button("Gửi đánh giá", use_container_width=True)
                if feedback_submit:
                    st.session_state.feedbacks.append({
                        "order_time": order["time"],
                        "rating": int(rating),
                        "message": feedback_message.strip(),
                        "submitted_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    })
                    st.session_state[feedback_key] = True
                    st.rerun()

        st.divider(); a,b=st.columns(2)
        with a:
            if st.button("🏠 Về trang chủ",use_container_width=True): navigate("Trang chủ")
        with b:
            if st.button("🛍️ Đặt đơn mới",use_container_width=True):
                st.session_state.cart=[]; st.session_state.voucher=""; st.session_state.voucher_applied=""; st.session_state.order_confirmation=None; navigate("Khám phá thực đơn")
    else:
        st.info("Chưa có đơn hàng nào được xác nhận.")
        if st.button("Đến giỏ hàng"): navigate("Giỏ hàng & thanh toán")

elif page=="Vòng quay may mắn":
    hero("❖ LUCKY CORNER ❖","Vòng quay may mắn","Ghé quán một chút, mang về niềm vui.")
    st.write("Mỗi lượt chơi nhận một phần quà. Hãy nhấn nút để thử vận may nhé!")
    st.markdown("<div style='background:#203F32;border:5px double #E4B548;border-radius:50%;width:245px;height:245px;margin:22px auto;display:flex;align-items:center;justify-content:center;text-align:center;box-shadow:0 8px 0 rgba(32,63,50,.12)'><div><div style='font-size:57px'>🎡</div><div style='font-family:Georgia,serif;font-size:21px;font-weight:bold;color:#F7EEDB'>VÒNG QUAY<br>HOÀI NIỆM</div><div style='color:#E4B548;font-size:12px;margin-top:8px'>❖ THỬ VẬN MAY ❖</div></div></div>",unsafe_allow_html=True)
    a,b,c=st.columns(3)
    for col,emoji,title,desc in [(a,"🎟️","Voucher","Giảm 10%, 15% hoặc 20%."),(b,"🧋","Quà nhỏ","Tặng một phần topping."),(c,"💌","Lời chúc","Một lời chúc dễ thương từ quán.")]:
        with col: st.markdown(f'<div class="paper-card"><h3>{emoji} {title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
    prizes=[{"name":"Giảm 10%","code":"HOAINIEM10","type":"voucher"},{"name":"Giảm 15%","code":"COBA15","type":"voucher"},{"name":"Giảm 20%","code":"TRAXUA20","type":"voucher"},{"name":"Tặng topping","code":None,"type":"gift"},{"name":"Một lời chúc an yên","code":None,"type":"message"}]
    if st.session_state.used_spin:
        st.info("Bạn đã sử dụng lượt quay trong phiên này."); result=st.session_state.spin_result
        if result:
            st.markdown(f"## 🎉 Bạn nhận được: {result['name']}")
            if result["code"]:
                st.code(result["code"])
                if st.button("Dùng voucher này",use_container_width=True):
                    st.session_state.voucher=result["code"]; st.session_state.voucher_applied=result["code"]; navigate("Giỏ hàng & thanh toán")
            elif result["type"]=="gift": st.success("Bạn đã nhận quà tặng topping. Nhân viên cần xác nhận và áp dụng vào đơn hàng.")
            else: st.success("Chúc bạn luôn bình yên và tìm thấy niềm vui trong những điều giản dị.")
    elif st.button("🎡 QUAY NGAY",use_container_width=True):
        st.session_state.spin_result=random.choice(prizes); st.session_state.used_spin=True; st.rerun()
    st.caption("Vòng quay là tính năng demo trong phiên ứng dụng. Khi kinh doanh thật, hãy thiết lập thể lệ và điều kiện đổi thưởng rõ ràng.")

elif page=="Về chúng tôi":
    hero("❖ OUR STORY ❖","Câu chuyện của Trà Quán","Giữ chút hương xưa giữa nhịp sống hiện đại.")
    left,right=st.columns([1,1],gap="large")
    with left: show_image("https://images.unsplash.com/photo-1498804103079-a6351b050096?auto=format&fit=crop&w=1200&q=85","Không gian thưởng trà đầy hoài niệm")
    with right:
        st.markdown("## Khởi nguồn từ những điều bình dị")
        st.write("Trà Quán Hoài Niệm được xây dựng từ mong muốn lưu giữ những hình ảnh thân thuộc của Việt Nam xưa: chiếc bàn gỗ, tách trà, con phố nhỏ và những lời hỏi thăm chân thành. Chúng tôi tin rằng một thức uống ngon không chỉ nằm ở hương vị, mà còn ở cảm xúc mà nó mang lại.")
        st.markdown('<div class="message-box">“Chậm một nhịp, để thương những điều bình dị.”</div>',unsafe_allow_html=True)
    section("ĐIỀU QUÁN LUÔN HƯỚNG ĐẾN")
    a,b,c=st.columns(3)
    for col,title,desc in [(a,"Chân thành","Trải nghiệm thân thiện và gần gũi."),(b,"Chất riêng","Thức uống hiện đại trong cảm hứng xưa."),(c,"Bình yên","Mỗi lần ghé quán là một lần sống chậm.")]:
        with col: st.markdown(f'<div class="paper-card"><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
    st.divider(); section("THÔNG TIN LIÊN HỆ")
    st.write("**Tên quán:** Trà Quán Hoài Niệm"); st.write("**Phong cách:** Trà sữa và matcha hoài cổ"); st.write("**Địa chỉ:** Bổ sung địa chỉ thật của quán tại đây"); st.write("**Fanpage:** Bổ sung đường dẫn fanpage tại đây")
    if st.button("📜 Xem thực đơn ngay",use_container_width=True): navigate("Khám phá thực đơn")

st.markdown("---")
st.markdown("<div class='footer'>❖ TRÀ QUÁN HOÀI NIỆM ❖<br>HƯƠNG XƯA · VỊ CŨ · CẢM ƠN BẠN ĐÃ GHÉ THĂM</div>",unsafe_allow_html=True)

