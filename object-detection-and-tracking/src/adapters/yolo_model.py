import numpy as np
from ultralytics import YOLO


class YoloModelAdapter:
    """Thin I/O boundary wrapping ultralytics YOLO inference."""

    def __init__(self, model_name: str) -> None:
        self._model = YOLO(model_name)

    def predict(self, frame: np.ndarray):
        return self._model(frame, verbose=False)
