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
* 7. increase the model to gargantuan proportions for the simulation. for multiple people to interact with. 

** - baseline code established = April 7th 2023. 
https://pygame-gui.readthedocs.io/en/latest/theme_reference/theme_horizontal_slider.html
https://pygame-gui.readthedocs.io/en/latest/index.html


'''
#-# this comment block is for all the db stuff.

# import tkinter as tk
import pygame as pg
#-#import os
#from PIL import Image
import random
from pygame.locals import *
import sys
#import time
import math
import pygame_gui
#-#import sqlite3

from pygame.locals import *
from pygame_gui import UIManager
from buttons_imp import Button
from inputboxes_imp import InputBox
from horizontal_sliders_imp import HSlider

# Initialize pg
pg.init()

# Initialize font module
pg.font.init()

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
detection_distance = 30

# the global start variable
started = False

# define a constant for the distance threshold for red organisms to detect yellow organisms
RED_YELLOW_DETECTION_DISTANCE = 30

# define a constant for the speed of red organisms
#RED_SPEED = 5

# Delete the database file if it exists
#-#if os.path.exists("organism_data.db"):
#-#    os.remove("organism_data.db")

# Connect to the database
#-#conn = sqlite3.connect("organism_data.db")
#-#c = conn.cursor()

# Create a table to store the organism data
# ID, RED, organism1.speed, random.randint(0, 740), random.randint(0, 740), 7, 7, 500
#-#

#-#c.execute('''CREATE TABLE organisms
#-#             (id INT,
#-#              color TEXT,
#-#              speed INT, 
#-#              x INT,
#-#              y INT,
#-#              width INT,
#-#              height INT,
#-#              lifespan INT)''')


# display screen configuration
pg.display.set_caption("Greeblies! - Single Cell Simulation Game")
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')

# Create a UI theme dictionary with the desired text color and font
ui_theme = {
    "label": {
        "text_color": pg.Color("green"),
        "font": pg.font.Font(None, 10),  # Set the font here, replace 'None' with a font file path if needed
        "text_horiz_alignment": "left" 
    }
}

# Create the UI Manager instance, pulling some parameters from the theme.json file
# If you upate the theme.json file it will update the UI Manager's theme dynamically
manager = UIManager((SCREEN_WIDTH, SCREEN_HEIGHT),'theme.json', ui_theme)

# Create a clock to keep track of time
clock = pg.time.Clock()

# Define a font and render the text
font = pg.font.SysFont(None, 10)
font2 = pg.font.SysFont(None, 20)

# Starting Speed of the organisms
#speeds = [1, 1, 7, 5, 10]
green_speed = 1
dark_green_speed = 1
brown_speed = 7
yellow_speed = 5
red_speed = 10

# Starting light intensity
light_intensity = 1
start_num_green = 150
start_num_brown = 75
start_num_yellow = 50
start_num_red = 15

# Colors
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Define a function to make the movenment vectro random
def random_movement_vector(speed):
    direction = random.uniform(0, 2 * math.pi)
    dx = speed * math.cos(direction)
    dy = speed * math.sin(direction)
    return dx, dy

# Collision handlers to handle each typ of collision between organisms
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
    green_organism_data = get_organism_data_by_color(GREEN)
    new_organism = Organism(green_organism_data["color"], green_organism_data["speed"], random.randint(0, 740), random.randint(0, 740), green_organism_data["width"],
                            green_organism_data["height"], green_organism_data["starvation"], id_counter)
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
            brown_organism_data = get_organism_data_by_color(BROWN)
            new_organism = Organism(brown_organism_data["color"], brown_organism_data["speed"], random.randint(0, 740), random.randint(0, 740), brown_organism_data["width"],
                            brown_organism_data["height"], brown_organism_data["starvation"], id_counter)
            all_sprites.add(new_organism)  # Add the new organism to all_sprites group
            #all_sprites.add(Organism(BROWN, organism1.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 2000, id_counter))
            organism1.food_count = 0
               
    else :
        all_sprites.remove(organism1)
        organism2.food_count += 1
        organism2.hasNotEaten = 0 #resest starvation counter
        if organism2.food_count >= 3:
            update_id_counter()
            brown_organism_data = get_organism_data_by_color(BROWN)
            new_organism = Organism(brown_organism_data["color"], brown_organism_data["speed"], random.randint(0, 740), random.randint(0, 740), brown_organism_data["width"],
                            brown_organism_data["height"], brown_organism_data["starvation"], id_counter)
            all_sprites.add(new_organism)  # Add the new organism to all_sprites group
            #all_sprites.add(Organism(BROWN, organism2.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 2000, id_counter))
            organism2.food_count = 0

