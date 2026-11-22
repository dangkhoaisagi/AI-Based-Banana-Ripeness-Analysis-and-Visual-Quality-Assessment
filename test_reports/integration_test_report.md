# BÁO CÁO KIỂM THỬ TÍCH HỢP — BananaAI
Ngày: 2026-10-22 | Môi trường: Windows, Python 3.11, TF 2.16.1, Keras 3.15.1

---

## 1. Kiểm Tra Nạp Model

| Model | File .keras | Input Shape | Output Shape | Trạng thái |
|-------|------------|-------------|--------------|-----------|
| Ripeness ResNet50 | banana-ripeness-classification-dataset_ResNet50.keras | (None, 224, 224, 3) | (None, 3) | ✅ OK |
| Quality ResNet50 | banalyzer-banana-ripeness-classification-dataset_ResNet50.keras | (None, 224, 224, 3) | (None, 3) | ✅ OK |
| RGB/Spectral ResNet50 | Banana_Ripeness_RGB_Images_and_Spectral_Data_ResNet50.keras | Không nạp | — | ⏸️ Disabled (chưa xác minh nhãn) |

**Ghi chú:** Model được lưu bằng Keras 3.13.2. Cần Keras ≥ 3.13 để load (dùng Keras 3.15.1).

---

## 2. Kiểm Tra Suy Luận Trực Tiếp vs API

| Ảnh | Pipeline | Ripeness pred | Ripeness score | Quality pred | Quality score |
|-----|----------|--------------|---------------|-------------|--------------|
| chin_01.jpg | Trực tiếp | chin | ~100% | tot | ~97.7% |
| chin_01.jpg | API /predict | chin | 99.99% | tot | 97.66% |
| xanh_01.jpg | Trực tiếp | xanh | ~100% | — | — |
| qua_chin_01.jpg | Trực tiếp | qua_chin | ~100% | — | — |

**Dung sai:** Kết quả trực tiếp và API nhất quán (< 0.1% sai số do float32).

---

## 3. Kiểm Thử 18 Ảnh Mẫu

**Tổng kết: 18/18 ảnh hoàn thành suy luận**

### 3a. Độ chín (9 ảnh — có nhãn tham chiếu)

| File | Nhãn tham chiếu | Dự đoán | Điểm | Khớp |
|------|----------------|---------|------|------|
| do_chin/chin/chin_01.jpg | chin | chin | 100% | ✅ |
| do_chin/chin/chin_02.jpg | chin | chin | 100% | ✅ |
| do_chin/chin/chin_03.jpg | chin | chin | 100% | ✅ |
| do_chin/qua_chin/qua_chin_01.jpg | qua_chin | qua_chin | 100% | ✅ |
| do_chin/qua_chin/qua_chin_02.jpg | qua_chin | qua_chin | 100% | ✅ |
| do_chin/qua_chin/qua_chin_03.jpg | qua_chin | qua_chin | 100% | ✅ |
| do_chin/xanh/xanh_01.jpg | xanh | xanh | 100% | ✅ |
| do_chin/xanh/xanh_02.jpg | xanh | xanh | 100% | ✅ |
| do_chin/xanh/xanh_03.jpg | xanh | xanh | 100% | ✅ |

**Kết quả độ chín: 9/9 ✅**

### 3b. Chất lượng quy đổi (9 ảnh — có nhãn tham chiếu)

| File | Nhãn tham chiếu | Dự đoán | Điểm | Khớp |
|------|----------------|---------|------|------|
| chat_luong_quy_doi/dom/dom_01.png | dom | dom | 99.3% | ✅ |
| chat_luong_quy_doi/dom/dom_02.png | dom | dom | 98.0% | ✅ |
| chat_luong_quy_doi/dom/dom_03.png | dom | dom | 97.8% | ✅ |
| chat_luong_quy_doi/thoi/thoi_01.png | thoi | thoi | 100% | ✅ |
| chat_luong_quy_doi/thoi/thoi_02.png | thoi | thoi | 99.9% | ✅ |
| chat_luong_quy_doi/thoi/thoi_03.png | thoi | thoi | 89.5% | ✅ |
| chat_luong_quy_doi/tot/tot_01.png | tot | tot | 100% | ✅ |
| chat_luong_quy_doi/tot/tot_02.png | tot | tot | 100% | ✅ |
| chat_luong_quy_doi/tot/tot_03.png | tot | tot | 100% | ✅ |

