"""
Operations: pure leaf functions for screenshot path construction.
No I/O — file writing belongs in the application shell (API layer).
"""
from datetime import datetime
from pathlib import Path


def build_screenshot_path(folder: Path, now: datetime) -> Path:
    filename = f"screenshot_{now.strftime('%Y%m%d_%H%M%S')}.png"
    return folder / filename


def default_screenshot_folder() -> Path:
    return Path.home() / "Downloads"
