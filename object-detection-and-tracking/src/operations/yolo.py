"""
Operations: pure leaf functions for YOLO result parsing and frame annotation.
Each function uses only cv2/numpy/builtins — no calls to other business functions.
"""
import cv2
import numpy as np

from ..data.models import BoundingBox, Detection

# Fixed palette; index is determined by hashing the class label so the same
# class always gets the same colour across frames.
_PALETTE: list[tuple[int, int, int]] = [
    (0, 0, 255),    # red
    (0, 255, 255),  # yellow
    (255, 0, 0),    # blue
    (0, 255, 0),    # green
    (255, 0, 255),  # magenta
    (0, 128, 255),  # orange
    (128, 0, 255),  # purple
    (255, 255, 0),  # cyan
]


def parse_yolo_detections(results, confidence_threshold: float) -> list[Detection]:
    detections: list[Detection] = []
    for result in results:
        boxes = result.boxes
        names = result.names
        for i in range(len(boxes)):
            confidence = float(boxes.conf[i])
            if confidence < confidence_threshold:
                continue
            x1, y1, x2, y2 = map(int, boxes.xyxy[i])
            label = names[int(boxes.cls[i])]
            detections.append(
                Detection(
                    bbox=BoundingBox(x=x1, y=y1, width=x2 - x1, height=y2 - y1),
                    label=label,
                    confidence=confidence,
                )
            )
    return detections


def draw_detections(frame: np.ndarray, detections: list[Detection], thickness: int) -> np.ndarray:
    output = frame.copy()
    for det in detections:
        color = _PALETTE[hash(det.label) % len(_PALETTE)]
        b = det.bbox
        cv2.rectangle(output, (b.x, b.y), (b.x + b.width, b.y + b.height), color, thickness)
        (text_w, text_h), _ = cv2.getTextSize(det.label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(output, (b.x, b.y - text_h - 10), (b.x + text_w + 6, b.y), color, -1)
        cv2.putText(output, det.label, (b.x + 3, b.y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    return output
