"""
Kiểm thử 18 ảnh mẫu: chạy suy luận và lập bảng kết quả.
Chạy: .venv\Scripts\python.exe test_reports\test_18_samples.py
"""
import sys
import os
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

BACKEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, os.path.abspath(BACKEND_DIR))

import json
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).parent.parent
SAMPLES_DIR = PROJECT_ROOT / "samples"
MODELS_DIR = PROJECT_ROOT / "models"

# Import backend modules
from image_processor import load_image_from_path

def load_model_safe(path, class_names, model_name):
    import tensorflow as tf
    print(f"Đang nạp {model_name}...")
    try:
        model = tf.keras.models.load_model(str(path))
        num_out = model.output_shape[-1]
        if len(class_names) != num_out:
            print(f"  [WARN] Số lớp config ({len(class_names)}) != model ({num_out})")
        print(f"  OK: input={model.input_shape}, output={model.output_shape}")
        return model
    except Exception as e:
        print(f"  [LỖI] {e}")
        return None

def predict(model, img_array, class_names):
    batch = np.expand_dims(img_array, 0)
    scores = model(batch, training=False).numpy()[0]
    pred_idx = int(np.argmax(scores))
    return class_names[pred_idx], {c: float(scores[i]) for i,c in enumerate(class_names)}

def main():
    print("=" * 70)
    print("KIỂM THỬ 18 ẢNH MẪU")
    print("=" * 70)

    # Nạp labels.json
    labels_path = SAMPLES_DIR / "labels.json"
    with open(labels_path, encoding="utf-8") as f:
        manifest = json.load(f)
    samples = manifest["samples"]
    print(f"Đọc được {len(samples)} bản ghi từ labels.json\n")

    # Nạp models
    RIPENESS_CLASSES = ["chin", "qua_chin", "xanh"]
    QUALITY_CLASSES = ["dom", "thoi", "tot"]
    RIPENESS_DISPLAY = {"chin": "Chín", "qua_chin": "Quá chín", "xanh": "Xanh"}
    QUALITY_DISPLAY  = {"dom": "Đốm", "thoi": "Thối", "tot": "Tốt"}

    m_ripeness = load_model_safe(
        MODELS_DIR / "banana-ripeness-classification-dataset_ResNet50.keras",
        RIPENESS_CLASSES, "Ripeness ResNet50"
    )
    m_quality = load_model_safe(
        MODELS_DIR / "banalyzer-banana-ripeness-classification-dataset_ResNet50.keras",
        QUALITY_CLASSES, "Quality ResNet50"
    )

    print()

    results = []
    correct_ripeness = 0
    correct_quality = 0
    ripeness_count = 0
    quality_count = 0

    for s in samples:
        rel_path = s["file"]          # e.g. "do_chin/chin/chin_01.jpg"
        img_path = SAMPLES_DIR / rel_path
        task = s.get("task")
        ref_label = s.get("label")

        if not img_path.exists():
            print(f"[THIẾU] {rel_path}")
            continue

        # Xử lý ảnh
        try:
            img = load_image_from_path(str(img_path))
        except Exception as e:
            print(f"[ĐỌC LỖI] {rel_path}: {e}")
            continue

        row = {
            "file": rel_path,
            "task": task,
            "ref_label": ref_label,
            "ripeness_pred": None,
            "ripeness_score": None,
            "quality_pred": None,
            "quality_score": None,
            "match": None,
        }

        # Suy luận độ chín
        if m_ripeness:
            pred_cls, scores = predict(m_ripeness, img, RIPENESS_CLASSES)
            row["ripeness_pred"] = pred_cls
            row["ripeness_score"] = round(scores[pred_cls] * 100, 1)
            if task == "do_chin":
                match = pred_cls == ref_label
                row["match"] = match
                correct_ripeness += int(match)
                ripeness_count += 1

        # Suy luận chất lượng
        if m_quality:
            pred_cls, scores = predict(m_quality, img, QUALITY_CLASSES)
            row["quality_pred"] = pred_cls
            row["quality_score"] = round(scores[pred_cls] * 100, 1)
            if task == "chat_luong_quy_doi":
                match = pred_cls == ref_label
                row["match"] = match
                correct_quality += int(match)
                quality_count += 1

        results.append(row)

    # In bảng kết quả
    print("\n" + "=" * 70)
    print("BẢNG KẾT QUẢ")
    print("=" * 70)
    print(f"{'File':<35} {'Task':<10} {'Ref':<12} {'Độ chín':<12} {'%':<8} {'Chất lượng':<12} {'%':<8} {'Khớp'}")
    print("-" * 110)

    for r in results:
        match_str = ""
        if r["match"] is not None:
            match_str = "✓" if r["match"] else "✗"
        print(
            f"{r['file']:<35} "
            f"{r['task']:<10} "
            f"{r['ref_label'] or '—':<12} "
            f"{r['ripeness_pred'] or '—':<12} "
            f"{str(r['ripeness_score'] or '—')+'%':<8} "
            f"{r['quality_pred'] or '—':<12} "
            f"{str(r['quality_score'] or '—')+'%':<8} "
            f"{match_str}"
        )

    print("\n" + "=" * 70)
    print("TỔNG KẾT")
    print("=" * 70)
    if ripeness_count > 0:
        print(f"Độ chín:   {correct_ripeness}/{ripeness_count} ảnh khớp nhãn tham chiếu")
    if quality_count > 0:
        print(f"Chất lượng: {correct_quality}/{quality_count} ảnh khớp nhãn tham chiếu")

    print("""
⚠️ GIỚI HẠN CỦA BẢNG NÀY:
- Nhãn tham chiếu lấy từ thư mục dataset gốc, chưa xác minh trùng lặp với tập train/val/test.
- 18 ảnh không đủ để đánh giá độ chính xác thực tế của model.
- Kết quả sai không đồng nghĩa lỗi tích hợp; có thể là sai số model.
- Bảng này chỉ dùng để kiểm tra chức năng tích hợp (pipeline ảnh → model → output).
""")

    # Lưu kết quả
    report_path = Path(__file__).parent / "sample_test_results.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_samples": len(results),
            "ripeness_correct": correct_ripeness,
            "ripeness_total": ripeness_count,
            "quality_correct": correct_quality,
            "quality_total": quality_count,
            "rows": results,
        }, f, ensure_ascii=False, indent=2)
    print(f"Kết quả chi tiết lưu vào: {report_path}")

if __name__ == "__main__":
    main()
