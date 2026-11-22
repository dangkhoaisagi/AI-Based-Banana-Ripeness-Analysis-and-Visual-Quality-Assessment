# BỘ GIÁO DỤC VÀ ĐÀO TẠO
# [TÊN TRƯỜNG ĐẠI HỌC]
# [TÊN KHOA / VIỆN]

---

# BÁO CÁO ĐỒ ÁN MÔN HỌC
# (ĐỒ ÁN XỬ LÝ ẢNH / TRÍ TUỆ NHÂN TẠO)

# PHÂN TÍCH ĐỘ CHÍN VÀ CHẤT LƯỢNG QUẢ CHUỐI
# BẰNG HỌC SÂU KẾT HỢP XỬ LÝ ẢNH SỐ
# (HỆ THỐNG BananaAI)

---

**Sinh viên thực hiện:** [Họ và tên]  
**Mã số sinh viên:** [MSSV]  
**Lớp:** [Mã lớp]  
**Giảng viên hướng dẫn:** [Học hàm, học vị, Họ và tên]  
**Học kỳ / Năm học:** [Học kỳ … / Năm học 2025–2026]

---

*Tháng 10 năm 2026*

\newpage

# LỜI CAM ĐOAN

Em xin cam đoan đây là công trình nghiên cứu của bản thân em, được thực hiện dưới sự hướng dẫn của [Giảng viên hướng dẫn]. Các số liệu, kết quả trình bày trong báo cáo là trung thực và chưa từng được công bố trong bất kỳ công trình nào khác, trừ những nội dung đã được trích dẫn đầy đủ nguồn.

Các bộ dữ liệu ảnh sử dụng trong đồ án được lấy từ nguồn công khai trên Kaggle, có ghi rõ tác giả và giấy phép. Các chỉ số Accuracy, Precision, Recall, Macro-F1 được đọc trực tiếp từ file kết quả thực nghiệm, không tự sinh hay chỉnh sửa. Hệ thống chỉ phân tích dấu hiệu hình ảnh của quả chuối; không dùng để kết luận an toàn thực phẩm.

Nếu sai em xin hoàn toàn chịu trách nhiệm.

[Địa phương], ngày … tháng … năm 2026

**Sinh viên**

*(ký và ghi rõ họ tên)*

[Họ và tên]

\newpage

# LỜI CẢM ƠN

Em xin bày tỏ lòng biết ơn sâu sắc tới thầy/cô [Giảng viên hướng dẫn] đã tận tình định hướng, góp ý chuyên môn và tạo điều kiện để em hoàn thành đồ án.

Em cảm ơn quý thầy cô [Tên khoa] — [Tên trường] đã trang bị kiến thức nền về xử lý ảnh số, học máy và phát triển phần mềm web trong suốt quá trình học tập.

Em cảm ơn các tác giả đã công bố ba bộ dữ liệu công khai trên Kaggle: S.M. Shahriar (Banana Ripeness Classification Dataset), Deeuk1985 (Banana Ripeness RGB Images and Spectral Data) và Charles C R (Banalyzer). Trong đồ án, em chỉ sử dụng kênh ảnh RGB; không dùng cảm biến phổ khi suy luận. Em sử dụng các bộ dữ liệu đúng theo giấy phép gốc.

Cuối cùng, em cảm ơn gia đình và bạn bè đã động viên, hỗ trợ em trong thời gian thực hiện đề tài.

Dù đã cố gắng, báo cáo khó tránh khỏi thiếu sót. Em rất mong nhận được ý kiến đóng góp của quý thầy cô và hội đồng.

Em xin chân thành cảm ơn.

\newpage

# TÓM TẮT

Đồ án xây dựng hệ thống **BananaAI** — ứng dụng web phân tích **độ chín** (xanh / chín / quá chín) và **chất lượng theo nhãn quy đổi** (tốt / đốm / thối) của quả chuối từ **ảnh RGB**. Em sử dụng **ba bộ dữ liệu công khai trên Kaggle**: (1) Banana Ripeness Classification Dataset — thực nghiệm phân loại độ chín chính; (2) Banana Ripeness RGB Images and Spectral Data — thực nghiệm thêm về độ chín trên kênh RGB (không dùng phổ khi triển khai); (3) Banalyzer — bài toán chất lượng theo nhãn quy đổi.

Phía học sâu, năm thuật toán CNN được so sánh trên cùng giao thức: **ResNet50, EfficientNetB0, InceptionV3, DenseNet121, MobileNetV3Small** (transfer learning ImageNet, fine-tune hoặc đóng băng backbone). Phía xử lý ảnh số: chuyển **RGB→HSV**, phân đoạn ngưỡng màu, **hình thái học** (opening/closing), **U2-Net** (tách nền), **entropy histogram**, tỷ lệ đốm tối và **hợp nhất quyết định lai**. ResNet50 được chọn triển khai web.

Kiến trúc phần mềm gồm backend FastAPI (Python 3.11, TensorFlow 2.16, Keras 3) và frontend React + Vite. Trên 18 ảnh mẫu có nhãn tham chiếu, hệ thống suy luận đúng 18/18 nhãn. Macro-F1 trên tập test thực nghiệm: ResNet50 **99,76%** (dataset độ chín chính), **93,35%** (Banalyzer); EfficientNetB0 **97,08%** (dataset RGB & Spectral, chỉ dùng ảnh RGB).

**Từ khóa:** ba bộ Kaggle, ảnh RGB, ResNet50, EfficientNet, HSV, U2-Net, hybrid fusion, FastAPI.

\newpage

# ABSTRACT

This project presents **BananaAI**, a web system that estimates banana **ripeness** (unripe / ripe / overripe) and **mapped quality labels** (good / spotted / rotten) from **RGB images only**. Three public Kaggle datasets are used: Shahriar’s ripeness set (main ripeness experiment), Deeuk1985’s RGB & spectral set (additional ripeness experiment on the RGB branch), and Banalyzer (mapped quality).

Five CNNs are compared under one protocol (ResNet50, EfficientNetB0, InceptionV3, DenseNet121, MobileNetV3Small). Classical algorithms include RGB–HSV conversion, color thresholding, morphological opening/closing, U2-Net background removal, histogram entropy, and rule-based hybrid fusion.

The software stack uses a FastAPI backend (Python 3.11, TensorFlow 2.16, Keras 3) and a React + Vite frontend. On an 18-image labeled smoke-test set the system matched all reference labels. On the original experiment test splits, ResNet50 reached **99.76%** Macro-F1 for ripeness and **93.35%** Macro-F1 for mapped quality; EfficientNetB0 reached **97.08%** Macro-F1 on the RGB & Spectral dataset.

**Keywords:** banana ripeness classification, ResNet50, digital image processing, HSV, hybrid AI, FastAPI, React.

\newpage

# MỤC LỤC

Lời cam đoan  
Lời cảm ơn  
Tóm tắt  
Abstract  
Danh mục hình  
Danh mục bảng  
Danh mục từ viết tắt  

**Chương 1. Mở đầu**  
1.1. Lý do chọn đề tài  
1.2. Mục tiêu đề tài  
1.3. Đối tượng và phạm vi nghiên cứu  
1.4. Phương pháp nghiên cứu  
1.5. Ý nghĩa khoa học và thực tiễn  
1.6. Cấu trúc báo cáo  
1.7. Tóm tắt đặc điểm đồ án (đầu vào – dataset – thuật toán – tiền xử lý)  

**Chương 2. Cơ sở lý thuyết và tổng quan**  
2.1. Đặc trưng hình ảnh của quả chuối theo giai đoạn chín  
2.2. Tổng hợp thuật toán sử dụng trong đồ án  
2.3. Xử lý ảnh số: HSV, ngưỡng màu, hình thái học, entropy  
2.4. Tách nền bằng U2-Net và phương án dự phòng  
2.5. Học sâu cho phân loại ảnh (tích chập, softmax, transfer learning)  
2.6. Năm kiến trúc CNN và cách từng mạng hoạt động  
2.7. Độ đo đánh giá mô hình  
2.8. Hợp nhất quyết định lai và softmax quá tự tin  
2.9. Các công trình liên quan  

**Chương 3. Phân tích và thiết kế hệ thống**  
3.1. Khảo sát hiện trạng và yêu cầu  
3.2. Mô hình use case  
3.3. Kiến trúc tổng thể  
3.4. Thiết kế pipeline suy luận lai  
3.5. Thiết kế mô-đun tách nền  
3.6. Thiết kế mô-đun phân tích phổ màu  
3.7. Thiết kế hợp nhất quyết định  
3.8. Thiết kế API  
3.9. Thiết kế giao diện người dùng  
3.10. Quy ước nhãn và tiền xử lý  

**Chương 4. Cài đặt hệ thống**  
4.1. Môi trường và công nghệ  
4.2. Cấu trúc thư mục dự án  
4.3. Nạp và quản lý mô hình  
4.4. Cài đặt xử lý ảnh đầu vào  
4.5. Cài đặt tách nền  
4.6. Cài đặt phân tích màu và OOD  
4.7. Cài đặt hợp nhất quyết định  
4.8. Cài đặt backend FastAPI  
4.9. Cài đặt frontend React  
4.10. An toàn sử dụng và giới hạn công bố  

**Chương 5. Thực nghiệm và đánh giá**  
5.1. Ba bộ dữ liệu Kaggle (chỉ dùng ảnh RGB)  
5.2. Kết quả huấn luyện năm kiến trúc  
5.3. Lựa chọn mô hình triển khai  
5.4. Kiểm thử tích hợp hệ thống  
5.5. Kiểm thử 18 ảnh mẫu  
5.6. Nhất quán suy luận trực tiếp và API  
5.7. Thảo luận kết quả  
5.8. Hạn chế  

**Chương 6. Kết luận và hướng phát triển**  
6.1. Kết luận  
6.2. Những điểm đã đạt được  
6.3. Hạn chế còn lại  
6.4. Hướng phát triển  

