# BÁO CÁO PHÂN TÍCH VÀ HƯỚNG GIẢI QUYẾT TOÀN DIỆN
## Hiện Tượng Mô Hình AI Nhận Diện Sai Ảnh Chuối Xanh Lạ (Blue Java) Thành "Quá Chín 100%"

---

## 1. Mô Tả Hiện Tượng & Dữ Liệu Kiểm Thử
- **Mẫu ảnh kiểm thử:** Nải chuối giống lạ (Blue Java / chuối vỏ ánh xanh lam ngọc, phủ phấn sáp bạc), quả chuối non/chưa chín, cuống còn tươi, được cầm trên tay ngoài tự nhiên.
- **Kết quả mô hình ResNet50:**
  - `Độ chín:` **Quá chín (100.0%)** (Chín: 0.0%, Xanh: 0.0%).
  - `Chất lượng quy đổi:` Tốt (99.5%).
- **Đánh giá:** Mô hình nhận diện **sai hoàn toàn** về mặt độ chín (chuối chưa chín nhưng dự đoán quá chín với độ tự tin cực đại 100%).

---

## 2. Phân Tích Nguyên Nhân Cốt Lõi (Root Cause Analysis)

### 2.1. Lệch phân phối dữ liệu (Out-of-Distribution - OOD / Covariate Shift)
- Tập dữ liệu huấn luyện (`Banana Ripeness Classification Dataset`) chủ yếu bao gồm giống chuối tiêu/Cavendish thông thường với 3 trạng thái rõ rệt:
  - `xanh`: Chuối xanh lá cây rực rỡ (Pure Green, Hue ~ 65°–130°).
  - `chin`: Chuối vàng tươi (Pure Yellow, Hue ~ 40°–60°).
  - `qua_chin`: Chuối vỏ màu sẫm xám, nâu thâm, đốm đen lớn.
- Quả chuối trong ảnh kiểm thử là giống **Blue Java** (hoặc chuối có sắc tố ánh lam bạc). Lớp phấn sáp mờ (glaucous bloom) và sắc thái xanh lục pha lam ngọc (Cyan-Green, Hue ~ 140°–210°) không có trong tập dữ liệu huấn luyện ban đầu. Các kênh màu RGB rơi vào vùng xám-lạnh, có khoảng cách đặc trưng (feature distance) gần với các vùng tối/xám của chuối quá chín hơn là màu xanh chuối tiêu.

### 2.2. Hiện tượng Quá tự tin của Mạng Nơ-ron Sâu (Softmax Overconfidence)
- Hàm Softmax $\sigma(z)_i = \frac{e^{z_i}}{\sum_j e^{z_j}}$ có đặc tính khuếch đại hàm mũ logit lớn nhất và luôn ép tổng xác suất về 1.
- Khi gặp dữ liệu OOD (nằm ngoài không gian phân phối đã học), mạng nơ-ron sâu không có khả năng tự biết "tôi không biết". Chỉ cần một trọng số trong lớp Fully Connected cuối cùng nhạy cảm với tông màu lạnh hoặc đốm sẫm ở đầu quả chuối, logit của `qua_chin` tăng nhẹ sẽ khiến điểm Softmax bị đẩy vọt lên **100%**.

### 2.3. Yếu tố gây nhiễu môi trường (Background & Shortcut Learning)
- Ảnh có **bàn tay người** cầm cuống chuối (tông màu da cam/nâu) và lá cây nền xung quanh. Mô hình ResNet50 phân loại toàn ảnh (global pooling) dễ bị ảnh hưởng bởi các đặc trưng màu sắc của bàn tay và các vùng bóng râm đổ bóng.

---

## 3. Các Hướng Giải Quyết Tốt Nhất & Đã Triển Khai Trong Hệ Thống

Chúng tôi triển khai giải pháp theo cấu trúc **2 tầng**: Tầng ứng dụng trực tiếp (đã tích hợp vào web) và Tầng nâng cấp mô hình học sâu (cho hướng phát triển đề tài).

### TẦNG 1: Giải Pháp Kỹ Thuật Trực Tiếp Đã Triển Khai (Hybrid AI & Computer Vision Verification)

Chúng tôi đã xây dựng và tích hợp mô-đun **Thị Giác Máy Tính Phân Tích Phổ Màu HSV (`backend/color_analyzer.py`)** song song với Deep Learning:

1. **Phân tích phổ màu thực tế:**
   - Chuyển đổi ảnh sang không gian màu HSV & tách biệt 4 phổ màu then chốt:
     - Sắc xanh lục chuẩn (Standard Green Hue: 65°–160°).
     - Sắc xanh lam ngọc / Blue Java (Cyan-Blue Hue: 140°–225°).
     - Sắc vàng chín (Yellow Hue: 35°–65°).
     - Sắc nâu thâm / đen nẫu (Dark / Brown).
