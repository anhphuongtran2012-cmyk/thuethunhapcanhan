import streamlit as st

# Cấu hình trang hiển thị trên trình duyệt
st.set_page_config(page_title="Tính Thuế TNCN", page_icon="💸", layout="centered")

# Tiêu đề ứng dụng
st.title("💸 Ứng dụng tính Thuế thu nhập cá nhân (TNCN)")
st.write("Công cụ tính thuế thu nhập từ tiền lương, tiền công theo biểu thuế lũy tiến từng phần.")

# --- NHẬP DỮ LIỆU ---
st.subheader("1. Nhập thông tin thu nhập")

thu_nhap_thong_tin = st.number_input(
    "Tổng thu nhập chịu thuế trong tháng (triệu đồng):",
    min_value=0.0,
    value=30.0,
    step=1.0,
    help="Tổng tiền lương, tiền công và các khoản giảm trừ không chịu thuế (nếu có)"
)

so_nguoi_phu_thuoc = st.number_input(
    "Số người phụ thuộc:",
    min_value=0,
    value=0,
    step=1
)

bao_hiem = st.number_input(
    "Tổng tiền đóng bảo hiểm bắt buộc (triệu đồng):",
    min_value=0.0,
    value=2.5,
    step=0.1,
    help="BHXH (8%), BHYT (1.5%), BHTN (1%) tính trên lương đóng bảo hiểm"
)

# --- XỬ LÝ LOGIC TÍNH THUẾ ---
# Các mốc giảm trừ cố định (Theo Nghị quyết 954/2020/UBTVQH14)
GIAM_TRU_BAN_THAN = 11.0  # 11 triệu đồng/tháng
GIAM_TRU_PHU_THUOC = 4.4   # 4.4 triệu đồng/tháng/người

# Tính thu nhập tính thuế
tong_giam_tru = GIAM_TRU_BAN_THAN + (so_nguoi_phu_thuoc * GIAM_TRU_PHU_THUOC) + bao_hiem
thu_nhap_tinh_thue = max(0.0, thu_nhap_thong_tin - tong_giam_tru)

def tinh_thue_luy_tien(tntt):
    """Hàm tính thuế TNCN theo biểu thuế lũy tiến từng phần"""
    thue = 0.0
    # Bậc 1: Đến 5 trđ -> 5%
    if tntt > 0:
        thue += min(tntt, 5) * 0.05
    # Bậc 2: Trên 5 trđ đến 10 trđ -> 10%
    if tntt > 5:
        thue += min(tntt - 5, 5) * 0.10
    # Bậc 3: Trên 10 trđ đến 18 trđ -> 15%
    if tntt > 10:
        thue += min(tntt - 10, 8) * 0.15
    # Bậc 4: Trên 18 trđ đến 32 trđ -> 20%
    if tntt > 18:
        thue += min(tntt - 18, 14) * 0.20
    # Bậc 5: Trên 32 trđ đến 52 trđ -> 25%
    if tntt > 32:
        thue += min(tntt - 32, 20) * 0.25
    # Bậc 6: Trên 52 trđ đến 80 trđ -> 30%
    if tntt > 52:
        thue += min(tntt - 52, 28) * 0.30
    # Bậc 7: Trên 80 trđ -> 35%
    if tntt > 80:
        thue += (tntt - 80) * 0.35
    return thue

# --- NÚT TÍNH TOÁN & HIỂN THỊ KẾT QUẢ ---
if st.button("Tính thuế", type="primary"):
    thue_phai_nop = tinh_thue_luy_tien(thu_nhap_tinh_thue)
    luong_thuc_nhan = thu_nhap_thong_tin - bao_hiem - thue_phai_nop

    st.success("📊 Kết quả tính toán chi tiết")
    
    # Tạo bảng hiển thị tóm tắt cho chuyên nghiệp
    st.markdown(f"""
    * **Giảm trừ gia cảnh bản thân:** `{GIAM_TRU_BAN_THAN} triệu đồng`
    * **Giảm trừ người phụ thuộc:** `{so_nguoi_phu_thuoc * GIAM_TRU_PHU_THUOC:.2f} triệu đồng`
    * **Tổng các khoản giảm trừ:** **{tong_giam_tru:.2f} triệu đồng**
    * ---------------------------------------------------------
    * 🎯 **Thu nhập tính thuế (TNTT):** <span style='color:orange'>**{thu_nhap_tinh_thue:.2f} triệu đồng**</span>
    * 💸 **Thuế TNCN phải nộp:** <span style='color:red'>**{thue_phai_nop:.2f} triệu đồng**</span>
    * 💰 **Thu nhập thực nhận (Net):** <span style='color:green'>**{luong_thuc_nhan:.2f} triệu đồng**</span>
    """, unsafe_allow_html=True)