Tài liệu tham khảo  
Phụ lục A. Danh sách API  
Phụ lục B. Lệnh khởi động hệ thống  
Phụ lục C. Bảng kết quả 18 ảnh mẫu  
Phụ lục D. Ánh xạ nhãn chất lượng  
Phụ lục E. Ánh xạ thuật toán — mô-đun mã nguồn  

\newpage

# DANH MỤC HÌNH

Hình 3.1. Sơ đồ use case hệ thống BananaAI  
Hình 3.2. Kiến trúc tổng thể frontend – backend – mô hình  
Hình 3.3. Pipeline suy luận lai (học sâu + XLA)  
Hình 3.4. Các bước tách nền hai giai đoạn  
Hình 3.5. Phân đoạn HSV không chồng chéo  
Hình 3.6. Cây quyết định hợp nhất lai  
Hình 3.7. Sơ đồ tuần tự xử lý một yêu cầu `/api/predict`  
Hình 4.1. Cấu trúc thư mục mã nguồn  
Hình 5.1. So sánh Macro-F1 năm mô hình trên ba bộ dữ liệu  

\newpage

# DANH MỤC BẢNG

Bảng 2.1. Đặc trưng màu – kết cấu theo giai đoạn chín  
Bảng 2.2. Danh mục thuật toán và vai trò trong hệ thống  
Bảng 2.3. Công thức các độ đo phân loại  
Bảng 2.4. So sánh năm CNN  
Bảng 5.1. Ba bộ dữ liệu Kaggle — vai trò, URL, nhãn, kênh dùng  
Bảng 3.1. Yêu cầu chức năng  
Bảng 3.2. Yêu cầu phi chức năng  
Bảng 3.3. Ánh xạ endpoint API  
Bảng 3.4. Thứ tự nhãn softmax  
Bảng 4.1. Công nghệ sử dụng  
Bảng 5.1. Tóm tắt bộ dữ liệu  
Bảng 5.2. Kết quả Banana Ripeness Classification Dataset  
Bảng 5.3. Kết quả Banalyzer (chất lượng quy đổi)  
Bảng 5.4. Kết quả Banana Ripeness RGB Images and Spectral Data  
Bảng 5.5. Kết quả kiểm thử 18 ảnh mẫu  
Bảng 5.6. Kiểm thử API và giao diện  

\newpage

# DANH MỤC TỪ VIẾT TẮT

| Viết tắt | Tiếng Anh | Tiếng Việt |
|----------|-----------|------------|
| API | Application Programming Interface | Giao diện lập trình ứng dụng |
| CNN | Convolutional Neural Network | Mạng nơ-ron tích chập |
| CV | Computer Vision | Thị giác máy tính |
| DL | Deep Learning | Học sâu |
| F1 | F1-score | Trung hòa Precision và Recall |
| HSV | Hue, Saturation, Value | Sắc độ, độ bão hòa, độ sáng |
| OOD | Out-of-Distribution | Ngoài phân phối huấn luyện |
| ReLU | Rectified Linear Unit | Hàm kích hoạt ReLU |
| RGB | Red, Green, Blue | Không gian màu đỏ–lục–lam |
| REST | Representational State Transfer | Kiến trúc dịch vụ web |
| XLA | — | Xử lý ảnh số (trong ngữ cảnh đồ án) |
| XLA (Google) | Accelerated Linear Algebra | Bộ biên dịch đại số tuyến tính (không dùng trong đồ án) |

*Lưu ý:* Trong mã nguồn và báo cáo này, **XLA** được dùng theo nghĩa **xử lý ảnh số**, không phải trình biên dịch XLA của TensorFlow.

\newpage

# CHƯƠNG 1. MỞ ĐẦU

## 1.1. Lý do chọn đề tài

Chuối là nông sản xuất khẩu và tiêu dùng nội địa quan trọng. Độ chín quyết định thời điểm thu hoạch, vận chuyển, bảo quản và giá trị thương mại. Việc phân loại thủ công dựa vào cảm quan của người lao động, dễ sai lệch theo ánh sáng, kinh nghiệm và mệt mỏi, khó chuẩn hóa trên dây chuyền.

Thị giác máy tính cho phép ước lượng độ chín từ ảnh RGB với chi phí cảm biến thấp, phù hợp cửa hàng, hộ nông dân và kiểm tra nhanh tại điểm thu mua. Học sâu, đặc biệt mạng tích chập chuyển giao (transfer learning) trên ImageNet, đã cho kết quả cao trên nhiều bài phân loại nông sản. Tuy nhiên, mô hình chỉ học phân phối của tập huấn luyện. Ảnh thực tế — chuối trên cây, nền phức tạp, giống Blue Java vỏ xanh ngọc, ánh sáng vàng — thường làm softmax đưa ra điểm rất cao nhưng **sai nhãn**. Đó là lỗ hổng cần bù bằng đặc trưng màu và kết cấu tính được bằng xử lý ảnh cổ điển.

Đồ án chọn hướng **lai**: dùng ResNet50 làm bộ phân loại chính, đồng thời dùng tách nền, phân đoạn HSV và entropy để kiểm chứng và hiệu chỉnh. Kết quả được đóng gói thành website tiếng Việt, có trang công bố số liệu thực nghiệm đọc từ file CSV gốc, nhằm phục vụ đồ án môn học xử lý ảnh / trí tuệ nhân tạo và minh họa quy trình từ dữ liệu đến ứng dụng.

## 1.2. Mục tiêu đề tài

**Mục tiêu tổng quát:** Xây dựng hệ thống web phân tích độ chín và chất lượng (theo nhãn quy đổi) của quả chuối từ một ảnh RGB, kết hợp học sâu và xử lý ảnh số.

**Mục tiêu cụ thể:**

1. Tìm hiểu cơ sở lý thuyết CNN (năm kiến trúc), transfer learning, HSV, hình thái học, U2-Net, fusion và các độ đo đa lớp.
2. Sử dụng **ba bộ Kaggle** (chỉ ảnh RGB): huấn luyện/so sánh năm kiến trúc trên mỗi bộ; chọn mô hình triển khai theo Macro-F1.
3. Thiết kế và cài đặt pipeline: kiểm tra file → resize 224×224 → tách nền → suy luận hai mô hình → phân tích phổ màu → hợp nhất quyết định.
4. Xây dựng REST API (health, models, predict, experiments) và giao diện React gồm ba trang: Phân tích, Thực nghiệm, Thông tin.
5. Kiểm thử tích hợp: nạp mô hình, 18 ảnh mẫu, đối chiếu API với suy luận trực tiếp, đọc CSV.

## 1.3. Đối tượng và phạm vi nghiên cứu

**Đối tượng:** Ảnh RGB quả chuối (JPG, JPEG, PNG, WebP), kích thước tối đa 10 MB và 4096 px mỗi chiều.

**Dữ liệu:** Toàn bộ thực nghiệm và suy luận web dùng **ảnh RGB** (ba kênh đỏ–lục–lam). Bộ thứ hai trên Kaggle có kèm dữ liệu phổ; đồ án **không** đưa phổ vào mô hình triển khai, chỉ huấn luyện/so sánh trên nhánh ảnh RGB của bộ đó.

**Ba bộ Kaggle:**

1. *Banana Ripeness Classification Dataset* (Shahriar) — thực nghiệm **phân loại độ chín chính**.  
   https://www.kaggle.com/datasets/shahriar26s/banana-ripeness-classification-dataset
2. *Banana Ripeness RGB Images and Spectral Data* (Deeuk1985) — thực nghiệm **thêm** về độ chín từ ảnh RGB.  
   https://www.kaggle.com/datasets/deeuk1985/banana-ripeness-rgb-images-and-spectral-data
3. *Banalyzer - Banana Ripeness Classification Dataset* (Charles C R) — bài toán **chất lượng theo nhãn quy đổi**.  
   https://www.kaggle.com/datasets/iamchaarles/banalyzer-banana-ripeness-classification-dataset

**Phạm vi còn lại:**

- Phân loại **một đối tượng chuối chiếm khung hình** (ảnh đơn). Chưa phát hiện từng quả trong ảnh nhiều quả (object detection).
- Độ chín: ba lớp `xanh`, `chin`, `qua_chin`.
- Chất lượng: ba lớp quy đổi `tot`, `dom`, `thoi` từ nhãn Banalyzer (ripe → tot, overripe → dom, rotten → thoi). Đây là quy ước thực nghiệm, **chưa phải** đánh giá an toàn thực phẩm.
- Không có lớp “không phải chuối”; ảnh vật thể khác vẫn được gán một trong các lớp trên.

## 1.4. Phương pháp nghiên cứu

- **Nghiên cứu tài liệu:** năm CNN [1]–[5]; HSV và hình thái học [6]; hiệu chuẩn softmax [7]; U2-Net [12]; ba dataset [8]–[10].
- **Dữ liệu:** ba dataset Kaggle, chỉ kênh RGB, cùng giao thức chia train/val/test trong notebook.
- **Thực nghiệm học máy:** transfer learning (đóng băng backbone rồi fine-tune), chọn mô hình theo Macro-F1 trên tập test (CSV gốc).
- **Thuật toán XLA khi suy luận:** HSV, morphology, entropy, U2-Net, fusion luật.
- **Thiết kế phần mềm:** frontend / backend / mô hình; API JSON.
- **Kiểm thử:** 18 ảnh mẫu có nhãn; đối chiếu pipeline Python và HTTP.

## 1.5. Ý nghĩa khoa học và thực tiễn

**Khoa học:** Đồ án minh họa cách kết hợp CNN với đặc trưng thủ công để giảm sai khi ảnh lệch phân phối, đồng thời nêu rõ giới hạn của softmax và của việc quy đổi nhãn độ chín sang “chất lượng”.

**Thực tiễn:** Người dùng tải ảnh, nhận nhãn tiếng Việt, điểm từng lớp, thông tin tách nền và cảnh báo khi hệ thống hiệu chỉnh theo thị giác. Trang thực nghiệm công bố trung thực số liệu năm mô hình.

