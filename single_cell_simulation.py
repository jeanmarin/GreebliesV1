'''
* Jean-Louis Marin 2023 - April.
* Single Cell Simulation - Called Greeblies. 
* This program simulates the behavior of a single cell organism.
* Greens photoplancton organisms are the primary producers of the ecosystem. They don't die of starvation, they have constant light, but they can be eaten by predators. 
* Browns are the primary consumers of the ecosystem. They eat greens and die of starvation. And are the primary food source for omnivores.
* Yellows are the secondary consumers of the ecosystem. They eat greens and browns and die of starvation. And are the primary food source for carnivores.
* Reds are the tertiary consumers of the ecosystem. They eat yellows and die of starvation.
* The variables to adjust are the number of organisms, the speed of the organisms, and the light intensity, and starvation counter.
* The organisms are randomly placed on the screen and move randomly.
* The organisms are drawn on the screen and the number of organisms of each type is displayed. -- BROKEN --
* The organisms are stored in a database. not ready yet. the information is dumped but needs ferter refinement.
* To Do:
* 1. Add a GUI to adjust the number of organisms, the speed of the organisms, and the light intensity.
* 2. Add a GUI to display the number of organisms of each type.
* 3. create a record of each even for each organism in the simulation in the database.
* 4. Hook up the database to BI reporting dashboard. for stats at the of the simulation.
* 5. create various hooks in the code to link exteral ML or AI to evolve the organisms' behavior each generation of the game.
* 6. Move the simulation to cloud hosted server with a web front end.
* 7. Add a GUI to adjust the number of organisms, the speed of the organisms, and the light intensity.
* 8. increase the model to gargantuan proportions for the simulation. for multiple people to interact with. 

** - baseline code established = April 7th 2023. 

'''

# import tkinter as tk
import pygame as pg
import os
from PIL import Image
import random
from pygame.locals import *
import sys
import time
import math
import pygame_gui
import sqlite3

from pygame.locals import *
from pygame_gui import UIManager


# Initialize pg
pg.init()

# Initialize font module
pg.font.init()


#from tkinter_pygame import PygameDisplay
PRINT_ORGANISM_COORDS = False

# Set up the screen
SCREEN_WIDTH = 910
SCREEN_HEIGHT = 750
GRID_WIDTH = 750
GRID_HEIGHT = 750

# Initialize counter variable
organism_count = 0
# Initialize counter variable
id_counter = 0

# Define detection distance for predator organisms
detection_distance = 10

# the global start variable
started = False

# Delete the database file if it exists
if os.path.exists("organism_data.db"):
    os.remove("organism_data.db")

# Connect to the database
conn = sqlite3.connect("organism_data.db")
c = conn.cursor()

# Create a table to store the organism data
# ID, RED, organism1.speed, random.randint(0, 740), random.randint(0, 740), 7, 7, 500

c.execute('''CREATE TABLE organisms
             (id INT,
              color TEXT,
              speed INT, 
              x INT,
              y INT,
              width INT,
              height INT,
              lifespan INT)''')


# display screen configuration
pg.display.set_caption("Single Cell Simulation")
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
manager = UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a clock to keep track of time
clock = pg.time.Clock()

# Define a font and render the text
font = pg.font.SysFont(None, 16)

speeds = [1, 1, 7, 5, 10]
light_intensity = 1
num_green = 0
num_brown = 0
num_yellow = 0
num_red = 0

# Colors
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)


# Define the global function for debugging. Comment out when not needed. 
'''
toggle = False
def print_organism_coords(organism, toggle):
    if toggle:
        print(f"Organism coordinates: x={organism.rect.x}, y={organism.rect.y}")
'''
#
def random_movement_vector(speed):
    direction = random.uniform(0, 2 * math.pi)
    dx = speed * math.cos(direction)
    dy = speed * math.sin(direction)
    return dx, dy

