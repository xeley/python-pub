"""Hand landmark detection using MediaPipe Tasks API (the "Brain")."""

import cv2
import mediapipe as mp
from mediapipe.tasks.python.core import base_options as base_options_module
from mediapipe.tasks.python.vision import hand_landmarker
from mediapipe.tasks.python.vision.core import vision_task_running_mode as running_mode_module

BaseOptions = base_options_module.BaseOptions
HandLandmarker = hand_landmarker.HandLandmarker
HandLandmarkerOptions = hand_landmarker.HandLandmarkerOptions
HandLandmarksConnections = hand_landmarker.HandLandmarksConnections
RunningMode = running_mode_module.VisionTaskRunningMode

# MediaPipe landmark index for index finger tip
INDEX_FINGER_TIP = 8


def create_hand_detector(
    model_path: str,
    max_num_hands: int = 1,
    min_detection_confidence: float = 0.7,
):
    """Create a MediaPipe HandLandmarker (Tasks API) for video mode."""
    base_options = BaseOptions(model_asset_path=model_path)
    options = HandLandmarkerOptions(
        base_options=base_options,
        running_mode=RunningMode.VIDEO,
        num_hands=max_num_hands,
        min_hand_detection_confidence=min_detection_confidence,
    )
    return HandLandmarker.create_from_options(options)


def process_hands(hands_detector, image_rgb, frame_timestamp_ms: int):
    """Process an RGB frame and return hand landmark results (Tasks API result)."""
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    return hands_detector.detect_for_video(mp_image, frame_timestamp_ms)


def _wrap_landmarks(landmarks_list):
    """Wrap a list of 21 landmarks so it has .landmark[i] for compatibility."""
    class HandLandmarksView:
        def __init__(self, landmarks):
            self.landmark = landmarks
    return HandLandmarksView(landmarks_list)


def result_to_multi_hand_landmarks(hand_landmarker_result):
    """Convert HandLandmarkerResult to list of hand landmark views (each has .landmark[i])."""
    if not hand_landmarker_result or not hand_landmarker_result.hand_landmarks:
        return []
    return [_wrap_landmarks(hl) for hl in hand_landmarker_result.hand_landmarks]


def draw_landmarks(image, hand_landmarks) -> None:
    """Draw the hand skeleton on the image in-place (Tasks API landmarks list)."""
    landmarks = hand_landmarks.landmark if hasattr(hand_landmarks, "landmark") else hand_landmarks
    h, w = image.shape[0], image.shape[1]
    for conn in HandLandmarksConnections.HAND_CONNECTIONS:
        start = landmarks[conn.start]
        end = landmarks[conn.end]
        x1, y1 = int(start.x * w), int(start.y * h)
        x2, y2 = int(end.x * w), int(end.y * h)
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    for lm in landmarks:
        cx, cy = int(lm.x * w), int(lm.y * h)
        cv2.circle(image, (cx, cy), 4, (0, 0, 255), -1)


def get_index_finger_xy(hand_landmarks, frame_width: int, frame_height: int) -> tuple[int, int]:
    """Get pixel (x, y) of the index finger tip from hand landmarks."""
    tip = hand_landmarks.landmark[INDEX_FINGER_TIP]
    x = int(tip.x * frame_width)
    y = int(tip.y * frame_height)
    return x, y


def frame_to_rgb(image_bgr):
    """Convert BGR image to RGB for MediaPipe."""
    return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