def handle_dark_green_brown_collision(organism1, organism2):
    if organism1.color == BROWN:
        all_sprites.remove(organism2)
        organism1.food_count += 1
        organism1.hasNotEaten = 0 #resest starvation counter
        if organism1.food_count >= 3:
            update_id_counter()
            brown_organism_data = get_organism_data_by_color(BROWN)
            new_organism = Organism(brown_organism_data["color"], brown_organism_data["speed"], random.randint(0, 740), random.randint(0, 740), brown_organism_data["width"],
                            brown_organism_data["height"], brown_organism_data["starvation"], id_counter)
            all_sprites.add(new_organism)  # Add the new organism to all_sprites group
            #all_sprites.add(Organism(BROWN, organism1.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 2000, id_counter))
            organism1.food_count = 0
               
    else :
        all_sprites.remove(organism1)
        organism2.food_count += 1
        organism2.hasNotEaten = 0 #resest starvation counter
        if organism2.food_count >= 3:
            update_id_counter()
            brown_organism_data = get_organism_data_by_color(BROWN)
            new_organism = Organism(brown_organism_data["color"], brown_organism_data["speed"], random.randint(0, 740), random.randint(0, 740), brown_organism_data["width"],
                            brown_organism_data["height"], brown_organism_data["starvation"], id_counter)
            all_sprites.add(new_organism)  # Add the new organism to all_sprites group
            #all_sprites.add(Organism(BROWN, organism2.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 2000, id_counter))
            organism2.food_count = 0

def handle_green_yellow_collision(organism1, organism2):
    if organism1.color == YELLOW:
        all_sprites.remove(organism2)
        organism1.food_count += 1
        organism1.hasNotEaten = 0 #resest starvation counter
        if organism1.food_count >= 5:
            update_id_counter()
            yellow_organism_data = get_organism_data_by_color(YELLOW)
            new_organism = Organism(yellow_organism_data["color"], yellow_organism_data["speed"], random.randint(0, 740), random.randint(0, 740), yellow_organism_data["width"],
                yellow_organism_data["height"], yellow_organism_data["starvation"], id_counter)
            all_sprites.add(new_organism)  # Add the new organism to all_sprites group

            #all_sprites.add(Organism(YELLOW, organism1.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 700, id_counter))
            organism1.food_count = 0
               
    else :
        all_sprites.remove(organism1)
        organism2.food_count += 1
        organism2.hasNotEaten = 0 #resest starvation counter
        if organism2.food_count >= 5:
            update_id_counter()
            yellow_organism_data = get_organism_data_by_color(YELLOW)
            new_organism = Organism(yellow_organism_data["color"], yellow_organism_data["speed"], random.randint(0, 740), random.randint(0, 740), yellow_organism_data["width"],
                yellow_organism_data["height"], yellow_organism_data["starvation"], id_counter)
            all_sprites.add(new_organism)  # Add the new organism to all_sprites group
            #all_sprites.add(Organism(YELLOW, organism2.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 700, id_counter))
            organism2.food_count = 0

