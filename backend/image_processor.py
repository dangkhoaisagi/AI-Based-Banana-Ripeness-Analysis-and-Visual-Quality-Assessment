"""
Module xử lý ảnh: decode, validate, resize.
Đầu vào cho model: float32, (224, 224, 3), range 0-255.
preprocess_input (ResNet50) nằm trong graph model => KHÔNG làm thêm.
"""
import io
import logging
import numpy as np
from pathlib import Path
from typing import Tuple

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
MAX_DIMENSION = 4096  # px
TARGET_SIZE = (224, 224)


def validate_and_decode(
    file_bytes: bytes,
    filename: str,
) -> np.ndarray:
    """
    Validate và decode ảnh. Trả về numpy array (224, 224, 3) float32 range 0-255.
    Ném ValueError với thông báo tiếng Việt nếu ảnh không hợp lệ.
    """
    # Kiểm tra dung lượng
    if len(file_bytes) > MAX_SIZE_BYTES:
        raise ValueError(
            f"Ảnh vượt giới hạn {MAX_SIZE_BYTES // (1024*1024)} MB "
            f"(kích thước hiện tại: {len(file_bytes) // (1024*1024)} MB)"
        )

    # Kiểm tra đuôi file
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Định dạng '{ext}' không được hỗ trợ. "
            f"Chấp nhận: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Thử decode bằng Pillow
    try:
        from PIL import Image
        pil_img = Image.open(io.BytesIO(file_bytes))
        pil_img.verify()  # Kiểm tra file không bị hỏng
    except Exception as e:
        raise ValueError(f"Không thể đọc ảnh (file có thể bị hỏng): {e}")

    # Load lại sau verify (verify đóng file stream)
    try:
        from PIL import Image
        pil_img = Image.open(io.BytesIO(file_bytes))

        # Kiểm tra kích thước
        w, h = pil_img.size
        if w > MAX_DIMENSION or h > MAX_DIMENSION:
            raise ValueError(
                f"Ảnh quá lớn ({w}x{h}px). "
                f"Tối đa {MAX_DIMENSION}x{MAX_DIMENSION}px."
            )

        # Chuyển sang RGB (xử lý RGBA, grayscale, palette)
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")

        # Resize về 224x224 bằng BICUBIC (nhất quán với Keras image_dataset_from_directory)
        pil_img = pil_img.resize(TARGET_SIZE, Image.BICUBIC)

        # Chuyển sang numpy float32 range 0-255
        img_array = np.array(pil_img, dtype=np.float32)  # (224, 224, 3)

        assert img_array.shape == (224, 224, 3), f"Shape bất ngờ: {img_array.shape}"
        return img_array

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Lỗi xử lý ảnh: {e}")


def load_image_from_path(image_path: str) -> np.ndarray:
    """Đọc ảnh từ đường dẫn file."""
    with open(image_path, "rb") as f:
        file_bytes = f.read()
    filename = Path(image_path).name
    return validate_and_decode(file_bytes, filename)
