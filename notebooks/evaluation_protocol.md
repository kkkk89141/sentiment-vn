# Evaluation Protocol v0.1 (W06, B)
 
> Mục tiêu: chốt **trước khi chạy thí nghiệm** cách đo, để mọi so sánh baseline/PhoBERT là công bằng và tái lập được.
> Cài đặt tương ứng: `src/evaluate.py`.
 
## 1. Nhãn
 
`0=negative, 1=neutral, 2=positive` (khớp annotation guideline). Mọi file dự đoán dùng đúng mã này.
 
## 2. Metric
 
| Vai trò | Metric | Ghi chú |
|---|---|---|
| **Chính** | **macro-F1** | Neutral ít mẫu, accuracy dễ gây hiểu nhầm |
| Phụ | precision / recall / F1 **từng lớp**, weighted-F1, accuracy | Luôn báo F1 neutral riêng |
| Phụ | confusion matrix | Hàng = thật, cột = dự đoán |
| Độ chắc chắn | khoảng tin cậy 95% của macro-F1 (bootstrap 1000 lần, seed 42) | Báo kèm mọi bảng kết quả chính |
| Hệ thống | latency p50/p95 (ms/câu, đã loại warm-up) | Đo trên máy chạy demo, gồm cả tách từ/tiền xử lý |
 
Quy ước macro-F1: trung bình F1 trên các lớp **có mẫu trong y_true**. Với test đủ 3 lớp thì trùng sklearn `average="macro"`.
 
## 3. Dữ liệu đánh giá
 
| Tập | Vai trò | Quy tắc |
|---|---|---|
| UIT-VSFC train / validation / test | In-domain | **Dùng split chính thức**, không tự chia lại |
| Social holdout tự gán nhãn | Out-of-domain (miền mạng xã hội) | Xem mục 3.1 |
| 32 ví dụ khó (`reports/hard_cases_v1.csv`) | Kiểm tra định tính | Không tính vào bảng metric chính (mục 3.2) |
 
Kết quả in-domain và out-of-domain luôn ở **hai bảng riêng**; không gộp, không so sánh trực tiếp số từ hai tập.
 
### 3.1 Cỡ mẫu của social holdout
 
Với n ≈ 200 và độ chính xác ≈ 0.8, sai số chuẩn khoảng 2.8 điểm phần trăm, tức CI 95% rộng khoảng ±5.5 điểm. Lớp neutral trong tập tự gán có thể chỉ ~20 mẫu: CI của recall lớp này rộng khoảng ±20 điểm. Hệ quả:
 
- Báo **n và số mẫu từng lớp** cạnh mọi con số; `evaluate.py` tự cảnh báo khi nhóm < 30 mẫu hoặc lớp < 20 mẫu.
- Chênh lệch nhỏ giữa hai mô hình trên tập này thường không có ý nghĩa; dùng `paired_bootstrap_diff`, nếu CI chứa 0 thì **không kết luận** mô hình nào tốt hơn.
- **Đề xuất:** dùng social holdout như tập **test-only**, không chia 70/15/15 (chia nhỏ sẽ còn vài chục mẫu mỗi phần). Nếu muốn dùng nó để huấn luyện, dùng k-fold cross-validation và báo rõ.
### 3.2 32 ví dụ khó
 
Các ví dụ tự viết (`source = synthetic`), nhãn là nhãn **đề xuất theo guideline** và chưa được duyệt. Dùng để (a) smoke-test đầu ra, (b) phân tích lỗi theo nhóm (`category`), (c) xây nền cho error taxonomy. Không dùng để tối ưu mô hình hay báo như một test set.
 
## 4. Quy tắc chống rò rỉ và dùng test
 
1. Loại trùng/gần trùng **trước** khi chia; các bản trùng nằm cùng một split.
2. Fit TF-IDF, từ điển, class weight, augmentation **chỉ trên train**.
3. Chọn siêu tham số và checkpoint trên **validation**.
4. Test (kể cả social holdout) **chỉ chạy một lần** cho cấu hình cuối cùng của mỗi mô hình. Không chọn baseline tốt nhất bằng test (giữa kỳ W08 cũng vậy).
5. Mọi lần chạy ghi: dataset version, seed, config, commit hash.
6. Trong ablation (có/không tiền xử lý teencode, emoji, tách từ), chỉ thay **một** yếu tố mỗi lần.
## 5. So sánh mô hình
 
- Cùng tập test, cùng cách tiền xử lý đã công bố (trừ yếu tố đang ablate).
- Mọi bảng so sánh gồm: macro-F1 [CI], F1 từng lớp, accuracy, n.
- PhoBERT: báo trung bình ± độ lệch trên ≥ 2–3 seed nếu có thời gian; nếu chỉ 1 seed, ghi rõ.
- Majority-class dummy (E0) luôn có mặt như mốc sàn.
## 6. Định dạng dự đoán
 
File CSV mỗi lần chạy: `reports/preds_<model>_<split>.csv`
 
| Cột | Bắt buộc | Ghi chú |
|---|---|---|
| `id` | ✔ | duy nhất |
| `y_true` | ✔ | 0/1/2 |
| `y_pred` | ✔ | 0/1/2 |
| `confidence` | | điểm của mô hình; không gọi mọi điểm là xác suất chuẩn |
| `model_name` | | vd `lr_tfidf_word12`, `phobert_base_v2_seed42` |
| `source` | | nguồn/nền tảng, để báo theo nhóm |
| `flags` | | cờ từ guideline, để phân tích lỗi |
 
Giao diện suy luận chung (đã có trong kế hoạch): `predict(text) -> {label, confidence, model_name}`; `label` là 0/1/2.
 
Lệnh:
 
```bash
python -m src.evaluate --pred reports/preds_lr_test.csv --out reports/metrics_lr_test.json \
    --group-col source --fig reports/figures/cm_lr_test.png
```
 
## 7. Mẫu bảng kết quả trong báo cáo
 
| Mô hình | Tập | n | macro-F1 [95% CI] | F1 neg | F1 neu | F1 pos | Acc |
|---|---|---|---|---|---|---|---|
| Dummy | UIT-VSFC test | | | | | | |
| LR + TF-IDF | UIT-VSFC test | | | | | | |
| … | … | | | | | | |
 
## 8. Điểm cần chốt
 
1. Social holdout là test-only (mục 3.1).
2. Dùng split chính thức của UIT-VSFC, không tự chia lại.
3. Định dạng file dự đoán (mục 6) và đường dẫn `reports/`.