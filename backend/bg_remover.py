"""
Module tách nền ảnh chuối thông minh:
1. Giai đoạn 1: AI salient segmentation bằng rembg (U2Net/U2Net_lite)
2. Giai đoạn 2: Tự động phục hồi bằng thị giác máy tính XLA (HSV Color Segmentation)
   khi rembg gặp ảnh ngoài trời (cây chuối, lá cây, buồng chuối trong vườn) làm mất chuối.
Kết quả: Tách biệt quả chuối khỏi nền, loại bỏ nhiễu ánh sáng và môi trường ngoài.
"""
import logging
import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

_rembg_session: Optional[object] = None
_rembg_available: bool = False


def _get_session():
    """Khởi tạo rembg session lần đầu (lazy init). Ưu tiên u2net đã có sẵn cục bộ."""
    global _rembg_session, _rembg_available
    if _rembg_session is not None:
        return _rembg_session

    try:
        from rembg import new_session
        import os
        from pathlib import Path
        # Kiểm tra file model đã có sẵn trên máy để load tức thì
        user_home = Path.home()
        u2net_path = user_home / ".u2net" / "u2net.onnx"
        model_name = "u2net" if u2net_path.exists() else "u2net_lite"
        _rembg_session = new_session(model_name)
        _rembg_available = True
        logger.info(f"rembg ({model_name}): sẵn sàng")
    except Exception as e:
        _rembg_available = False
        logger.warning(f"rembg không khả dụng: {e}")
        _rembg_session = None

    return _rembg_session


def is_available() -> bool:
    """Kiểm tra chức năng tách nền sẵn sàng."""
    return True


def segment_banana_by_color(img_rgb: np.ndarray) -> np.ndarray:
    """
    Phân đoạn vùng quả chuối bằng xử lý ảnh số (XLA - HSV color morphology).
    Đặc biệt hiệu quả cho ảnh chụp thực tế ngoài vườn / trên cây chuối.
    """
    img_uint8 = np.clip(img_rgb, 0, 255).astype(np.uint8)
    hsv = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2HSV)

    # 1. Sắc xanh chuối: H in [30, 88], S in [35, 255], V in [30, 255]
    green_mask = cv2.inRange(hsv, np.array([30, 35, 30]), np.array([88, 255, 255]))

    # 2. Sắc vàng chuối: H in [16, 36], S in [40, 255], V in [60, 255]
    yellow_mask = cv2.inRange(hsv, np.array([16, 40, 60]), np.array([36, 255, 255]))

    # 3. Vùng chuối nẫu / đốm thâm: H in [5, 35], S in [20, 230], V in [15, 110]
    brown_mask = cv2.inRange(hsv, np.array([5, 20, 15]), np.array([35, 230, 110]))

    # 4. Vùng chuối thối cực đậm: chỉ lấy sắc ấm nâu-đỏ tối H in [0, 35] hoặc [160, 180], tránh lấy nền đen xanh/xám
    very_dark_mask1 = cv2.inRange(hsv, np.array([0, 15, 8]), np.array([35, 255, 60]))
    very_dark_mask2 = cv2.inRange(hsv, np.array([160, 15, 8]), np.array([180, 255, 60]))
    very_dark_mask = cv2.bitwise_or(very_dark_mask1, very_dark_mask2)

    banana_mask = cv2.bitwise_or(green_mask, yellow_mask)
    banana_mask = cv2.bitwise_or(banana_mask, brown_mask)
    banana_mask = cv2.bitwise_or(banana_mask, very_dark_mask)

    # Khử nhiễu và nối liền các nải chuối bằng hình thái học (Morphology)
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    clean_mask = cv2.morphologyEx(banana_mask, cv2.MORPH_CLOSE, kernel_close, iterations=2)
    clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_OPEN, kernel_open, iterations=1)

    # Lọc thành phần liên thông: loại bỏ các đốm nhỏ rời rạc của nền
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(clean_mask, connectivity=8)
    if num_labels > 1:
        min_area = img_rgb.shape[0] * img_rgb.shape[1] * 0.02
        filtered_mask = np.zeros_like(clean_mask)
        for i in range(1, num_labels):
            if stats[i, cv2.CC_STAT_AREA] >= min_area:
                filtered_mask[labels == i] = 255
        clean_mask = filtered_mask

    return clean_mask > 0


def remove_background(
    img_array: np.ndarray,
    bg_color: Tuple[int, int, int] = (245, 245, 245),
) -> Tuple[np.ndarray, np.ndarray, str]:
    """
    Tách nền thông minh đa tầng:
    - Thử rembg trước.
    - Nếu rembg bị lỗi hoặc trả về vùng quả quá nhỏ (< 12%) hoặc quá lớn (> 95%),
      kích hoạt thuật toán phân đoạn quang phổ màu XLA để giữ trọn vẹn buồng/quả chuối.

    Returns:
        (img_no_bg, fg_mask, method_used)
    """
    h, w = img_array.shape[:2]
    img_uint8 = np.clip(img_array, 0, 255).astype(np.uint8)

    fg_mask = None
    method = "none"

    # Thử rembg nếu có
    session = _get_session()
    if session is not None:
        try:
            from rembg import remove
            pil_in = Image.fromarray(img_uint8, mode="RGB")
            pil_rgba = remove(pil_in, session=session)
            rgba = np.array(pil_rgba, dtype=np.uint8)
            alpha = rgba[:, :, 3]
            candidate_mask = alpha > 127
            ratio = candidate_mask.mean()

            # rembg hợp lệ nếu nhận diện được 12% - 85% diện tích ảnh là đối tượng
            if 0.12 <= ratio <= 0.85:
                fg_mask = candidate_mask
                method = "rembg_ai"
                logger.info(f"rembg AI tách nền thành công: {ratio*100:.1f}% foreground")
            else:
                logger.info(f"rembg ratio ({ratio*100:.1f}%) ngoài dải hợp lý, chuyển sang XLA CV")
        except Exception as e:
            logger.warning(f"rembg gặp sự cố: {e}, chuyển sang XLA CV")

    # Nếu rembg không đạt yêu cầu, dùng phân đoạn màu XLA
    if fg_mask is None:
        cv_mask = segment_banana_by_color(img_array)
        cv_ratio = cv_mask.mean()
        if cv_ratio >= 0.15:
            fg_mask = cv_mask
            method = "xla_color_segmentation"
            logger.info(f"XLA Color Segmentation tách nền thành công: {cv_ratio*100:.1f}% chuối")
        else:
            # Fallback an toàn: giữ nguyên toàn bộ ảnh nếu không chắc chắn
            fg_mask = np.ones((h, w), dtype=bool)
            method = "passthrough"
            logger.info("Giữ ảnh gốc để đảm bảo thông tin nguyên vẹn")

    # Tạo ảnh sau khi tách nền
    rgb = img_uint8.copy()
    bg = np.array(bg_color, dtype=np.uint8)
    rgb[~fg_mask] = bg
    img_no_bg = rgb.astype(np.float32)

    return img_no_bg, fg_mask, method