## 1.6. Cấu trúc báo cáo

- **Chương 1** nêu lý do, mục tiêu, phạm vi.
- **Chương 2** trình bày lý thuyết và công trình liên quan.
- **Chương 3** phân tích yêu cầu và thiết kế.
- **Chương 4** mô tả cài đặt.
- **Chương 5** báo cáo thực nghiệm và thảo luận.
- **Chương 6** kết luận và hướng phát triển.

## 1.7. Tóm tắt đặc điểm đồ án (đầu vào – dataset – thuật toán – tiền xử lý)

Mục này trả lời trực tiếp bốn câu hỏi thường gặp khi **thuyết trình / bảo vệ**: hệ thống nhận gì, dữ liệu lấy từ đâu, dùng thuật toán nào, và tiền xử lý ra sao.

### 1.7.1. Nhận về cái gì (đầu vào) và trả về cái gì (đầu ra)

**A. Khi huấn luyện (notebook trên ba dataset)**

| Nhận vào | Mô tả chi tiết |
|----------|----------------|
| Ảnh RGB | File JPG/PNG trong thư mục lớp; **không** đưa phổ (spectral) vào mạng |
| Nhãn lớp | Lấy từ **tên thư mục** (`image_dataset_from_directory`), sắp alphabet |
| Kích thước chuẩn | Resize về **224×224×3**, pixel thang **0–255** trước `preprocess_input` trong graph |
| Trọng số khởi tạo | ImageNet (transfer learning) |

| Trả ra sau train | Mô tả |
|------------------|--------|
| File `.keras` | Mô hình đã fine-tune / frozen theo `Selected_Stage` |
| File CSV | Accuracy, Macro-P/R/F1, Test_Loss, thời gian train của **5 CNN × 3 dataset** |

**B. Khi chạy website (suy luận)**

| Nhận vào từ người dùng | Ràng buộc |
|------------------------|-----------|
| **Một ảnh** JPG / JPEG / PNG / WebP | ≤ 10 MB; mỗi cạnh ≤ 4096 px; phải decode được bằng Pillow |
| Nội dung kỳ vọng | Ảnh RGB quả chuối (ưu tiên **một quả / một nải chiếm khung**) |

Hệ thống **không** nhận: điểm phổ hyperspectral, video, nhiều file cùng lúc, hay nhãn do người dùng gõ.

| Trả về cho người dùng (JSON + UI) | Ý nghĩa |
|-----------------------------------|---------|
| Nhãn **độ chín** | `xanh` / `chin` / `qua_chin` (+ tên tiếng Việt) |
| Điểm softmax 3 lớp độ chín | Điểm mạng, **không** gọi là “xác suất đã hiệu chuẩn” |
| Nhãn **chất lượng quy đổi** | `tot` / `dom` / `thoi` |
| Điểm softmax 3 lớp chất lượng | Tương tự |
| `raw_dl` | Nhãn/điểm **trước** khi fusion ghi đè |
| `bg_method`, mask tách nền | rembg (U2-Net) hoặc HSV+morphology |
| Hồ sơ màu HSV, entropy, `rotten_score` | Đặc trưng XLA giải thích được |
| Cờ `is_hybrid_corrected` + cảnh báo | Có/không hiệu chỉnh theo thị giác |
| Trang Thực nghiệm | Bảng metric đọc từ CSV gốc ba dataset |

**Tóm một câu khi thuyết trình:** *“Em nhận một ảnh RGB chuối; hệ thống trả độ chín, chất lượng quy đổi, điểm từng lớp, và giải thích tách nền / màu / có hiệu chỉnh lai hay không.”*

### 1.7.2. Link dataset (ba bộ Kaggle, chỉ dùng ảnh RGB)

| # | Vai trò trong đồ án | Tên dataset | Link đầy đủ |
|---|---------------------|-------------|-------------|
| 1 | Phân loại **độ chín chính** → model web ripeness | Banana Ripeness Classification Dataset (S.M. Shahriar) | https://www.kaggle.com/datasets/shahriar26s/banana-ripeness-classification-dataset |
| 2 | Thực nghiệm **thêm** độ chín trên ảnh RGB (bộ có spectral nhưng **em không dùng phổ**) | Banana Ripeness RGB Images and Spectral Data (Deeuk1985) | https://www.kaggle.com/datasets/deeuk1985/banana-ripeness-rgb-images-and-spectral-data |
| 3 | Bài **chất lượng theo nhãn quy đổi** → model web quality | Banalyzer - Banana Ripeness Classification Dataset (Charles C R) | https://www.kaggle.com/datasets/iamchaarles/banalyzer-banana-ripeness-classification-dataset |

**Ánh xạ nhãn khi nói chuyện:**

- Dataset 1 & 2: unripe/under-ripe → **Xanh**; ripe → **Chín**; overripe/past-ripe → **Quá chín**.
- Dataset 3: ripe → **Tốt (`tot`)**; overripe → **Đốm (`dom`)**; rotten → **Thối (`thoi`)** — đây là **quy đổi thực nghiệm**, không phải kết luận an toàn thực phẩm.

### 1.7.3. Thuật toán dùng trong đồ án

Chia hai nhóm cho dễ thuyết trình:

**Nhóm A — Học sâu (phân loại ảnh RGB)**

| Thuật toán | Dùng để làm gì | Giai đoạn |
|------------|----------------|-----------|
| CNN + Softmax + Cross-entropy | Phân 3 lớp; tối ưu nhãn | Train + suy luận |
| Transfer learning (ImageNet) | Mượn bộ lọc sẵn, đổi đầu 3 lớp | Train |
| Frozen backbone / Fine-tune | Chọn stage tốt trên validation | Train |
| **ResNet50** | Mạng **triển khai web** (độ chín + chất lượng) | Train + web |
| EfficientNetB0, InceptionV3, DenseNet121, MobileNetV3Small | So sánh công bằng trên cả 3 dataset | Train (bảng CSV) |
| Data augmentation (trong graph) | Lật, xoay, đổi sáng lúc train; tắt lúc infer | Train |

**Nhóm B — Xử lý ảnh số / lai (khi suy luận trên web)**

| Thuật toán | Dùng để làm gì |
|------------|----------------|
| Validate + decode (Pillow) | Chặn file hỏng, sai định dạng, quá dung lượng |
| Resize BICUBIC 224×224 | Khớp kích thước lúc train |
| U2-Net (rembg) | Tách quả khỏi nền studio |
| Ngưỡng HSV + opening/closing | Tách nền dự phòng (ảnh vườn) + làm sạch mask |
| Phân band HSV không chồng + entropy + rotten score | Đo xanh/vàng/nâu/thối bằng đặc trưng giải thích được |
| Hybrid decision fusion (luật ưu tiên) | Hiệu chỉnh khi CNN mâu thuẫn với XLA (OOD / softmax quá tự tin) |

**Câu chốt thuyết trình:** *“Năm CNN được so sánh; web chạy ResNet50. Song song em dùng HSV, hình thái học, U2-Net và fusion để kiểm chứng kết quả.”*

### 1.7.4. Tiền xử lý gì — thuật toán nào (chuỗi dành cho slide thuyết trình)

Thuyết trình nên tách **hai pipeline** để hội đồng không nhầm train với web.

**Pipeline 1 — Tiền xử lý khi HUẤN LUYỆN (notebook)**

```
Ảnh RGB trong thư mục lớp
  → image_dataset_from_directory (nhãn = tên thư mục, sort alphabet)
  → resize 224×224
  → augmentation (train): flip / rotate / brightness (trong graph Keras)
  → preprocess_input của từng backbone (ResNet/EfficientNet/…) trong graph
  → CNN (frozen rồi/hoặc fine-tune)
  → Softmax 3 lớp → Cross-entropy
  → Chọn best theo Macro-F1 → lưu .keras + ghi CSV
```

**Pipeline 2 — Tiền xử lý + thuật toán khi SUY LUẬN (website)**

```
Người dùng upload 1 ảnh
  → [1] Kiểm tra đuôi + dung lượng ≤ 10 MB
  → [2] Pillow verify + decode → RGB (bỏ alpha/grayscale)
  → [3] Resize BICUBIC 224×224, float32 0–255
  → [4] Tách nền: U2-Net; nếu mask quá nhỏ → HSV + morphology
  → [5] Thuật toán chính: ResNet50 độ chín + ResNet50 chất lượng (softmax)
  → [6] XLA: band HSV, entropy, rotten_score trên vùng quả
  → [7] Fusion luật (thối → đốm → xanh → chín → giữ CNN)
  → [8] Trả JSON/UI (kèm raw_dl và giải thích)
```

**Bảng nhớ nhanh “tiền xử lý gì”**

| Bước | Huấn luyện | Website |
|------|------------|---------|
| Chỉ RGB | Có | Có |
| Resize 224 | Có | Có (BICUBIC) |
| Augmentation | Có | Không |
| Tách nền U2-Net / HSV | Không (thường train trên ảnh gốc dataset) | Có |
| Phân tích HSV + fusion | Không | Có |
| Mạng phân loại | 5 CNN so sánh | ResNet50 × 2 |

Chi tiết công thức HSV, morphology, từng CNN nằm ở **Chương 2**; chuỗi thiết kế đầy đủ ở **mục 3.4 và 3.10**.

\newpage

# CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ TỔNG QUAN

## 2.1. Đặc trưng hình ảnh của quả chuối theo giai đoạn chín

Vỏ chuối thay đổi sắc tố theo quá trình chín: chlorophyll giảm, carotenoid tăng, sau đó xuất hiện đốm đường (sugar spots) màu nâu và vùng hoại tử tối. Bảng 2.1 tóm tắt đặc trưng dùng cho cả CNN (học tự động) và XLA (ngưỡng HSV, entropy).

**Bảng 2.1.** Đặc trưng màu và kết cấu theo giai đoạn

