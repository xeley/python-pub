from dataclasses import dataclass


@dataclass(frozen=True)
class BoundingBox:
    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class Detection:
    bbox: BoundingBox
    label: str
    confidence: float


@dataclass(frozen=True)
class DetectionConfig:
    camera_index: int = 0
    model_name: str = "yolov8n.pt"
    confidence_threshold: float = 0.5
    box_thickness: int = 2
    window_title: str = "Object Detection"
    display_width: int = 640
    display_height: int = 480
