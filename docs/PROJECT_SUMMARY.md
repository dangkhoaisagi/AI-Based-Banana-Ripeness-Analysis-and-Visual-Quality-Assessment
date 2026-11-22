# BananaAI — Tổng Kết Dự Án

## Kết Quả Kiểm Thử

| Hạng mục | Kết quả |
|----------|---------|
| Model nạp (Keras 3.15.1 + TF 2.16.1) | ✅ 2/2 model OK |
| Suy luận 18 ảnh mẫu | ✅ **18/18 khớp nhãn tham chiếu** |
| API /health, /models, /predict, /experiments | ✅ Tất cả hoạt động |
| Frontend React + Vite | ✅ Chạy tại localhost:5173 |
| Trang Phân Tích (upload + kết quả) | ✅ |
| Trang Thực Nghiệm (3 CSV datasets) | ✅ |
| Trang Thông Tin | ✅ |

---

## Hướng Dẫn Khởi Động Nhanh

### Terminal 1 — Backend
```powershell
cd D:\banana-ai-web_XLA_Python_2\banana-ai-web
.venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
> Đợi ~30-60 giây đến khi thấy `Application startup complete.`

### Terminal 2 — Frontend
```powershell
cd D:\banana-ai-web_XLA_Python_2\banana-ai-web\frontend
npm run dev
```

### Mở trình duyệt
→ **http://localhost:5173**

---

## Cấu Trúc Đã Tạo

```
banana-ai-web/
├── backend/
│   ├── main.py           ← FastAPI app (port 8000)
│   ├── model_config.py   ← Cấu hình model và nhãn
│   ├── model_loader.py   ← Nạp model Keras
│   ├── image_processor.py← Resize ảnh 224×224
│   ├── inference.py      ← Suy luận 2 model song song
│   ├── verify_models.py  ← Script kiểm thử model
│   ├── .env              ← KERAS_BACKEND=tensorflow
│   └── requirements.txt  ← tensorflow==2.16.1, keras==3.15.1, ...
├── frontend/
│   ├── src/
│   │   ├── pages/AnalyzePage.jsx    ← Tải ảnh + kết quả
│   │   ├── pages/ExperimentsPage.jsx← Bảng CSV thực nghiệm
│   │   ├── pages/AboutPage.jsx      ← Thông tin hệ thống
│   │   ├── components/Navbar.jsx    ← Điều hướng + status
│   │   ├── api.js                   ← Giao tiếp backend
│   │   ├── App.jsx                  ← Router chính
│   │   └── index.css                ← Design system đầy đủ
│   └── vite.config.js   ← Proxy /api → localhost:8000
├── test_reports/
│   ├── integration_test_report.md   ← Báo cáo kiểm thử
│   ├── test_18_samples.py           ← Script kiểm thử 18 ảnh
│   └── sample_test_results.json     ← Kết quả chi tiết JSON
└── README.md            ← Hướng dẫn cài đặt và khởi động
```

## Ghi Chú Kỹ Thuật Quan Trọng

- Model được lưu bằng **Keras 3.13.2** → cần **Keras ≥ 3.13** (dùng 3.15.1)
- TensorFlow 2.16.1 là phiên bản đầu tiên native hỗ trợ Keras 3
- Phải đặt `KERAS_BACKEND=tensorflow` trước khi import Keras
- Input pipeline: RGB → resize 224×224 BICUBIC → float32 **0-255** (không /255) vì model đã có `preprocess_input` bên trong graph
- Suy luận song song 2 model trong cùng 1 request bằng `training=False`
