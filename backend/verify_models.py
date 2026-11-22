"""
Script kiểm tra nạp và suy luận model trực tiếp (không qua API).
Chạy: python3.11 verify_models.py
"""
import sys
import os
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(__file__))
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
SAMPLES_DIR = PROJECT_ROOT / "samples"


def load_and_check(keras_path: str, class_names: list, model_name: str):
    """Nạp model và kiểm tra shape, số class, output."""
    import tensorflow as tf
    print(f"\n{'='*60}")
    print(f"MODEL: {model_name}")
    print(f"Path: {keras_path}")
    print(f"Exists: {Path(keras_path).exists()}")
    print(f"Size: {Path(keras_path).stat().st_size / 1e6:.1f} MB")

    try:
        model = tf.keras.models.load_model(keras_path)
        print(f"Input shape:  {model.input_shape}")
        print(f"Output shape: {model.output_shape}")
        num_classes = model.output_shape[-1]
        print(f"Num classes:  {num_classes}")
        print(f"Config classes: {class_names} (n={len(class_names) if class_names else 'N/A'})")

        if class_names and len(class_names) != num_classes:
            print(f"[WARN] Số lớp KHÔNG KHỚP!")

        # Tạo ảnh dummy và chạy suy luận
        dummy = np.zeros((1, 224, 224, 3), dtype=np.float32)
        scores = model(dummy, training=False).numpy()[0]
        print(f"Dummy scores: {[round(float(s),4) for s in scores]}")
        print(f"Sum scores: {sum(scores):.4f} (kỳ vọng ~1.0 nếu có softmax)")
        print(f"Finite: {np.all(np.isfinite(scores))}")
        return model
    except Exception as e:
        print(f"[ERROR] Nạp model thất bại: {e}")
        return None


def test_with_sample(model, img_path: str, class_names: list, display_names: dict):
    """Chạy suy luận trên ảnh mẫu thực tế."""
    from PIL import Image
    import numpy as np

    try:
        img = Image.open(img_path).convert("RGB").resize((224, 224), Image.BICUBIC)
        arr = np.array(img, dtype=np.float32)
        batch = np.expand_dims(arr, 0)
        scores = model(batch, training=False).numpy()[0]
        pred_idx = int(np.argmax(scores))
        pred_cls = class_names[pred_idx]
        pred_display = display_names.get(pred_cls, pred_cls)
        print(f"  Ảnh: {Path(img_path).name}")
        print(f"  Dự đoán: {pred_cls} ({pred_display})")
        print(f"  Điểm: {[f'{cls}={scores[i]:.3f}' for i, cls in enumerate(class_names)]}")
    except Exception as e:
        print(f"  [ERROR] {img_path}: {e}")


if __name__ == "__main__":
    print("=== Kiểm tra model nạp và suy luận ===")

    import tensorflow as tf
    keras_ver = getattr(tf.keras, "__version__", "N/A")
    print(f"TF: {tf.__version__}, Keras: {keras_ver}")

    # Model 1: Độ chín
    RIPENESS_PATH = str(MODELS_DIR / "banana-ripeness-classification-dataset_ResNet50.keras")
    RIPENESS_CLASSES = ["chin", "qua_chin", "xanh"]
    RIPENESS_DISPLAY = {"chin": "Chín", "qua_chin": "Quá chín", "xanh": "Xanh"}

    m1 = load_and_check(RIPENESS_PATH, RIPENESS_CLASSES, "Ripeness ResNet50")
    if m1:
        print("\n--- Kiểm tra với ảnh mẫu (độ chín) ---")
        for cls in ["chin", "xanh", "qua_chin"]:
            sample_dir = SAMPLES_DIR / "do_chin" / cls
            samples = list(sample_dir.glob("*.jpg"))[:1]
            for s in samples:
                test_with_sample(m1, str(s), RIPENESS_CLASSES, RIPENESS_DISPLAY)

    # Model 2: Chất lượng
    QUALITY_PATH = str(MODELS_DIR / "banalyzer-banana-ripeness-classification-dataset_ResNet50.keras")
    QUALITY_CLASSES = ["dom", "thoi", "tot"]
    QUALITY_DISPLAY = {"dom": "Đốm", "thoi": "Thối", "tot": "Tốt"}

    m2 = load_and_check(QUALITY_PATH, QUALITY_CLASSES, "Quality ResNet50")
    if m2:
        print("\n--- Kiểm tra với ảnh mẫu (chất lượng) ---")
        for cls in ["tot", "dom", "thoi"]:
            sample_dir = SAMPLES_DIR / "chat_luong_quy_doi" / cls
            samples = list(sample_dir.glob("*.jpg"))[:1]
            for s in samples:
                test_with_sample(m2, str(s), QUALITY_CLASSES, QUALITY_DISPLAY)

    print("\n=== Kiểm tra hoàn tất ===")
