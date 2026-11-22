"""
Module suy luận kết hợp (Hybrid AI Fusion):
1. Tách nền thông minh (rembg AI + fallback XLA HSV Color Segmentation).
2. Chạy hai model ResNet50: Ripeness (độ chín) và Quality (chất lượng).
3. Phân tích quang phổ màu HSV và entropy kết cấu (Computer Vision - XLA).
4. Hợp nhất quyết định đa tầng (Hybrid Decision Fusion) đảm bảo chính xác mọi trường hợp.
"""
import logging
import numpy as np
from PIL import Image
from model_loader import get_loader, ModelLoader
from color_analyzer import evaluate_ood_and_contradiction
import bg_remover

logger = logging.getLogger(__name__)

# Model IDs mặc định
RIPENESS_MODEL_ID = "ripeness_resnet50"
QUALITY_MODEL_ID = "quality_resnet50"


def run_single_model(
    loader: ModelLoader,
    img_array: np.ndarray,
) -> dict:
    """Chạy suy luận một model và trả về kết quả chuẩn hóa."""
    cfg = loader.config
    try:
        # Đảm bảo kích thước chuẩn (224, 224, 3) cho ResNet50
        if img_array.shape[:2] != (224, 224):
            pil_tmp = Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))
            pil_tmp = pil_tmp.resize((224, 224), Image.BICUBIC)
            img_input = np.array(pil_tmp, dtype=np.float32)
        else:
            img_input = img_array

        scores = loader.predict(img_input)  # (num_classes,) float32

        class_names = cfg["class_names"]
        display_names = cfg.get("display_names", {})

        # Điểm từng lớp
        scores_dict = {
            cls: float(scores[i]) for i, cls in enumerate(class_names)
        }

        # Lớp dự đoán
        pred_idx = int(np.argmax(scores))
        pred_class = class_names[pred_idx]
        pred_display = display_names.get(pred_class, pred_class)

        return {
            "status": "ok",
            "model_id": cfg["model_id"],
            "architecture": cfg["architecture"],
            "dataset": cfg["dataset"],
            "task": cfg["task"],
            "predicted_class": pred_class,
            "predicted_display": pred_display,
            "scores": scores_dict,
            "display_names": display_names,
        }
    except Exception as e:
        logger.exception(f"Lỗi suy luận {loader.config['model_id']}: {e}")
        return {
            "status": "error",
            "model_id": cfg["model_id"],
            "architecture": cfg["architecture"],
            "dataset": cfg["dataset"],
            "task": cfg["task"],
            "error": str(e),
        }


