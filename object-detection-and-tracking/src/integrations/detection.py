"""
Integrations: linear call sequences only — no if/switch/loops.
Each function composes Operations and Adapters; no business logic lives here.
"""
import numpy as np

from ..adapters.yolo_model import YoloModelAdapter
from ..data.models import Detection, DetectionConfig
from ..operations.yolo import draw_detections, parse_yolo_detections


def detect_objects(
    model: YoloModelAdapter,
    frame: np.ndarray,
    config: DetectionConfig,
) -> list[Detection]:
    results = model.predict(frame)
    return parse_yolo_detections(results, config.confidence_threshold)


def annotate_frame(
    frame: np.ndarray,
    detections: list[Detection],
    config: DetectionConfig,
) -> np.ndarray:
    return draw_detections(frame, detections, config.box_thickness)
