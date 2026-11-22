"""
Module nạp và quản lý model.
- Nạp model một lần, tái sử dụng cho mỗi request.
- Dùng inference mode để tắt augmentation và dropout.
- preprocess_input nằm trong graph model => truyền pixel 0-255.
"""
import logging
import numpy as np
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class ModelLoader:
    """Quản lý việc nạp và tái sử dụng model Keras."""

    def __init__(self, config: dict):
        self.config = config
        self.model = None
        self.status = "not_loaded"
        self.error_message: Optional[str] = None
        self.input_shape: Optional[tuple] = None
        self.output_shape: Optional[tuple] = None
        self.num_classes: Optional[int] = None

    def load(self) -> bool:
        """Nạp model từ file .keras. Trả về True nếu thành công."""
        if self.config.get("enabled") is False:
            self.status = "disabled"
            self.error_message = self.config.get("not_ready_reason", "Bị tắt")
            return False

        keras_path = self.config.get("keras_path")
        if not keras_path or not Path(keras_path).exists():
            self.status = "file_missing"
            self.error_message = f"Không tìm thấy file model: {keras_path}"
            logger.error(self.error_message)
            return False

        try:
            import tensorflow as tf
            logger.info(f"Đang nạp model: {keras_path}")
            self.model = tf.keras.models.load_model(keras_path)

            # Xác minh input/output shape
            self.input_shape = tuple(self.model.input_shape)
            self.output_shape = tuple(self.model.output_shape)
            self.num_classes = self.output_shape[-1]

            # Kiểm tra số class khớp với config
            expected_classes = self.config.get("class_names")
            if expected_classes and len(expected_classes) != self.num_classes:
                msg = (
                    f"Số lớp model ({self.num_classes}) "
                    f"không khớp config ({len(expected_classes)})"
                )
                logger.error(msg)
                self.status = "shape_mismatch"
                self.error_message = msg
                return False

            self.status = "ready"
            logger.info(
                f"Model nạp thành công: {self.config['model_id']} "
                f"| input={self.input_shape} | output={self.output_shape}"
            )
            return True

        except Exception as e:
            self.status = "load_error"
            self.error_message = str(e)
            logger.exception(f"Lỗi nạp model {keras_path}: {e}")
            return False

    def predict(self, image_array: np.ndarray) -> Optional[np.ndarray]:
        """
        Dự đoán từ ảnh đã resize về (224, 224, 3), dtype float32, range 0-255.
        Model graph đã có preprocess_input và augmentation (tắt khi inference).
        Trả về mảng điểm softmax shape (num_classes,).
        """
        if self.model is None or self.status != "ready":
            raise RuntimeError(f"Model chưa sẵn sàng: {self.status}")

        # Thêm batch dimension
        img_batch = np.expand_dims(image_array, axis=0)  # (1, 224, 224, 3)

        # inference=True để tắt augmentation và dropout
        scores = self.model(img_batch, training=False)
        scores_np = scores.numpy()[0]  # (num_classes,)

        # Kiểm tra đầu ra hữu hạn
        if not np.all(np.isfinite(scores_np)):
            raise ValueError("Đầu ra model có giá trị vô cực hoặc NaN")

        return scores_np

    def get_info(self) -> dict:
        """Trả về thông tin trạng thái model."""
        return {
            "model_id": self.config["model_id"],
            "task": self.config["task"],
            "architecture": self.config["architecture"],
            "dataset": self.config["dataset"],
            "status": self.status,
            "error": self.error_message,
            "input_shape": list(self.input_shape) if self.input_shape else None,
            "output_shape": list(self.output_shape) if self.output_shape else None,
            "class_names": self.config.get("class_names"),
            "display_names": self.config.get("display_names", {}),
            "description_vi": self.config.get("description_vi", ""),
        }


# Registry toàn cục
_loaders: dict[str, ModelLoader] = {}


def initialize_models(configs: dict) -> None:
    """Nạp tất cả model được bật khi khởi động server."""
    import tensorflow as tf
    logger.info(f"TensorFlow {tf.__version__}")
    logger.info(f"Keras {tf.keras.__version__}")

    for model_id, cfg in configs.items():
        if cfg.get("enabled") is False:
            loader = ModelLoader(cfg)
            loader.status = "disabled"
            loader.error_message = cfg.get("not_ready_reason", "Bị tắt")
            _loaders[model_id] = loader
            logger.info(f"Model {model_id}: disabled")
            continue

        loader = ModelLoader(cfg)
        loader.load()
        _loaders[model_id] = loader


def get_loader(model_id: str) -> Optional[ModelLoader]:
    return _loaders.get(model_id)


def get_all_status() -> list[dict]:
    return [loader.get_info() for loader in _loaders.values()]
