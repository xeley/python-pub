"""
Application shell (API layer).
Owns the event loop, startup/shutdown, and I/O adapter wiring.
Business logic is delegated entirely to Integrations and Operations.
"""
from .adapters.camera import CameraAdapter
from .adapters.display import DisplayAdapter
from .adapters.yolo_model import YoloModelAdapter
from .data.models import DetectionConfig
from .integrations.detection import annotate_frame, detect_objects
from .operations.motion import is_frame_valid


def main() -> None:
    config = DetectionConfig()
    camera = CameraAdapter(config.camera_index)
    display = DisplayAdapter(config.window_title)
    model = YoloModelAdapter(config.model_name)

    if not camera.is_open():
        display.show_error("Camera unavailable — could not open camera feed.")
        return

    while True:
        frame = camera.read()

        if not is_frame_valid(frame):
            display.show_error("Camera unavailable — lost camera feed.")
            break

        detections = detect_objects(model, frame, config)
        annotated = annotate_frame(frame, detections, config)
        display.show(annotated)

        if display.should_quit():
            break

    camera.release()
    display.close()


if __name__ == "__main__":
    main()
