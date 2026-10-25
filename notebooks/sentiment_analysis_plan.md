# KẾ HOẠCH DỰ ÁN: PHÂN LOẠI CẢM XÚC BÌNH LUẬN TIẾNG VIỆT

**Nhóm:** 2 sinh viên CS | **Môn:** Trí tuệ nhân tạo | **Thời gian:** W06–W15; bảo vệ W16–W18  
**Đầu ra:** phân loại `negative / neutral / positive` cho bình luận tiếng Việt trên Facebook, YouTube, TikTok, Instagram bằng baseline và PhoBERT; demo Streamlit. **Không cam kết tự động trích xuất trực tiếp từ cả bốn nền tảng.**

## 1. Mục tiêu và phạm vi

- **MVP tại W08:** dữ liệu đã kiểm tra và chia train/dev/test, nhãn thống nhất, 3 baseline TF-IDF + Naive Bayes / Logistic Regression / Linear SVM, báo cáo macro-F1 và confusion matrix, Streamlit nhập một bình luận → dự đoán.
- **Sản phẩm tại W15:** fine-tune PhoBERT (nếu có tài nguyên), so sánh công bằng trên cùng tập test, có bộ test social media gán nhãn thủ công, phân tích lỗi tiếng lóng/phủ định/mỉa mai/emoji, demo nhập nhiều bình luận bằng CSV.
- **Tiêu chí chất lượng:** metric chính **macro-F1**; theo dõi F1 từng lớp, đặc biệt neutral; đo latency p50/p95 trên máy chạy demo; ghi rõ kết quả theo từng nguồn dữ liệu và limitations.
- **Không mở rộng ở MVP:** scraping tự động Facebook/TikTok/Instagram; phân tích cảm xúc đa nhãn, đa ngôn ngữ, sarcasm detection độc lập, dashboard realtime. Các chức năng đó chỉ là stretch goals.

## 2. Quy ước dữ liệu và phương pháp khoa học

**Nhãn chuẩn:** `0=negative`, `1=neutral`, `2=positive`; kiểm tra mapping từng bộ dữ liệu gốc (AIVIVN có mapping khác). **Neutral:** câu chủ yếu cung cấp thông tin/không biểu lộ thái độ rõ; câu cảm xúc pha trộn hoặc mỉa mai cần quy tắc gán nhãn và đánh dấu ambiguous. Bình luận chỉ có emoji hoặc chỉ có ảnh/video không có nội dung cần xử lý riêng.

**Các trường dữ liệu:** `id, text_raw, text_clean, label, source, dataset_name, split, annotation_status` (có thể bổ sung `annotator_1, annotator_2, adjudicated_label`). Không đưa username/link cá nhân vào dữ liệu chia sẻ.

**Chia dữ liệu:** tôn trọng splits chính thức của UIT-VSFC; tập mới dùng chia stratified train/dev/test theo 70/15/15 hay 80/10/10 (chọn một phương án trước thí nghiệm). Loại bình luận trùng/gần trùng **trước khi chia**; nhóm các bản trùng cùng một split. Mọi thao tác học thống kê như fit TF-IDF, augmentation, class-weight tuning phải làm **chỉ trên train**; chọn hyperparameter trên dev; test giữ nguyên đến đánh giá cuối. Khi test theo nền tảng, báo số mẫu từng nền tảng. Nếu có nhiều tập nguồn, luôn phân biệt kết quả *in-domain* và *out-of-domain*.

**Chính sách dữ liệu:** ưu tiên corpus có điều kiện sử dụng rõ; nếu lấy bình luận thật, tuân thủ ToS/API, tránh scraping trái phép, loại thông tin nhận dạng, không đăng lại bình luận có thông tin cá nhân, lưu nguồn và quyền sử dụng.

## 3. Roadmap theo sprint