# Collision handlers
def handle_green_green_collision(organism1, organism2):
    # Turn the parent organisms dark green
    organism1.set_color(DARK_GREEN)
    organism1.set_size(3) 
    organism2.set_color(DARK_GREEN)
    organism2.set_size(3)
    organism1.set_coor(random.randint(0, 740), random.randint(0, 740))
    organism2.set_coor(random.randint(0, 740), random.randint(0, 740))


    # Reproduction: Create a new green organism
    update_id_counter()
    new_organism = Organism(GREEN, organism1.speed, random.randint(0, 740), random.randint(0, 740), 2 , 2, 6000, id_counter)
    all_sprites.add(new_organism)
    
def handle_brown_brown_collision(organism1, organism2):
    pass
      
def handle_yellow_yellow_collision(organism1, organism2):
    pass

def handle_red_red_collision(organism1, organism2):
    pass

def handle_green_brown_collision(organism1, organism2):
    if organism1.color == BROWN:
        all_sprites.remove(organism2)
        organism1.food_count += 1
        organism1.hasNotEaten = 0 #resest starvation counter
        if organism1.food_count >= 3:
            update_id_counter()
            all_sprites.add(Organism(BROWN, organism1.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 2000, id_counter))
            organism1.food_count = 0
               
    else :
        all_sprites.remove(organism1)
        organism2.food_count += 1
        organism2.hasNotEaten = 0 #resest starvation counter
        if organism2.food_count >= 3:
            update_id_counter()
            all_sprites.add(Organism(BROWN, organism2.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 2000, id_counter))
            organism2.food_count = 0

def handle_dark_green_brown_collision(organism1, organism2):
    if organism1.color == BROWN:
        all_sprites.remove(organism2)
        organism1.food_count += 1
        organism1.hasNotEaten = 0 #resest starvation counter
        if organism1.food_count >= 3:
            update_id_counter()
            all_sprites.add(Organism(BROWN, organism1.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 2000, id_counter))
            organism1.food_count = 0
               
    else :
        all_sprites.remove(organism1)
        organism2.food_count += 1
        organism2.hasNotEaten = 0 #resest starvation counter
        if organism2.food_count >= 3:
            update_id_counter()
            all_sprites.add(Organism(BROWN, organism2.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 2000, id_counter))
            organism2.food_count = 0

def handle_green_yellow_collision(organism1, organism2):
    if organism1.color == YELLOW:
        all_sprites.remove(organism2)
        organism1.food_count += 1
        organism1.hasNotEaten = 0 #resest starvation counter
        if organism1.food_count >= 5:
            update_id_counter()
            all_sprites.add(Organism(YELLOW, organism1.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 700, id_counter))
            organism1.food_count = 0
               
    else :
        all_sprites.remove(organism1)
        organism2.food_count += 1
        organism2.hasNotEaten = 0 #resest starvation counter
        if organism2.food_count >= 5:
            update_id_counter()
            all_sprites.add(Organism(YELLOW, organism2.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 700, id_counter))
            organism2.food_count = 0

def handle_brown_yellow_collision(organism1, organism2):
    if organism1.color == YELLOW:
        all_sprites.remove(organism2)
        organism1.food_count += 1
        organism1.hasNotEaten = 0 #resest starvation counter
        if organism1.food_count >= 5:
            update_id_counter()
            all_sprites.add(Organism(YELLOW, organism1.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 700, id_counter))
            organism1.food_count = 0
               
    else :
        all_sprites.remove(organism1)
        organism2.food_count += 1
        organism2.hasNotEaten = 0 #resest starvation counter
        if organism2.food_count >= 5:
            update_id_counter()
            all_sprites.add(Organism(YELLOW, organism2.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 700, id_counter))
            organism2.food_count = 0

