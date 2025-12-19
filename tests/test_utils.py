import math
import random

from greeblies.utils import convert_color_to_label, random_movement_vector


def test_convert_color_to_label_known_values():
    assert convert_color_to_label((255, 0, 0)) == "RED"
    assert convert_color_to_label((0, 255, 0)) == "GREEN"
    assert convert_color_to_label((0, 100, 0)) == "DARK_GREEN"
    assert convert_color_to_label((139, 69, 19)) == "BROWN"
    assert convert_color_to_label((255, 255, 0)) == "YELLOW"
    assert convert_color_to_label((255, 255, 255)) == "WHITE"
    assert convert_color_to_label((128, 128, 128)) == "GRAY"


def test_convert_color_to_label_unknown_value_returns_none():
    assert convert_color_to_label((1, 2, 3)) is None


def test_random_movement_vector_has_expected_magnitude():
    rng = random.Random(1234)
    speed = 7.5
    dx, dy = random_movement_vector(speed, rng=rng)
    assert math.isclose(math.hypot(dx, dy), speed, rel_tol=1e-12, abs_tol=1e-12)