| Giai đoạn | Cảm quan | Hue HSV điển hình | Kết cấu |
|-----------|----------|-------------------|---------|
| Xanh (unripe) | Vỏ lục, đôi khi lục-lam (Blue Java) | H ≈ 62°–155° (lục); 155°–225° (lam ngọc) | Mịn, entropy thấp |
| Chín (ripe) | Vàng đều | H ≈ 24°–62°, V cao | Mịn đến hơi sần |
| Quá chín (overripe) | Vàng xen đốm nâu | Vùng nâu V trung bình | Entropy tăng |
| Thối (rotten) | Nâu đen diện rộng | V rất thấp, đốm tối | Entropy cao |

Các ngưỡng trên là **heuristic** gắn với pipeline XLA của đồ án, không phải định luật vật lý phổ quát cho mọi giống chuối và mọi thiết bị chụp.

## 2.2. Tổng hợp thuật toán sử dụng trong đồ án

Đồ án không dùng một thuật toán duy nhất. Có **hai tầng**: (A) học sâu để phân loại trên ảnh RGB 224×224; (B) xử lý ảnh cổ điển để tách nền, đo màu/kết cấu và hiệu chỉnh khi CNN mâu thuẫn với quan sát.

**Bảng 2.2.** Danh mục thuật toán — “nó làm gì” trong dự án

| Nhóm | Thuật toán | Giai đoạn | Việc cụ thể |
|------|------------|-----------|-------------|
| Học sâu | Tích chập CNN | Huấn luyện + suy luận | Học đặc trưng vỏ chuối từ pixel RGB |
| Học sâu | Softmax + cross-entropy | Huấn luyện + suy luận | Đưa 3 logit thành 3 điểm lớp; tối ưu nhãn |
| Học sâu | Transfer learning ImageNet | Huấn luyện | Mượn bộ lọc đã học trên 1,28 triệu ảnh, đổi đầu 3 lớp |
| Học sâu | Fine-tune / frozen backbone | Huấn luyện | Mở hoặc đóng trọng số backbone; CSV ghi `Selected_Stage` |
| Học sâu | ResNet50 | Huấn luyện + **web** | Mạng triển khai cho độ chín và chất lượng |
| Học sâu | EfficientNetB0, InceptionV3, DenseNet121, MobileNetV3Small | Huấn luyện | So sánh công bằng trên cả 3 dataset |
| Học sâu | Data augmentation | Huấn luyện | Lật, xoay, đổi sáng trong graph Keras; tắt khi infer |
| XLA | Resize BICUBIC | Suy luận | Đưa ảnh về 224×224 giống lúc train |
| XLA | RGB → HSV | Suy luận | Tách sắc (H) khỏi sáng (V) để đo “xanh/vàng/nâu” |
| XLA | Ngưỡng màu (`inRange`) | Suy luận | Mặt nạ pixel thuộc quả / thuộc từng band chín |
| XLA | Opening, closing (hình thái) | Suy luận | Lấp lỗ trên nải, xóa đốm nhiễu |
| XLA | U2-Net (rembg) | Suy luận | Tách quả khỏi nền studio |
| XLA | Entropy histogram + tỷ lệ đốm tối | Suy luận | Đo vỏ sần / hoại tử |
| XLA | Fusion luật (ưu tiên) | Suy luận | Ghi đè nhãn CNN khi XLA thấy thối/đốm/xanh/chín rõ |

Luồng một ảnh lúc chạy web: **validate RGB → resize → U2-Net hoặc HSV-morph tách nền → ResNet50 độ chín + ResNet50 chất lượng → HSV/entropy → fusion → JSON**.

## 2.3. Xử lý ảnh số: HSV, ngưỡng màu, hình thái học, entropy

### 2.3.1. Vì sao không phân loại trực tiếp trên RGB

Một quả chuối chín vàng dưới đèn vàng và một quả xanh dưới đèn lạnh có thể có kênh R, G gần nhau. HSV tách:

- **H (Hue):** loại màu (lục, vàng, nâu, lam ngọc).
- **S (Saturation):** màu đậm hay bạc.
- **V (Value):** sáng–tối, chịu ảnh hưởng đèn.

Đồ án chuyển RGB→HSV bằng Pillow: \(H \in [0,360]\), \(S,V \in [0,1]\). Nhánh OpenCV khi tách nền dùng thang H 0–180 (chia đôi), nên ngưỡng trong `bg_remover.py` khác số trong `color_analyzer.py` — cùng ý nghĩa vật lý, khác đơn vị.

### 2.3.2. Thuật toán phân đoạn ngưỡng màu

Với mỗi pixel, mặt nạ nhị phân:

\[
M(x,y)=\mathbf{1}\big[H_{\min}\le H\le H_{\max}\big]\cdot\mathbf{1}\big[S\ge S_{\min}\big]\cdot\mathbf{1}\big[V_{\min}\le V\le V_{\max}\big]
\]

`cv2.inRange` hiện thực đúng phép này trên ba kênh. Đồ án **hợp** (OR) các mặt nạ lục ∪ vàng ∪ nâu ∪ tối ấm để ước lượng “đây là quả chuối”, rồi **loại trừ lẫn nhau** khi thống kê độ chín: pixel đã vào `dark_heavy` không vào `dark_light`; pixel nâu không vào vàng/xanh. Nếu không loại trừ, một pixel nâu-vàng bị đếm hai lần, tỷ lệ % sẽ > 100% và luật fusion sai.

### 2.3.3. Hình thái học toán tử opening và closing

Mặt nạ sau ngưỡng thường: (i) lỗ thủng giữa nải; (ii) hạt nhiễu nền. Với phần tử cấu trúc ellipse:

- **Dilation** (giãn): pixel thành 1 nếu hàng xóm trong kernel có 1 → phình vùng.
- **Erosion** (co): pixel còn 1 chỉ khi cả kernel là 1 → teo vùng.
- **Closing** = dilation rồi erosion: lấp lỗ nhỏ bên trong quả (kernel 9×9, 2 lần).
- **Opening** = erosion rồi dilation: xóa đốm nhỏ ngoài quả (kernel 5×5, 1 lần).

Đây là thuật toán chuẩn Gonzalez–Woods [6], không học tham số.

### 2.3.4. Entropy kết cấu và tỷ lệ đốm tối

Đưa vùng quả về xám ITU-R 601: \(Y=0{,}299R+0{,}587G+0{,}114B\). Histogram 32 bin, \(p_i=h_i/\sum h\),

\[
E=-\sum_{p_i>0}p_i\log_2 p_i.
\]

Vỏ trơn: vài bin chiếm hết khối lượng → \(E\) thấp (~2,5–3,5). Vỏ đốm/thối: xám trải rộng → \(E\) cao (~4,2–5). Tỷ lệ đốm tối: phần pixel \(Y<0{,}25\times 255\) trên mask quả — dấu hiệu hoại tử.

Điểm thối tổng hợp (0–100) trong mã:

\[
R=0{,}5\,d_{\mathrm{heavy}}+0{,}3\,d_{\mathrm{spot}}+0{,}3\max(0,d_{\mathrm{brown}}-20)+5\max(0,E-3{,}2).
\]

Các hệ số là heuristic, chọn để \(R\) lớn khi vừa tối diện rộng vừa sần.

## 2.4. Tách nền bằng U2-Net và phương án dự phòng

### 2.4.1. U2-Net hoạt động như thế nào

U2-Net [12] là mạng **phát hiện vật nổi bật** (salient object): encoder–decoder lồng nhau hình chữ U, mỗi tầng lại là một mini U-Net. Đầu ra là bản đồ xác suất “pixel thuộc vật thể chính”. Thư viện rembg bọc mô hình ONNX (`u2net` nếu có file `~/.u2net/u2net.onnx`, không thì `u2net_lite`).

Trên ảnh studio (nền trắng/xám), quả chuối là vật nổi bật → mask tốt, CNN ít bị nhiễu nền.

### 2.4.2. Khi nào U2-Net thất bại và thuật toán dự phòng

Ảnh vườn: lá, thân, nải đều lục, độ nổi bật thấp. U2-Net có thể trả mask gần rỗng (nuốt mất chuối). Hệ thống đo tỷ lệ foreground; nếu quá thấp thì **bỏ mask AI**, chạy lại `segment_banana_by_color` (HSV + morphology mục 2.3). Chuỗi `bg_method` ghi `rembg` hay `hsv` để UI giải thích.

## 2.5. Học sâu cho phân loại ảnh

### 2.5.1. Phép tích chập

Một bộ lọc \(k\times k\) trượt trên feature map, nhân-cộng rồi qua ReLU \(\max(0,z)\). Lớp nông học cạnh; lớp sâu học “vỏ vàng có đốm”. Ảnh đồ án luôn **3 kênh RGB**, kích thước 224×224 — cùng cỡ ImageNet crop phổ biến.

### 2.5.2. Softmax và hàm mất mát

Ba số logit \(z_0,z_1,z_2\) (tương ứng thứ tự thư mục alphabet) thành

\[
\hat{y}_k=\frac{e^{z_k}}{\sum_{j=0}^{2}e^{z_j}}.
\]

Huấn luyện tối thiểu cross-entropy \(-\sum_k y_k\log\hat{y}_k\) với \(y\) one-hot. \(\hat{y}_k\) **không** phải xác suất đã hiệu chuẩn [7]; giao diện gọi “điểm softmax”.

### 2.5.3. Transfer learning — hai giai đoạn

1. **Frozen backbone:** khóa trọng số ImageNet, chỉ train lớp Dense 3 nơ-ron. Nhanh, ít overfit khi dataset nhỏ (bộ RGB & Spectral).
2. **Fine-tune:** mở một phần/toàn bộ backbone, learning rate nhỏ, chỉnh bộ lọc cho vỏ chuối.

Cột `Selected_Stage` trong CSV cho biết giai đoạn **thắng trên validation** được giữ để đánh giá test. Augmentation (lật, xoay, sáng) nằm trong graph; `training=False` khi suy luận để tắt tăng cường và dropout.

