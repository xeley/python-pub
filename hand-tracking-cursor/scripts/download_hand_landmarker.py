"""Download the Hand Landmarker .task model into models/ (run once)."""

import urllib.request
from pathlib import Path

URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
# Script is in scripts/, so project root is parent of scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = PROJECT_ROOT / "models" / "hand_landmarker.task"


def main() -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {URL} ...")
    urllib.request.urlretrieve(URL, OUT_PATH)
    print(f"Saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
