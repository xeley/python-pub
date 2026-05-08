import cv2
import numpy as np


class DisplayAdapter:
    """Thin I/O boundary wrapping cv2 window output."""

    def __init__(self, window_title: str) -> None:
        self._title = window_title

    def show(self, frame: np.ndarray) -> None:
        cv2.imshow(self._title, frame)

    def show_error(self, message: str) -> None:
        print(f"[ERROR] {message}")

    def should_quit(self, wait_ms: int = 30) -> bool:
        return cv2.waitKey(wait_ms) & 0xFF == ord("q")

    def close(self) -> None:
        cv2.destroyAllWindows()
