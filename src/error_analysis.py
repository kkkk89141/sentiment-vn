import pandas as pd

from src.evaluate import (
    analyze_errors_by_flags,
    compute_metrics,
    export_markdown_report_tables,
    plot_and_save_confusion_matrix,
)

# 1. Đọc tập test social media (chỉ lấy các mẫu 'labeled')
df_all = pd.read_csv("data/social_test_pilot.csv")
df_test = df_all[df_all["annotation_status"] == "labeled"].copy().reset_index(drop=True)

# 2. Giả sử bạn đã chạy model.predict() trên df_test["text_raw"] và thu được y_pred
# (Ở đây minh họa bằng dữ liệu giả lập để bạn test thử hàm ngay lập tức)
y_true = df_test["adjudicated_label"].astype(int).to_numpy()
y_pred = y_true.copy()
# Giả lập mô hình đoán sai các câu sarcasm (nhầm thành positive=2) và mixed
sarcasm_mask = df_test["flags"].fillna("").str.contains("sarcasm")
y_pred[sarcasm_mask] = 2

# 3. Tính metrics tổng thể và vẽ Confusion Matrix
metrics = compute_metrics(y_true, y_pred)
print(f"Macro-F1: {metrics['macro_f1']:.4f} | Accuracy: {metrics['accuracy']:.4f}")
plot_and_save_confusion_matrix(y_true, y_pred, model_name="LinearSVC Baseline")

# 4. Chạy phân tích lỗi và in ra bảng Markdown để dán vào Project report Nxx.ipynb
results = analyze_errors_by_flags(df_test, y_pred, model_name="LinearSVC Baseline")
markdown_output = export_markdown_report_tables(results, model_name="LinearSVC Baseline")
print("\n" + markdown_output)