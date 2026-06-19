"""
Operations: pure leaf functions containing logic.
Each function uses only cv2/numpy (stdlib-level) — no calls to other business functions.
"""
import cv2
import numpy as np

from ..data.models import BoundingBox


def to_grayscale(frame: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def apply_blur(frame: np.ndarray) -> np.ndarray:
    return cv2.GaussianBlur(frame, (21, 21), 0)


def compute_frame_delta(prev_frame: np.ndarray, curr_frame: np.ndarray) -> np.ndarray:
    return cv2.absdiff(prev_frame, curr_frame)


def apply_threshold(delta: np.ndarray, threshold: int) -> np.ndarray:
    _, binary = cv2.threshold(delta, threshold, 255, cv2.THRESH_BINARY)
    return binary


def dilate_mask(mask: np.ndarray, iterations: int) -> np.ndarray:
    return cv2.dilate(mask, None, iterations=iterations)


def extract_contours(mask: np.ndarray) -> list:
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return list(contours)


def filter_significant_contours(contours: list, min_area: int) -> list:
    return [c for c in contours if cv2.contourArea(c) >= min_area]


def build_bounding_boxes(contours: list) -> list[BoundingBox]:
    boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        boxes.append(BoundingBox(x=x, y=y, width=w, height=h))
    return boxes


def merge_overlapping_boxes(boxes: list[BoundingBox], margin: int) -> list[BoundingBox]:
    """Merge boxes that overlap or are within `margin` pixels of each other.

    Iterates until no further merges occur so chains of close boxes collapse
    into a single enclosing rectangle.
    """
    if not boxes:
        return boxes

    rects = [(b.x, b.y, b.x + b.width, b.y + b.height) for b in boxes]
    changed = True
    while changed:
        changed = False
        merged: list[tuple[int, int, int, int]] = []
        used = [False] * len(rects)
        for i in range(len(rects)):
            if used[i]:
                continue
            x1, y1, x2, y2 = rects[i]
            for j in range(i + 1, len(rects)):
                if used[j]:
                    continue
                ox1, oy1, ox2, oy2 = rects[j]
                overlaps = ox1 - margin <= x2 and x1 <= ox2 + margin and oy1 - margin <= y2 and y1 <= oy2 + margin
                if overlaps:
                    x1 = min(x1, ox1)
                    y1 = min(y1, oy1)
                    x2 = max(x2, ox2)
                    y2 = max(y2, oy2)
                    used[j] = True
                    changed = True
            merged.append((x1, y1, x2, y2))
        rects = merged

    return [BoundingBox(x=r[0], y=r[1], width=r[2] - r[0], height=r[3] - r[1]) for r in rects]


def is_frame_valid(frame) -> bool:
    return frame is not None and frame.size > 0


def draw_bounding_boxes(frame: np.ndarray, boxes: list[BoundingBox], color: tuple, thickness: int) -> np.ndarray:
    output = frame.copy()
    for box in boxes:
        cv2.rectangle(
            output,
            (box.x, box.y),
            (box.x + box.width, box.y + box.height),
            color,
            thickness,
        )
    return output