| Sprint | Thành viên A — Data / Baseline / Web | Thành viên B — PhoBERT / Evaluation / Error | Deliverables & điều kiện nghiệm thu |
|---|---|---|---|
| **W06 (1 tuần)** | Khởi tạo Git, môi trường, schema dữ liệu; tải UIT-VSFC, EDA, kiểm tra nhãn và trùng lặp; thiết kế cấu trúc Streamlit | Viết annotation guideline và test cases tiếng lóng; nghiên cứu PhoBERT tokenizer & GPU; thiết kế protocol đánh giá | Repo chạy được, Data Card v1, bảng phân bố nhãn, ≥20 ví dụ khó, metric protocol đã chốt |
| **W07–W08 (2 tuần) — GIỮA KỲ** | Làm preprocessing v1; chạy NB/LR/LinearSVM + TF-IDF; GridSearch trên dev; Streamlit input đơn; lưu baseline artifact | Tạo bộ test social media thí điểm (đề xuất 150–300 bình luận có quyền dùng, hai người gán nhãn); đánh giá baseline theo lớp; smoke-test PhoBERT với một batch | Báo cáo W08: bảng baseline, macro-F1, confusion matrix, demo sơ bộ chạy offline, lỗi chính, kế hoạch tiếp |
| **W09–W10 (2 tuần)** | Thử word-vs-character n-gram, từ điển teencode, emoji, so sánh preprocessing ablation; viết inference API chung | Fine-tune PhoBERT-base lần 1 trên train, chọn checkpoint bằng dev macro-F1; ghi seed, epoch, lr, batch, GPU; phân tích lỗi neutral | Baseline cải tiến, PhoBERT checkpoint v1 (hoặc documented fallback), cùng một schema prediction |
| **W11–W12 (2 tuần)** | Nâng Streamlit: chọn model, nhập CSV, bảng tải kết quả; benchmark p50/p95; cache model | Tune PhoBERT có giới hạn (2–4 cấu hình); thử class weights / sampling chỉ trên train; đánh giá theo source, slang, negation, emoji, sarcasm | Báo cáo thực nghiệm có ablation, tập social holdout, latency và lỗi có ví dụ ẩn danh |
| **W13–W14 (2 tuần)** | Test integration/robustness, README hướng dẫn setup, fallback CPU, bảo mật dữ liệu demo; chuẩn bị live demo | Đóng băng model và test cuối, confusion matrix & F1 từng lớp, confidence calibration nếu thời gian cho phép, limitations, biểu đồ | Release candidate có thể chạy từ đầu đến cuối; bảng kết quả tái lập và phân tích lỗi hoàn chỉnh |
| **W15 (1 tuần) — CUỐI KỲ** | Hoàn thiện UI, demo script, đóng gói artifacts, kiểm thử máy trình chiếu | Hoàn thiện báo cáo, kết quả so sánh, đóng góp kỹ thuật, trả lời câu hỏi về metric/overfit/leakage | Tag `v1.0`, slide/báo cáo, demo dự phòng, checklist QA hoàn thành |
| **W16–W18 (bảo vệ)** | Demo trực tiếp + kiến trúc + reproducibility | Phương pháp ML + đánh giá + error analysis | Q&A tập dượt: giải thích 3 lớp, dữ liệu khác miền, false positive/false negative, latency |

### Các mốc kiểm soát và thời gian dự phòng
- Cuối **W06**: khóa định nghĩa nhãn và lựa chọn nguồn dữ liệu.
- Cuối **W07**: cả hai dùng chung `predict(text) -> {label, confidence, model_name}`; A không phụ thuộc PhoBERT để dựng demo.
- **W08**: không dùng test để chọn baseline tốt nhất; giữ demo chạy bằng LR/SVM kể cả khi GPU lỗi.
- Cuối **W10**: nếu không fine-tune được PhoBERT, B dùng contextual embeddings cố định + Logistic Regression hoặc checkpoint sentiment có giấy phép phù hợp, trình bày như phương án thay thế (không gọi là fine-tuned model).
- Đầu **W14**: đóng băng dataset/test, kết thúc các thí nghiệm lớn.

## 4. Phân công và cơ chế làm việc

**A (primary owner):** data acquisition/cleaning, EDA, preprocessing baseline, TF-IDF models, serialization, Streamlit, deploy, latency; **B review** dữ liệu/nhãn trước training.

**B (primary owner):** annotation protocol, PhoBERT segmentation/tokenization/fine-tuning, experiment tracking, metrics, error taxonomy, báo cáo; **A review** evaluation script và so sánh model.

**Công việc chung:** hai người cùng gán nhãn bộ test mạng xã hội độc lập trước khi thảo luận; A tích hợp biểu đồ do B cung cấp; B test UI của A. Mỗi tuần 1 buổi 30 phút review + PR; mỗi PR có code review của người còn lại. Cả hai đều trình bày được baseline và PhoBERT.

