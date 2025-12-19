"""UI helpers: horizontal slider wrapper for pygame_gui."""

from __future__ import annotations

from collections.abc import Callable
from typing import Optional

import pygame as pg
import pygame_gui


class HSlider:
    """A thin wrapper around `pygame_gui.elements.UIHorizontalSlider`.

    This wrapper provides convenience methods and retains the last slider value.
    """

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        start_value: float,
        value_range: tuple[float, float],
        manager: pygame_gui.UIManager,
        callback: Optional[Callable[[float], None]] = None,
    ) -> None:
        self.slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pg.Rect((x, y), (w, h)),
            start_value=start_value,
            value_range=value_range,
            manager=manager,
        )
        self.callback = callback
        self.slider_value: float = float(start_value)

    def handle_event(self, event: pg.event.Event) -> None:
        """Update slider value on UI events and invoke callback when provided."""
        if event.type == pg.USEREVENT and getattr(event, "user_type", None) == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if getattr(event, "ui_element", None) == self.slider:
                self.slider_value = float(getattr(event, "value", self.slider_value))
                if self.callback:
                    self.callback(self.slider_value)

    def update(self, time_delta: float) -> None:
        self.slider.update(time_delta)

    def draw(self, surface: pg.Surface) -> None:
        self.slider.draw(surface)

    def set_position(self, x: int, y: int) -> None:
        """Move the slider to a new top-left position."""
        self.slider.relative_rect.topleft = (x, y)
        self.slider.update_containing_rect_position()
