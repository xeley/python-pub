import cv2
import numpy as np


class DisplayAdapter:
    """Thin I/O boundary wrapping cv2 window output."""

    def __init__(self, window_title: str, width: int, height: int) -> None:
        self._title = window_title
        cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_title, width, height)

    def show(self, frame: np.ndarray) -> None:
        cv2.imshow(self._title, frame)

    def show_error(self, message: str) -> None:
        print(f"[ERROR] {message}")

    def read_key(self, wait_ms: int = 30) -> str | None:
        code = cv2.waitKey(wait_ms) & 0xFF
        return chr(code) if code != 255 else None

    def reset_size(self, width: int, height: int) -> None:
        cv2.resizeWindow(self._title, width, height)

    def close(self) -> None:
        cv2.destroyAllWindows()
