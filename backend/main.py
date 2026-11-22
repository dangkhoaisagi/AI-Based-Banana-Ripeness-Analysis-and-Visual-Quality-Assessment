"""
FastAPI backend cho hệ thống phân tích chuối.
Chạy với: python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000
"""
import io
import csv
import logging
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

# Keras 3 dùng TF backend; phải đặt trước khi import keras
os.environ.setdefault("KERAS_BACKEND", "tensorflow")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Thêm thư mục backend vào path
sys.path.insert(0, str(Path(__file__).parent))

from model_config import MODEL_CONFIGS, CSV_CONFIGS, MAX_IMAGE_SIZE_BYTES
import model_loader as ml
import image_processor as ip
import inference as infer

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Nạp model khi server khởi động."""
    logger.info("=== Khởi động backend phân tích chuối ===")
    ml.initialize_models(MODEL_CONFIGS)
    logger.info("=== Backend sẵn sàng ===")
    yield
    logger.info("=== Backend đang dừng ===")


app = FastAPI(
    title="Banana AI Analysis API",
    description="Backend phân tích độ chín và chất lượng quả chuối bằng deep learning",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS cho frontend cục bộ
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:3000",
]
for origin in os.getenv("FRONTEND_ORIGINS", "").split(","):
    if origin.strip():
        allowed_origins.append(origin.strip())

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(dict.fromkeys(allowed_origins)),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    """Trạng thái backend và từng model."""
    statuses = ml.get_all_status()
    any_ready = any(s["status"] == "ready" for s in statuses)
    return {
        "status": "ok",
        "backend": "running",
        "any_model_ready": any_ready,
        "models": statuses,
    }


@app.get("/api/models")
async def get_models():
    """Danh sách model với cấu hình và khả năng sử dụng thực tế."""
    statuses = ml.get_all_status()
    return {"models": statuses}


@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    """
    Nhận ảnh (JPG/PNG/WebP), phân tích bằng hai model mặc định.
    Trả về kết quả độ chín và chất lượng.
    """
    # Đọc bytes
    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Không thể đọc file: {e}",
        )

    # Validate và decode ảnh
    try:
        img_array = ip.validate_and_decode(
            file_bytes,
            filename=file.filename or "upload.jpg",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    # Suy luận
    try:
        result = infer.predict_image(img_array)
    except Exception as e:
        logger.exception(f"Lỗi suy luận: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi suy luận: {e}",
        )

    return {
        "filename": file.filename,
        "image_shape": list(img_array.shape),
        "result": result,
    }


@app.get("/api/experiments")
async def get_experiments():
    """Đọc ba file CSV kết quả và trả về dữ liệu chuẩn hóa."""
    experiments = []

    for cfg in CSV_CONFIGS:
        csv_path = cfg["path"]
        if not Path(csv_path).exists():
            experiments.append({
                "dataset": cfg["dataset"],
                "task": cfg["task"],
                "filename": cfg["filename"],
                "status": "file_missing",
                "rows": [],
            })
            continue

        try:
            rows = []
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Chuyển số thực
                    parsed = {}
                    for k, v in row.items():
                        if v is None or v.strip() == "":
                            parsed[k] = None
                        else:
                            try:
                                parsed[k] = float(v)
                            except (ValueError, AttributeError):
                                parsed[k] = v
                    rows.append(parsed)

            # Tìm dòng tốt nhất theo Macro_F1
            best_row = None
            best_f1 = -1.0
            for row in rows:
                f1 = row.get("Macro_F1")
                if f1 is not None and isinstance(f1, float) and f1 > best_f1:
                    best_f1 = f1
                    best_row = row.get("Model")

            experiments.append({
                "dataset": cfg["dataset"],
                "task": cfg["task"],
                "filename": cfg["filename"],
                "status": "ok",
                "best_model_by_macro_f1": best_row,
                "rows": rows,
            })
        except Exception as e:
            logger.exception(f"Lỗi đọc CSV {csv_path}: {e}")
            experiments.append({
                "dataset": cfg["dataset"],
                "task": cfg["task"],
                "filename": cfg["filename"],
                "status": "read_error",
                "error": str(e),
                "rows": [],
            })

    return {"experiments": experiments}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