def handle_brown_yellow_collision(organism1, organism2):
    if organism1.color == YELLOW:
        all_sprites.remove(organism2)
        organism1.food_count += 1
        organism1.hasNotEaten = 0 #resest starvation counter
        if organism1.food_count >= 5:
            update_id_counter()
            yellow_organism_data = get_organism_data_by_color(YELLOW)
            new_organism = Organism(yellow_organism_data["color"], yellow_organism_data["speed"], random.randint(0, 740), random.randint(0, 740), yellow_organism_data["width"],
                yellow_organism_data["height"], yellow_organism_data["starvation"], id_counter)
            all_sprites.add(new_organism)  # Add the new organism to all_sprites group    
            # all_sprites.add(Organism(YELLOW, organism1.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 700, id_counter))
            organism1.food_count = 0
               
    else :
        all_sprites.remove(organism1)
        organism2.food_count += 1
        organism2.hasNotEaten = 0 #resest starvation counter
        if organism2.food_count >= 5:
            update_id_counter()
            yellow_organism_data = get_organism_data_by_color(YELLOW)
            new_organism = Organism(yellow_organism_data["color"], yellow_organism_data["speed"], random.randint(0, 740), random.randint(0, 740), yellow_organism_data["width"],
                yellow_organism_data["height"], yellow_organism_data["starvation"], id_counter)
            all_sprites.add(new_organism)  # Add the new organism to all_sprites group
            #all_sprites.add(Organism(YELLOW, organism2.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 700, id_counter))
            organism2.food_count = 0

def handle_dark_green_yellow_collision(organism1, organism2):
    if organism1.color == YELLOW:
        all_sprites.remove(organism2)
        organism1.food_count += 1
        organism1.hasNotEaten = 0 #resest starvation counter
        if organism1.food_count >= 5:
            update_id_counter()
            yellow_organism_data = get_organism_data_by_color(YELLOW)
            new_organism = Organism(yellow_organism_data["color"], yellow_organism_data["speed"], random.randint(0, 740), random.randint(0, 740), yellow_organism_data["width"],
                yellow_organism_data["height"], yellow_organism_data["starvation"], id_counter)
            all_sprites.add(new_organism)  # Add the new organism to all_sprites group
            #all_sprites.add(Organism(YELLOW, organism1.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 700, id_counter))
            organism1.food_count = 0
               
    else :
        all_sprites.remove(organism1)
        organism2.food_count += 1
        organism2.hasNotEaten = 0 #resest starvation counter
        if organism2.food_count >= 5:
            update_id_counter()
            yellow_organism_data = get_organism_data_by_color(YELLOW)
            new_organism = Organism(yellow_organism_data["color"], yellow_organism_data["speed"], random.randint(0, 740), random.randint(0, 740), yellow_organism_data["width"],
                            yellow_organism_data["height"], yellow_organism_data["starvation"], id_counter)
            all_sprites.add(new_organism)  # Add the new organism to all_sprites group            
            #all_sprites.add(Organism(YELLOW, organism2.speed, random.randint(0, 740), random.randint(0, 740), 3, 3, 700, id_counter))
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
            red_organism_data = get_organism_data_by_color(RED)
            new_organism = Organism(red_organism_data["color"], red_organism_data["speed"], random.randint(0, 740), random.randint(0, 740), red_organism_data["width"],
                red_organism_data["height"], red_organism_data["starvation"], id_counter)
            all_sprites.add(new_organism)  # Add the new organism to all_sprites group
            #all_sprites.add(Organism(RED, organism1.speed, random.randint(0, 740), random.randint(0, 740), 7, 7, 500, id_counter))
            organism1.food_count = 0   
    else :
        all_sprites.remove(organism1)
        organism2.food_count += 1
        organism2.hasNotEaten = 0 #resest starvation counter
        if organism2.food_count >= 5:
            update_id_counter()
            red_organism_data = get_organism_data_by_color(RED)
            new_organism = Organism(red_organism_data["color"], red_organism_data["speed"], random.randint(0, 740), random.randint(0, 740), red_organism_data["width"],
                red_organism_data["height"], red_organism_data["starvation"], id_counter)
            all_sprites.add(new_organism)  # Add the new organism to all_sprites group
            #all_sprites.add(Organism(RED, organism2.speed, random.randint(0, 740), random.randint(0, 740), 7, 7, 500, id_counter))
            organism2.food_count = 0

def update_id_counter():
    global id_counter
    id_counter += 1

# callback handlers for the buttons
def start_button_callback():
    global started
    started = True

