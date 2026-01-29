"""Configuration for the hand-tracking mouse controller."""

# Cursor movement: higher = smoother but more lag
SMOOTHING = 5

# Camera
CAMERA_INDEX = 0
# On Windows, use 700 (cv2.CAP_DSHOW) if the default backend fails to grab frames (e.g. MSMF -1072875772).
# Use None for default backend.
CAMERA_API = 700  # cv2.CAP_DSHOW

# Hand detection (MediaPipe Tasks API)
# Path to hand_landmarker.task (relative to project root). Download from:
# https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
HAND_LANDMARKER_MODEL_PATH = "models/hand_landmarker.task"
MAX_NUM_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.7

# Display
WINDOW_NAME = "AI Mouse Controller"
QUIT_KEY = "q"
