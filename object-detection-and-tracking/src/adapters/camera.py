import cv2
import numpy as np


class CameraAdapter:
    """Thin I/O boundary wrapping cv2.VideoCapture."""

    def __init__(self, camera_index: int = 0) -> None:
        self._cap = cv2.VideoCapture(camera_index)

    def is_open(self) -> bool:
        return self._cap.isOpened()

    def read(self) -> np.ndarray | None:
        success, frame = self._cap.read()
        return frame if success else None

    def release(self) -> None:
        self._cap.release()
