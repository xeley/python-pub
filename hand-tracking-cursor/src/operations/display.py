"""Display operations using OpenCV."""

import cv2


def show_frame(image, window_name: str) -> None:
    """Display the image in a named window."""
    cv2.imshow(window_name, image)


def wait_key(milliseconds: int) -> int:
    """Wait for a key event. Returns the key code or -1."""
    return cv2.waitKey(milliseconds) & 0xFF


def destroy_all_windows() -> None:
    """Close all OpenCV windows."""
    cv2.destroyAllWindows()
