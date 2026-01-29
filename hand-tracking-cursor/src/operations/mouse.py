"""Mouse control using PyAutoGUI (the "Act")."""

import pyautogui


def get_screen_size() -> tuple[int, int]:
    """Return (width, height) of the primary screen in pixels."""
    w, h = pyautogui.size()
    return w, h


def move_to(x: float, y: float) -> None:
    """Move the system mouse cursor to the given screen coordinates."""
    pyautogui.moveTo(x, y)
