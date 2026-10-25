# src/evaluate.py
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)

LABEL_MAP: dict[int, str] = {0: "negative", 1: "neutral", 2: "positive"}
LABEL_NAMES: list[str] = ["negative", "neutral", "positive"]


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, Any]:
    """Tính toán toàn diện các chỉ số đánh giá chính (ưu tiên Macro-F1)."""
    macro_f1 = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    weighted_f1 = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))
    acc = float(accuracy_score(y_true, y_pred))

    report: dict[str, Any] = classification_report(
        y_true,
        y_pred,
        labels=[0, 1, 2],
        target_names=LABEL_NAMES,
        digits=4,
        output_dict=True,
        zero_division=0,
    )

    return {
        "accuracy": acc,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "f1_negative": float(report["negative"]["f1-score"]),
        "f1_neutral": float(report["neutral"]["f1-score"]),
        "f1_positive": float(report["positive"]["f1-score"]),
        "detailed_report": report,
    }


def plot_and_save_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    model_name: str = "Model",
    save_path: str = "reports/figures/confusion_matrix.png",
) -> None:
    """Vẽ và lưu Confusion Matrix dạng số lượng và phần trăm."""
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])
    row_sums = cm.sum(axis=1)[:, np.newaxis]
    cm_percent = np.divide(
        cm.astype("float"), row_sums, out=np.zeros_like(cm, dtype=float), where=row_sums != 0
    ) * 100

    annot = np.empty_like(cm).astype(str)
    nrows, ncols = cm.shape
    for i in range(nrows):
        for j in range(ncols):
            annot[i, j] = f"{cm[i, j]}\n({cm_percent[i, j]:.1f}%)"

    plt.figure(figsize=(6.5, 5.5))
    sns.heatmap(
        cm,
        annot=annot,
        fmt="",
        cmap="Blues",
        xticklabels=LABEL_NAMES,
        yticklabels=LABEL_NAMES,
        cbar=False,
    )
    plt.xlabel("Nhãn dự đoán (Predicted)", fontweight="bold")
    plt.ylabel("Nhãn thực tế (Ground Truth)", fontweight="bold")
    plt.title(f"Confusion Matrix — {model_name}", fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


def analyze_errors_by_flags(
    df_eval: pd.DataFrame,
    y_pred: np.ndarray,
    y_prob: np.ndarray | None = None,
    model_name: str = "Baseline",
    output_dir: str = "reports",
) -> dict[str, pd.DataFrame]:
    """
    Phân tích lỗi chi tiết theo từng nhóm cờ (flags), theo nền tảng (source),
    và xuất danh sách các mẫu đoán sai để đưa vào báo cáo.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    df = df_eval.copy().reset_index(drop=True)
    df["y_true"] = df["adjudicated_label"].astype(int)
    df["y_pred"] = np.asarray(y_pred, dtype=int)
    df["true_name"] = df["y_true"].map(LABEL_MAP)
    df["pred_name"] = df["y_pred"].map(LABEL_MAP)
    df["is_correct"] = df["y_true"] == df["y_pred"]
    df["confidence"] = np.round(y_prob, 4) if y_prob is not None else np.nan

    # 1. BẢNG PHÂN TÍCH LỖI THEO NHÓM CỜ NGÔN NGỮ (FLAGS)
    df["flags_clean"] = df["flags"].fillna("normal_clean").replace("", "normal_clean")
    df_exploded = df.assign(flag_item=df["flags_clean"].str.split("|")).explode("flag_item")

    flag_records: list[dict[str, Any]] = []
    for flag_name, group in df_exploded.groupby("flag_item"):
        total = len(group)
        errors = int((~group["is_correct"]).sum())
        error_rate = (errors / total) * 100
        acc = (1.0 - errors / total) * 100
        macro_f1 = float(
            f1_score(group["y_true"], group["y_pred"], average="macro", zero_division=0) * 100
        )

        wrong_group = group[~group["is_correct"]]
        if len(wrong_group) > 0:
            confusion_pairs = (
                wrong_group["true_name"] + " → " + wrong_group["pred_name"]
            ).value_counts()
            top_confusion = f"{confusion_pairs.index[0]} ({confusion_pairs.iloc[0]})"
        else:
            top_confusion = "Không có lỗi"

        flag_records.append(
            {
                "Nhóm hiện tượng (Flag)": flag_name,
                "Số mẫu": total,
                "Số mẫu sai": errors,
                "Tỷ lệ lỗi (%)": round(error_rate, 2),
                "Accuracy (%)": round(acc, 2),
                "Macro-F1 (%)": round(macro_f1, 2),
                "Kiểu nhầm phổ biến nhất ( Thực tế → Dự đoán )": top_confusion,
            }
        )

    df_flag_summary = (
        pd.DataFrame(flag_records)
        .sort_values(by=["Tỷ lệ lỗi (%)", "Số mẫu"], ascending=[False, False])
        .reset_index(drop=True)
    )

    # 2. BẢNG ĐÁNH GIÁ THEO NỀN TẢNG MẠNG XÃ HỘI (SOURCE)
    source_records: list[dict[str, Any]] = []
    for src_name, group in df.groupby("source"):
        total = len(group)
        errors = int((~group["is_correct"]).sum())
        macro_f1 = float(
            f1_score(group["y_true"], group["y_pred"], average="macro", zero_division=0) * 100
        )
        acc = float(accuracy_score(group["y_true"], group["y_pred"]) * 100)

        source_records.append(
            {
                "Nền tảng (Source)": src_name,
                "Số mẫu": total,
                "Số mẫu sai": errors,
                "Accuracy (%)": round(acc, 2),
                "Macro-F1 (%)": round(macro_f1, 2),
            }
        )

    df_source_summary = (
        pd.DataFrame(source_records)
        .sort_values(by="Macro-F1 (%)", ascending=True)
        .reset_index(drop=True)
    )

    # 3. DANH SÁCH CHI TIẾT CÁC MẪU ĐOÁN SAI (ERROR CASES)
    df_errors = df[~df["is_correct"]][
        [
            "id",
            "source",
            "text_raw",
            "true_name",
            "pred_name",
            "confidence",
            "flags",
        ]
    ].copy()

    safe_name = model_name.lower().replace(" ", "_")
    df_flag_summary.to_csv(f"{output_dir}/error_by_flags_{safe_name}.csv", index=False)
    df_source_summary.to_csv(f"{output_dir}/eval_by_source_{safe_name}.csv", index=False)
    df_errors.to_csv(f"{output_dir}/error_analysis_{safe_name}.csv", index=False)

    return {
        "flag_summary": df_flag_summary,
        "source_summary": df_source_summary,
        "error_samples": df_errors,
    }


def export_markdown_report_tables(
    analysis_results: dict[str, pd.DataFrame],
    model_name: str = "Baseline",
    max_error_examples: int = 10,
) -> str:
    """Chuyển đổi kết quả Error Analysis thành định dạng bảng Markdown cho báo cáo."""
    flag_df = analysis_results["flag_summary"]
    source_df = analysis_results["source_summary"]
    err_df = analysis_results["error_samples"].head(max_error_examples)

    md_lines = [
        f"#### Phân tích lỗi chi tiết — Mô hình: {model_name}\n",
        "**1. Bảng thống kê lỗi theo hiện tượng ngôn ngữ (Flags):**\n",
        flag_df.to_markdown(index=False),
        "\n\n**2. Hiệu năng theo nền tảng mạng xã hội (Source):**\n",
        source_df.to_markdown(index=False),
        f"\n\n**3. Một số ví dụ dự đoán sai điển hình (Top {len(err_df)} mẫu):**\n",
        err_df.to_markdown(index=False),
    ]
    return "\n".join(md_lines)