### 2.5.4. Tiền xử lý trong graph

`resnet50.preprocess_input` (và tương ứng từng backbone) **nằm trong file `.keras`**. Backend đưa pixel **0–255 float32**, không chia 255 — nếu chia nhầm, toàn bộ phân phối lệch và nhãn đảo loạn.

## 2.6. Năm kiến trúc CNN và cách từng mạng hoạt động

Năm mạng được train **cùng chia dữ liệu, cùng 3 lớp, cùng ảnh RGB 224×224** trên cả ba dataset, để Macro-F1 so sánh được.

**Bảng 2.4.** Năm CNN

| Mạng | Ý tưởng cốt lõi | Cách hoạt động (rút gọn) | Vai trò đồ án |
|------|-----------------|---------------------------|---------------|
| ResNet50 | Kết nối tắt | Xem 2.6.1 | **Triển khai web** (2 bài chính) |
| EfficientNetB0 | Scale đồng thời sâu–rộng–độ phân giải | 2.6.2 | Best trên dataset RGB & Spectral |
| InceptionV3 | Lọc 1×1, 3×3, 5×5 song song | 2.6.3 | Đối chứng |
| DenseNet121 | Mỗi lớp nhận mọi feature map trước | 2.6.4 | Đối chứng |
| MobileNetV3Small | Depthwise conv + NAS | 2.6.5 | Đối chứng nhẹ |

### 2.6.1. ResNet50

Mạng rất sâu dễ **suy giảm độ chính xác** vì gradient tắt. ResNet [1] học phần dư \(\mathcal{F}(x)\) rồi cộng input:

\[
y=\mathcal{F}(x)+x.
\]

Nếu \(\mathcal{F}\approx 0\), khối vẫn là ánh xạ đồng nhất — mạng không bị “càng sâu càng tệ”. ResNet50 dùng **bottleneck**: 1×1 giảm kênh → 3×3 → 1×1 tăng kênh, khoảng 25 triệu tham số. Đầu ImageNet (1000 lớp) thay bằng Dense 3 lớp.

**Vì sao web dùng ResNet50:** Macro-F1 cao nhất trên dataset độ chín chính (99,76%) và Banalyzer (93,35%).

### 2.6.2. EfficientNetB0

Tan & Le [2] không chỉ “chồng thêm lớp” mà nhân đồng thời độ sâu, độ rộng và độ phân giải theo hệ số compound. B0 là bản nhỏ nhất. Depthwise separable conv giảm phép tính. Trên bộ RGB & Spectral (ít ảnh hơn), **frozen EfficientNetB0** đạt Macro-F1 97,08%, hơn ResNet50 fine-tune — hợp lý vì ít tham số cần cập nhật, ít overfit.

Không chọn B0 làm mặc định web: hai bài cốt lõi ResNet50 thắng; thống nhất một backbone giảm RAM; nhánh RGB/Spectral không phải API mặc định.

### 2.6.3. InceptionV3

Một block Inception [3] chạy **song song** conv 1×1 (rẻ, giảm chiều), 3×3, 5×5 (xấp xỉ bằng hai 3×3) và pooling, rồi ghép kênh. Mạng nhìn quả chuối ở nhiều tỷ lệ (đốm nhỏ vs. cả trái) trong cùng tầng. Factorization giảm chi phí so với Inception gốc.

### 2.6.4. DenseNet121

Lớp \( \ell \) nhận **nối kênh** từ mọi lớp 0…ℓ−1 [4]. Feature được tái sử dụng, số tham số từng lớp nhỏ (growth rate). 121 lớp phù hợp dataset vừa. Trên bộ độ chín chính, DenseNet thắng ở chế độ *frozen_backbone* (CSV), không phải fine-tune — cho thấy backbone ImageNet đã đủ mạnh với tập đó.

### 2.6.5. MobileNetV3Small

Thiết kế cho điện thoại [5]: conv tách chiều sâu, khối nghịch đảo, SE (siêu chú ý kênh), hàm h-swish, kiến trúc tìm bằng NAS. Train nhanh nhất trên bộ độ chín chính (~145 s) nhưng Macro-F1 thấp hơn ResNet50. Đồ án giữ để chứng minh đánh đổi tốc độ–độ chính xác, không triển khai web.

## 2.7. Độ đo đánh giá mô hình

Accuracy dễ thiên lớp đa số. Macro-P, Macro-R, Macro-F1 trung bình **đều** ba lớp — mỗi giai đoạn chín/chất lượng được tính một phiếu.

**Bảng 2.3.** Một lớp, rồi lấy macro-average

\[
\mathrm{Precision}=\frac{TP}{TP+FP},\quad
\mathrm{Recall}=\frac{TP}{TP+FN},\quad
\mathrm{F1}=\frac{2PR}{P+R}.
\]

Test loss = cross-entropy trên test. Thời gian train (giây) chỉ tham khảo chi phí GPU.

## 2.8. Hợp nhất quyết định lai và softmax quá tự tin

CNN luôn phân phối 100% xác suất vào đúng 3 lớp đã học. Ảnh OOD (Blue Java, nền cây, đèn vàng) vẫn có \(\max\hat{y}\approx 1\) nhưng **sai lớp** [7].

Đồ án không dùng temperature scaling toàn cục. Thuật toán fusion **luật if–else có ưu tiên** (chi tiết thiết kế Chương 3):

1. Thối (XLA hoặc quality=thoi kèm đốm tối) → ripeness `qua_chin`, quality `thoi`.
2. Quá chín / đốm → chỉnh tương ứng.
3. Xanh rõ mà CNN ra chín/quá chín → `xanh`.
4. Vàng rõ mà CNN ra xanh → `chin`.
5. Không mâu thuẫn → giữ CNN, `is_hybrid_corrected=false`.

Sau ghi đè, điểm softmax được **phân bổ lại** (heuristic) — UI bắt buộc hiện `raw_dl` (CNN gốc) để không giấu thông tin.

## 2.9. Các công trình liên quan

Phân loại nông sản bằng CNN trên RGB phổ biến trên Kaggle. Đồ án khác notebook thuần huấn luyện ở chỗ: **ba dataset được gán vai trò rõ** (độ chín chính / độ chín RGB bổ sung / chất lượng quy đổi), **không dùng phổ khi chạy web**, và **cộng XLA + fusion**. YOLO/instance segmentation cho nhiều quả trên một ảnh nằm ngoài phạm vi.

\newpage

# CHƯƠNG 3. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG

## 3.1. Khảo sát hiện trạng và yêu cầu

Người dùng mục tiêu: sinh viên bảo vệ đồ án, người kiểm tra nhanh ảnh chuối, người xem lại bảng so sánh mô hình. Họ cần giao diện tiếng Việt, phản hồi rõ khi file sai định dạng, và **không** bị hệ thống khẳng định “an toàn để ăn”.

**Bảng 3.1.** Yêu cầu chức năng

| Mã | Mô tả |
|----|--------|
| UC01 | Tải ảnh JPG/PNG/WebP, xem trước |
| UC02 | Gửi ảnh, nhận độ chín và chất lượng |
| UC03 | Xem điểm softmax từng lớp, cờ hiệu chỉnh lai |
| UC04 | Xem tỷ lệ màu HSV, entropy, điểm thối, phương pháp tách nền |
| UC05 | Xem trạng thái backend và từng mô hình |
| UC06 | Xem bảng thực nghiệm ba dataset × năm mô hình, đánh dấu best Macro-F1 |
| UC07 | Đọc trang thông tin phạm vi, thứ tự nhãn, nguồn dữ liệu |

**Bảng 3.2.** Yêu cầu phi chức năng

| Mã | Mô tả |
|----|--------|
| NF01 | Ảnh ≤ 10 MB, cạnh ≤ 4096 px |
| NF02 | CORS chỉ origin dev local (5173, 5174, 3000) |
| NF03 | Mô hình nạp một lần lúc khởi động, tái sử dụng |
| NF04 | Thông báo lỗi tiếng Việt khi file hỏng / sai định dạng |
| NF05 | Giao diện tối, dùng được trên màn hình máy tính; mobile chưa phải mục tiêu kiểm thử bắt buộc |

## 3.2. Mô hình use case

**Hình 3.1.** Use case (mô tả)

Tác nhân **Người dùng** liên kết UC01–UC07. Tác nhân **Hệ thống file** cung cấp `.keras` và CSV. Không có tác nhân thanh toán hay tài khoản: đồ án chạy local, không đăng nhập.

## 3.3. Kiến trúc tổng thể

**Hình 3.2.** Kiến trúc ba lớp

```
[Trình duyệt React :5173]
        |  HTTP JSON / multipart
[FastAPI :8000]
        |  load 1 lần
[Keras ResNet50 ripeness] [Keras ResNet50 quality]
        |
[OpenCV + NumPy HSV/XLA] [rembg U2-Net tùy chọn]
        |
[results/*.csv] [models/*.keras] [samples/]
```

Nguyên tắc:

- Frontend không chạy TensorFlow.
- Backend không tin đuôi file: decode bằng Pillow, `verify()` rồi load lại.
- Trang Thực nghiệm **không** bịa số: đọc CSV, nhân 100 **một lần** khi hiện phần trăm.

## 3.4. Thiết kế pipeline suy luận lai

**Hình 3.3.** Các bước `/api/predict`

1. Đọc bytes, kiểm tra dung lượng và phần mở rộng.
2. Decode RGB, resize BICUBIC 224×224, `float32` 0–255.
3. Tách nền → ảnh đưa vào CNN và vào phân tích màu.
4. Softmax ripeness (3 lớp) và quality (3 lớp).
5. Phân tích HSV + entropy trên mask quả.
6. Fusion theo mức ưu tiên: thối → quá chín/đốm → xanh bị gán chín → chín bị gán xanh → đồng thuận.
7. JSON: nhãn hiển thị, điểm, `raw_dl`, `ood_analysis`, `bg_method`.

