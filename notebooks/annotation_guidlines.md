# Annotation Guideline — Phân loại cảm xúc bình luận tiếng Việt
 
## 1. Phạm vi
 
- **Đơn vị gán nhãn:** một bình luận (toàn văn, kể cả emoji).
- **Nhãn:** thái độ/cảm xúc mà **người viết** thể hiện trong chính bình luận, không phải đánh giá của người gán nhãn về sự việc.
- Chỉ dùng thông tin trong bình luận. Không đoán ngữ cảnh bên ngoài (video, bài đăng); nếu cần ngữ cảnh mới hiểu được thì gắn cờ `needs_context` (mục 5).
## 2. Ba nhãn
 
| Nhãn | Mã | Định nghĩa | Ví dụ |
|---|---|---|---|
| negative | 0 | Chê, bực, thất vọng, phản đối, chỉ trích, xúc phạm, buồn/lo | "Ko đc như quảng cáo, thất vọng" |
| neutral | 1 | Hỏi, thông tin, mô tả, tag, không có thái độ rõ, hoặc thái độ lưng chừng | "Giá bao nhiêu vậy ad?" |
| positive | 2 | Khen, hài lòng, ủng hộ, vui, cảm ơn, chúc mừng | "Quá tuyệt vời luôn 😍" |
 
Mã nhãn phải khớp `0=negative, 1=neutral, 2=positive` trong toàn bộ repo (kiểm tra lại mapping khi nhập dataset ngoài).
 
## 3. Thứ tự áp dụng quy tắc
 
1. **Loại trừ** (mục 4.1): không có nội dung để gán nhãn, hoặc không phải tiếng Việt → `annotation_status = excluded`.
2. **Xác định thái độ thật của người viết** (phủ định, mỉa mai, từ lóng tăng nghĩa: mục 4.2–4.4).
3. Nếu có nhiều thái độ trái chiều → quy tắc câu pha trộn (4.5).
4. Nếu vẫn không quyết định được sau khi áp dụng quy tắc → gắn `ambiguous`, ghi lý do, **không ép nhãn**.
## 4. Quy tắc cho từng tình huống
 
### 4.1 Loại trừ
| Tình huống | Xử lý |
|---|---|
| Chỉ có tag/@mention/link/ảnh/video/sticker, không có chữ | `excluded` |
| Chủ yếu ngôn ngữ khác tiếng Việt | `excluded` |
| Bình luận trống sau khi ẩn danh | `excluded` |
 
### 4.2 Phủ định và từ lóng
- Gán theo **ý toàn câu**, không theo từ đơn lẻ. "không tệ" ≈ positive nhẹ; "không hay" = negative.
- Từ tục/lóng tăng nghĩa (`vl`, `vcl`, `dữ`, `kinh`, `đỉnh của chóp`) **không tự động là negative**: "Đẹp vl" = positive, "Dở vl" = negative.
- Chửi/xúc phạm **cá nhân** hoặc nhóm người → negative. (Đây là cảm xúc của bài toán sentiment, không phải bài toán hate-speech; không tách riêng.)
### 4.3 Teencode, không dấu, kéo dài ký tự
- Gán nhãn theo nghĩa đã giải mã ("ko đc" = "không được", "tuyet voi" = "tuyệt vời", "đẹpppp" = "đẹp").
- Nếu không giải mã được chắc chắn → `ambiguous`.
### 4.4 Mỉa mai
- Nếu **trong chính bình luận** có tín hiệu rõ (đối lập nội dung–thực tế, "hay quá ha", "giỏi lắm", emoji 🙃/🤡 đi kèm khen) → gán theo ý thật (thường negative), gắn cờ `sarcasm`.
- Nếu mỉa mai chỉ nhận ra được khi biết ngữ cảnh ngoài → `ambiguous` + `needs_context`.
### 4.5 Cảm xúc pha trộn
- Có "nhưng/tuy nhiên/mà": **ưu tiên mệnh đề sau**. "Phim hay nhưng kết thúc dở" → negative.
- Hai vế ngang trọng lượng, không có mệnh đề kết luận → neutral + cờ `mixed`.
- Cả hai trường hợp đều gắn `mixed`, vì đây là nhóm lỗi cần theo dõi riêng.
### 4.6 Câu hỏi
- Hỏi thông tin thuần → neutral.
- Câu hỏi tu từ mang thái độ ("Sao dở vậy trời?") → theo thái độ (negative), cờ `rhetorical_question`.
### 4.7 Emoji
- Chỉ có emoji rõ nghĩa (😍❤️👏 → positive; 😡😤 → negative) → gán theo emoji.
- Emoji nhiều nghĩa (😂 🙃 😭 😅) đứng một mình → `ambiguous`.
- Emoji đi kèm chữ: xét cùng chữ; emoji có thể **đảo nghĩa** (xem 4.4).
### 4.7b Quảng cáo/spam
- Không có thái độ → neutral + cờ `spam`. (Có thể lọc riêng khi phân tích; giữ để phản ánh phân phối thật.)
### 4.8 Đồng cảm / tin buồn
- Bày tỏ buồn/thương cảm trước tin buồn → negative + cờ `sympathy` (cảm xúc người viết là tiêu cực, dù thiện chí).
- Chúc mừng, vui cùng → positive.
## 5. Cờ (`flags`, phân tách bằng `|`)
 
`sarcasm`, `mixed`, `needs_context`, `rhetorical_question`, `sympathy`, `spam`, `teencode`, `no_diacritics`, `emoji_only`, `code_mix`.
 
Cờ dùng để phân tích lỗi theo nhóm ở W11–W12
 
## 6. Quy trình gán nhãn và đo đồng thuận
 
1. **Pilot:** 50 bình luận, gán **độc lập**, không trao đổi.
2. Tính **Cohen's κ** (3 lớp) và bảng bất đồng. Mục tiêu κ ≥ 0.6; thấp hơn thì sửa quy tắc, gán lại pilot.
3. Họp thảo luận bất đồng → cập nhật guideline v0.2.
4. Gán độc lập toàn bộ bộ holdout (150–300 mẫu đầu, sau đó mở rộng nếu đủ thời gian).
5. **Adjudication:** thảo luận từng mẫu bất đồng. Không đồng thuận được → `adjudicated_label` để trống, `annotation_status = ambiguous`.
6. Báo cáo kết quả theo hai cách: (a) bỏ mẫu ambiguous, (b) tập ambiguous riêng. Không âm thầm loại.
Cột dữ liệu cần ghi: `annotator_1, annotator_2, adjudicated_label, annotation_status (labeled|ambiguous|excluded), flags`.
 
## 7. Quyền riêng tư và nguồn
 
- Thay `@tên`, tên riêng, SĐT, email, link cá nhân bằng `@user`, `<name>`, `<phone>`, `<url>` **trước khi lưu**.
- Không lưu username hay URL bình luận trong dữ liệu dùng chung; dùng `id` nội bộ.
- Chỉ dùng bình luận lấy qua kênh được phép (API chính thức, nội dung có quyền dùng). Ghi `source` và cách lấy.
- Không đăng lại nguyên văn bình luận thật trong báo cáo nếu nhận dạng được người viết.

## 8. Điểm cần chốt
 
1. 4.2: xúc phạm cá nhân tính là negative (không tách hate-speech).
2. 4.5: ưu tiên mệnh đề sau "nhưng".
3. 4.7b: spam giữ lại ở neutral hay loại hẳn.
4. 4.8: đồng cảm trước tin buồn là negative.
5. Ngưỡng K chấp nhận được và ai là người quyết định khi bất đồng.
