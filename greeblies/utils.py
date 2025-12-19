"""Small, testable utilities for Greeblies.

These functions are intentionally dependency-light so they can be imported in
unit tests without initializing pygame or starting the simulation.
"""

from __future__ import annotations

import math
import random
from typing import Dict, Tuple

Color = Tuple[int, int, int]


def random_movement_vector(speed: float, *, rng: random.Random | None = None) -> tuple[float, float]:
    """Return a random 2D movement vector with magnitude approximately `speed`.

    Args:
        speed: Desired magnitude of the vector.
        rng: Optional RNG for deterministic behavior in tests.

    Returns:
        (dx, dy) where sqrt(dx^2 + dy^2) == speed (within float error).
    """
    rng = rng or random
    direction = rng.uniform(0.0, 2.0 * math.pi)
    dx = speed * math.cos(direction)
    dy = speed * math.sin(direction)
    return dx, dy


def convert_color_to_label(color: Color, *, mapping: Dict[Color, str] | None = None) -> str | None:
    """Convert an RGB tuple to a color label used by the simulation.

    Args:
        color: An RGB tuple, e.g. (255, 0, 0).
        mapping: Optional override mapping.

    Returns:
        Label string if known, otherwise None.
    """
    if mapping is None:
        mapping = {
            (0, 255, 0): "GREEN",
            (0, 100, 0): "DARK_GREEN",
            (139, 69, 19): "BROWN",
            (255, 255, 0): "YELLOW",
            (255, 0, 0): "RED",
            (255, 255, 255): "WHITE",
            (128, 128, 128): "GRAY",
        }
    return mapping.get(color)