## 3.5. Thiết kế mô-đun tách nền

**Hình 3.4.** Hai giai đoạn

- **Giai đoạn 1:** rembg (u2net nếu có file local `~/.u2net/u2net.onnx`, không thì u2net_lite).
- **Giai đoạn 2:** nếu mask AI mất quả (foreground quá nhỏ — điển hình ảnh ngoài trời), dùng `segment_banana_by_color`: hợp mặt nạ lục, vàng, nâu, tối ấm; closing 9×9, opening 5×5.

Đầu ra: ảnh RGB đã loại nền (hoặc passthrough), mask boolean, chuỗi `bg_method` để UI giải thích.

## 3.6. Thiết kế mô-đun phân tích phổ màu

**Hình 3.5.** Các band HSV (không chồng)

| Band | Ý nghĩa | Điều kiện chính (rút gọn) |
|------|---------|---------------------------|
| dark_heavy | Hoại tử / gần đen | V < 0,22 hoặc nâu tối V ≤ 0,30 |
| dark_light | Đốm đồi mồi | H nâu, V ∈ (0,22; 0,52], trừ dark_heavy |
| green | Chưa chín lục | H 62–155 |
| cyan | Blue Java / phủ sáp | H 155–225 |
| yellow | Chín vàng | H 24–62, trừ nâu và xanh |

Điểm thối (0–100):

\[
R = 0{,}5\,d_h + 0{,}3\,d_s + 0{,}3\max(0, d_b-20) + 5\max(0, E-3{,}2)
\]

với \(d_h, d_s, d_b\) là phần trăm dark_heavy, dark_spot, dark_brown; \(E\) là entropy.

Luật verdict: thối rõ, quá chín, xanh, chín, hoặc “nghiêng về” lớp có tỷ lệ band lớn nhất khi không luật nào khớp.

Điều kiện bảo vệ: không gắn thối nếu tỷ lệ xanh ≥ 20% (tránh nhầm cuống tối trên chuối xanh).

## 3.7. Thiết kế hợp nhất quyết định

**Hình 3.6.** Ưu tiên

1. **Thối xác nhận:** `is_clearly_rotten` **hoặc** (quality = thoi **và** (nâu ≥ 25% hoặc đốm tối ≥ 18% hoặc \(R\) ≥ 35)). Ghi đè ripeness → `qua_chin`, quality → `thoi` nếu chưa đúng.
2. **Quá chín / đốm:** XLA overripe **hoặc** (quality = dom và nâu ≥ 20%). Ghi đè ripeness xanh/chín → quá chín; quality tot → đốm.
3. **Xanh:** XLA unripe trong khi CNN ra chín/quá chín → `xanh`.
4. **Chín:** XLA ripe trong khi CNN ra xanh → `chin`.
5. Còn lại: giữ nguyên CNN, `is_hybrid_corrected = false`.

Điểm softmax sau ghi đè được **phân bổ lại** (lớp chọn nhận confidence heuristic, các lớp còn chia phần dư). Đây là điểm hiển thị, không còn là softmax gốc — UI phải cho xem `raw_dl`.

## 3.8. Thiết kế API

**Bảng 3.3.** Endpoint

| Phương thức | Đường dẫn | Mô tả |
|-------------|-----------|--------|
| GET | `/api/health` | Backend chạy, từng model ready/error |
| GET | `/api/models` | Cấu hình và trạng thái model |
| POST | `/api/predict` | Multipart file → JSON kết quả |
| GET | `/api/experiments` | Parse 3 CSV, `best_model_by_macro_f1` |

Mã lỗi: 400 đọc file thất bại; 422 ảnh không hợp lệ; 500 lỗi suy luận.

## 3.9. Thiết kế giao diện người dùng

Ba trang, thanh điều hướng chung, footer disclaimer.

- **Phân tích:** dropzone, preview, nút phân tích, khối kết quả hai cột độ chín / chất lượng, hộp cảnh báo hybrid, chi tiết XLA.
- **Thực nghiệm:** tab theo dataset, bảng metric, badge BEST theo Macro-F1.
- **Thông tin:** phạm vi, status model realtime, kiến trúc, thứ tự nhãn, nguồn Kaggle.

## 3.10. Quy ước nhãn và tiền xử lý

Keras `image_dataset_from_directory` sắp thư mục **theo alphabet**. Notebook huấn luyện xác nhận:

**Bảng 3.4.** Index softmax

| Model | [0] | [1] | [2] |
|-------|-----|-----|-----|
| Ripeness | chin | qua_chin | xanh |
| Quality | dom | thoi | tot |

Sai thứ tự nhãn sẽ đảo toàn bộ ý nghĩa hệ thống — đây là rủi ro đã được kiểm soát bằng cấu hình tường minh trong `model_config.py`.

\newpage

# CHƯƠNG 4. CÀI ĐẶT HỆ THỐNG

## 4.1. Môi trường và công nghệ

**Bảng 4.1.** Công nghệ

| Thành phần | Công nghệ | Vai trò |
|------------|-----------|---------|
| Ngôn ngữ backend | Python 3.11 | Suy luận, API |
| Web API | FastAPI + Uvicorn | REST |
| Học sâu | TensorFlow 2.16.1, Keras 3.15.1 | Load `.keras` |
| XLA | NumPy, Pillow, OpenCV | Màu, morphology, resize |
| Tách nền AI | rembg (U2-Net) | Salient mask |
| Frontend | React 18, Vite 5 | SPA |
| Dữ liệu | CSV UTF-8 | Công bố thực nghiệm |

`KERAS_BACKEND=tensorflow` và `TF_CPP_MIN_LOG_LEVEL=2` được đặt trước khi import Keras.

## 4.2. Cấu trúc thư mục dự án

**Hình 4.1.** Cấu trúc (rút gọn)

```
banana-ai-web/
  backend/
    main.py              # FastAPI
    model_config.py      # Nhãn, đường dẫn
    model_loader.py      # Nạp một lần
    image_processor.py   # Validate + resize
    bg_remover.py        # rembg + HSV
    color_analyzer.py    # HSV, entropy, OOD
    inference.py         # Fusion
  frontend/src/
    App.jsx, api.js
    pages/AnalyzePage.jsx, ExperimentsPage.jsx, AboutPage.jsx
  models/                # File .keras
  results/               # 3 file CSV
  samples/               # 18 ảnh + labels.json
  notebooks/             # Huấn luyện gốc
  test_reports/          # Báo cáo kiểm thử tích hợp
  bao_cao/               # Báo cáo đồ án (file này)
```

## 4.3. Nạp và quản lý mô hình

Lớp `ModelLoader`: nếu `enabled is False` thì `disabled`; nếu thiếu file thì `file_missing`; load bằng `tf.keras.models.load_model`; so sánh `output_shape[-1]` với số phần tử `class_names`. `predict` thêm batch dimension, `training=False`.

`initialize_models` chạy trong `lifespan` FastAPI: nạp hết cấu hình khi server start, tránh tải 25M tham số mỗi request.

## 4.4. Cài đặt xử lý ảnh đầu vào

`validate_and_decode`:

- Từ chối > 10 MB, đuôi ngoài {`.jpg`, `.jpeg`, `.png`, `.webp`}.
- `Image.verify()` phát hiện file hỏng; mở lại stream vì verify đóng file.
- Convert RGB (RGBA, L, P).
- Resize 224×224 BICUBIC — cùng interpolation với `image_dataset_from_directory` lúc train, giảm lệch phân phối kích thước.

## 4.5. Cài đặt tách nền

`bg_remover.segment_banana_by_color` dùng `cv2.inRange` trên HSV OpenCV (H 0–180). Các dải: lục [30,88], vàng [16,36], nâu [5,35] V thấp, tối ấm [0,35] và [160,180]. Morph close/open ellipse.

`remove_background` gọi rembg trước, đánh giá mask, fallback XLA.

## 4.6. Cài đặt phân tích màu và OOD

`analyze_banana_colors` tính phần trăm band, `rotten_score`, các cờ `is_clearly_rotten`, `is_overripe`, `is_unripe`, `is_ripe`.

`evaluate_ood_and_contradiction` so nhãn CNN với verdict XLA, xuất thông tin cho UI (cảnh báo mâu thuẫn, hồ sơ màu).

## 4.7. Cài đặt hợp nhất quyết định

Toàn bộ luật mục 3.7 nằm trong `predict_image` (`inference.py`). Mỗi lần ghi đè gán `cv_assisted_recommendation` hoặc `cv_quality_correction` — chuỗi tiếng Việt để báo cáo và UI dùng chung một nguồn sự thật.

## 4.8. Cài đặt backend FastAPI

CORS cho localhost. `/api/experiments` parse CSV bằng `csv.DictReader`, ép float khi được, chọn `best_model_by_macro_f1` theo max cột `Macro_F1`. File thiếu → `file_missing`, không crash server.

## 4.9. Cài đặt frontend React

`api.js` gọi `http://localhost:8000`. AnalyzePage validate type/size phía client trước khi POST. Hiển thị điểm bằng thanh, phân biệt nhãn sau fusion và `raw_dl`. ExperimentsPage nhân 100 một lần cho cột tỷ lệ. AboutPage poll `/api/health`.

## 4.10. An toàn sử dụng và giới hạn công bố

Footer và trang Thông tin nêu: mô hình không kết luận an toàn thực phẩm; điểm không phải xác suất hiệu chuẩn; nhãn chất lượng là quy đổi. Đồ án local không có xác thực người dùng; không triển khai production trong phạm vi này.

\newpage

# CHƯƠNG 5. THỰC NGHIỆM VÀ ĐÁNH GIÁ

## 5.1. Ba bộ dữ liệu Kaggle (chỉ dùng ảnh RGB)