def handle_dark_green_yellow_collision(organism1, organism2):
    if organism1.color == YELLOW:
        all_sprites.remove(organism2)
        organism1.food_count += 1
        organism1.hasNotEaten = 0 #resest starvation counter
        if organism1.food_count >= 5:
            update_id_counter()
            all_sprites.add(Organism(YELLOW, organism1.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 700, id_counter))
            organism1.food_count = 0
               
    else :
        all_sprites.remove(organism1)
        organism2.food_count += 1
        organism2.hasNotEaten = 0 #resest starvation counter
        if organism2.food_count >= 5:
            update_id_counter()
            all_sprites.add(Organism(YELLOW, organism2.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 700, id_counter))
            organism2.food_count = 0

def handle_green_red_collision(organism1, organism2):
    pass
    
def handle_red_brown_collision(organism1, organism2):
    pass
    '''
    if organism1.color == RED:
        all_sprites.remove(organism2)
        organism1.food_count += 1
        organism1.hasNotEaten = 0 #resest starvation counter
        if organism1.food_count >= 5:
            update_id_counter()
            all_sprites.add(Organism(RED, organism1.speed, random.randint(0, 740), random.randint(0, 740), 7, 7, 500, id_counter))
            organism1.food_count = 0   
    else :
        all_sprites.remove(organism1)
        organism2.food_count += 1
        organism2.hasNotEaten = 0 #resest starvation counter
        if organism2.food_count >= 5:
            update_id_counter()
            all_sprites.add(Organism(RED, organism2.speed, random.randint(0, 740), random.randint(0, 740), 7, 7, 500, id_counter))
            organism2.food_count = 0
    '''

def handle_red_yellow_collision(organism1, organism2):
    if organism1.color == RED:
        all_sprites.remove(organism2)
        organism1.food_count += 1
        organism1.hasNotEaten = 0 #resest starvation counter
        if organism1.food_count >= 5:
            update_id_counter()
            all_sprites.add(Organism(RED, organism1.speed, random.randint(0, 740), random.randint(0, 740), 7, 7, 500, id_counter))
            organism1.food_count = 0   
    else :
        all_sprites.remove(organism1)
        organism2.food_count += 1
        organism2.hasNotEaten = 0 #resest starvation counter
        if organism2.food_count >= 5:
            update_id_counter()
            all_sprites.add(Organism(RED, organism2.speed, random.randint(0, 740), random.randint(0, 740), 7, 7, 500, id_counter))
            organism2.food_count = 0

def update_id_counter():
    global id_counter
    id_counter += 1

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

# def __init__(self, color, x, y, width, height, text=None):
class Button:
    def __init__(self, x, y, w, h, text='', color=(255, 255, 255), font=None):
        self.rect = pg.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.font = font if font else pg.font.Font(None, 32)
         # Use black for the initial text color since the hover state is initially False
        self.txt_surface = self.font.render(text, True, "black")
        self.hover = False
        #global started

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Perform the desired action
                print(self.text)
                if self.text == "Start":
                    print("start")
                    global started
                    started = True
                elif self.text == "Stop":
                    print("stop")
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



