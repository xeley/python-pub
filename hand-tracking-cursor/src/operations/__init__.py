"""Operations: logic using 3rd-party libraries (OpenCV, MediaPipe, PyAutoGUI)."""

from src.operations.camera import open_camera, read_frame, flip_frame, release_camera
from src.operations.hands import (
    create_hand_detector,
    process_hands,
    draw_landmarks,
    get_index_finger_xy,
    frame_to_rgb,
    result_to_multi_hand_landmarks,
)
from src.operations.mouse import get_screen_size, move_to
from src.operations.coordinates import map_to_screen, smooth_position
from src.operations.display import show_frame, wait_key, destroy_all_windows

__all__ = [
    "open_camera",
    "read_frame",
    "flip_frame",
    "release_camera",
    "create_hand_detector",
    "process_hands",
    "draw_landmarks",
    "get_index_finger_xy",
    "frame_to_rgb",
    "result_to_multi_hand_landmarks",
    "get_screen_size",
    "move_to",
    "map_to_screen",
    "smooth_position",
    "show_frame",
    "wait_key",
    "destroy_all_windows",
]