Em sử dụng **ba dataset công khai**. Cả ba đều có ảnh màu; hệ thống train và suy luận **chỉ nhận RGB**. Bộ thứ hai có file phổ (spectral) đi kèm trên Kaggle — đồ án **không** đưa phổ vào mạng, không yêu cầu máy quét hyperspectral khi chạy website.

**Bảng 5.1.** Vai trò từng bộ

| # | Tên dataset | Tác giả Kaggle | URL | Bài toán trong đồ án | Nhãn dùng | Kênh đưa vào CNN |
|---|-------------|----------------|-----|----------------------|-----------|------------------|
| 1 | Banana Ripeness Classification Dataset | S.M. Shahriar (`shahriar26s`) | https://www.kaggle.com/datasets/shahriar26s/banana-ripeness-classification-dataset | **Thực nghiệm phân loại độ chín chính** | `xanh` / `chin` / `qua_chin` (từ unripe / ripe / overripe) | RGB 224×224 |
| 2 | Banana Ripeness RGB Images and Spectral Data | Deeuk1985 (`deeuk1985`) | https://www.kaggle.com/datasets/deeuk1985/banana-ripeness-rgb-images-and-spectral-data | **Thực nghiệm thêm** độ chín từ ảnh RGB | Cùng ba lớp độ chín; notebook map under-ripe → xanh, ripe → chín, past-ripe → quá chín | **Chỉ RGB** (bỏ qua phổ) |
| 3 | Banalyzer - Banana Ripeness Classification Dataset | Charles C R (`iamchaarles`) | https://www.kaggle.com/datasets/iamchaarles/banalyzer-banana-ripeness-classification-dataset | **Chất lượng theo nhãn quy đổi** | `tot` / `dom` / `thoi` ← ripe / overripe / rotten | RGB 224×224 |

Giấy phép do trang Kaggle công bố: bộ (1) Apache 2.0; bộ (3) MIT; bộ (2) theo trang dataset tại thời điểm tải.

### 5.1.1. Dataset 1 — độ chín chính

Đây là bộ **chọn mô hình web cho nhánh ripeness**. Năm CNN train cùng split. ResNet50 fine-tune thắng Macro-F1 99,76% → file `banana-ripeness-classification-dataset_ResNet50.keras`. Thứ tự softmax alphabet: `[chin, qua_chin, xanh]`. Chín ảnh mẫu `samples/do_chin/` lấy từ thư mục test của bộ này.

### 5.1.2. Dataset 2 — độ chín RGB bổ sung

Mục tiêu: kiểm tra thuật toán CNN có **lặp lại được** trên nguồn ảnh khác, vẫn chỉ RGB. Tập này nhỏ hơn (thời gian train trên CSV chỉ ~36–124 s). EfficientNetB0 *frozen_backbone* thắng 97,08% F1; ResNet50 đứng thứ tư. Kết luận: **không có một CNN nào thắng mọi dataset**. File `.keras` RGB/Spectral có thể nạp thêm, không phải cặp mặc định `/api/predict`.

### 5.1.3. Dataset 3 — chất lượng quy đổi (Banalyzer)

Nhãn gốc là độ chín/thối; notebook **đổi tên** ripe→tot, overripe→dom, rotten→thoi để đặt bài “chất lượng”. Quy đổi này **không** được kiểm định cảm quan độc lập. ResNet50 fine-tune thắng Macro-F1 93,35% → `banalyzer-..._ResNet50.keras`. Softmax: `[dom, thoi, tot]`. Chín ảnh `samples/chat_luong_quy_doi/` từ test set bộ này.

### 5.1.4. Ảnh kiểm thử chức năng

Mười tám file trong `samples/` tải nguyên byte, chỉ đổi tên; SHA-256 trong `labels.json`. **Chưa** chứng minh chúng nằm ngoài train của notebook. Không dùng bảng 18 ảnh để công bố Accuracy mới.

## 5.2. Kết quả huấn luyện năm kiến trúc

Số liệu dưới đây lấy nguyên từ CSV trong `results/`. Phần trăm = giá trị gốc × 100, làm tròn hiển thị.

### 5.2.1. Dataset 1 — độ chín chính (Banana Ripeness Classification Dataset)

**Bảng 5.2.** Tập test (cột Macro_F1 dùng chọn mô hình)

| Mô hình | Stage | Accuracy | Macro-P | Macro-R | Macro-F1 | Test loss | Thời gian (s) |
|---------|-------|----------|---------|---------|----------|-----------|----------------|
| **ResNet50** | fine_tuned | 99,74% | 99,78% | 99,75% | **99,76%** | 0,0067 | 674,5 |
| EfficientNetB0 | fine_tuned | 99,31% | 99,31% | 99,43% | 99,37% | 0,0260 | 414,8 |
| InceptionV3 | fine_tuned | 99,14% | 99,15% | 99,27% | 99,21% | 0,0240 | 407,1 |
| DenseNet121 | frozen_backbone | 98,54% | 98,59% | 98,74% | 98,66% | 0,0445 | 740,3 |
| MobileNetV3Small | fine_tuned | 98,46% | 98,53% | 98,64% | 98,58% | 0,0359 | 145,3 |

### 5.2.2. Dataset 3 — chất lượng quy đổi (Banalyzer)

**Bảng 5.3.**

| Mô hình | Stage | Accuracy | Macro-P | Macro-R | Macro-F1 | Test loss | Thời gian (s) |
|---------|-------|----------|---------|---------|----------|-----------|----------------|
| **ResNet50** | fine_tuned | 93,33% | 93,63% | 93,33% | **93,35%** | 0,1402 | 211,9 |
| InceptionV3 | fine_tuned | 93,33% | 93,66% | 93,33% | 93,17% | 0,2207 | 291,7 |
| EfficientNetB0 | fine_tuned | 89,33% | 90,02% | 89,33% | 88,92% | 0,2600 | 274,3 |
| DenseNet121 | fine_tuned | 89,33% | 90,02% | 89,33% | 88,92% | 0,2452 | 314,7 |
| MobileNetV3Small | fine_tuned | 88,67% | 89,39% | 88,67% | 88,18% | 0,2534 | 242,3 |

Accuracy ResNet50 và InceptionV3 trùng 93,33%; Macro-F1 của ResNet50 cao hơn nên được chọn.

### 5.2.3. Dataset 2 — độ chín từ ảnh RGB (bộ RGB Images and Spectral Data)

*Chỉ train trên ảnh RGB của bộ này; không dùng kênh phổ.*

**Bảng 5.4.**

| Mô hình | Stage | Accuracy | Macro-F1 |
|---------|-------|----------|----------|
| **EfficientNetB0** | frozen_backbone | 97,14% | **97,08%** |
| DenseNet121 | fine_tuned | 95,24% | 95,39% |
| MobileNetV3Small | frozen_backbone | 95,24% | 95,16% |
| ResNet50 | fine_tuned | 94,29% | 94,41% |
| InceptionV3 | fine_tuned | 88,57% | 87,93% |

## 5.3. Lựa chọn mô hình triển khai

- Web mặc định: **ResNet50** train trên **dataset 1** (độ chín) + **ResNet50** train trên **dataset 3** (chất lượng quy đổi).
- Dataset 2: công bố bảng so sánh năm CNN; mô hình RGB có thể nạp thêm, không bắt buộc cho `/api/predict`.
- Không chọn EfficientNetB0 làm mặc định web dù thắng trên dataset 2: hai bài cốt lõi ResNet50 thắng; một backbone giảm RAM.

## 5.4. Kiểm thử tích hợp hệ thống

Môi trường: Windows, Python 3.11, TF 2.16.1, Keras 3.15.1 (file `.keras` lưu bằng Keras 3.13.2).

- Nạp ripeness và quality: input `(None, 224, 224, 3)`, output `(None, 3)` — thành công.
- GET `/api/health`, `/api/models`, `/api/experiments` — thành công; experiments 3 dataset × 5 mô hình, best đúng bảng 5.2–5.4.
- Frontend: upload zone, trạng thái “Sẵn sàng”, tab thực nghiệm, disclaimer footer — hoạt động (kiểm thử ngày 22/10/2026).

## 5.5. Kiểm thử 18 ảnh mẫu

**Bảng 5.5.** Tóm tắt (chi tiết Phụ lục C)

| Nhóm | Số ảnh | Khớp nhãn tham chiếu |
|------|--------|----------------------|
| Độ chín (xanh, chín, quá chín) | 9 | 9/9 |
| Chất lượng (tốt, đốm, thối) | 9 | 9/9 |
| **Tổng** | **18** | **18/18** |

Điểm softmax trên nhóm độ chín thường ~100%; nhóm thối có mẫu thấp nhất khoảng 89,5% (`thoi_03.png`) vẫn đúng lớp. Kết quả chỉ chứng minh **đường ống không gán nhãn ngược** trên mẫu này, không chứng minh generalization.

## 5.6. Nhất quán suy luận trực tiếp và API

Cùng ảnh `chin_01.jpg`: pipeline Python và POST `/api/predict` cho ripeness `chin` ≈ 99,99%, quality `tot` ≈ 97,66%. Sai khác < 0,1% do làm tròn float32. Ảnh `xanh_01.jpg`, `qua_chin_01.jpg` khớp lớp khi chạy trực tiếp.

## 5.7. Thảo luận kết quả

1. Macro-F1 độ chín gần bão hòa trên tập test nguồn mở — cần cảnh giác **rò rỉ train/test** hoặc ảnh studio đồng nhất. Đồ án không tuyên bố “99,76% trên mọi ảnh thực tế”.
2. Bài chất lượng khó hơn (~93% F1): đốm và thối gần nhau về màu, nhãn quy đổi từ ripe/overripe/rotten có thể không trùng cảm quan “tốt/đốm/thối” của người Việt.
3. Hybrid fusion nhắm đúng điểm yếu CNN trên OOD; đồng thời có rủi ro **ghi đè nhãn đúng** nếu ngưỡng HSV kích hoạt nhầm (ví dụ bóng tối). Luật `unripe_total_pct < 20` khi gắn thối là biện pháp giảm rủi ro, chưa tối ưu bằng tập validation riêng cho fusion.
4. Tách nền kép là cần thiết: rembg tốt studio, HSV tốt vườn.

