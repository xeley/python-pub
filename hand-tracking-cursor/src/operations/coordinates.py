"""Coordinate mapping and smoothing (frame -> screen, jitter reduction)."""

import numpy as np


def map_to_screen(
    x: int,
    y: int,
    frame_width: int,
    frame_height: int,
    screen_width: int,
    screen_height: int,
) -> tuple[float, float]:
    """Map pixel (x, y) from frame space to screen space."""
    mouse_x = np.interp(x, (0, frame_width), (0, screen_width))
    mouse_y = np.interp(y, (0, frame_height), (0, screen_height))
    return mouse_x, mouse_y


def smooth_position(
    prev_x: float, prev_y: float, curr_x: float, curr_y: float, smoothing: float
) -> tuple[float, float]:
    """Smooth current position toward previous for less jitter. Returns (new_x, new_y)."""
    new_x = prev_x + (curr_x - prev_x) / smoothing
    new_y = prev_y + (curr_y - prev_y) / smoothing
    return new_x, new_y
