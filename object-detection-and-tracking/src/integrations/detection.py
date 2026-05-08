"""
Integrations: linear call sequences only — no if/switch/loops.
Each function composes Operations and Adapters; no business logic lives here.
"""
import numpy as np

from ..adapters.yolo_model import YoloModelAdapter
from ..data.models import Detection, DetectionConfig
from ..operations.yolo import compute_fps, draw_detections, draw_fps, draw_key_hints, parse_yolo_detections


def detect_objects(
    model: YoloModelAdapter,
    frame: np.ndarray,
    config: DetectionConfig,
) -> list[Detection]:
    results = model.predict(frame)
    return parse_yolo_detections(results, config.confidence_threshold)


def measure_fps(prev_time: float, curr_time: float) -> float:
    return compute_fps(prev_time, curr_time)


def annotate_frame(
    frame: np.ndarray,
    detections: list[Detection],
    fps: float,
    config: DetectionConfig,
) -> np.ndarray:
    with_boxes = draw_detections(frame, detections, config.box_thickness)
    with_fps = draw_fps(with_boxes, fps)
    return draw_key_hints(with_fps, "q  quit    r  reset size    s  screenshot")
