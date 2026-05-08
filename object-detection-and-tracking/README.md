# Object Detection and Tracking

A Python project for real-time object detection using a camera feed.
Objects are identified by class name (person, cat, dog, car, …) and highlighted with
labelled, per-class coloured bounding boxes powered by YOLOv8.

## How it works

Each video frame is passed through a YOLOv8 neural network:

1. The model runs inference and returns a list of detected objects with bounding boxes, class labels, and confidence scores.
2. Detections below the confidence threshold are discarded.
3. Each remaining detection is drawn on the frame with a colour unique to its class and a label showing the class name.
4. The annotated frame is displayed in real time.

When the camera feed drops the system surfaces an error and exits cleanly.

## Requirements

- Python 3.10+
- A connected camera (built-in webcam or USB camera)

## Installation

```bash
# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate         # Windows
# source .venv/bin/activate    # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

On first run the YOLOv8n weights (~6 MB) are downloaded automatically.

## Usage

```bash
python -m src.main
```

Press **q** to quit the detection window.

## Configuration

Edit `DetectionConfig` in `src/data/models.py` to tune behaviour:

| Field | Default | Description |
|---|---|---|
| `camera_index` | `0` | Camera device index |
| `model_name` | `"yolov8n.pt"` | YOLO model weights (`yolov8n`, `yolov8s`, `yolov8m`, …) |
| `confidence_threshold` | `0.5` | Minimum confidence score to show a detection |
| `box_thickness` | `2` | Bounding-box line thickness in pixels |

## Project Structure

```
object-detection-and-tracking/
├── src/
│   ├── main.py                    # Application shell — event loop, adapter wiring
│   ├── data/
│   │   └── models.py              # Immutable data shapes (BoundingBox, Detection, DetectionConfig)
│   ├── operations/
│   │   ├── yolo.py                # Pure leaf functions — parse YOLO results, draw labelled boxes
│   │   └── motion.py              # Pure leaf functions — frame-diff motion utilities
│   ├── integrations/
│   │   └── detection.py           # Orchestration — detect_objects, annotate_frame
│   └── adapters/
│       ├── yolo_model.py          # I/O boundary wrapping ultralytics YOLO
│       ├── camera.py              # I/O boundary wrapping cv2.VideoCapture
│       └── display.py             # I/O boundary wrapping cv2 window output
├── requirements.txt
└── README.md
```

### Architecture — IOSP (Integration Operation Segregation Principle)

Every function is classified as exactly one of:

- **Operation** — contains `if`/loops/decisions, calls only stdlib/cv2, is pure and testable.
- **Integration** — a flat, linear sequence of calls to Operations and other Integrations; zero branching.
- **Adapter** — thin I/O wrapper at the system boundary (camera, YOLO model, display).
- **Data** — immutable, typed value objects with no behaviour.

## License

MIT