**Giao ước code:** `src/preprocessing.py`, `src/train_baseline.py`, `src/train_phobert.py`, `src/evaluate.py`, `src/inference.py`, `app.py`; dùng config/version dataset cố định, seed=42 cho experiments, requirements/lockfile, `.gitignore` cho PII/checkpoint lớn. Không commit tokens hoặc dữ liệu thu thập không được chia sẻ.

## 5. Dataset được khuyến nghị

| Dataset | Mức phù hợp | Cách dùng / lưu ý |
|---|---|---|
| **UIT-VSFC** | **Ưu tiên baseline**: tiếng Việt 3 lớp, >16k nhận xét sinh viên; chia chính thức 11,426 train / 1,583 validation / 3,166 test | Dễ khởi động và so sánh nghiên cứu; **khác miền** bình luận mạng xã hội, neutral rất ít; xác minh license/điều khoản trước phát hành |
| **AIVIVN 2019 Sentiment Challenge** | Bổ sung dữ liệu review với văn phong tự nhiên, **chỉ 2 lớp positive/negative** | Không tự ép dữ liệu này thành 3 lớp; dùng thí nghiệm bổ trợ hoặc training positive/negative có thuyết minh, tuyệt đối không trộn test không tương thích |
| **VLSP 2016 Sentiment** | Dữ liệu tiếng Việt sentiment tham chiếu, 6,450 câu | Cần thủ tục xin quyền truy cập; không dựa vào nó cho deadline W08 |
| **UIT-ViSFD** | Smartphone/e-commerce 11,122 comment; thích hợp thử domain shift | Đây là **aspect-based sentiment**, không mặc định tương đương nhãn 3-class toàn câu; phải xây dựng quy tắc chuyển hoặc dùng đánh giá chuyên biệt |
| **Social Media Holdout tự gán nhãn** | **Quan trọng nhất cho luận điểm tiếng lóng/ngữ cảnh** | Nhắm 150–300 mẫu ban đầu, sau đó ≥400 nếu đủ thời gian, phân bổ nguồn và lớp theo khả năng thu thập; hai người annotate độc lập, giải quyết bất đồng, không dùng để tối ưu nếu là test cuối |

**Nguồn:**
- UIT-VSFC: https://github.com/kietnv/uit-vsfc và https://huggingface.co/datasets/uitnlp/vietnamese_students_feedback
- AIVIVN / VLSP / corpora overview: https://github.com/undertheseanlp/NLP-Vietnamese-progress/blob/master/tasks/sentiment_analysis.md
- VLSP chính thức: https://vlsp.org.vn/resources-vlsp2016
- UIT-ViSFD: https://github.com/LuongPhan/UIT-ViSFD
- PhoBERT: https://github.com/VinAIResearch/PhoBERT

## 6. Rủi ro, cách phát hiện và phương án dự phòng

| Rủi ro | Phát hiện | Phòng tránh / fallback |
|---|---|---|
| **Lệch lớp neutral** | Bảng phân bố; F1-neutral thấp dù accuracy cao | Macro-F1 làm metric chính; `class_weight='balanced'` cho LR/SVM; lấy thêm mẫu neutral hợp lệ; báo per-class F1; không oversample test |
| **Domain shift từ phản hồi sinh viên → MXH** | Macro-F1 trên social holdout thấp hơn UIT-VSFC | Tập social holdout theo nền tảng; bổ sung dữ liệu thật đã gán nhãn nếu quyền cho phép; fine-tune trên train social, giữ test riêng; nêu giới hạn |
| **Teencode, dấu, emoji, mỉa mai/phủ định** | Error buckets; ví dụ `không tệ`, `đỉnh của chóp`, `hay quá ha` | Giữ emoji/phủ định, Unicode NFC; từ điển slang phiên bản hóa; char n-gram; ablation để xác minh tiền xử lý có hiệu quả, không tự đổi nghĩa câu |
| **Data leakage/duplicate** | Near-duplicate giữa splits; metric quá tốt bất thường | Dedupe trước split; dùng official split; `Pipeline(TfidfVectorizer, classifier)` fit train-only; test 1 lần cuối |
| **Hết VRAM/training quá lâu** | OOM/training chưa xong cuối W10 | `phobert-base`, batch 8–16, gradient accumulation, max_length=128, early stop, mixed precision nếu GPU hỗ trợ; fallback frozen embeddings/LR |
| **Demo latency/network** | Đo p50/p95, test offline | Cache model một lần bằng `st.cache_resource`, mặc định baseline nhanh, load PhoBERT khi chọn; tắt gọi API live; video backup + CSV demo có sẵn |
| **Confidence gây hiểu nhầm** | Softmax cao ở ví dụ sai, SVM không có `predict_proba` | Hiển thị score/estimated confidence đúng bản chất; dùng LR hoặc `CalibratedClassifierCV` trên dev với split phù hợp; không gọi mọi score là xác suất chuẩn |
| **ToS/quyền riêng tư/giấy phép** | Không chứng minh nguồn hoặc quyền sử dụng | Dataset cấp phép rõ, ghi provenance, ẩn danh, không tự động scrape nền tảng bị hạn chế; demo với câu tự viết hoặc mẫu được phép |
| **Hai người chặn việc nhau** | Chờ schema/model interface | Khóa interface từ W07, mock prediction cho Streamlit, Git branches + PR tuần; backlog chia task độc lập |