2. **Bộ kiểm chứng mâu thuẫn nhận thức (Contradiction & OOD Detector):**
   - Khi mô hình Deep Learning dự đoán `Quá chín` nhưng phân tích màu sắc cho thấy:
     - Tỷ lệ sắc xanh (lục + lam ngọc) $\ge 18\%$.
     - Tỷ lệ sắc vàng $\le 10\%$.
     - Không có dấu hiệu nẫu thâm diện rộng.
   - Hệ thống tự động:
     - Kích hoạt cảnh báo **`OOD Detected: True`** và **`Contradiction: True`**.
     - Đưa ra kết luận hiệu chỉnh từ Thị giác máy tính: **`Xanh (Chuối chưa chín / Giống vỏ xanh-lam Blue Java)`**.
     - Cập nhật cảnh báo cho mô hình Chất Lượng (do chuối xanh chưa có trong tập chất lượng).
3. **Nâng cấp giao diện Web người dùng:**
   - **OOD Alert Banner:** Hiển thị cảnh báo trực quan, giải thích rõ nguyên nhân OOD và Softmax overconfidence.
   - **Card Phân Tích Phổ Màu Thực Tế:** Hiển thị thanh tiến trình trực quan phân bổ % các sắc màu trong ảnh.
   - **Hiển thị kết luận song song:** Người dùng nhìn thấy rõ cả kết quả của mô hình gốc (ResNet50) và khuyến nghị hiệu chỉnh của Thị giác máy tính.

---

### TẦNG 2: Hướng Giải Quyết Dài Hạn Cho Đề Tài Nghiên Cứu (Model Retraining Roadmap)

Để nâng cao năng lực cốt lõi của mô hình Deep Learning trong báo cáo đề tài, các bước sau được đề xuất:

#### 1. Mở rộng tập dữ liệu đa giống chuối (Multi-cultivar Data Augmentation)
- Thu thập bổ sung 100–200 ảnh của các giống chuối bản địa và đặc thù:
  - Chuối Blue Java (vỏ ánh lam bạc).
  - Chuối sáp, chuối ngự, chuối tiêu hồng, chuối mật.
- Áp dụng các kỹ thuật tăng cường dữ liệu màu sắc (Color Jittering):
  - Dịch chuyển ngẫu nhiên kênh Hue: $\Delta H \in [-30^\circ, +30^\circ]$.
  - Điều chỉnh Saturation & Contrast bằng thư viện `Albumentations`.

#### 2. Lượng hóa độ bất định (Uncertainty Estimation)
- **Monte Carlo Dropout (MC-Dropout):** Bật Dropout trong quá trình suy luận (Inference), chạy $N=30$ lần cho một ảnh. Nếu phương sai giữa các lần chạy cao $\sigma^2 > \tau$, mô hình gắn nhãn "Độ bất định cao / Cần kiểm tra thủ công".
- **Temperature Scaling (Platt Scaling):** Thêm tham số nhiệt độ $T > 1$ vào lớp Softmax:
  $$\hat{p}_i = \frac{e^{z_i / T}}{\sum_j e^{z_j / T}}$$
  giúp làm mềm phân phối xác suất và giảm thiểu hiện tượng overconfidence.
- **Thêm lớp Out-of-Distribution (OOD Class):** Thêm nhãn thứ 4: `khac / ood` vào tập huấn luyện để mạng học cách từ chối các mẫu không phù hợp.

#### 3. Tách biệt vật thể quả chuối (Object Detection / Segmentation)
- Tích hợp mạng YOLOv8 hoặc Mask R-CNN để crop chính xác quả chuối trước khi đưa vào bộ phân loại độ chín. Điều này loại bỏ hoàn toàn nhiễu từ bàn tay người cầm hoặc cây cối phía sau.

---

## 4. Kết Quả Sau Khi Triển Khai
- **Ảnh Blue Java kiểm thử:**
  - Hệ thống nhận diện sắc xanh tổng hợp đạt **54.5%** (26.1% xanh lục + 30.1% xanh lam ngọc).
  - Sắc vàng chỉ **0.7%**.
  - Hệ thống tự động kích hoạt cờ OOD, gắn nhãn mâu thuẫn, và đưa ra khuyến nghị hiệu chỉnh: **Xanh (Chuối chưa chín / Blue Java)**.
- **Các mẫu ảnh bình thường (18 mẫu tham chiếu):** Tiếp tục hoạt động chuẩn xác 100%, không bị báo động giả.
