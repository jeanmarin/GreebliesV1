import pygame as pg
import pygame_gui


# Horizontal Slider class
class HSlider:
    def __init__(self, x, y, w, h, start_value, value_range, manager, callback=None):
        self.slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pg.Rect((x, y), (w, h)),
            start_value=start_value,
            value_range=value_range,
            manager=manager,
        )
        self.callback = callback
        self.slider_value = start_value

    def handle_event(self, event):
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.slider:
                    self.slider_value = int(event.value)
                    #print(f"HSlider value: {self.slider_value}")

    def update(self, time_delta):
        self.slider.update(time_delta)

    def draw(self, surface):
        self.update(time_delta)