"""Camera operations using OpenCV (the "Eyes")."""

from typing import Optional

import cv2


def open_camera(camera_index: int, api_preference: Optional[int] = None):
    """Open the default or specified webcam. Returns a VideoCapture object.
    api_preference: e.g. cv2.CAP_DSHOW (700) on Windows if default backend fails.
    """
    if api_preference is not None:
        return cv2.VideoCapture(camera_index, api_preference)
    return cv2.VideoCapture(camera_index)


def read_frame(cap) -> tuple[bool, object]:
    """Read the next frame from the camera. Returns (success, image)."""
    return cap.read()


def flip_frame(img, flip_code: int = 1):
    """Mirror the image horizontally so movement feels natural. Returns flipped image."""
    return cv2.flip(img, flip_code)


def release_camera(cap) -> None:
    """Release the camera resource."""
    cap.release()
