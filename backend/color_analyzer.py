"""
Module phan tich pho mau va phat hien Out-of-Distribution (OOD) / Contradiction.
Su dung khong gian mau HSV de phan tich ty le sac thai thuc te cua qua chuoi.

Phien ban v4 - Hieu chinh can bang toan dien cho tat ca cac truong hop:
  - Phan loai mau khong chong cheo (Mutually Exclusive HSV Segmentation):
      + dark_heavy: thoi đen / hoai tu (V < 0.22 hoac nau sam toi V <= 0.30)
      + dark_light: dom nau tham doi moi / qua chin (V in 0.22 - 0.52)
      + dark_brown: tong hop ca 2 tang (dark_light | dark_heavy)
      + green & cyan: sac xanh thuan va xanh lam ngoc (Blue Java)
      + yellow: vang chin tu nhien, khong chong lan voi nau hay xanh
  - Tinh toan rotten_score da yeu to (dark_heavy + dark_spot + dark_brown + entropy)
  - Nhan dien ro net 4 trang thai: Thoi, Qua chin / Dom, Chin, Xanh
  - Co che Hybrid OOD Contradiction dong bo chat che voi ca Ripeness va Quality
"""
import logging
import numpy as np
from PIL import Image
from typing import Dict, Any, Tuple, Optional

logger = logging.getLogger(__name__)


