"""Legacy tkinter UI prototype.

This script appears to be an early GUI experiment and is kept as a standalone
entrypoint. It should not be imported by other modules (it creates windows on
construction).
"""

from __future__ import annotations

import tkinter
import tkinter.font
from tkinter import Frame, HORIZONTAL, Scale, Tk

class Widget1:
    """Simple tkinter window with a few horizontal sliders."""

    def __init__(self, parent):
        self.gui(parent)

    def gui(self, parent):
        if parent == 0:
            self.w1 = Tk()
            self.w1.configure(bg = '#04413f')
            self.w1.geometry('940x670')
        else:
            self.w1 = Frame(parent)
            self.w1.configure(bg = '#04413f')
            self.w1.place(x = 0, y = 0, width = 940, height = 670)
        self.hslider1 = Scale(self.w1, from_ = 0, to = 100, resolution = 1, orient = HORIZONTAL, font = tkinter.font.Font(family = "Calibri", size = 9), cursor = "arrow", state = "normal")
        self.hslider1.place(x = 790, y = 210, width = 110, height = 22)
        self.hslider1['command'] = self.red_size
        self.hslider2 = Scale(self.w1, from_ = 0, to = 100, resolution = 1, orient = HORIZONTAL, font = tkinter.font.Font(family = "Calibri", size = 9), cursor = "arrow", state = "normal")
        self.hslider2.place(x = 790, y = 260, width = 110, height = 22)
        self.hslider2['command'] = self.brown_reproduction_threshold
        self.hslider3 = Scale(self.w1, from_ = 0, to = 100, resolution = 1, orient = HORIZONTAL, font = tkinter.font.Font(family = "Calibri", size = 9), cursor = "arrow", state = "normal")
        self.hslider3.place(x = 790, y = 170, width = 110, height = 22)
        self.hslider3['command'] = self.light_intensity
        self.hslider4 = Scale(self.w1, from_ = 0, to = 100, resolution = 1, orient = HORIZONTAL, font = tkinter.font.Font(family = "Calibri", size = 9), cursor = "arrow", state = "normal")
        self.hslider4.place(x = 790, y = 300, width = 110, height = 22)
        self.hslider4['command'] = self.yellow_reproduction_threshold
        self.hslider5 = Scale(self.w1, from_ = 0, to = 100, resolution = 1, orient = HORIZONTAL, font = tkinter.font.Font(family = "Calibri", size = 9), cursor = "arrow", state = "normal")
        self.hslider5.place(x = 790, y = 360, width = 110, height = 22)
        self.hslider5['command'] = self.red_reproduction_threshold

    def red_reproduction_threshold(self, e):
        """Slider callback."""
        print('red_reproduction_threshold')

    def yellow_reproduction_threshold(self, e):
        """Slider callback."""
        print('yellow_reproduction_threshold')

    def brown_reproduction_threshold(self, e):
        """Slider callback."""
        print('brown_reproduction_threshold')

    def red_size(self, e):
        """Slider callback."""
        print('red_size')

    def light_intensity(self, e):
        """Slider callback."""
        print('light_intensity')

if __name__ == '__main__':
    a = Widget1(0)
    a.w1.mainloop()