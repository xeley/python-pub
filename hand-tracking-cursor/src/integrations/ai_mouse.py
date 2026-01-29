"""AI Mouse integration: connects eyes (camera), brain (hand detection), and act (mouse)."""

from pathlib import Path

import src.config as config
from src.operations import (
    open_camera,
    read_frame,
    flip_frame,
    release_camera,
    create_hand_detector,
    process_hands,
    draw_landmarks,
    get_index_finger_xy,
    frame_to_rgb,
    result_to_multi_hand_landmarks,
    get_screen_size,
    move_to,
    map_to_screen,
    smooth_position,
    show_frame,
    wait_key,
    destroy_all_windows,
)


def run_ai_mouse() -> None:
    """Run the hand-tracking mouse controller. Press config.QUIT_KEY to exit."""
    project_root = Path(__file__).resolve().parent.parent.parent
    model_path = project_root / config.HAND_LANDMARKER_MODEL_PATH
    if not model_path.is_file():
        print(f"Model not found: {model_path}")
        print("Download hand_landmarker.task from:")
        print("  https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task")
        print(f"and save it as: {model_path}")
        return

    cap = open_camera(config.CAMERA_INDEX, getattr(config, "CAMERA_API", None))
    hands = create_hand_detector(
        str(model_path),
        max_num_hands=config.MAX_NUM_HANDS,
        min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
    )
    screen_width, screen_height = get_screen_size()

    ploc_x, ploc_y = 0.0, 0.0
    frame_timestamp_ms = 0

    print("AI Mouse Active. Press 'q' to quit.")

    try:
        while True:
            success, img = read_frame(cap)
            if not success:
                break

            img = flip_frame(img)
            frame_height, frame_width = img.shape[0], img.shape[1]
            img_rgb = frame_to_rgb(img)

            results = process_hands(hands, img_rgb, frame_timestamp_ms)
            frame_timestamp_ms += 33  # ~30 fps

            multi_hand_landmarks = result_to_multi_hand_landmarks(results)
            if multi_hand_landmarks:
                for hand_landmarks in multi_hand_landmarks:
                    draw_landmarks(img, hand_landmarks)

                    x, y = get_index_finger_xy(hand_landmarks, frame_width, frame_height)
                    mouse_x, mouse_y = map_to_screen(
                        x, y, frame_width, frame_height, screen_width, screen_height
                    )
                    cloc_x, cloc_y = smooth_position(
                        ploc_x, ploc_y, mouse_x, mouse_y, config.SMOOTHING
                    )

                    move_to(cloc_x, cloc_y)
                    ploc_x, ploc_y = cloc_x, cloc_y

            show_frame(img, config.WINDOW_NAME)

            if wait_key(1) == ord(config.QUIT_KEY):
                break
    finally:
        release_camera(cap)
        destroy_all_windows()