def rgb_to_hsv_array(img_rgb: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Chuyen doi anh RGB sang H, S, V.
    H: [0, 360], S: [0, 1], V: [0, 1].
    """
    if img_rgb.dtype != np.uint8:
        img_uint8 = np.clip(img_rgb, 0, 255).astype(np.uint8)
    else:
        img_uint8 = img_rgb

    pil_img = Image.fromarray(img_uint8, mode="RGB")
    hsv_pil = pil_img.convert("HSV")
    hsv_arr = np.array(hsv_pil, dtype=np.float32)

    H = hsv_arr[:, :, 0] * (360.0 / 255.0)
    S = hsv_arr[:, :, 1] / 255.0
    V = hsv_arr[:, :, 2] / 255.0

    return H, S, V


def compute_texture_entropy(img_rgb: np.ndarray, fg_mask: Optional[np.ndarray] = None) -> float:
    """
    Tinh entropy do xam tren vung chuoi.
    Chuoi xanh/chin deu: entropy thap (~2.5-3.5)
    Chuoi qua chin / dom: entropy trung binh (~3.5-4.2)
    Chuoi thoi nang: entropy cao (~4.2-5.0)
    """
    try:
        img_uint8 = np.clip(img_rgb, 0, 255).astype(np.uint8)
        gray = (0.299 * img_uint8[:, :, 0]
                + 0.587 * img_uint8[:, :, 1]
                + 0.114 * img_uint8[:, :, 2]).astype(np.uint8)

        if fg_mask is not None and fg_mask.sum() > 50:
            gray_pixels = gray[fg_mask]
        else:
            gray_pixels = gray.flatten()

        if gray_pixels.size < 50:
            return 0.0

        hist, _ = np.histogram(gray_pixels, bins=32, range=(0, 256))
        hist = hist.astype(np.float64)
        total = hist.sum()
        if total == 0:
            return 0.0
        probs = hist / total
        probs = probs[probs > 0]
        entropy = -np.sum(probs * np.log2(probs))
        return float(entropy)
    except Exception:
        return 0.0


def compute_dark_spot_ratio(img_rgb: np.ndarray, fg_mask: Optional[np.ndarray] = None) -> float:
    """
    Ty le vung cuc toi (luminance < 25%) tren dien tich qua chuoi.
    Dau hieu dac trung cua dom thoi hoai tu tren vo chuoi.
    """
    try:
        img_uint8 = np.clip(img_rgb, 0, 255).astype(np.uint8)
        gray = (0.299 * img_uint8[:, :, 0]
                + 0.587 * img_uint8[:, :, 1]
                + 0.114 * img_uint8[:, :, 2])
        very_dark = gray < (0.25 * 255)

        if fg_mask is not None and fg_mask.sum() > 50:
            total = float(fg_mask.sum())
            dark_in_fg = float(np.sum(very_dark & fg_mask))
        else:
            total = float(gray.size)
            dark_in_fg = float(np.sum(very_dark))

        return dark_in_fg / max(1.0, total)
    except Exception:
        return 0.0


def analyze_banana_colors(
    img_rgb: np.ndarray,
    fg_mask: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    """
    Phan tich ty le mau sac qua chuoi voi do phan chia quang pho khong chong cheo.
    """
    H, S, V = rgb_to_hsv_array(img_rgb)

    # 1. Xac dinh vung qua chuoi hop le
    if fg_mask is not None and fg_mask.sum() > 50:
        # Loai bo pixel nen trang phong lab / chói gat tuyet doi (S < 0.04 & V > 0.95)
        valid_banana = fg_mask & ~((S < 0.04) & (V > 0.95))
        if valid_banana.sum() < 50:
            valid_banana = fg_mask
    else:
        # Khi khong co mask tach nen: loai bo pixel qua trang hoac qua den vo nghia
        valid_banana = ~((S < 0.05) & (V > 0.92)) & ~((S < 0.04) & (V < 0.04))
        if valid_banana.sum() < 50:
            valid_banana = np.ones(H.shape, dtype=bool)

    total_banana_pixels = max(1.0, float(np.sum(valid_banana)))

    # 2. MASK THOI DEN / NAU DAM HOAI TU (dark_heavy)
    # - Gan den hoan toan: V < 0.22, co mau S >= 0.04
    # - Nau toi dam: Hue 0-42 hoac >=340, S >= 0.12, V <= 0.30
    dark_heavy_mask = (
        (
            ((V < 0.22) & (S >= 0.04))
            | (((H <= 42) | (H >= 340)) & (S >= 0.12) & (V <= 0.30))
        )
        & valid_banana
    )

    # 3. MASK DOM NAU / QUA CHIN (dark_light)
    # - Vung dom doi moi tham nau: Hue 8-38 hoac >=345, S >= 0.14, V 0.22 - 0.52
    # - Tuyet doi khong trung voi dark_heavy
    dark_light_mask = (
        (
            (((H >= 8) & (H <= 38)) | (H >= 345))
            & (S >= 0.14) & (V > 0.22) & (V <= 0.52)
        )
        & valid_banana
        & ~dark_heavy_mask
    )

    # Tong hop vung tham nau / dom hoai tu
    dark_brown_mask = dark_heavy_mask | dark_light_mask

    # 4. MASK XANH LA (green - chua chin)
    # H: 62 - 155 deg, S >= 0.15, V >= 0.12
    green_mask = (
        (H >= 62) & (H <= 155)
        & (S >= 0.15) & (V >= 0.12)
        & valid_banana
        & ~dark_brown_mask
    )

    # 5. MASK XANH LAM NGOC (cyan - Blue Java, phu phan sap)
    # H: 155 - 225 deg, S >= 0.07, V >= 0.14
    cyan_mask = (
        (H > 155) & (H <= 225)
        & (S >= 0.07) & (V >= 0.14)
        & valid_banana
        & ~dark_brown_mask
    )

    unripe_mask = green_mask | cyan_mask

    # 6. MASK VANG CHIN (yellow - chin deu, thom ngon)
    # - Vang chuoi tieu chuan: H in [33, 62], S >= 0.16, V >= 0.30
    # - Vang cam chin dam: H in [24, 33], S >= 0.22, V >= 0.48
    # - Tuyet doi khong trung voi vung dom thoi hay xanh
    yellow_mask = (
        (
            ((H >= 33) & (H < 62) & (S >= 0.16) & (V >= 0.30))
            | ((H >= 24) & (H < 33) & (S >= 0.22) & (V >= 0.48))
        )
        & valid_banana
        & ~dark_brown_mask
        & ~unripe_mask
    )

    # Ty le phan tram mau tren dien tich qua chuoi
    green_pct        = float(np.sum(green_mask)       / total_banana_pixels * 100.0)
    cyan_pct         = float(np.sum(cyan_mask)        / total_banana_pixels * 100.0)
    unripe_total_pct = float(np.sum(unripe_mask)      / total_banana_pixels * 100.0)
    yellow_pct       = float(np.sum(yellow_mask)      / total_banana_pixels * 100.0)
    dark_light_pct   = float(np.sum(dark_light_mask)  / total_banana_pixels * 100.0)
    dark_heavy_pct   = float(np.sum(dark_heavy_mask)  / total_banana_pixels * 100.0)
    dark_brown_pct   = float(np.sum(dark_brown_mask)  / total_banana_pixels * 100.0)

    # Thong ke sac thai trung binh
    banana_H = H[valid_banana]
    banana_S = S[valid_banana]
    banana_V = V[valid_banana]
    mean_hue = float(np.mean(banana_H)) if banana_H.size > 0 else 0.0
    mean_sat = float(np.mean(banana_S)) if banana_S.size > 0 else 0.0
    mean_val = float(np.mean(banana_V)) if banana_V.size > 0 else 0.0

    # Texture & dom toi
    texture_entropy = compute_texture_entropy(img_rgb, fg_mask)
    dark_spot_ratio = compute_dark_spot_ratio(img_rgb, fg_mask)
    dark_spot_pct   = dark_spot_ratio * 100.0

    # Diem thoi hong toan dien (Rotten Score: 0 - 100)
    rotten_score = (
        dark_heavy_pct * 0.50
        + dark_spot_pct * 0.30
        + max(0.0, dark_brown_pct - 20.0) * 0.30
        + max(0.0, texture_entropy - 3.2) * 5.0
    )
    rotten_score = min(100.0, max(0.0, rotten_score))

    # --- NHAN DIEN TRANG THAI THEO QUANG PHO THUC TE ---

    # 1. THOI HONG RO RET:
    # - dark_heavy >= 28%
    # - hoac (dark_spot >= 22% va dark_brown >= 32%)
    # - hoac dark_brown >= 60%
    # - hoac rotten_score >= 45
    # (dieu kien bao ve: unripe < 20% de khong nham chuoi xanh co cuong toi)
    is_clearly_rotten = (
        (
            (dark_heavy_pct >= 28.0)
            or (dark_spot_pct >= 22.0 and dark_brown_pct >= 32.0)
            or (dark_brown_pct >= 60.0)
            or (rotten_score >= 45.0)
        )
        and unripe_total_pct < 20.0
        and mean_val < 0.58
    )

    # 2. QUA CHIN / DOM DOI MOI:
    # - Co mang tham nau dang ke: dark_brown >= 25% hoac dark_spot >= 18%
    # - Con giu sac vang dac trung: yellow >= 12%
    # - Khong phai thoi nang va khong xanh
    is_overripe = (
        (dark_brown_pct >= 25.0 or dark_spot_pct >= 18.0)
        and yellow_pct >= 12.0
        and unripe_total_pct < 18.0
        and not is_clearly_rotten
    )

    # 3. XANH (CHUA CHIN):
    # - Sac xanh chiem uu the: unripe_total >= 25%
    # - Vuot troi so voi vang va khong co dom thoi
    is_unripe = (
        unripe_total_pct >= 25.0
        and unripe_total_pct > yellow_pct * 1.3
        and dark_heavy_pct < 15.0
        and not is_clearly_rotten
    )

    # 4. CHIN VANG:
    # - Sac vang chiem uu the: yellow >= 28%
    # - Vang ap dao xanh va it tham nau (< 25%)
    is_ripe = (
        yellow_pct >= 28.0
        and yellow_pct > unripe_total_pct
        and dark_brown_pct < 25.0
        and not is_clearly_rotten
        and not is_overripe
    )

    # Ket luan thi giac may tinh (CV Verdict)
    if is_clearly_rotten:
        cv_verdict      = "thoi"
        cv_display      = "Thoi / Hong (Nau đen chiem dien rong)"
        cv_confidence   = min(0.98, max(0.78, rotten_score / 80.0))
        cv_quality_hint = "thoi"

    elif is_overripe:
        cv_verdict      = "qua_chin"
        cv_display      = "Qua chin (Nhieu dom tham nau)"
        cv_confidence   = min(0.94, max(0.68, dark_brown_pct / 55.0))
        cv_quality_hint = "dom"

    elif is_unripe:
        cv_verdict      = "xanh"
        cv_display      = "Xanh (Chuoi chua chin)"
        cv_confidence   = min(0.98, max(0.72, unripe_total_pct / 65.0))
        cv_quality_hint = "tot"

    elif is_ripe:
        cv_verdict      = "chin"
        cv_display      = "Chin (Sac to vang chiem uu the)"
        cv_confidence   = min(0.97, max(0.70, yellow_pct / 65.0))
        cv_quality_hint = "tot"

    else:
        # Vung chuyen tiep / Uong: so sanh truc tiep
        candidates = [
            ("thoi",     dark_heavy_pct * 1.2),
            ("qua_chin", dark_brown_pct),
            ("xanh",     unripe_total_pct),
            ("chin",     yellow_pct),
        ]
        dominant = max(candidates, key=lambda x: x[1])[0]
        cv_verdict = dominant
        if dominant == "thoi":
            cv_display      = "Nghieng ve Thoi / Hong"
            cv_confidence   = 0.65
            cv_quality_hint = "thoi"
        elif dominant == "qua_chin":
            cv_display      = "Nghieng ve Qua chin / Nau"
            cv_confidence   = 0.65
            cv_quality_hint = "dom"
        elif dominant == "xanh":
            cv_display      = "Nghieng ve Xanh"
            cv_confidence   = 0.65
            cv_quality_hint = "tot"
        else:
            cv_display      = "Nghieng ve Chin"
            cv_confidence   = 0.65
            cv_quality_hint = "tot"

    return {
        "green_pct":         round(green_pct, 1),
        "cyan_pct":          round(cyan_pct, 1),
        "unripe_total_pct":  round(unripe_total_pct, 1),
        "yellow_pct":        round(yellow_pct, 1),
        "dark_light_pct":    round(dark_light_pct, 1),
        "dark_heavy_pct":    round(dark_heavy_pct, 1),
        "dark_brown_pct":    round(dark_brown_pct, 1),
        "dark_spot_pct":     round(dark_spot_pct, 1),
        "texture_entropy":   round(texture_entropy, 2),
        "rotten_score":      round(rotten_score, 1),
        "mean_hue":          round(mean_hue, 1),
        "mean_sat":          round(mean_sat, 2),
        "mean_val":          round(mean_val, 2),
        "cv_verdict":        cv_verdict,
        "cv_display":        cv_display,
        "cv_confidence":     round(cv_confidence, 2),
        "cv_quality_hint":   cv_quality_hint,
        "is_clearly_rotten": bool(is_clearly_rotten),
        "is_overripe":       bool(is_overripe),
        "is_unripe":         bool(is_unripe),
        "is_ripe":           bool(is_ripe),
    }


def evaluate_ood_and_contradiction(
    img_rgb: np.ndarray,
    ripeness_result: Dict[str, Any],
    fg_mask: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    """
    So sanh ket qua Deep Learning voi phan tich pho mau XLA.
    Tu dong hieu chinh khi co mau thuan ro rang (Hybrid Decision Fusion).
    """
    color_profile = analyze_banana_colors(img_rgb, fg_mask=fg_mask)

    dl_class  = ripeness_result.get("predicted_class")
    scores    = ripeness_result.get("scores", {})
    dl_score  = scores.get(dl_class, 0.0)

    is_ood            = False
    is_contradiction  = False
    warning_title     = None
    warning_message   = None
    scientific_explanation = None
    recommended_class   = dl_class
    recommended_display = ripeness_result.get("predicted_display", dl_class)

    unripe_pct        = color_profile["unripe_total_pct"]
    cyan_pct          = color_profile["cyan_pct"]
    yellow_pct        = color_profile["yellow_pct"]
    dark_light_pct    = color_profile["dark_light_pct"]
    dark_heavy_pct    = color_profile["dark_heavy_pct"]
    dark_brown_pct    = color_profile["dark_brown_pct"]
    dark_spot_pct     = color_profile["dark_spot_pct"]
    rotten_score      = color_profile["rotten_score"]
    texture_entropy   = color_profile["texture_entropy"]
    is_clearly_rotten = color_profile["is_clearly_rotten"]
    is_overripe       = color_profile["is_overripe"]
    is_unripe         = color_profile["is_unripe"]
    is_ripe           = color_profile["is_ripe"]
    cv_quality_hint   = color_profile.get("cv_quality_hint", "tot")

    # KICH BAN 1 (UU TIEN CAO NHAT: CHUOI THOI NANG BI DOAN SAI LA XANH HOAC CHIN):
    if is_clearly_rotten and dl_class in ("xanh", "chin"):
        is_ood = True
        is_contradiction = True
        recommended_class   = "qua_chin"
        recommended_display = "Thoi / Hong (Hieu chinh theo Phan Tich Thi Giac)"
        warning_title       = "Canh Bao: Chuoi Thoi Nau - Model Deep Learning Nhan Dien Sai"
        warning_message     = (
            f"Model Deep Learning du doan '{dl_class}' ({dl_score*100:.1f}%), "
            f"nhung thi giac may tinh phat hien hoai tu nang: "
            f"nau sam/den={dark_heavy_pct:.1f}%, tong tham={dark_brown_pct:.1f}%, "
            f"diem toi={dark_spot_pct:.1f}% (Rotten Score={rotten_score:.0f}/100)."
        )
        scientific_explanation = (
            "Chuoi thoi nau ngoai thuc te co vo chuyen sang mau nau den loang lo voi "
            "do phuc tap be mat cao (entropy >= 3.8). Mang no-ron ResNet50 huan luyen "
            "tren chuoi phong lab khong the nhan dien phan phoi anh nay (Out-of-Distribution). "
            "He thong thi giac XLA da tu dong hieu chinh ket qua ve Quá chín / Thối."
        )

    # KICH BAN 2: CHUOI QUA CHIN / NHIEU DOM NAU BI DOAN SAI LA XANH HOAC CHIN:
    elif is_overripe and dl_class in ("xanh", "chin"):
        is_ood = True
        is_contradiction = True
        recommended_class   = "qua_chin"
        recommended_display = "Qua chin / Dom (Hieu chinh theo Phan Tich Thi Giac)"
        dl_name = "Xanh" if dl_class == "xanh" else "Chin"
        warning_title       = f"Hieu Chinh: Chuoi Qua Chin / Dom Bi Doan '{dl_name}'"
        warning_message     = (
            f"Model du doan '{dl_name}' ({dl_score*100:.1f}%), "
            f"nhung XLA phat hien {dark_brown_pct:.1f}% mang tham nau / dom "
            f"va {yellow_pct:.1f}% vang - chuoi da qua do chin ly tuong."
        )
        scientific_explanation = (
            "Chuoi qua chin co vo xuat hien nhieu dom tham doi moi (sugar spots). "
            "Thuat toan XLA phan tach dom nau da xac dinh qua chuoi o giai doan Qua chin."
        )

    # KICH BAN 3: CHUOI XANH / BLUE JAVA BI DOAN SAI LA CHIN HOAC QUA CHIN:
    elif is_unripe and dl_class in ("qua_chin", "chin"):
        is_ood = True
        is_contradiction = True
        recommended_class   = "xanh"
        recommended_display = "Xanh (Hieu chinh theo Phan Tich Thi Giac May Tinh)"
        warning_title       = "Canh Bao: Vo Chuoi Mau Xanh nhung Model Du Doan Chin"
        variety_note = (
            "Anh chua qua chuoi co sac xanh lam ngoc / anh bac (Blue Java hoac phu sap). "
            if cyan_pct >= 8.0
            else "Anh chua qua chuoi co sac xanh luc chiem uu the ro ret. "
        )
        dl_name = "Qua chin" if dl_class == "qua_chin" else "Chin"
        warning_message = (
            f"Model du doan '{dl_name}' ({dl_score*100:.1f}%), "
            f"nhung XLA phat hien {unripe_pct:.1f}% sac xanh "
            f"(vang chi co {yellow_pct:.1f}%)."
        )
        scientific_explanation = (
            f"{variety_note}"
            "Hien tuong mang no-ron bi anh huong boi cuong hoac moi truong sang phong lab "
            "da duoc phat hien va khac phuc boi bo loc thi giac HSV."
        )

    # KICH BAN 4: CHUOI CHIN VANG BI DOAN SAI LA XANH:
    elif is_ripe and dl_class == "xanh" and yellow_pct >= 30.0:
        is_ood = True
        is_contradiction = True
        recommended_class   = "chin"
        recommended_display = "Chin (Hieu chinh theo Phan Tich Thi Giac May Tinh)"
        warning_title       = "Canh Bao: Chuoi Vang Chin nhung Model Du Doan Xanh"
        warning_message     = (
            f"Model du doan 'Xanh' ({dl_score*100:.1f}%), "
            f"nhung sac vang thuc te dat {yellow_pct:.1f}% "
            f"(xanh chi con {unripe_pct:.1f}%)."
        )
        scientific_explanation = (
            "Mau vang chuoi chiem uu the tren be mat qua chuoi. "
            "Bo loc mau XLA da xac nhan chuoi da chin vang deu."
        )

    return {
        "color_profile":          color_profile,
        "is_ood":                 is_ood,
        "is_contradiction":       is_contradiction,
        "warning_title":          warning_title,
        "warning_message":        warning_message,
        "scientific_explanation": scientific_explanation,
        "recommended_class":      recommended_class,
        "recommended_display":    recommended_display,
        "cv_quality_hint":        cv_quality_hint,
    }