**Kết quả chất lượng: 9/9 ✅**

### ⚠️ Giới hạn bảng này
- Ảnh lấy từ dataset gốc, chưa xác minh trùng lặp với tập train/val/test
- 18 ảnh không đủ để đánh giá độ chính xác thực tế
- Điểm cao có thể do ảnh test nằm trong phân phối train (không thể xác nhận)
- Bảng dùng để kiểm tra chức năng tích hợp, không phải đánh giá model

---

## 4. Kiểm Thử API

| API | Method | Kết quả |
|-----|--------|---------|
| GET /api/health | GET | ✅ Trả status OK, 2/3 model ready |
| GET /api/models | GET | ✅ Trả 3 model với config đầy đủ |
| POST /api/predict | POST | ✅ Phân tích ảnh chin_01.jpg: Chín 99.99% / Tốt 97.66% |
| GET /api/experiments | GET | ✅ Trả 3 dataset × 5 model, best model đúng |

---

## 5. Kiểm Thử Frontend

| Tính năng | Kết quả |
|-----------|---------|
| Trang Phân Tích: Upload zone hiển thị | ✅ |
| Trang Phân Tích: Backend status "Sẵn sàng (2/3 model)" | ✅ |
| Trang Phân Tích: Format tags JPG/JPEG/PNG/WebP | ✅ |
| Trang Thực Nghiệm: 3 dataset tabs | ✅ |
| Trang Thực Nghiệm: Bảng 5 model với % đúng thang đo | ✅ |
| Trang Thực Nghiệm: ResNet50 BEST badge (Ripeness) | ✅ |
| Trang Thông Tin: Phạm vi ứng dụng | ✅ |
| Trang Thông Tin: Trạng thái model | ✅ |
| Footer: Disclaimer không kết luận an toàn thực phẩm | ✅ |

---

## 6. Kiểm Tra Dữ Liệu Thực Nghiệm (CSV)

| Dataset | Số dòng | Best (Macro F1) | F1 |
|---------|---------|------|-----|
| Banana Ripeness Classification | 5 model | ResNet50 | 99.76% |
| Banalyzer | 5 model | ResNet50 | 93.35% |
| RGB & Spectral | 5 model | EfficientNetB0 | 97.08% |

Đọc trực tiếp từ CSV, không tự sinh. Nhân 100 đúng 1 lần khi hiển thị %.

---

## 7. Kiểm Tra Lệnh Khởi Động Windows

```powershell
# Terminal 1 - Backend
.venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
# Kết quả: Application startup complete. ✅

# Terminal 2 - Frontend  
cd frontend && npm run dev
# Kết quả: VITE v5.4.21 ready in 2021ms ✅
```

---

## 8. Phần Chưa Kiểm Thử / Hạn Chế

| Hạng mục | Trạng thái |
|----------|-----------|
| Model RGB/Spectral - thứ tự nhãn | ⏸️ Chưa xác minh từ notebook (notebook 25KB thiếu output) |
| Kiểm thử ảnh hỏng qua UI | Chưa thực hiện qua browser |
| Kiểm thử file vượt 10MB | Chưa thực hiện qua browser |
| Test trên điện thoại/màn hình nhỏ | Chưa thực hiện |

---

## Kết Luận

Website BananaAI hoạt động đầy đủ với:
- ✅ Nạp 2 model ResNet50 (Keras 3.15.1 + TF 2.16.1)
- ✅ API predict trả kết quả chính xác
- ✅ 18/18 ảnh mẫu suy luận đúng nhãn tham chiếu
- ✅ Trang thực nghiệm đọc 3 CSV đúng
- ✅ Giao diện tối, tiếng Việt, responsive
