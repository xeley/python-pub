"""
Application shell (API layer).
Owns the event loop, startup/shutdown, and I/O adapter wiring.
Business logic is delegated entirely to Integrations and Operations.
"""
import time

from .adapters.camera import CameraAdapter
from .adapters.display import DisplayAdapter
from .adapters.yolo_model import YoloModelAdapter
from .data.models import DetectionConfig
from .integrations.detection import annotate_frame, detect_objects, measure_fps
from .operations.motion import is_frame_valid


def main() -> None:
    config = DetectionConfig()
    camera = CameraAdapter(config.camera_index)
    display = DisplayAdapter(config.window_title, config.display_width, config.display_height)
    model = YoloModelAdapter(config.model_name)

    if not camera.is_open():
        display.show_error("Camera unavailable — could not open camera feed.")
        return

    prev_time = time.time()

    while True:
        frame = camera.read()

        if not is_frame_valid(frame):
            display.show_error("Camera unavailable — lost camera feed.")
            break

        curr_time = time.time()
        fps = measure_fps(prev_time, curr_time)
        prev_time = curr_time

        detections = detect_objects(model, frame, config)
        annotated = annotate_frame(frame, detections, fps, config)
        display.show(annotated)

        key = display.read_key()
        if key == "q":
            break
        if key == "r":
            display.reset_size(config.display_width, config.display_height)

    camera.release()
    display.close()


if __name__ == "__main__":
    main()
