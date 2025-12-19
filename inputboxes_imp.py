"""UI helpers: simple input box widget for pygame."""

from __future__ import annotations

from collections.abc import Callable
from typing import Optional

import pygame as pg

COLOR_INACTIVE = pg.Color("lightskyblue3")
COLOR_ACTIVE = pg.Color("dodgerblue2")


class InputBox:
    """A basic text input box for pygame UIs.

    Notes:
        This is intentionally minimal and does not attempt to do validation.
        Provide a `callback` if you want to react to "enter" submissions.
    """

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        font: pg.font.Font,
        text: str = "",
        callback: Optional[Callable[[str], None]] = None,
    ) -> None:
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.font = font
        self.txt_surface = font.render(text, True, self.color)
        self.active = False
        self.callback = callback

    def handle_event(self, event: pg.event.Event) -> None:
        """Handle mouse/keyboard events to edit/submit text."""
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect, toggle active state.
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pg.KEYDOWN and self.active:
            if event.key == pg.K_RETURN:
                if self.callback:
                    self.callback(self.text)
                self.text = ""
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self) -> None:
        """Resize the box if text gets long."""
        self.rect.w = max(150, self.txt_surface.get_width() + 10)

    def draw(self, screen: pg.Surface) -> None:
        """Draw the input box."""
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pg.draw.rect(screen, self.color, self.rect, 2)