# Organism class
class Organism(pg.sprite.Sprite):
    
    # This class represents an organism. It derives from the "Sprite" class in Pygame.
    def __init__(self, color, speed, x, y, width, height, starvation_count, OrganismID):
        super().__init__()
        self.image = pg.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.organismID = OrganismID
        self.food_count = 0  # New variable to keep track of how much food a red organism has eaten
        self.light_exposure_count = 0  # New variable to keep track of how much light a green / darkGreen organism has been exposed to
        self.hasNotEaten = 0 # it has not eaten anything yet
        self.starvation_count = starvation_count  # variable max value of how long an organism can go without eating
        
        global id_counter
        self.id = id_counter
        update_id_counter()
    
    # Update the organism's position        
    def update(self, all_sprites):
        
        # Generate a random movement vector with a magnitude equal to the organism's speed
        magnitude = self.speed

        # Otherwise, generate a random direction
        direction = random.uniform(0, 2 * math.pi)
        dx = magnitude * math.cos(direction)
        dy = magnitude * math.sin(direction)

        # Add the movement vector to the current position to obtain the new position
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # Check if the new position is within the screen boundaries and update the position accordingly
        if 0 <= new_x <= 740:
            self.rect.x = new_x
        if 0 <= new_y <= 740:
            self.rect.y = new_y
                
        # Check for light exposure count. If the organism is exposed to light, it will reproduce
        if self.color == GREEN or self.color == DARK_GREEN:
            if self.light_exposure_count >= 550:    
                update_id_counter()    
                all_sprites.add(Organism(GREEN, self.speed, random.randint(0, 740), random.randint(0, 740), 2, 2, 6000, id_counter))
                self.light_exposure_count = 0
            else:
                self.light_exposure_count += light_intensity

        # Checks if the organism has eaten something. If it has not and reaches 15 seconds, it will die
        # Remove the sprite if it hasn't eaten in a while
        if self.hasNotEaten >= self.starvation_count:
            all_sprites.remove(self)
        else:
            self.hasNotEaten += 1

        # Check for collisions with other organisms
        collisions = pg.sprite.spritecollide(self, all_sprites, False)
        for collision in collisions:
            if collision != self:
                # Define the collision handlers for each type of organism
                collision_handlers = {
                    (GREEN, GREEN): handle_green_green_collision,
                    (BROWN, BROWN): handle_brown_brown_collision,
                    (YELLOW, YELLOW): handle_yellow_yellow_collision,
                    (RED, RED): handle_red_red_collision,
                    (GREEN, BROWN): handle_green_brown_collision,
                    (DARK_GREEN, BROWN): handle_dark_green_brown_collision,
                    (GREEN, YELLOW): handle_green_yellow_collision,
                    (YELLOW, GREEN): handle_green_yellow_collision,
                    (DARK_GREEN, YELLOW): handle_dark_green_yellow_collision,
                    (YELLOW, DARK_GREEN): handle_dark_green_yellow_collision,
                    (BROWN, YELLOW): handle_brown_yellow_collision,
                    (YELLOW, BROWN): handle_brown_yellow_collision,
                    (GREEN, RED): handle_green_red_collision,
                    (RED, YELLOW): handle_red_yellow_collision,
                    (BROWN, RED): handle_red_brown_collision
                }

                # Call the appropriate collision handler based on the colors of the colliding organisms
                handler_key = tuple(sorted([self.color, collision.color]))
                if handler_key in collision_handlers:
                    collision_handlers[handler_key](self, collision)

    def set_color(self, color):
        self.color = color
        self.image.fill(color)
    def set_size(self, size):
        self.image = pg.Surface([size, size])
        self.rect = self.image.get_rect()
        self.image.fill(self.color)
    def set_coor(self,new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y
        self.image.fill(self.color)

'''
# Define the input variables for the text entry boxes  
green_input = pg_gui.elements.UITextEntryLine(relative_rect=pg.Rect((760, 120), (100, 30)), manager=manager) # , container=container)
# container.add_ui_element(green_input)
dark_green_input = pg_gui.elements.UITextEntryLine(relative_rect=pg.Rect((760, 140), (100, 30)), manager=manager) # , container=container)
# container.add_ui_element(dark_green_input)
brown_input = pg_gui.elements.UITextEntryLine(relative_rect=pg.Rect((760, 160), (100, 30)), manager=manager) # , container=container)
# container.add_ui_element(brown_input)
yellow_input = pg_gui.elements.UITextEntryLine(relative_rect=pg.Rect((760, 180), (100, 30)), manager=manager) # , container=container)
# container.add_ui_element(yellow_input)
red_input = pg_gui.elements.UITextEntryLine(relative_rect=pg.Rect((760, 200), (100, 30)), manager=manager) # , container=container)
# container.add_ui_element(red_input)
light_intensity_input = pg_gui.elements.UITextEntryLine(relative_rect=pg.Rect((760, 260), (100, 30)), manager=manager) # , container=container)
# container.add_ui_element(light_intensity_input)


# Define a function to handle the text entry finished event
def handle_text_entry_finished(event):
    if event.ui_element in [green_input, dark_green_input, brown_input, yellow_input, red_input]:
        update_starvation_variables()

# Define a function to handle the text entry finished event
def handle_text_entry_finished(event):
    if event.ui_element in [green_input, dark_green_input, brown_input, yellow_input, red_input]:
        update_starvation_variables()

# Create the buttons
class Button:
    def __init__(self, color, x, y, width, height, text=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        

    def draw(self, screen):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text:
            font = pg.font.Font(None, 20)
            text = font.render(self.text, 1, WHITE)
            screen.blit(text, (self.x + (self.width // 2 - text.get_width() // 2), self.y + (self.height // 2 - text.get_height() // 2)))

    def is_mouse_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height
'''
# Define a function to parse and update the starvation variables
'''
def update_starvation_variables():
    try:
        
        green_starvation = int(green_input.get_text())
        dark_green_starvation = int(dark_green_input.get_text())
        brown_starvation = int(brown_input.get_text())
        yellow_starvation = int(yellow_input.get_text())
        red_starvation = int(red_input.get_text())
        light_intensity = int(light_intensity_input.get_text())
       
        for organism in all_sprites:
            if organism.color == "GREEN":
                organism.starvation_count = green_starvation
            elif organism.color == "DARK_GREEN":
                organism.starvation_count = dark_green_starvation
            elif organism.color == "BROWN":
                organism.starvation_count = brown_starvation
            elif organism.color == "YELLOW":
                organism.starvation_count = yellow_starvation
            elif organism.color == "RED":
                organism.starvation_count = red_starvation
            elif organism.color == "LIGHT":
                organism.starvation_count = light_intensity
    except ValueError:
        print("Invalid input")
 '''
# Set up the gray bar and buttons
button_height = 30
button_width = 70
button_x = GRID_WIDTH + 30
start_button_y = 30
stop_button_y = 70


# postion the button objects.
#start_button_rect = pg.Rect(button_x, start_button_y, button_width, button_height)
#stop_button_rect = pg.Rect(button_x, stop_button_y, button_width, button_height)

# Create start and stop buttons # (self, x, y, w, h, text='', color=(255, 255, 255), font=None):
start_button = Button(button_x, start_button_y, button_width, button_height, 'Start', GREEN)
stop_button = Button(button_x, stop_button_y, button_width, button_height, 'Stop', RED)
buttons = [start_button, stop_button]
#def __init__(self, x, y, w, h, text='')
#(760, 120), (100, 30)
input_box1 = InputBox(760, 120, 100, 18)
input_box2 = InputBox(760, 140, 100, 18)
input_boxes = [input_box1, input_box2]


#start_button.draw(screen)
#stop_button.draw(screen)

# Initialize the simulation
all_sprites = pg.sprite.Group()

organisms_data = [
    {"color": GREEN, "speed": speeds[0], "width": 2, "height": 2, "starvation": 6000},
    {"color": DARK_GREEN, "speed": speeds[1] , "width": 3, "height": 3, "starvation": 6000},
    {"color": BROWN, "speed": speeds[3], "width": 3, "height": 3, "starvation": 2000},
    {"color": YELLOW, "speed": speeds[2],   "width": 5, "height": 5, "starvation": 1000},
    {"color": RED, "speed": speeds[4] , "width": 7, "height": 7, "starvation": 850}
]
# this function is used to create the starting organisms
for organism_data in organisms_data:
    if organism_data["color"] == GREEN:
        num_green = 100
    elif organism_data["color"] == BROWN:
        num_brown = 75
    elif organism_data["color"] == YELLOW:
        num_yellow = 30
    elif organism_data["color"] == RED:
        num_red = 6
    
    for _ in range(num_green if organism_data["color"] == GREEN else
                   num_brown if organism_data["color"] == BROWN else
                   num_yellow if organism_data["color"] == YELLOW else
                   num_red if organism_data["color"] == RED else 0):
        update_id_counter()
        all_sprites.add(Organism(organism_data["color"], organism_data["speed"], random.randint(0, 740), random.randint(0, 740), organism_data["width"], \
                                  organism_data["height"], organism_data["starvation"], id_counter))
        num_sprites = len(all_sprites)
        all_organisms_text = font.render(f"Organism Count: {num_sprites}", True, WHITE)

# this function is used to convert the color to a label
def convert_color_to_label(color):
    color_dict = {(0, 255, 0): "GREEN", (0, 100, 0): "DARK_GREEN", (139, 69, 19): "BROWN", 
                  (255, 255, 0): "YELLOW", (255, 0, 0): "RED", (255, 255, 255): "WHITE",
                  (128, 128, 128): "GRAY"}
    for key, value in color_dict.items():
        if key == color:
            return value
    return None




# Game loop
running = True




while running:
    time_delta = clock.tick(60) / 1000.0  # Update the clock and get the time delta
    #global started
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                '''
                if event.ui_element == green_input:
                    num_green = int(green_input.get_text())
                elif event.ui_element == dark_green_input:
                    num_dark_green = int(dark_green_input.get_text())
                elif event.ui_element == brown_input:
                    num_brown = int(brown_input.get_text())
                elif event.ui_element == yellow_input:
                    num_yellow = int(yellow_input.get_text())
                elif event.ui_element == red_input:
                    num_red = int(red_input.get_text())'''
        '''        
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            if start_button.is_mouse_over(mouse_pos):
                started = True
            if stop_button.is_mouse_over(mouse_pos):
                started = False        
            manager.process_events(event)
        ''' 
        for button in buttons:
            button.handle_event(event)
        for box in input_boxes:
            box.handle_event(event)
    for button in buttons:
        button.update(pg.mouse.get_pos())   
    for box in input_boxes:
        box.update()



    # # ID, RED, organism1.speed, random.randint(0, 740), random.randint(0, 740), 7, 7, 500
    if started:
        all_sprites.update(all_sprites)
    for organism in all_sprites:
        color_label = convert_color_to_label(organism.color)
        data = (organism.id, color_label, organism.speed, organism.rect.x, organism.rect.y, organism.width, organism.height, organism.starvation_count)
        c.execute("INSERT INTO organisms VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()          

    screen.fill((0, 0, 0))
    screen.blit(screen, (0, 0))

    if len(all_sprites) == 0: # Stop the game if there are no more sprites
        #global started
        started = False
        running = False
        text_surface = font.render(f"Total Organisms: Game Over!", True, WHITE)

    # Draw the gray bar
    gray_bar_rect = pg.Rect(GRID_WIDTH, 0, SCREEN_WIDTH - GRID_WIDTH, SCREEN_HEIGHT)
    pg.draw.rect(screen, GRAY, gray_bar_rect)

    # Update and draw the UI elements
    manager.update(time_delta)
    manager.draw_ui(screen)

    # Draw the sprites and buttons
    all_sprites.draw(screen)
    start_button.draw(screen)
    stop_button.draw(screen)
    for box in input_boxes:
        box.draw(screen)
    screen.blit(all_organisms_text, (760, 720))

    # Update the count of organisms
    num_sprites = len(all_sprites)
    all_organisms_text = font.render(f"Organism Count: {num_sprites}", True, WHITE)
    text_surface = font.render(f"Total Organisms: {num_sprites}", True, WHITE)

    # Update the screen
    pg.display.flip()

conn.close()
pg.quit()
sys.exit()