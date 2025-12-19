"""UI helpers: simple pygame button widget."""

from __future__ import annotations

from collections.abc import Callable
from typing import Optional

import pygame as pg


class Button:
    """Clickable rectangular button for pygame UIs.

    This component is intentionally lightweight: it only knows how to render
    itself and detect clicks. Any "Start/Stop" behavior should be implemented
    by supplying a `callback`.
    """

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        text: str = "",
        color: pg.Color | tuple[int, int, int] = (255, 255, 255),
        font: Optional[pg.font.Font] = None,
        callback: Optional[Callable[[], None]] = None,
    ) -> None:
        self.rect = pg.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.font = font if font else pg.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, "black")
        self.hover = False
        self.callback = callback

    def handle_event(self, event: pg.event.Event) -> None:
        """Handle a pygame event and invoke callback on click."""
        if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.callback:
                self.callback()

    def update(self, mouse_pos: tuple[int, int]) -> None:
        """Update hover state from the current mouse position."""
        self.hover = self.rect.collidepoint(mouse_pos)

    def draw(self, screen: pg.Surface) -> None:
        """Draw the button to the provided pygame surface."""
        # Filled rectangle
        pg.draw.rect(screen, "lightskyblue3" if self.hover else "dodgerblue2", self.rect)

        # Border
        pg.draw.rect(screen, self.color if self.hover else "red", self.rect, 2)

        # Text
        self.txt_surface = self.font.render(self.text, True, "white" if self.hover else "black")
        screen.blit(
            self.txt_surface,
            (
                self.rect.x + (self.rect.w - self.txt_surface.get_width()) // 2,
                self.rect.y + (self.rect.h - self.txt_surface.get_height()) // 2,
            ),
        )
