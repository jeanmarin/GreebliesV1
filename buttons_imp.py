# def __init__(self, color, x, y, width, height, text=None):
# Button class
import pygame as pg

class Button:
    def __init__(self, x, y, w, h, text='', color=(255, 255, 255), font=None, callback=None):
        self.rect = pg.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.font = font if font else pg.font.Font(None, 32)
         # Use black for the initial text color since the hover state is initially False
        self.txt_surface = self.font.render(text, True, "black")
        self.hover = False
        self.callback = callback
        #global started


    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                # Perform the desired action
                #print(self.text)
                if self.text == "Start":
                    #print("start")
                    global started
                    started = True
                elif self.text == "Stop":
                    #print("stop")
                    # global started
                    started = False
                

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.hover = True
        else:
            self.hover = False
# the if than statement inline in the parameter allows for conditional behavior. The button border is red unit you hover over it then it turns white
    def draw(self, screen):
        # Draw the filled rectangle with the appropriate color based on hover state
        pg.draw.rect(screen, "lightskyblue3" if self.hover else "dodgerblue2", self.rect)
    
        # Draw the border with the appropriate color based on hover state
        pg.draw.rect(screen, self.color if self.hover else "red", self.rect, 2)
    
        # Render the text with the appropriate color based on hover state
        self.txt_surface = self.font.render(self.text, True, "white" if self.hover else "black")
    
        screen.blit(self.txt_surface, (self.rect.x + (self.rect.w - self.txt_surface.get_width()) // 2,
                                        self.rect.y + (self.rect.h - self.txt_surface.get_height()) // 2))