## 5.8. Hạn chế của thực nghiệm

- 18 ảnh không đủ thống kê; có thể trùng phân phối train.
- Chưa kiểm thử có hệ thống: file > 10 MB trên UI, ảnh hỏng trên UI, viewport điện thoại.
- Chưa có ma trận nhầm lẫn trên tập ảnh tự chụp.
- Model RGB/Spectral chưa phải nhánh mặc định đã kiểm chứng nhãn đầy đủ.

\newpage

# CHƯƠNG 6. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 6.1. Kết luận

Đồ án đã hoàn thành hệ thống BananaAI trên **ba bộ Kaggle**, **chỉ dùng ảnh RGB**: dataset 1 cho độ chín chính, dataset 2 cho thực nghiệm độ chín bổ sung, dataset 3 cho chất lượng quy đổi. Năm CNN được so sánh; ResNet50 triển khai web; XLA (HSV, morphology, U2-Net, entropy) và fusion hỗ trợ suy luận. Hệ thống **không** thay thế kiểm định vệ sinh an toàn thực phẩm.

## 6.2. Những điểm đã đạt được

1. Trình bày chi tiết cách hoạt động của CNN (ResNet, EfficientNet, Inception, DenseNet, MobileNet), transfer learning, HSV, morphology, U2-Net, entropy và fusion.
2. Gán đúng vai trò ba dataset Kaggle; so sánh năm kiến trúc bằng CSV gốc; triển khai ResNet50 cho dataset 1 và 3.
3. Cài đặt tách nền AI + dự phòng XLA; phổ màu không chồng; fusion có ưu tiên.
4. API FastAPI và UI React ba trang.
5. Kiểm thử tích hợp: nạp model, 18/18 mẫu, API khớp pipeline, đọc experiments.

## 6.3. Hạn chế còn lại

Phạm vi ảnh đơn; không có lớp từ chối phi-chuối; nhãn chất lượng là quy đổi; fusion heuristic; chưa đánh giá độc lập trên ảnh hiện trường quy mô lớn.

## 6.4. Hướng phát triển

1. Thu thập ảnh tự chụp (nhiều giống, ánh sáng, nền) làm tập test độc lập; vẽ confusion matrix trước/sau fusion.
2. Thêm detector (YOLO) cho nhiều quả trên một khung hình.
3. Lớp “không phải chuối” hoặc ngưỡng OOD (Mahalanobis / energy score) thay vì luôn gán 3 lớp.
4. Hiệu chuẩn nhiệt (temperature scaling) trên validation, tách biệt với điểm fusion.
5. Xác minh và (nếu đúng) bật nhánh RGB/Spectral; cân nhắc ensemble.
6. Đóng gói Docker; kiểm thử responsive; có thể xuất báo cáo PDF từng lần phân tích.

\newpage

# TÀI LIỆU THAM KHẢO

[1] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2016, pp. 770–778.

[2] M. Tan and Q. V. Le, “EfficientNet: Rethinking model scaling for convolutional neural networks,” in *Proc. Int. Conf. Mach. Learn. (ICML)*, 2019, pp. 6105–6114.

[3] C. Szegedy, V. Vanhoucke, S. Ioffe, J. Shlens, and Z. Wojna, “Rethinking the Inception architecture for computer vision,” in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2016, pp. 2818–2826.

[4] G. Huang, Z. Liu, L. van der Maaten, and K. Q. Weinberger, “Densely connected convolutional networks,” in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2017, pp. 4700–4708.

[5] A. Howard et al., “Searching for MobileNetV3,” in *Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV)*, 2019, pp. 1314–1324.

[6] R. C. Gonzalez and R. E. Woods, *Digital Image Processing*, 4th ed. New York, NY, USA: Pearson, 2018.

[7] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, “On calibration of modern neural networks,” in *Proc. Int. Conf. Mach. Learn. (ICML)*, 2017, pp. 1321–1330.

[8] S. M. Shahriar, “Banana Ripeness Classification Dataset.” [Online]. Available: https://www.kaggle.com/datasets/shahriar26s/banana-ripeness-classification-dataset

[9] Deeuk1985, “Banana Ripeness RGB Images and Spectral Data.” [Online]. Available: https://www.kaggle.com/datasets/deeuk1985/banana-ripeness-rgb-images-and-spectral-data

[10] Charles C R, “Banalyzer - Banana Ripeness Classification Dataset.” [Online]. Available: https://www.kaggle.com/datasets/iamchaarles/banalyzer-banana-ripeness-classification-dataset

[11] O. Ronneberger, P. Fischer, and T. Brox, “U-Net: Convolutional networks for biomedical image segmentation,” in *Med. Image Comput. Comput. Assist. Interv. (MICCAI)*, 2015, pp. 234–241.

[12] X. Qin, Z. Zhang, C. Huang, M. Dehghan, O. R. Zaiane, and M. Jagersand, “U2-Net: Going deeper with nested U-structure for salient object detection,” *Pattern Recognition*, vol. 106, 2020, Art. no. 107404.

[13] FastAPI documentation. [Online]. Available: https://fastapi.tiangolo.com/

[14] TensorFlow / Keras documentation. [Online]. Available: https://www.tensorflow.org/

[15] React documentation. [Online]. Available: https://react.dev/

\newpage

# PHỤ LỤC A. DANH SÁCH API

**GET `/api/health`**  
Trả `status`, `backend`, `any_model_ready`, mảng `models` (model_id, status, input_shape, error).

**GET `/api/models`**  
Danh sách cấu hình kèm trạng thái nạp.

**POST `/api/predict`**  
Body: `multipart/form-data`, field `file`.  
Response: `filename`, `image_shape`, `result.ripeness`, `result.quality`, `result.ood_analysis`, `bg_removed`, `bg_method`.

**GET `/api/experiments`**  
Mảng experiments: dataset, task, filename, status, best_model_by_macro_f1, rows.

\newpage

# PHỤ LỤC B. LỆNH KHỞI ĐỘNG HỆ THỐNG (WINDOWS)

Terminal 1 — backend (thư mục `banana-ai-web`):

```powershell
.venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Terminal 2 — frontend:

```powershell
cd frontend
npm run dev
```

Trình duyệt: `http://localhost:5173`. Backend: `http://localhost:8000/docs` (Swagger).

\newpage

# PHỤ LỤC C. BẢNG KẾT QUẢ 18 ẢNH MẪU

Nguồn: `test_reports/integration_test_report.md`, ngày 22/10/2026.

### C.1. Độ chín

| File | Nhãn tham chiếu | Dự đoán | Điểm | Khớp |
|------|-----------------|---------|------|------|
| chin_01.jpg | chin | chin | 100% | Có |
| chin_02.jpg | chin | chin | 100% | Có |
| chin_03.jpg | chin | chin | 100% | Có |
| qua_chin_01.jpg | qua_chin | qua_chin | 100% | Có |
| qua_chin_02.jpg | qua_chin | qua_chin | 100% | Có |
| qua_chin_03.jpg | qua_chin | qua_chin | 100% | Có |
| xanh_01.jpg | xanh | xanh | 100% | Có |
| xanh_02.jpg | xanh | xanh | 100% | Có |
| xanh_03.jpg | xanh | xanh | 100% | Có |

### C.2. Chất lượng quy đổi

| File | Nhãn tham chiếu | Dự đoán | Điểm | Khớp |
|------|-----------------|---------|------|------|
| dom_01.png | dom | dom | 99,3% | Có |
| dom_02.png | dom | dom | 98,0% | Có |
| dom_03.png | dom | dom | 97,8% | Có |
| thoi_01.png | thoi | thoi | 100% | Có |
| thoi_02.png | thoi | thoi | 99,9% | Có |
| thoi_03.png | thoi | thoi | 89,5% | Có |
| tot_01.png | tot | tot | 100% | Có |
| tot_02.png | tot | tot | 100% | Có |
| tot_03.png | tot | tot | 100% | Có |

\newpage

# PHỤ LỤC D. ÁNH XẠ NHÃN CHẤT LƯỢNG

Theo notebook thực nghiệm trên Banalyzer:

| Nhãn nguồn dataset | Nhãn hệ thống | Tên hiển thị |
|--------------------|---------------|--------------|
| ripe | tot | Tốt |
| overripe | dom | Đốm |
| rotten | thoi | Thối |

Quy đổi phục vụ huấn luyện và demo. **Không** suy ra “ripe luôn an toàn” hay “overripe luôn chỉ là đốm”. Không sử dụng bảng này cho kết luận y tế hoặc an toàn thực phẩm.

\newpage

# PHỤ LỤC E. ÁNH XẠ THUẬT TOÁN — MÔ-ĐUN MÃ NGUỒN

| Thuật toán | File chính | Dataset liên quan |
|------------|------------|-------------------|
| Transfer learning 5 CNN | `notebooks/*.ipynb` | Cả 3 bộ Kaggle, chỉ RGB |
| ResNet50 suy luận độ chín | `backend/inference.py`, model dataset 1 | [8] |
| ResNet50 suy luận chất lượng | `backend/inference.py`, model dataset 3 | [10] |
| So sánh EfficientNet/Inception/DenseNet/MobileNet | `results/*.csv` | [8], [9], [10] |
| Resize BICUBIC, validate RGB | `backend/image_processor.py` | Mọi ảnh upload |
| U2-Net tách nền | `backend/bg_remover.py` | Suy luận web |
| HSV + morphology tách nền dự phòng | `backend/bg_remover.py` | Suy luận web |
| HSV band, entropy, rotten score | `backend/color_analyzer.py` | Suy luận web |
| Fusion luật | `backend/inference.py` | Suy luận web |
| Đọc CSV thực nghiệm | `backend/main.py` `/api/experiments` | Cả 3 bộ |

---

*Hết báo cáo.*
