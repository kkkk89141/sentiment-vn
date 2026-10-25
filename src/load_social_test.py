import pandas as pd
from sklearn.metrics import cohen_kappa_score


def load_and_verify_social_holdout(csv_path="data/social_test_pilot.csv"):
    df = pd.read_csv(csv_path)
    
    # 1. Thống kê theo annotation_status
    print("=== THỐNG KÊ TRẠNG THÁI GÁN NHÃN ===")
    print(df["annotation_status"].value_counts())
    
    # 2. Tính Cohen's Kappa trên các mẫu đã gán nhãn của 2 annotators (labeled + ambiguous)
    valid_annot = df[df["annotation_status"].isin(["labeled", "ambiguous"])].dropna(
        subset=["annotator_1", "annotator_2"]
    )
    kappa = cohen_kappa_score(
        valid_annot["annotator_1"].astype(int), 
        valid_annot["annotator_2"].astype(int)
    )
    print(f"\n>> Hệ số đồng thuận Cohen's Kappa (trên {len(valid_annot)} mẫu): {kappa:.4f}")
    
    # 3. Lọc tập dữ liệu sạch để chạy đánh giá mô hình (chỉ lấy status == 'labeled')
    df_eval = df[df["annotation_status"] == "labeled"].copy()
    df_eval["adjudicated_label"] = df_eval["adjudicated_label"].astype(int)
    
    print("\n=== PHÂN BỐ NHÃN TẬP LABELED (280 MẪU) ===")
    print(df_eval["adjudicated_label"].value_counts().sort_index())
    
    # 4. Thống kê các nhóm cờ (Flags) để phục vụ Error Analysis
    all_flags = df_eval["flags"].dropna().str.split("|").explode()
    print("\n=== THỐNG KÊ CÁC NHÓM HIỆN TƯỢNG NGÔN NGỮ (FLAGS) ===")
    print(all_flags.value_counts())
    
    return df_eval, df[df["annotation_status"] == "ambiguous"]

if __name__ == "__main__":
    df_labeled, df_ambiguous = load_and_verify_social_holdout()