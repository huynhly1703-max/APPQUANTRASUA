            (item["unit_price"] + item["topping_price"]) * item["quantity"]
            for item in items
        )
        now = datetime.now()
        order_code = f"HQN-{now.strftime('%y%m%d')}-{st.session_state.order_number:03d}"
        customer_line = f"<p>Khách hàng: {escape(customer)}</p>" if customer.strip() else ""
        bill_html = f"""
        <div class="bill">
          <div class="bill-head">
            <div style="font-size:1.8rem">🍵</div>
            <h2>TRÀ QUÁN HOÀI NIỆM</h2>
            <div style="font-size:.82rem;letter-spacing:.1em">HÓA ĐƠN THANH TOÁN</div>
            <p style="font-size:.82rem;margin:.5rem 0 0">Mã đơn: {order_code}</p>
            <p style="font-size:.82rem;margin:.2rem 0">{now.strftime('%d/%m/%Y %H:%M')}</p>
            {customer_line}
          </div>
        """
        for item in items:
            unit_total = item["unit_price"] + item["topping_price"]
            line_total = unit_total * item["quantity"]
            topping_text = item["topping"] if item["topping_price"] else "Không topping"
            bill_html += f"""
            <div class="bill-row">
              <div style="flex:1">
                <strong>{escape(item['drink'])}</strong>
                <div class="bill-sub">{item['quantity']} ly × {unit_total:,.0f} đ</div>
                <div class="bill-sub">Topping: {escape(topping_text)} · Độ ngọt: {escape(item['sweetness'])}</div>
                <div class="bill-sub">{escape(item['ice'])}</div>
              </div>
              <strong style="white-space:nowrap">{line_total:,.0f} đ</strong>
            </div>
            """
        bill_html += f"""
          <div class="bill-row"><span>Tạm tính</span><strong>{subtotal:,.0f} đ</strong></div>
          <div class="bill-total"><span>TỔNG CỘNG</span><span>{subtotal:,.0f} đ</span></div>
          <div style="text-align:center;margin-top:1.2rem;font-size:.9rem">
            <strong>Thanh toán: {escape(payment)}</strong>
            <p style="color:#826e5b;margin:.5rem 0 0">Cảm ơn quý khách đã ghé thăm!</p>
            <p style="font-family:'Playfair Display',serif;color:#8f3028;font-style:italic;margin:.2rem 0">Hẹn gặp lại trong một ngày bình yên.</p>
          </div>
        </div>
        """
        st.markdown(bill_html, unsafe_allow_html=True)

        if payment == "Quét mã QR":
            st.markdown("#### 📱 Thanh toán bằng QR")
            st.info(
                "Đây là khu vực hướng dẫn thanh toán QR. Để nhận tiền thật, hãy cấu hình "
                "mã VietQR của quán ở phần bên dưới hoặc thay bằng ảnh QR ngân hàng của quán."
            )
            with st.expander("Cấu hình thông tin QR"):
                st.caption("Điền thông tin tài khoản để tạo đường dẫn VietQR theo chuẩn VietQR.")
                bank_id = st.text_input("Mã ngân hàng (ví dụ: MB, VCB, ACB)", key="bank_id")
                account_no = st.text_input("Số tài khoản", key="account_no")
                account_name = st.text_input("Tên chủ tài khoản", key="account_name")
                if bank_id.strip() and account_no.strip():
                    from urllib.parse import quote
                    qr_url = (
                        f"https://img.vietqr.io/image/{quote(bank_id.strip())}-"
                        f"{quote(account_no.strip())}-compact2.png"
                        f"?amount={subtotal}&addInfo={quote('Thanh toan ' + order_code)}"
                        f"&accountName={quote(account_name.strip())}"
                    )
                    st.image(qr_url, caption="Quét mã để thanh toán đúng số tiền trên hóa đơn.", width=280)
                    st.caption("Vui lòng kiểm tra tên người nhận và số tiền trước khi chuyển khoản.")

        st.markdown("")
        col_a, col_b = st.columns(2)
        with col_a:
            st.download_button(
                "⬇️ Tải bill dạng TXT",
                data=(
                    f"TRÀ QUÁN HOÀI NIỆM\\nMã đơn: {order_code}\\n"
                    f"Thời gian: {now.strftime('%d/%m/%Y %H:%M')}\\n"
                    f"Khách: {customer or 'Khách lẻ'}\\n\\n"
                    + "\\n".join(
                        f"{i['drink']} x{i['quantity']} | "
                        f"Topping: {i['topping']} | Độ ngọt: {i['sweetness']} | {i['ice']} | "
                        f"{(i['unit_price'] + i['topping_price']) * i['quantity']:,.0f} đ"
                        for i in items
                    )
                    + f"\\n\\nTỔNG CỘNG: {subtotal:,.0f} đ\\nThanh toán: {payment}\\n"
                ),
                file_name=f"{order_code}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col_b:
            if st.button("🧹 Tạo đơn mới", use_container_width=True):
                st.session_state.order_items = []
                st.session_state.order_number += 1
                st.session_state.customer_name = ""
                for idx in range(len(DRINKS)):
                    for key in (f"qty_{idx}",):
                        if key in st.session_state:
                            st.session_state[key] = 0
                st.rerun()

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#826e5b;font-size:.82rem'>"
    "TRÀ QUÁN HOÀI NIỆM · Lưu giữ hương vị xưa trong từng ly trà"
    "</div>",
    unsafe_allow_html=True,
)
