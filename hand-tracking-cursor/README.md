# Hand Tracking Cursor

Control your system cursor using hand tracking via the webcam. Your index finger drives the mouse; a live preview shows hand landmarks. Press **q** to quit.

This project was motivated by the article [*I Ditched My Mouse: How I Control My Computer With Hand Gestures (In 60 Lines of Python)*](https://towardsdatascience.com/i-ditched-my-mouse-how-i-control-my-computer-with-hand-gestures-in-60-lines-of-python/) (Towards Data Science).

## Features

- **Index-finger cursor**: MediaPipe Hand Landmarker tracks one hand and maps the index fingertip to screen coordinates.
- **Smoothing**: Configurable smoothing reduces jitter (see `src/config.py`).
- **Live preview**: OpenCV window shows the camera feed with drawn hand landmarks.
- **Configurable**: Camera index/API, detection confidence, model path, quit key, and more in `src/config.py`.

## Project layout

```
hand-tracking-cursor/
├── src/
│   ├── main.py              # Entry point; runs the AI mouse integration
│   ├── config.py            # Cursor smoothing, camera, hand detection, display settings
│   ├── integrations/
│   │   ├── __init__.py
│   │   └── ai_mouse.py      # Orchestrates camera → hand detection → mouse movement
│   └── operations/          # Logic using OpenCV, MediaPipe, PyAutoGUI
│       ├── __init__.py
│       ├── camera.py        # Open/read/flip/release camera
│       ├── coordinates.py   # Map frame to screen, smooth position
│       ├── display.py       # Show frame, wait key, destroy windows
│       ├── hands.py         # Hand detector, process frame, landmarks, index-finger XY
│       └── mouse.py         # Screen size, move cursor
├── scripts/
│   └── download_hand_landmarker.py   # Download MediaPipe hand_landmarker.task
├── models/
│   ├── README.md            # How to obtain hand_landmarker.task
│   └── hand_landmarker.task # (after download)
├── .venv/
├── .gitignore
├── README.md
└── requirements.txt
```

## Architecture

The project follows **IODA** and **Integration–Operation** separation:

- **Integrations** (e.g. `ai_mouse.py`) orchestrate behaviour by calling operations; they contain no logic.
- **Operations** (in `src/operations/`) contain the logic and use third-party APIs: OpenCV (camera, display), MediaPipe (hand detection), PyAutoGUI (mouse).

`main.py` only calls the integration `run_ai_mouse()`, which composes camera, hand detection, coordinate mapping, smoothing, and mouse movement.

## Requirements

- **Python 3.9–3.12** (MediaPipe has no wheels for Python 3.13; 3.12 is recommended)
- Webcam
- **Hand Landmarker model**: must be present at `models/hand_landmarker.task` (see [models/README.md](models/README.md))

## Setup

### 1. Virtual environment and dependencies

Create and activate a virtual environment, then install dependencies.

**Windows (PowerShell):**

```powershell
cd "d:\Code\Python-Pub\hand-tracking-cursor"
& "D:\Python3.12\python.exe" -m venv .venv   # or Python 3.11 if 3.12 is not installed
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If the venv was created with `--without-pip`, bootstrap pip first:

```powershell
.\.venv\Scripts\python.exe -m ensurepip --upgrade --default-pip
```

**Using `venv-3.12` (Python 3.12.10):**

```powershell
cd "d:\Code\Python-Pub\hand-tracking-cursor"
.\venv-3.12\Scripts\Activate.ps1
.\venv-3.12\Scripts\python.exe -m ensurepip --upgrade --default-pip   # if pip is missing
.\venv-3.12\Scripts\python.exe -m pip install -r requirements.txt
```

**macOS/Linux:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Hand Landmarker model

**Option A – run the download script (recommended):**

```powershell
python scripts\download_hand_landmarker.py
```

**Option B – manual:** see [models/README.md](models/README.md) for the download URL and where to save the file.

## Configuration

Edit `src/config.py` to adjust:

| Setting | Description |
|--------|-------------|
| `SMOOTHING` | Cursor smoothing (higher = smoother, more lag) |
| `CAMERA_INDEX` | Webcam device index (default `0`) |
| `CAMERA_API` | OpenCV backend (e.g. `700` for `cv2.CAP_DSHOW` on Windows if default fails) |
| `HAND_LANDMARKER_MODEL_PATH` | Path to `hand_landmarker.task` (relative to project root) |
| `MAX_NUM_HANDS` | Number of hands to detect (`1` for cursor control) |
| `MIN_DETECTION_CONFIDENCE` | Hand detection confidence threshold |
| `WINDOW_NAME` | Title of the preview window |
| `QUIT_KEY` | Key to exit (default `"q"`) |

## Usage

From the project root, with the venv activated:

```powershell
python src\main.py
```

A window titled **AI Mouse Controller** (or the name in `config.WINDOW_NAME`) shows the camera feed with hand landmarks. Move your index finger to move the cursor; press **q** to quit.

## License

MIT