def predict_image(img_array: np.ndarray) -> dict:
    """
    Chạy hệ thống AI Hybrid (Deep Learning + Xử Lý Ảnh XLA):
    1. Tách nền thông minh bằng rembg AI hoặc phân đoạn màu XLA.
    2. Chạy ResNet50 Ripeness và ResNet50 Quality trên ảnh.
    3. Phân tích quang phổ màu (loại trừ nền) để kiểm chứng tính nhất quán.
    4. Tự động hợp nhất quyết định (Hybrid AI Fusion) để đưa ra kết luận chuẩn xác nhất.
    """
    ripeness_loader = get_loader(RIPENESS_MODEL_ID)
    quality_loader = get_loader(QUALITY_MODEL_ID)

    # ── Bước 1: Tách nền thông minh ──────────────────────────────────────────
    bg_removed = False
    bg_method = "none"
    fg_mask = None
    img_for_model = img_array
    img_for_color = img_array

    try:
        img_no_bg, fg_mask, bg_method = bg_remover.remove_background(img_array)
        img_for_model = img_no_bg
        img_for_color = img_no_bg
        bg_removed = (bg_method != "none" and bg_method != "passthrough")
        logger.info(f"Tách nền ({bg_method}): fg_mask mean={fg_mask.mean()*100:.1f}%")
    except Exception as e:
        logger.warning(f"Lỗi tách nền, dùng ảnh gốc: {e}")
        fg_mask = np.ones(img_array.shape[:2], dtype=bool)

    # ── Bước 2: Chạy Model Độ Chín từ Deep Learning ──────────────────────────
    if ripeness_loader and ripeness_loader.status == "ready":
        ripeness_result = run_single_model(ripeness_loader, img_for_model)
    else:
        err = (
            ripeness_loader.error_message
            if ripeness_loader
            else "Model chưa được nạp"
        )
        ripeness_result = {
            "status": "not_ready",
            "model_id": RIPENESS_MODEL_ID,
            "task": "ripeness",
            "error": err,
        }

    ripeness_result["bg_removed"] = bg_removed
    ripeness_result["bg_method"] = bg_method

    # ── Bước 3: Chạy Model Chất Lượng từ Deep Learning ───────────────────────
    if quality_loader and quality_loader.status == "ready":
        quality_result = run_single_model(quality_loader, img_for_model)
        quality_result["quality_map_note"] = (
            "Nhãn quy đổi từ Banalyzer: ripe→Tốt, overripe→Đốm, rotten→Thối."
        )
    else:
        err = (
            quality_loader.error_message
            if quality_loader
            else "Model chưa được nạp"
        )
        quality_result = {
            "status": "not_ready",
            "model_id": QUALITY_MODEL_ID,
            "task": "quality",
            "error": err,
        }

    # ── Bước 3b: Chạy Model Độ Chín RGB Spectral nếu được bật ────────────────
    ripeness_rgb_loader = get_loader("ripeness_rgb_resnet50")
    ripeness_rgb_result = None
    if ripeness_rgb_loader and ripeness_rgb_loader.status == "ready":
        ripeness_rgb_result = run_single_model(ripeness_rgb_loader, img_for_model)

    # ── Bước 4: Phân tích phổ màu XLA & Kiểm chứng OOD ───────────────────────
    ood_info = evaluate_ood_and_contradiction(img_for_color, ripeness_result, fg_mask=fg_mask)
    ripeness_result["ood_analysis"] = ood_info

    color_profile     = ood_info.get("color_profile", {})
    is_clearly_rotten = color_profile.get("is_clearly_rotten", False)
    is_overripe_cv    = color_profile.get("is_overripe", False)
    is_unripe_cv      = color_profile.get("is_unripe", False)
    is_ripe_cv        = color_profile.get("is_ripe", False)
    dark_brown_pct    = color_profile.get("dark_brown_pct", 0.0)
    dark_spot_pct     = color_profile.get("dark_spot_pct", 0.0)
    rotten_score      = color_profile.get("rotten_score", 0.0)

    # Lưu kết quả thô của Deep Learning để minh bạch thông tin
    raw_dl_rip_class   = ripeness_result.get("predicted_class")
    raw_dl_rip_display = ripeness_result.get("predicted_display")
    raw_dl_rip_score   = (
        ripeness_result.get("scores", {}).get(raw_dl_rip_class, 0.0)
        if raw_dl_rip_class else 0.0
    )
    ripeness_result["raw_dl"] = {
        "predicted_class": raw_dl_rip_class,
        "predicted_display": raw_dl_rip_display,
        "score": raw_dl_rip_score,
    }

    raw_quality_class   = quality_result.get("predicted_class")
    raw_quality_display = quality_result.get("predicted_display")
    raw_quality_score   = (
        quality_result.get("scores", {}).get(raw_quality_class, 0.0)
        if raw_quality_class else 0.0
    )
    quality_result["raw_dl"] = {
        "predicted_class": raw_quality_class,
        "predicted_display": raw_quality_display,
        "score": raw_quality_score,
    }

    # ── Bước 5: Hợp Nhất Quyết Định Đa Tầng (Hybrid Decision Fusion) ─────────
    rip_display_map = ripeness_loader.config.get("display_names", {}) if ripeness_loader else {}
    quality_display_map = quality_loader.config.get("display_names", {}) if quality_loader else {}

    # --- 5.1 XỬ LÝ CHUỐI THỐI HỎNG (ƯU TIÊN CAO NHẤT) ---
    # Chuối thối khi XLA phát hiện thối RÕ HOẶC model Quality khẳng định thối kèm đốm thâm bất thường
    is_rotten_confirmed = (
        is_clearly_rotten
        or (raw_quality_class == "thoi" and (dark_brown_pct >= 25.0 or dark_spot_pct >= 18.0 or rotten_score >= 35.0))
    )

    if is_rotten_confirmed:
        # 1. Hiệu chỉnh Ripeness sang "qua_chin" (Quá chín / Thối)
        if raw_dl_rip_class in ("xanh", "chin") or is_clearly_rotten:
            cv_conf = min(0.98, max(0.75, rotten_score / 75.0))
            ripeness_result["predicted_class"] = "qua_chin"
            ripeness_result["predicted_display"] = "Quá chín / Thối (Hiệu chỉnh theo Thị Giác)"
            ripeness_result["is_hybrid_corrected"] = True
            ripeness_result["hybrid_confidence"] = cv_conf
            if "scores" in ripeness_result:
                new_scores = {}
                for k in ripeness_result["scores"]:
                    new_scores[k] = cv_conf if k == "qua_chin" else round(
                        (1.0 - cv_conf) / max(1, len(ripeness_result["scores"]) - 1), 3
                    )
                ripeness_result["scores"] = new_scores

            ripeness_result["cv_assisted_recommendation"] = {
                "recommended_class": "qua_chin",
                "recommended_display": "Quá chín / Thối (Hiệu chỉnh theo Thị Giác)",
                "cv_confidence": cv_conf,
                "warning_title": "Cảnh Báo: Chuối Thối Hỏng Ngoài Thực Tế",
                "warning_message": (
                    f"Thị giác máy tính phát hiện hoại tử nâu đen chiếm diện rộng "
                    f"({dark_brown_pct:.1f}% đốm thâm, điểm thối={rotten_score:.0f}/100). "
                    "Kết quả được tự động hiệu chỉnh chính xác sang Quá chín / Thối."
                ),
            }
        else:
            ripeness_result["is_hybrid_corrected"] = False

        # 2. Hiệu chỉnh Quality sang "thoi"
        if raw_quality_class != "thoi":
            cv_q_conf = min(0.97, max(0.75, rotten_score / 80.0))
            quality_result["predicted_class"] = "thoi"
            quality_result["predicted_display"] = quality_display_map.get("thoi", "Thối")
            quality_result["is_hybrid_corrected"] = True
            quality_result["hybrid_confidence"] = cv_q_conf
            if "scores" in quality_result:
                new_q_scores = {}
                for k in quality_result["scores"]:
                    new_q_scores[k] = cv_q_conf if k == "thoi" else round(
                        (1.0 - cv_q_conf) / max(1, len(quality_result["scores"]) - 1), 3
                    )
                quality_result["scores"] = new_q_scores
            quality_result["cv_quality_correction"] = (
                f"XLA phát hiện chuối thối hoại tử (RottenScore={rotten_score:.0f}/100, "
                f"dark_brown={dark_brown_pct:.1f}%). Chất lượng được hiệu chỉnh sang 'Thối'."
            )
        else:
            quality_result["is_hybrid_corrected"] = False

    # --- 5.2 XỬ LÝ CHUỐI QUÁ CHÍN / ĐỐM ĐỒI MỒI ---
    elif is_overripe_cv or (raw_quality_class == "dom" and dark_brown_pct >= 20.0):
        # 1. Hiệu chỉnh Ripeness sang "qua_chin"
        if raw_dl_rip_class in ("xanh", "chin"):
            cv_conf = min(0.94, max(0.68, dark_brown_pct / 55.0))
            ripeness_result["predicted_class"] = "qua_chin"
            ripeness_result["predicted_display"] = "Quá chín / Đốm (Hiệu chỉnh theo Thị Giác)"
            ripeness_result["is_hybrid_corrected"] = True
            ripeness_result["hybrid_confidence"] = cv_conf
            if "scores" in ripeness_result:
                new_scores = {}
                for k in ripeness_result["scores"]:
                    new_scores[k] = cv_conf if k == "qua_chin" else round(
                        (1.0 - cv_conf) / max(1, len(ripeness_result["scores"]) - 1), 3
                    )
                ripeness_result["scores"] = new_scores

            ripeness_result["cv_assisted_recommendation"] = {
                "recommended_class": "qua_chin",
                "recommended_display": "Quá chín / Đốm (Hiệu chỉnh theo Thị Giác)",
                "cv_confidence": cv_conf,
                "warning_title": "Hiệu Chỉnh: Chuối Xuất Hiện Nhiều Đốm Thâm Nâu",
                "warning_message": (
                    f"Thị giác máy tính phát hiện {dark_brown_pct:.1f}% mảng đốm thâm nâu (sugar spots). "
                    "Kết quả được hiệu chỉnh chính xác sang Quá chín."
                ),
            }
        else:
            ripeness_result["is_hybrid_corrected"] = False

        # 2. Hiệu chỉnh Quality sang "dom" nếu DL đoán "tot"
        if raw_quality_class == "tot":
            cv_q_conf = min(0.92, max(0.65, dark_brown_pct / 50.0))
            quality_result["predicted_class"] = "dom"
            quality_result["predicted_display"] = quality_display_map.get("dom", "Đốm")
            quality_result["is_hybrid_corrected"] = True
            quality_result["hybrid_confidence"] = cv_q_conf
            if "scores" in quality_result:
                new_q_scores = {}
                for k in quality_result["scores"]:
                    new_q_scores[k] = cv_q_conf if k == "dom" else round(
                        (1.0 - cv_q_conf) / max(1, len(quality_result["scores"]) - 1), 3
                    )
                quality_result["scores"] = new_q_scores
            quality_result["cv_quality_correction"] = (
                f"XLA phát hiện chuối có {dark_brown_pct:.1f}% đốm nâu đồi mồi. "
                "Chất lượng được hiệu chỉnh sang 'Đốm'."
            )
        else:
            quality_result["is_hybrid_corrected"] = False

    # --- 5.3 XỬ LÝ CHUỐI XANH / BLUE JAVA ---
    elif is_unripe_cv and raw_dl_rip_class in ("chin", "qua_chin"):
        cv_conf = min(0.97, max(0.70, color_profile.get("unripe_total_pct", 50) / 65.0))
        ripeness_result["predicted_class"] = "xanh"
        ripeness_result["predicted_display"] = "Xanh (Hiệu chỉnh theo Thị Giác)"
        ripeness_result["is_hybrid_corrected"] = True
        ripeness_result["hybrid_confidence"] = cv_conf
        if "scores" in ripeness_result:
            new_scores = {}
            for k in ripeness_result["scores"]:
                new_scores[k] = cv_conf if k == "xanh" else round(
                    (1.0 - cv_conf) / max(1, len(ripeness_result["scores"]) - 1), 3
                )
            ripeness_result["scores"] = new_scores

        quality_result["is_hybrid_corrected"] = False

    # --- 5.4 XỬ LÝ CHUỐI CHÍN VÀNG BỊ ĐOÁN XANH ---
    elif is_ripe_cv and raw_dl_rip_class == "xanh":
        cv_conf = min(0.96, max(0.70, color_profile.get("yellow_pct", 50) / 60.0))
        ripeness_result["predicted_class"] = "chin"
        ripeness_result["predicted_display"] = "Chín (Hiệu chỉnh theo Thị Giác)"
        ripeness_result["is_hybrid_corrected"] = True
        ripeness_result["hybrid_confidence"] = cv_conf
        if "scores" in ripeness_result:
            new_scores = {}
            for k in ripeness_result["scores"]:
                new_scores[k] = cv_conf if k == "chin" else round(
                    (1.0 - cv_conf) / max(1, len(ripeness_result["scores"]) - 1), 3
                )
            ripeness_result["scores"] = new_scores

        quality_result["is_hybrid_corrected"] = False

    else:
        # Trường hợp bình thường: DL và XLA đồng thuận
        ripeness_result["is_hybrid_corrected"] = False
        quality_result["is_hybrid_corrected"] = False

    ret = {
        "ripeness": ripeness_result,
        "quality": quality_result,
        "ood_analysis": ood_info,
        "bg_removed": bg_removed,
        "bg_method": bg_method,
    }
    if ripeness_rgb_result is not None:
        ret["ripeness_rgb"] = ripeness_rgb_result

    return ret
