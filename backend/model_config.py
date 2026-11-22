"""
Cấu hình model cho hệ thống phân tích chuối.
Thứ tự class_names xác minh từ notebook: image_dataset_from_directory sắp xếp theo alphabet.
- Ripeness: chin < qua_chin < xanh  → index [0, 1, 2]
- Quality:  dom  < thoi   < tot     → index [0, 1, 2]
"""
import os
from pathlib import Path

# Đường dẫn tương đối từ thư mục gốc dự án (banana-ai-web)
BACKEND_DIR = Path(__file__).parent
PROJECT_ROOT = BACKEND_DIR.parent
MODELS_DIR = PROJECT_ROOT / "models"
RESULTS_DIR = PROJECT_ROOT / "results"
SAMPLES_DIR = PROJECT_ROOT / "samples"

# Cấu hình các model
MODEL_CONFIGS = {
    "ripeness_resnet50": {
        "model_id": "ripeness_resnet50",
        "task": "ripeness",
        "architecture": "ResNet50",
        "dataset": "Banana Ripeness Classification Dataset",
        "dataset_short": "shahriar26s",
        "keras_path": str(MODELS_DIR / "banana-ripeness-classification-dataset_ResNet50.keras"),
        # Từ notebook: image_dataset_from_directory trên thư mục [chin, qua_chin, xanh]
        # Alphabetical sort: chin(0) < qua_chin(1) < xanh(2)
        "class_names": ["chin", "qua_chin", "xanh"],
        "display_names": {
            "chin": "Chín",
            "qua_chin": "Quá chín",
            "xanh": "Xanh",
        },
        "input_shape": (224, 224, 3),
        # preprocess_input nằm trong graph model (resnet50.preprocess_input)
        # => truyền pixel 0-255 nguyên, KHÔNG chia 255
        "preprocess_mode": "in_graph",
        "description_vi": "Phân loại độ chín: Xanh / Chín / Quá chín",
    },
    "quality_resnet50": {
        "model_id": "quality_resnet50",
        "task": "quality",
        "architecture": "ResNet50",
        "dataset": "Banalyzer - Banana Ripeness Classification Dataset",
        "dataset_short": "banalyzer",
        "keras_path": str(MODELS_DIR / "banalyzer-banana-ripeness-classification-dataset_ResNet50.keras"),
        # Từ notebook: image_dataset_from_directory trên thư mục [dom, thoi, tot]
        # Alphabetical sort: dom(0) < thoi(1) < tot(2)
        "class_names": ["dom", "thoi", "tot"],
        "display_names": {
            "dom": "Đốm",
            "thoi": "Thối",
            "tot": "Tốt",
        },
        "input_shape": (224, 224, 3),
        "preprocess_mode": "in_graph",
        "description_vi": "Chất lượng theo nhãn quy đổi: Tốt / Đốm / Thối",
        # Ghi chú: model không có lớp unripe (xanh)
        "missing_classes": ["unripe"],
        "quality_map_note": (
            "Nhãn quy đổi từ Banalyzer: ripe→tot, overripe→dom, rotten→thoi. "
            "Đây là cách quy đổi trong thực nghiệm, chưa xác minh độc lập."
        ),
    },
    # Model dùng ảnh RGB; thứ tự nhãn suy ra từ notebook người dùng cung cấp.
    "ripeness_rgb_resnet50": {
        "model_id": "ripeness_rgb_resnet50",
        "task": "ripeness",
        "architecture": "ResNet50",
        "dataset": "Banana Ripeness RGB Images and Spectral Data",
        "dataset_short": "rgb_spectral",
        "keras_path": str(MODELS_DIR / "Banana_Ripeness_RGB_Images_and_Spectral_Data_ResNet50.keras"),
        # Notebook chuẩn hóa thư mục rồi đọc theo alphabet: chin, qua_chin, xanh.
        # Áp dụng cho model được huấn luyện bằng notebook đã cung cấp.
        "class_names": ["chin", "qua_chin", "xanh"],
        "display_names": {
            "chin": "Chín",
            "qua_chin": "Quá chín",
            "xanh": "Xanh",
        },
        "input_shape": (224, 224, 3),
        "preprocess_mode": "in_graph",
        "description_vi": "Phân loại độ chín từ ảnh RGB: Xanh / Chín / Quá chín",
        "enabled": True,
    },
}

# Mapping CSV tới dataset
CSV_CONFIGS = [
    {
        "dataset": "Banana Ripeness Classification Dataset",
        "task": "ripeness",
        "filename": "five_models_results_Banana_Ripeness_Classification_Dataset.csv",
        "path": str(RESULTS_DIR / "five_models_results_Banana_Ripeness_Classification_Dataset.csv"),
        "best_model_by_macro_f1": "ResNet50",
    },
    {
        "dataset": "Banalyzer - Banana Ripeness Classification Dataset",
        "task": "banana_quality",
        "filename": "five_models_results_banalyzer-banana-ripeness-classification-dataset.csv",
        "path": str(RESULTS_DIR / "five_models_results_banalyzer-banana-ripeness-classification-dataset.csv"),
        "best_model_by_macro_f1": "ResNet50",
    },
    {
        "dataset": "Banana Ripeness RGB Images and Spectral Data",
        "task": "ripeness",
        "filename": "five_models_results_Banana_Ripeness_RGB_Images_and_Spectral_Data.csv",
        "path": str(RESULTS_DIR / "five_models_results_Banana_Ripeness_RGB_Images_and_Spectral_Data.csv"),
        "best_model_by_macro_f1": "EfficientNetB0",
    },
]

# Giới hạn ảnh
MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
MAX_IMAGE_DIMENSION = 4096  # px
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
