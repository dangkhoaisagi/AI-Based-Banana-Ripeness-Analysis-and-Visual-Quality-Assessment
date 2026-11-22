# BananaAI - Phân Tích Độ Chín và Chất Lượng Quả Chuối

Đồ án sử dụng học sâu **ResNet50**, **FastAPI** và **React/Vite** để phân tích một ảnh chuối trên máy cục bộ.

Repository: https://github.com/dangkhoaisagi/AI-Based-Banana-Ripeness-Analysis-and-Visual-Quality-Assessment.git

## Deploy

- Frontend được build tự động lên GitHub Pages khi push lên nhánh `main`.
- Backend được deploy bằng Blueprint `render.yaml` trên Render.
- Sau khi Render tạo xong URL backend, thêm GitHub Repository Secret `VITE_API_BASE` với giá trị `https://ten-service.onrender.com/api`, rồi chạy lại workflow **Deploy frontend to GitHub Pages**.

## Chức năng

- Tải ảnh hoặc kéo thả JPG, JPEG, PNG và WebP, tối đa 10 MB.
- Phân loại độ chín thành **Xanh**, **Chín**, **Quá chín**.
- Phân loại chất lượng theo nhãn quy đổi thành **Tốt**, **Đốm**, **Thối**.
- Hiển thị điểm dự đoán của từng lớp và kết quả ResNet50.
- Phân tích phổ màu HSV để hỗ trợ cơ chế kiểm chứng Hybrid AI.
- Tách nền và đánh giá sắc xanh, sắc vàng, sắc nâu/thâm và nguy cơ thối hỏng.
- Hiển thị trạng thái nạp model và kết nối backend.
- Hiển thị bảng so sánh năm kiến trúc học sâu trên ba bộ dữ liệu.
- Cung cấp tài liệu API Swagger tại `/docs`.

Hệ thống chỉ phân tích ảnh chuối đơn. Nó không phát hiện từng quả trong ảnh nhiều chuối, không có lớp "không phải chuối" và không được dùng để kết luận an toàn thực phẩm.

## Kiến trúc

```text
Trình duyệt React/Vite
        |
        | HTTP /api
        v
FastAPI backend
        |
        +-- Keras ResNet50: độ chín
        +-- Keras ResNet50: chất lượng
        +-- OpenCV/HSV: phân tích màu
        +-- CSV: kết quả thực nghiệm
```

## Cấu trúc thư mục

```text
banana-ai-web/
├── backend/        API, nạp model, tiền xử lý và suy luận
├── frontend/       Giao diện React/Vite
├── models/         Ba checkpoint ResNet50 .keras
├── notebooks/      Notebook huấn luyện và thử nghiệm
├── results/        Ba file CSV kết quả thực nghiệm
├── samples/        18 ảnh mẫu
├── test_reports/   Script và kết quả kiểm thử
└── docs/           Tài liệu bổ sung
```

## Yêu cầu

- Windows 10/11
- Python 3.11
- Node.js 18 trở lên và npm
- RAM khuyến nghị từ 8 GB
- Ổ đĩa trống ít nhất 5 GB
- Git LFS để tải checkpoint `.keras`

## Cài đặt lần đầu

### 1. Clone repository

```powershell
git clone https://github.com/dangkhoaisagi/AI-Based-Banana-Ripeness-Analysis-and-Visual-Quality-Assessment.git
cd AI-Based-Banana-Ripeness-Analysis-and-Visual-Quality-Assessment
git lfs install
git lfs pull
```

### 2. Tạo môi trường Python

Mở PowerShell trong thư mục gốc:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

Nếu PowerShell chặn kích hoạt môi trường:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Hoặc không kích hoạt môi trường:

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

### 3. Cài frontend

```powershell
cd frontend
npm install
cd ..
```

## Chạy đồ án

Mở hai cửa sổ PowerShell tại thư mục gốc.

### Terminal 1 - Backend

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Sau khi kích hoạt `.venv`, có thể dùng:

```powershell
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Đợi thông báo `Application startup complete`. Nạp model có thể mất 30-90 giây.

### Terminal 2 - Frontend

```powershell
cd frontend
npm run dev
```

Mở:

- Giao diện: http://localhost:5173
- API Swagger: http://localhost:8000/docs
- Kiểm tra backend: http://localhost:8000/api/health

Nhấn `Ctrl+C` trong từng terminal để dừng dịch vụ.

## API

| Endpoint | Method | Chức năng |
|---|---|---|
| `/api/health` | GET | Trạng thái backend và từng model |
| `/api/models` | GET | Danh sách model, task, kiến trúc và nhãn |
| `/api/predict` | POST | Gửi ảnh bằng `multipart/form-data` để suy luận |
| `/api/experiments` | GET | Đọc và tổng hợp ba file CSV thực nghiệm |

Ví dụ PowerShell:

```powershell
curl.exe -F "file=@D:\duong-dan\anh-chuoi.jpg" http://localhost:8000/api/predict
```

## Model

| Model | Bài toán | Nhãn |
|---|---|---|
| `banana-ripeness-classification-dataset_ResNet50.keras` | Độ chín | `chin`, `qua_chin`, `xanh` |
| `banalyzer-banana-ripeness-classification-dataset_ResNet50.keras` | Chất lượng | `dom`, `thoi`, `tot` |
| `Banana_Ripeness_RGB_Images_and_Spectral_Data_ResNet50.keras` | Độ chín RGB/spectral | `chin`, `qua_chin`, `xanh` |

Thứ tự nhãn xác định theo thứ tự sắp xếp thư mục trong notebook:

- Độ chín: `chin(0)`, `qua_chin(1)`, `xanh(2)`
- Chất lượng: `dom(0)`, `thoi(1)`, `tot(2)`

Kết quả thực nghiệm dùng Macro F1 làm tiêu chí chính:

- Banana Ripeness Classification: ResNet50 đạt 99.76% Macro F1.
- Banalyzer: ResNet50 đạt 93.35% Macro F1.

Các giá trị này là kết quả trong file CSV thực nghiệm, không phải bằng chứng cho độ chính xác trên mọi dữ liệu thực tế.

## Kiểm thử

```powershell
.\.venv\Scripts\python.exe backend\verify_models.py
.\.venv\Scripts\python.exe test_reports\test_18_samples.py
```

## Giới hạn

- Điểm softmax không phải xác suất đã hiệu chuẩn.
- Mô hình có thể nhận sai với giống chuối hoặc điều kiện ánh sáng ngoài dữ liệu huấn luyện.
- Cơ chế HSV hỗ trợ thị giác máy tính nhưng không thay thế đánh giá chuyên môn.
- Nhãn chất lượng quy đổi: ripe -> Tốt, overripe -> Đốm, rotten -> Thối.
- Không hỗ trợ nhiều ảnh hoặc phát hiện Bounding Box.

## Tài liệu bổ sung

- [Tổng kết dự án](docs/PROJECT_SUMMARY.md)
- [Hướng dẫn xử lý dữ liệu ngoài phân phối](docs/HUONG_GIAI_QUYET_OOD_AI.md)
- [Báo cáo kiểm thử tích hợp](test_reports/integration_test_report.md)

## Nguồn dữ liệu

- [Banana Ripeness Classification Dataset](https://www.kaggle.com/datasets/shahriar26s/banana-ripeness-classification-dataset) - S.M. Shahriar
- [Banalyzer - Banana Ripeness Classification Dataset](https://www.kaggle.com/datasets/iamchaarles/banalyzer-banana-ripeness-classification-dataset) - Charles C R
- [Banana Ripeness RGB Images and Spectral Data](https://www.kaggle.com)
