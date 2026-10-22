import streamlit as st
import random
import qrcode
import re
from pathlib import Path
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Trà Quán Hoài Niệm", page_icon="🍵", layout="wide", initial_sidebar_state="expanded")

# Bảng màu poster retro: đỏ rượu, hồng đất, kem trên nền tối sang trọng
MOSS = "#263F32"          # xanh rêu
MOSS_LIGHT = "#355746"
TURMERIC = "#E0B44F"      # vàng nghệ
BRICK = "#A94332"         # đỏ gạch
PAPER = "#F5EBD7"         # nền kem
PAPER_DARK = "#DCC9A7"
INK = "#263329"
MUTED = "#C7BCA5"
WHITE = "#FFF9ED"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@500;600;700;800;900&family=Oswald:wght@400;500;600;700&display=swap');
:root{--moss:#263F32;--moss2:#355746;--moss3:#172B22;--gold:#E0B44F;--brick:#A94332;--cream:#F5EBD7;--cream2:#DCC9A7;--ink:#263329;--muted:#C7BCA5;--line:rgba(224,180,79,.34);--card:#20372B}
.stApp{background:radial-gradient(ellipse at 8% 2%,rgba(224,180,79,.12),transparent 28%),radial-gradient(ellipse at 92% 85%,rgba(169,67,50,.16),transparent 30%),linear-gradient(145deg,#14251D 0%,#20372B 52%,#263F32 100%);color:var(--cream);font-family:'DM Sans',sans-serif}
[data-testid="stHeader"]{background:rgba(20,37,29,.92)} [data-testid="stAppViewContainer"]{background:transparent}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#14251D 0%,#263F32 100%);border-right:1px solid var(--gold);box-shadow:8px 0 32px rgba(0,0,0,.18)}
[data-testid="stSidebar"] *{color:var(--cream)}
[data-testid="stSidebar"] [data-testid="stButton"] button{background:rgba(224,180,79,.08);border:1px solid rgba(224,180,79,.22);text-align:left;color:var(--cream);border-radius:3px}
[data-testid="stSidebar"] [data-testid="stButton"] button:hover{background:var(--gold);color:#1B2C22;border-color:var(--gold)}
[data-testid="stSidebar"] [data-testid="stExpander"]{background:rgba(255,255,255,.035);border-color:var(--line)}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"]{color:var(--gold)!important}
h1,h2,h3,h4{font-family:'Playfair Display',Georgia,serif!important;color:var(--cream)!important;letter-spacing:.2px} h1{font-weight:800!important} h2,h3{font-weight:700!important}
p,label,li{color:var(--cream)} hr{border-color:var(--line)!important} [data-testid="stCaptionContainer"],.stCaption{color:var(--muted)!important}
.hero{position:relative;overflow:hidden;background:linear-gradient(125deg,rgba(53,87,70,.97),rgba(23,43,34,.99) 72%);color:var(--cream);border:1px solid var(--gold);border-radius:3px;padding:clamp(26px,4vw,48px);margin:4px 0 28px;box-shadow:inset 0 0 0 7px rgba(224,180,79,.055),0 18px 42px rgba(0,0,0,.22)}
.hero:before{content:'✦  ━━━━━━━━━  ✦';position:absolute;right:22px;top:17px;color:var(--gold);font-size:10px;letter-spacing:3px}.hero:after{content:'❧';position:absolute;right:18px;bottom:-72px;color:rgba(224,180,79,.10);font-family:Georgia,serif;font-size:230px;line-height:1;transform:rotate(-12deg)}
.hero h1{color:var(--cream)!important;font-size:clamp(2.4rem,5.4vw,4.7rem)!important;line-height:1.02;margin:12px 0 15px;position:relative;z-index:1;text-transform:uppercase;letter-spacing:-1.2px}.hero p{color:#E4D8BE!important;position:relative;z-index:1;max-width:760px;font-size:1.02rem;line-height:1.8}.kicker{color:var(--gold);font-family:'Oswald',sans-serif;font-size:11px;font-weight:600;letter-spacing:4px;position:relative;z-index:1;text-transform:uppercase}
.section-heading{border-left:3px solid var(--gold);padding-left:14px;margin:25px 0 13px}.section-heading h2{margin-bottom:3px;text-transform:uppercase;letter-spacing:.7px}
.paper-card{background:linear-gradient(145deg,rgba(53,87,70,.64),rgba(32,55,43,.96));border:1px solid var(--line);border-radius:3px;padding:19px;box-shadow:0 12px 28px rgba(0,0,0,.14);margin-bottom:12px;height:100%}.paper-card h3{color:var(--gold)!important}.price-tag{display:inline-block;background:var(--gold);color:#1B2C22;font-family:'Oswald',sans-serif;font-weight:700;font-size:19px;letter-spacing:.4px;padding:6px 12px;border-radius:2px}
.message-box{background:rgba(224,180,79,.10);border-left:3px solid var(--gold);border-radius:0;padding:12px 15px;color:var(--cream);margin:10px 0}.info-strip{background:rgba(224,180,79,.08);border:1px solid var(--line);border-radius:3px;padding:14px 17px;color:var(--cream)}.bill-box{background:rgba(13,25,19,.48);border:1px dashed var(--gold);border-radius:3px;padding:20px}.big-total{color:var(--gold);font-family:'Oswald','Playfair Display',serif;font-weight:700;font-size:29px;letter-spacing:.4px}
div.stButton>button,div.stFormSubmitButton>button{background:var(--brick);color:var(--cream);border:1px solid var(--gold);border-radius:2px;min-height:43px;font-family:'DM Sans',sans-serif;font-weight:700;letter-spacing:.25px;transition:all .18s ease}div.stButton>button:hover,div.stFormSubmitButton>button:hover{background:var(--gold);color:#1B2C22;border-color:var(--gold);transform:translateY(-1px);box-shadow:0 5px 16px rgba(224,180,79,.15)}
.stTextInput input,.stTextArea textarea,.stNumberInput input,.stSelectbox [data-baseweb="select"]>div,.stMultiSelect [data-baseweb="select"]>div{background:#20372B!important;color:var(--cream)!important;border-color:var(--line)!important;border-radius:2px!important}.stTextInput input::placeholder,.stTextArea textarea::placeholder{color:#C7BCA5!important}
[data-baseweb="popover"],[data-baseweb="menu"],[role="listbox"]{background:#20372B!important;color:var(--cream)!important}[data-baseweb="radio"] label,[data-baseweb="checkbox"] label{color:var(--cream)!important}
[data-testid="stExpander"]{background:rgba(32,55,43,.68);border:1px solid var(--line);border-radius:3px}[data-testid="stExpander"] summary{color:var(--cream)}[data-testid="stAlert"]{border-radius:3px;border:1px solid var(--line)}[data-testid="stImage"] img{border-radius:2px;border:1px solid rgba(224,180,79,.25)}[data-testid="stForm"]{background:rgba(32,55,43,.55);border:1px solid var(--line);border-radius:3px;padding:17px}[data-testid="stMetric"]{background:rgba(53,87,70,.32);border:1px solid var(--line);padding:12px;border-radius:3px}[data-testid="stMetricValue"]{color:var(--gold)}.stRadio [role="radiogroup"]{gap:10px}[data-testid="stMarkdownContainer"] a{color:var(--gold)}
.footer{text-align:center;color:var(--gold);font-family:'Oswald',sans-serif;font-size:11px;letter-spacing:2.2px;padding:18px 0 6px;line-height:2}
@media(max-width:700px){.hero{padding:27px 20px}.hero:before{font-size:8px;right:10px}.hero h1{font-size:2.4rem!important}.paper-card{padding:14px}}
</style>
""", unsafe_allow_html=True)

MENU = {
    "Trà sữa": [
        {"name":"Trà Sữa Cô Ba","price":35000,"image":"TRASUACOBA.jpg","description":"Trà đen thơm dịu, sữa béo vừa, ngọt ngào như ký ức.","message":"Cô Ba gửi bạn một chút ngọt ngào của những ngày xưa cũ!"},
        {"name":"Trà Sữa Gánh Hàng Rong","price":39000,"image":"TRASUAGANHHANGRONG.jpg","description":"Vị trà đậm đà, sữa thơm, gợi nhớ những con phố thân quen.","message":"Mời bạn nhâm nhi một ly trà, nghe phố kể chuyện ngày xưa."},
        {"name":"Trà Sữa Phố Hội","price":42000,"image":"TRASUAPHOHOI.jpg","description":"Trà sữa thơm mượt, lấy cảm hứng từ nét trầm mặc phố cổ.","message":"Chúc bạn có một chuyến dạo chơi thật an yên tại Phố Hội!"},
        {"name":"Trà Sữa Mợ Hai","price":40000,"image":"TRASUAMOHAI.jpg","description":"Vị trà thanh, sữa dịu, nhẹ nhàng và tinh tế.","message":"Mợ Hai chúc bạn hôm nay gặp toàn điều dễ thương!"},
    ],
    "Matcha": [
        {"name":"Matcha Ngọc Bích","price":42000,"image":"MATCHANGOCBICH.jpg","description":"Matcha xanh mịn, thơm dịu, hòa cùng sữa tươi.","message":"Một chút xanh bình yên, mong ngày của bạn dịu dàng hơn."},
        {"name":"Matcha Sữa Cô Tư","price":45000,"image":"MATCHASUACOTU.jpg","description":"Matcha đậm vị, sữa béo nhẹ, hậu vị thanh.","message":"Cô Tư mời bạn một ly xanh mát, uống là thấy thương!"},
        {"name":"Matcha Đêm Trăng","price":47000,"image":"MATCHADEMTRANG.jpg","description":"Matcha sữa mềm mượt, cảm hứng từ đêm trăng tĩnh lặng.","message":"Chúc tâm hồn bạn nhẹ như ánh trăng đêm nay."},
    ],
    "Cà phê": [
        {"name":"Cà Phê Phin Sài Gòn Xưa","price":29000,"image":"https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=900&q=85","description":"Cà phê đậm vị, sữa đặc ngọt dịu, đúng chất quán xưa.","message":"Chúc bạn có một buổi chiều chậm rãi bên ly cà phê thân quen!"},
        {"name":"Bạc Xỉu Góc Phố","price":35000,"image":"https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=85","description":"Sữa thơm béo quyện chút cà phê, nhẹ nhàng và dễ uống.","message":"Một chút ngọt ngào, một chút tỉnh táo cho ngày thêm vui."},
        {"name":"Cà Phê Đêm Sài Thành","price":28000,"image":"https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=900&q=85","description":"Cà phê đen thơm sâu, hậu vị đậm dành cho người yêu vị nguyên bản.","message":"Mong bạn tìm thấy khoảng bình yên trong từng ngụm cà phê."},
    ],
}
TOPPINGS={"Không topping":0,"Trân châu đen":7000,"Trân châu trắng":8000,"Thạch củ năng":8000,"Pudding trứng":10000,"Kem cheese":12000}
SWEETNESS=["0%","30%","50%","70%","100%"]
ICE=["Có đá","Ít đá","Không đá"]
VOUCHERS={"HOAINIEM10":0.10,"COBA15":0.15,"TRAXUA20":0.20}
PAGES=["Trang chủ","Một góc tham quan","Khám phá thực đơn","Giỏ hàng & thanh toán","Vòng quay may mắn","Về chúng tôi","Đơn hàng đã xác nhận"]

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
def add_item(product, quantity, topping, sweetness, ice, customer_note=""):
    unit=product["price"]+TOPPINGS[topping]
    st.session_state.cart.append({"name":product["name"],"base_price":product["price"],"topping":topping,"topping_price":TOPPINGS[topping],"sweetness":sweetness,"ice":ice,"quantity":int(quantity),"unit_price":unit,"subtotal":unit*int(quantity),"message":product["message"],"customer_note":customer_note.strip()})
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
def image_slug(name):
    import unicodedata
    text = unicodedata.normalize("NFD", name)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = text.replace("đ", "d").replace("Đ", "D")
    return re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()

IMAGE_DIR = Path(__file__).resolve().parent / "images"
IMAGE_DIR.mkdir(exist_ok=True)

def show_image(url,caption):
    slug = image_slug(caption)
    local_images = [p for p in IMAGE_DIR.glob(f"{slug}.*") if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}]
    image_source = str(local_images[0]) if local_images else url
    st.image(image_source,use_container_width=True,caption=caption)

# Sidebar uses buttons instead of a radio widget so navigation buttons never conflict with widget state.
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:14px 0 8px'><div style='font-size:42px'>🍵</div><div style='font-family:Georgia,serif;font-size:25px;font-weight:700;color:#E0B44F'>TRÀ QUÁN</div><div style='font-size:11px;letter-spacing:3px'>HOÀI NIỆM</div><div style='color:#E0B44F;font-size:18px;margin-top:8px'>❖ ── ✦ ── ❖</div></div>",unsafe_allow_html=True)
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
    st.markdown(f"<div style='background:#355746;border:1px solid #E0B44F;padding:10px;border-radius:8px'>Tạm tính<br><span style='font-size:22px;font-weight:800;color:#E0B44F'>{money(subtotal())}</span></div>",unsafe_allow_html=True)
    if st.button("Mở giỏ hàng →",key="sidebar_cart",use_container_width=True): navigate("Giỏ hàng & thanh toán")
    with st.expander("🖼️ Thay ảnh món uống"):
        st.caption("Chọn món rồi tải ảnh từ máy tính. Ảnh sẽ được lưu trong thư mục images cạnh file app này.")
        all_products = [product for group in MENU.values() for product in group]
        chosen_name = st.selectbox("Chọn món cần đổi ảnh", [p["name"] for p in all_products], key="upload_image_product")
        uploaded_image = st.file_uploader("Tải ảnh mới lên", type=["jpg", "jpeg", "png", "webp"], key="upload_drink_image")
        if uploaded_image is not None and st.button("Lưu ảnh cho món này", key="save_drink_image", use_container_width=True):
            suffix = Path(uploaded_image.name).suffix.lower()
            slug = image_slug(chosen_name)
            for old_image in IMAGE_DIR.glob(f"{slug}.*"):
                if old_image.is_file(): old_image.unlink()
            destination = IMAGE_DIR / f"{slug}{suffix}"
            destination.write_bytes(uploaded_image.getvalue())
            st.success(f"Đã lưu ảnh cho {chosen_name}!")
            st.rerun()
    st.markdown("<div style='padding-top:18px;font-size:11px;line-height:1.8;color:#C7BCA5'>HƯƠNG XƯA · VỊ CŨ<br>Chậm một nhịp, thương một đời.</div>",unsafe_allow_html=True)

page=st.session_state.page

if page=="Trang chủ":
    hero("❖ CHÀO MỪNG BẠN GHÉ THĂM ❖","Trà Quán Hoài Niệm","Một chút hương xưa · Một chút vị trà · Một khoảng bình yên.")
    left,right=st.columns([1.05,1],gap="large")
    with left:
        st.markdown('<div style="color:#E0B44F;font-weight:800;letter-spacing:3px">✦ HƯƠNG XƯA VỊ CŨ ✦</div>',unsafe_allow_html=True)
        st.markdown("## Nơi ký ức được pha thành vị")
        st.write("Giữa nhịp sống hiện đại, hãy dừng chân bên một ly trà và nhớ về Sài Gòn xưa: những góc phố rợp bóng cây, mái hiên cũ, xe máy lướt qua con đường quen và quán nước nơi người ta ngồi kể chuyện đời. Trà Quán Hoài Niệm gửi chút ký ức ấy vào từng thức uống.")
        st.markdown('<div class="message-box">“Có những điều xưa cũ, chỉ cần nhấp một ngụm là thấy lòng dịu lại.”</div>',unsafe_allow_html=True)
        if st.button("📜 Khám phá thực đơn",key="home_explore",use_container_width=True): navigate("Khám phá thực đơn")
        if st.button("📷 Dạo một vòng Sài Gòn xưa",key="home_sightseeing",use_container_width=True): navigate("Một góc tham quan")
    with right: show_image("https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=1200&q=85","Góc phố Sài Gòn xưa — hình minh họa không gian đô thị hoài niệm")
    section("DẤU ẤN CỦA QUÁN","Ba điều nhỏ tạo nên trải nghiệm riêng.")
    a,b,c=st.columns(3)
    for col,emoji,title,desc in [(a,"🍃","Hương vị thân quen","Trà sữa, matcha và cà phê mang tên gọi gợi nhớ những câu chuyện xưa."),(b,"🎁","Quà tặng bất ngờ","Thử vận may với voucher hoặc một món quà nhỏ từ quán."),(c,"🧾","Đặt món dễ dàng","Tùy chỉnh thức uống và xem hóa đơn ngay trên ứng dụng.")]:
        with col: st.markdown(f'<div class="paper-card"><div style="font-size:30px">{emoji}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)

elif page=="Một góc tham quan":
    hero("❖ SAIGON MEMORY LANE ❖","Một góc Sài Gòn xưa","Dạo qua những mái hiên cũ, con phố thân quen và nhịp sống chậm của Sài Gòn trong ký ức.")
    st.markdown('<div class="info-strip">✦ Góc tham quan là không gian hình ảnh gợi nhớ Sài Gòn xưa. Bạn có thể thay các hình minh họa bằng ảnh tư liệu hoặc ảnh quán tự chụp trong thư mục <b>images</b>.</div>',unsafe_allow_html=True)
    st.write("")
    c1,c2=st.columns(2,gap="large")
    with c1:
        show_image("https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=1200&q=85","Góc phố đô thị — gợi nhắc nhịp sống Sài Gòn")
        st.markdown("### 01 · Những con đường thân quen")
        st.write("Một góc phố để nhớ về hàng cây, mái hiên và những buổi chiều chậm rãi. Hình ảnh mang tính minh họa; bạn có thể thay bằng ảnh đường phố Sài Gòn xưa phù hợp hơn.")
    with c2:
        show_image("https://images.unsplash.com/photo-1449824913935-59a10b8d2000?auto=format&fit=crop&w=1200&q=85","Nhịp sống thành phố và những dãy nhà cũ")
        st.markdown("### 02 · Dấu xưa trong phố")
        st.write("Từ bảng hiệu, cửa gỗ đến những quán nhỏ ven đường, các chi tiết bình dị làm nên nét duyên riêng của Sài Gòn qua nhiều thế hệ.")
    st.divider()
    left,right=st.columns([1,1],gap="large")
    with left:
        show_image("https://images.unsplash.com/photo-1498804103079-a6351b050096?auto=format&fit=crop&w=1200&q=85","Không gian quán cà phê hoài niệm")
    with right:
        st.markdown("### 03 · Ngồi lại bên ly nước")
        st.write("Một chiếc bàn nhỏ, một ly cà phê sữa đá và vài câu chuyện không vội. Đây là cảm hứng cho không gian Trà Quán Hoài Niệm — nơi hương vị hôm nay gặp ký ức ngày xưa.")
        st.markdown('<div class="message-box">“Sài Gòn đổi thay từng ngày, nhưng những ký ức đẹp vẫn luôn có một chỗ để trở về.”</div>',unsafe_allow_html=True)
    a,b=st.columns(2)
    with a:
        if st.button("← Về trang chủ",key="sight_home",use_container_width=True): navigate("Trang chủ")
    with b:
        if st.button("Khám phá thức uống →",key="sight_menu",use_container_width=True): navigate("Khám phá thực đơn")

elif page=="Khám phá thực đơn":
    hero("❖ MENU NHÀ TRÀ ❖","Thực đơn nhà trà","Chọn một hương vị, gửi gắm một tâm tình.")
    category=st.radio("Chọn nhóm thức uống",["Trà sữa","Matcha","Cà phê"],horizontal=True,key="drink_category")
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
                    customer_note=st.text_input("Lời nhắn riêng cho ly này (không bắt buộc)",placeholder="Ví dụ: ít ngọt hơn, ghi tên lên ly...",max_chars=120,key=f"note_{category}_{idx}")
                    unit=product["price"]+TOPPINGS[topping]
                    st.markdown(f"**Giá mỗi ly:** {money(unit)}　·　**Thành tiền:** {money(unit*qty)}")
                    submitted=st.form_submit_button("＋ Thêm vào giỏ hàng",use_container_width=True)
                    if submitted:
                        add_item(product,qty,topping,sweet,ice,customer_note)
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
                    if item.get("customer_note"):
                        st.caption("Lời nhắn riêng: " + item["customer_note"])
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
            if item.get("customer_note"):
                st.caption("Lời nhắn riêng: " + item["customer_note"])
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
    st.markdown("<div style='background:#172B22;border:5px double #E0B44F;border-radius:50%;width:245px;height:245px;margin:22px auto;display:flex;align-items:center;justify-content:center;text-align:center;box-shadow:0 8px 0 rgba(32,63,50,.12)'><div><div style='font-size:57px'>🎡</div><div style='font-family:Georgia,serif;font-size:21px;font-weight:bold;color:#F5EBD7'>VÒNG QUAY<br>HOÀI NIỆM</div><div style='color:#E0B44F;font-size:12px;margin-top:8px'>❖ THỬ VẬN MAY ❖</div></div></div>",unsafe_allow_html=True)
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
    hero("❖ OUR STORY ❖","Câu chuyện của Trà Quán","Giữ chút hương Sài Gòn xưa giữa nhịp sống hiện đại.")
    left,right=st.columns([1,1],gap="large")
    with left: show_image("https://images.unsplash.com/photo-1498804103079-a6351b050096?auto=format&fit=crop&w=1200&q=85","Góc quán mang cảm hứng Sài Gòn xưa")
    with right:
        st.markdown("## Khởi nguồn từ những điều bình dị")
        st.write("Trà Quán Hoài Niệm được xây dựng từ mong muốn lưu giữ những hình ảnh thân thuộc của Việt Nam xưa: chiếc bàn gỗ, tách trà, con phố nhỏ và những lời hỏi thăm chân thành. Chúng tôi tin rằng một thức uống ngon không chỉ nằm ở hương vị, mà còn ở cảm xúc mà nó mang lại.")
        st.markdown('<div class="message-box">“Chậm một nhịp, để thương những điều bình dị.”</div>',unsafe_allow_html=True)
    section("ĐIỀU QUÁN LUÔN HƯỚNG ĐẾN")
    a,b,c=st.columns(3)
    for col,title,desc in [(a,"Chân thành","Trải nghiệm thân thiện và gần gũi."),(b,"Chất riêng","Thức uống hiện đại trong cảm hứng xưa."),(c,"Bình yên","Mỗi lần ghé quán là một lần sống chậm.")]:
        with col: st.markdown(f'<div class="paper-card"><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
    st.divider(); section("THÔNG TIN LIÊN HỆ")
    st.write("**Tên quán:** Trà Quán Hoài Niệm"); st.write("**Phong cách:** Trà sữa, matcha và cà phê hoài cổ"); st.write("**Địa chỉ:** Bổ sung địa chỉ thật của quán tại đây"); st.write("**Fanpage:** Bổ sung đường dẫn fanpage tại đây")
    if st.button("📜 Xem thực đơn ngay",use_container_width=True): navigate("Khám phá thực đơn")

st.markdown("---")
st.markdown("<div class='footer'>❖ TRÀ QUÁN HOÀI NIỆM ❖<br>HƯƠNG XƯA · VỊ CŨ · CẢM ƠN BẠN ĐÃ GHÉ THĂM</div>",unsafe_allow_html=True)