## 7. Thí nghiệm tối thiểu cần có

1. **E0:** Majority-class dummy classifier (sanity check).
2. **E1–E3:** TF-IDF word n-gram (1,2) + MultinomialNB / LogisticRegression / LinearSVC.
3. **E4:** TF-IDF char n-gram (3,5), có/không normalization slang (ablation).
4. **E5:** PhoBERT-base fine-tuned 3-class; chọn checkpoint bằng validation macro-F1.
5. **Evaluation:** macro-F1, weighted-F1, accuracy, per-class precision/recall/F1, confusion matrix, latency; chạy trên một test chuẩn và social holdout, không so sánh số từ test khác nhau như trực tiếp tương đương.

**Ngưỡng hoàn thành (engineering gates, không phải lời hứa về model):** 100% inference outputs thuộc ba nhãn; 0 lỗi ứng dụng trên bộ 20 test inputs; có bảng kết quả 3 baselines; có script reproduce; demo chạy bằng CPU khi không có GPU; mỗi kết luận cải tiến kèm chênh lệch metric và kích thước mẫu.

## 8. Cấu trúc thư mục đề xuất

```text
sentiment-vn/
├── README.md
├── requirements.txt
├── configs/
├── data/                 # raw/private không đẩy lên git
├── notebooks/            # EDA và các thử nghiệm
├── src/
│   ├── preprocessing.py
│   ├── train_baseline.py
│   ├── train_phobert.py
│   ├── evaluate.py
│   └── inference.py
├── artifacts/            # trọng số/model theo đúng quyền phân phối
├── reports/
│   ├── figures/
│   └── error_analysis.csv
├── tests/
└── app.py
```

## 9. Checklist nghiệm thu cuối kỳ

- [ ] Mô tả nguồn và quyền dùng dữ liệu; lớp được chuẩn hóa.
- [ ] Có bảng thống kê nguồn/nền tảng/split/nhãn và kiểm tra trùng lặp.
- [ ] 3 baselines, PhoBERT hoặc phương án dự phòng, lưu config và seed.
- [ ] Bảng macro-F1 + per-class F1 + confusion matrix + kết quả holdout.
- [ ] Có đánh giá preprocessing tiếng Việt bằng ablation, lỗi được phân loại.
- [ ] Demo single input + CSV, cho chọn model, nêu rõ confidence.
- [ ] Kiểm thử offline/CPU, có demo fallback, báo cáo latency.
- [ ] README hướng dẫn tái lập và nêu giới hạn quyền riêng tư/domain shift.
- [ ] Hai người nắm rõ phần việc của nhau và có kịch bản Q&A.

## 10. Lịch học lý thuyết gắn với thực hành

- **W06:** text classification, nhãn 3 lớp, annotation, EDA, data leakage, train/dev/test.
- **W07:** TF-IDF, n-gram, MultinomialNB, LR, SVM, sklearn Pipeline.
- **W08:** precision/recall/F1, macro/weighted, confusion matrix, error analysis.
- **W09:** tiếng Việt Unicode, word segmentation, teencode, negation, embeddings.
- **W10:** attention, transformers, pretrained language models, PhoBERT, tokenization.
- **W11–W12:** fine-tuning, cross-entropy, optimizer, warmup, overfit, class weights, calibration.
- **W13–W15:** ablation studies, domain shift, latency, deployment, reproducibility, limitations.
