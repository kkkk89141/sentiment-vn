import pandas as pd
import streamlit as st

# Cấu hình trang cơ bản
st.set_page_config(page_title="Phân loại cảm xúc Tiếng Việt", layout="centered")

# Tiêu đề ứng dụng
st.title("📊 Ứng dụng Phân loại Cảm xúc Bình luận")
st.markdown("Dự án Trí tuệ Nhân tạo - Nhóm 15")

# Sidebar để cấu hình (Chuẩn bị cho W07-W08)
st.sidebar.header("Cài đặt Mô hình")
model_choice = st.sidebar.selectbox(
    "Chọn mô hình phân loại:",
    ["Baseline (TF-IDF + Naive Bayes)", "PhoBERT (Đang phát triển)"]
)

# Chia giao diện thành 2 tab theo chuẩn đầu ra
tab_single, tab_batch = st.tabs(["📝 Dự đoán câu đơn", "📂 Dự đoán hàng loạt (CSV)"])

# --- TAB 1: DỰ ĐOÁN MỘT CÂU ---
with tab_single:
    st.subheader("Nhập bình luận cần phân tích")
    user_input = st.text_area("Nội dung bình luận:", height=100, placeholder="Ví dụ: Sản phẩm này rất tốt, tôi rất thích!")
    
    if st.button("Phân tích cảm xúc", type="primary"):
        if user_input.strip() == "":
            st.warning("Vui lòng nhập nội dung trước khi phân tích.")
        else:
            # Code giữ chỗ (mockup) cho W06, W07 sẽ thay bằng model.predict()
            st.success("Dự đoán mô phỏng: Tích cực (Positive) - 2")
            st.info("Chức năng này sẽ được tích hợp model thật vào tuần W08.")

# --- TAB 2: DỰ ĐOÁN TỪ FILE CSV ---
with tab_batch:
    st.subheader("Tải lên file CSV chứa dữ liệu")
    st.markdown("File CSV cần có cột tên là `text_raw`.")
    
    uploaded_file = st.file_uploader("Chọn file CSV:", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Bản xem trước 5 dòng đầu tiên:")
            st.dataframe(df.head())
            
            if st.button("Chạy phân tích toàn bộ file"):
                st.info("Chức năng chạy hàng loạt sẽ được hoàn thiện trong các tuần tới.")
        except Exception as e:
            st.error(f"Lỗi khi đọc file: {e}")