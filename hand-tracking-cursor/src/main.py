"""Entry point for the hand-tracking mouse controller."""

import sys
from pathlib import Path

# Ensure project root is on path when running as script (e.g. python src/main.py)
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from src.integrations import run_ai_mouse

if __name__ == "__main__":
    run_ai_mouse()