def stop_button_callback():
    global started
    started = False

def update_red_organism_size(text):
    new_size = int(text)
    update_red_organism_size(new_size, all_sprites)

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

            # Check if this organism is a red organism
        if self.color == RED:
            #
            # Check for nearby yellow organisms
            # nearby_yellow_organisms = [organism for organism in all_sprites if organism.color == YELLOW and organism != self and self.rect.colliderect(organism.rect)]
            nearby_yellow_organisms = [organism for organism in all_sprites if organism.color == YELLOW and organism != self and 
                            math.hypot(organism.rect.centerx - self.rect.centerx, organism.rect.centery - self.rect.centery) <= 30 + self.rect.width/2 + organism.rect.width/2]
            if nearby_yellow_organisms:
                #print("nearby_yellow_organisms: ", nearby_yellow_organisms)
                # Calculate the distance to the nearest yellow organism
                distances = [(organism.rect.x - self.rect.x) ** 2 + (organism.rect.y - self.rect.y) ** 2 for organism in nearby_yellow_organisms]
                nearest_yellow_organism = nearby_yellow_organisms[distances.index(min(distances))]
                
                # Calculate the movement vector towards the nearest yellow organism
                dx = nearest_yellow_organism.rect.x - self.rect.x
                dy = nearest_yellow_organism.rect.y - self.rect.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance > 0:
                    dx = dx / distance
                    dy = dy / distance
                magnitude = self.speed
                dx *= magnitude
                dy *= magnitude
                
            else:
                # Generate a random movement vector with a magnitude equal to the organism's speed
                direction = random.uniform(0, 2 * math.pi)
                dx = self.speed * math.cos(direction)
                dy = self.speed * math.sin(direction)
            
        else:
            # Generate a random movement vector with a magnitude equal to the organism's speed
            direction = random.uniform(0, 2 * math.pi)
            dx = self.speed * math.cos(direction)
            dy = self.speed * math.sin(direction)

        # Add the movement vector to the current position to obtain the new position
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # Check if the new position is within the screen boundaries and update the position accordingly
        if 0 <= new_x <= 740:
            self.rect.x = new_x
        if 0 <= new_y <= 740:
            self.rect.y = new_y
        # Otherwise, generate a random direction
        # direction = random.uniform(0, 2 * math.pi)
        # dx = magnitude * math.cos(direction)
        # # dy = magnitude * math.sin(direction)

        # # Add the movement vector to the current position to obtain the new position
        # new_x = self.rect.x + dx
        # new_y = self.rect.y + dy

        # # Check if the new position is within the screen boundaries and update the position accordingly
        # if 0 <= new_x <= 740:
        #     self.rect.x = new_x
        # if 0 <= new_y <= 740:
        #     self.rect.y = new_y
                
        # Check for light exposure count. If the organism is exposed to light, it will reproduce
        if self.color == GREEN or self.color == DARK_GREEN:
            if self.light_exposure_count >= 550:    
                update_id_counter()   
                green_organism_data = get_organism_data_by_color(GREEN)
                new_organism = Organism(green_organism_data["color"], green_organism_data["speed"], random.randint(0, 740), random.randint(0, 740), green_organism_data["width"],
                            green_organism_data["height"], green_organism_data["starvation"], id_counter)
                all_sprites.add(new_organism) 
                #all_sprites.add(Organism(GREEN, self.speed, random.randint(0, 740), random.randint(0, 740), 2, 2, 6000, id_counter))
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
        # Save the original x and y coordinates
        x = self.rect.x
        y = self.rect.y
        # Create the new surface and rect
        self.image = pg.Surface([size, size])
        self.rect = self.image.get_rect()
        # Fill the new surface with the original color
        self.image.fill(self.color)
        # Set the x and y coordinates to match the original rect
        self.rect.x = x
        self.rect.y = y
    def set_coor(self,new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y
        self.image.fill(self.color)

# Set up the gray bar and buttons
button_height = 30 # button height
button_width = 70 # button width
button_y = 6 # y coordinate of the buttons
start_button_X = GRID_WIDTH + 6 # x coordinate of the start button
stop_button_X = GRID_WIDTH + 84 # x coordinate of the stop button

# Create start and stop buttons # (self, x, y, w, h, text='', color=(255, 255, 255), font=None):
start_button = Button(start_button_X, button_y,  button_width, button_height, 'Start', GREEN, callback=start_button_callback)
stop_button = Button(stop_button_X, button_y,  button_width, button_height, 'Stop', RED, callback=stop_button_callback )
buttons = [start_button, stop_button]

# Create the text labels 100
text_1 = pygame_gui.elements.UILabel(relative_rect=pg.Rect((755, 60), (140, 20)),
                            text='Red Organism size',
                            manager=manager,
                            object_id="label" ) # Set the text color to green)
text_2 = pygame_gui.elements.UILabel(relative_rect=pg.Rect((755, 100), (140, 20)),
                            text='Green Organism size',
                            manager=manager,
                            object_id="label" ) # Set the text color to green)
# Create the input boxes
input_box1 = InputBox(755, 120, 100, 18, font, callback=update_red_organism_size)
#input_box1 = InputBox(755, 120, 100, 18)
input_box2 = InputBox(755, 140, 100, 18, font, callback=update_red_organism_size)
input_boxes = [input_box1, input_box2]

# Create the sliders
slider1 = HSlider(755, 160, 100, 18, 5, (1, 20), manager)
#slider2 = HSlider(755, 180, 100, 18, 25, (0, 50), manager)
#sliders = [slider1, slider2]

# Initialize the simulation
all_sprites = pg.sprite.Group()

organisms_data = [
    {"color": GREEN, "speed": green_speed, "width": 2, "height": 2, "starvation": 6000, "radar": 10},
    {"color": DARK_GREEN, "speed": dark_green_speed , "width": 3, "height": 3, "starvation": 6000, "radar": 10},
    {"color": BROWN, "speed": brown_speed, "width": 3, "height": 3, "starvation": 2000, "radar": 10},
    {"color": YELLOW, "speed": yellow_speed,   "width": 5, "height": 5, "starvation": 1000, "radar": 15},
    {"color": RED, "speed": red_speed , "width": 7, "height": 7, "starvation": 850, "radar": 20}
]
# Update the size of all RED organisms
def update_red_organism_size(size,all_sprites):
    for organism_data in organisms_data:
        if organism_data["color"] == RED:
            organism_data["width"] = size
            organism_data["height"] = size
            #break
    for organism in all_sprites:
        if organism.color == RED:
            organism.set_size(size)

# Get all Organism data by color
def get_organism_data_by_color(color):
    for data in organisms_data:
        if data["color"] == color:
            return data
    return None

# this function is used to create the starting organisms
for organism_data in organisms_data:
    if organism_data["color"] == GREEN:
        num_green = start_num_green
    elif organism_data["color"] == BROWN:
        num_brown = start_num_brown
    elif organism_data["color"] == YELLOW:
        num_yellow = start_num_yellow
    elif organism_data["color"] == RED:
        num_red = start_num_red
    
    for _ in range(num_green if organism_data["color"] == GREEN else
                   num_brown if organism_data["color"] == BROWN else
                   num_yellow if organism_data["color"] == YELLOW else
                   num_red if organism_data["color"] == RED else 0):
        update_id_counter()
        all_sprites.add(Organism(organism_data["color"], organism_data["speed"], random.randint(0, 740), random.randint(0, 740), organism_data["width"], \
                                  organism_data["height"], organism_data["starvation"], id_counter))
        num_sprites = len(all_sprites)
        all_organisms_text = font.render(f"Organism Count: {num_sprites}", True, WHITE)
        red_organisms_text = font.render(f"Red Count: {num_sprites}", True, WHITE)
        green_organisms_text = font.render(f"Green Count: {num_sprites}", True, WHITE)
        yellow_organisms_text = font.render(f"Yellow Count: {num_sprites}", True, WHITE)
        brown_organisms_text = font.render(f"Brown Count: {num_sprites}", True, WHITE)



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
        manager.process_events(event)

         # Handle slider events
        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == slider1.slider:
                    #pass
                    #print('Slider value:', event.value)
                    update_red_organism_size(event.value, all_sprites)
        start_button.handle_event(event)
        stop_button.handle_event(event)
        #for button in buttons:
        #    button.handle_event(event)
        for box in input_boxes:
            box.handle_event(event)
    mouse_pos = pg.mouse.get_pos()
    # Update button states
    start_button.update(mouse_pos)
    stop_button.update(mouse_pos)
    #for button in buttons:
    #    button.update(pg.mouse.get_pos())   
    for box in input_boxes:
        box.update()

    
    manager.update(time_delta)

    # # ID, RED, organism1.speed, random.randint(0, 740), random.randint(0, 740), 7, 7, 500
    if started:
        all_sprites.update(all_sprites)
    for organism in all_sprites:
        color_label = convert_color_to_label(organism.color)
        #-#data = (organism.id, color_label, organism.speed, organism.rect.x, organism.rect.y, organism.width, organism.height, organism.starvation_count)
        #-#c.execute("INSERT INTO organisms VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
    #-#conn.commit()          

    screen.fill((0, 0, 0))
    screen.blit(screen, (0, 0))

    if len(all_sprites) == 0: # Stop the game if there are no more sprites
        started = False
        running = False
        print("Game Over! Nothing left")
        text_surface = font.render(f"Total Organisms: Game Over!", True, WHITE)
    elif len([organism for organism in all_sprites if organism.color == RED]) == 0 \
        and len([organism for organism in all_sprites if organism.color == YELLOW]) == 0 \
        and len([organism for organism in all_sprites if organism.color == BROWN]) == 0 \
        and len([organism for organism in all_sprites if organism.color == WHITE]) == 0:
        started = False
        running = False
        print("Game Over! Only plant organisms left!")
        text_surface = font.render(f"Total Organisms: Game Over!", True, WHITE)


    # Draw the gray bar
    gray_bar_rect = pg.Rect(GRID_WIDTH, 0, SCREEN_WIDTH - GRID_WIDTH, SCREEN_HEIGHT)
    pg.draw.rect(screen, GRAY, gray_bar_rect)

    # Update and draw the UI elements
    manager.update(time_delta)
    manager.draw_ui(screen)

    # Draw the sprites and buttons
    all_sprites.draw(screen)
    #start_button.draw(screen)
    #stop_button.draw(screen)
    # Draw buttons
    start_button.draw(screen)
    stop_button.draw(screen)
    # Draw input boxes
    for box in input_boxes:
        box.draw(screen)
    #for slider in sliders:
    #    slider.draw(screen, time_delta)
    #slider1.draw(screen)

    screen.blit(all_organisms_text, (760, 640))
    screen.blit(red_organisms_text, (760, 660))
    screen.blit(green_organisms_text, (760, 680))
    screen.blit(yellow_organisms_text, (760, 700))
    screen.blit(brown_organisms_text, (760, 720))

    # Update the count of organisms
    num_sprites = len(all_sprites)
    # Count number of each color
    red_count = len([organism for organism in all_sprites if organism.color == RED])
    yellow_count = len([organism for organism in all_sprites if organism.color == YELLOW])
    green_count = len([organism for organism in all_sprites if organism.color == GREEN or organism.color == DARK_GREEN])
    brown_count = len([organism for organism in all_sprites if organism.color == BROWN])
    all_organisms_text = font2.render(f"Organism Count: {num_sprites}", True, WHITE)
    red_organisms_text = font2.render(f"Red Count: {red_count}", True, WHITE)
    green_organisms_text = font2.render(f"Green Count: {green_count}", True, WHITE)
    yellow_organisms_text = font2.render(f"Yellow Count: {yellow_count}", True, WHITE)
    brown_organisms_text = font2.render(f"Brown Count: {brown_count}", True, WHITE)
    #text_surface = font2.render(f"Total Organisms: {num_sprites}", True, WHITE)

    # Update the screen
    pg.display.flip()

#-#conn.close()
pg.quit()
sys.exit()