#!/bin/env python3

import numpy as np
import re
from PIL import Image
import pygame
from matplotlib import pyplot as plt
import subprocess
import pygame.freetype
import json
import random

# Initialize Pygame and open an 800x800 drawing window.
pygame.init()
w = pygame.display.set_mode([1600, 1200])

# Drawing state and configuration.
grid = []               # 2D pixel grid for the canvas
saved_places = set()     # recorded drawn cell positions (set = no duplicates, faster lookups)
pixel_size = 5       # size of each drawn square in pixels
font = pygame.freetype.Font(None,26)
font.fgcolor = (255,255,255)
playing = True
s_time = 60
running = True
inter = True
score = 0
# Reusable rectangle object for rendering drawn squares.
ink_rect = pygame.Rect(0, 0, pixel_size, pixel_size)
color = (0, 0, 0)        # black drawing color
running = True
c = pygame.time.Clock()  # frame rate limiter for the main loop

#Saves the image and sends it to doodle
def img_save(img_array, file_name, title='', show=True, cmap=None):
    """Save a NumPy image array to disk and optionally display it."""

    if show:
        plt.imshow(img_array.astype(np.uint8), cmap=cmap)
        plt.title(title)
        # plt.show()  # commented out to avoid blocking the script

    plt.imsave(file_name, img_array.astype(np.uint8), cmap=cmap)



#all images that the ai detects
classes = [
    "The Eiffel Tower",
    "The Great Wall of China",
    "The Mona Lisa",
    "aircraft carrier",
    "airplane",
    "alarm clock",
    "ambulance",
    "angel",
    "animal migration",
    "ant",
    "anvil",
    "apple",
    "arm",
    "asparagus",
    "axe",
    "backpack",
    "banana",
    "bandage",
    "barn",
    "baseball",
    "baseball bat",
    "basket",
    "basketball",
    "bat",
    "bathtub",
    "beach",
    "bear",
    "beard",
    "bed",
    "bee",
    "belt",
    "bench",
    "bicycle",
    "binoculars",
    "bird",
    "birthday cake",
    "blackberry",
    "blueberry",
    "book",
    "boomerang",
    "bottlecap",
    "bowtie",
    "bracelet",
    "brain",
    "bread",
    "bridge",
    "broccoli",
    "broom",
    "bucket",
    "bulldozer",
]

# grid = np.array(grid).astype(np.uint8)
# img_save(grid,"2.png",'Q2',show = True)
# Place a filled square at the current mouse position.
def place_ink(mx, my):
    global grid, saved_places

    # Snap the mouse coordinates to the drawing grid.
    mx = mx // pixel_size * pixel_size
    my = my // pixel_size * pixel_size

    # Only draw inside the canvas bounds.
    for i in range(pixel_size):
        for y in range(pixel_size):
            if mx+i >= 0+175 and mx+i + pixel_size <= 1600-175 and my+y >= 0+150 and my+y+5 <= 1200-150:
                grid[mx + i][my + y] = color

    # Only add this cell once per call, not once per inner-loop iteration
    saved_places.add((mx, my))


# Draw all saved ink cells onto the Pygame window.
#Draws all the pixels that were saved
def draw_ink():
    w.fill((255, 255, 255))
    r = pygame.Rect(0,0,1600,1200)
    pygame.draw.rect(w,(171, 170, 91),r,150)
    global ink_rect

    for pos in saved_places:
        ink_rect.x, ink_rect.y = pos
        x, y = pos

        c = grid[x][y]
        pygame.draw.rect(w, c, ink_rect)

#Since the image gets rotated when I try to save it, this funtion unrotates it
def un_rotate(grid):
    """Transpose the canvas grid so the saved image has the expected orientation."""
    new_grid = []
    for i in range(1200):
        col = []
        for j in range(1600):
            col.append("")
        new_grid.append(col)
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            new_grid[y][x] = grid[x][y]
    return new_grid
time = 60
#Finds out how to center the text in the middle of the screen using a string
def find_mid(text):
    fr = font.get_rect(text)
    fx,fy = -fr.x//2+400, -fr.y//2+600

    return (fx,fy)
#Takes two points and uses place ink to make a line to try to fix the lag 
def draw_points(p1, p2):
    global times
    x1, y1 = p1

    if times == 0:
        x2, y2 = x1, y1
        times += 1
    else:
        x2, y2 = p2

    if x1 - x2 != 0:
        slope = (y1 - y2) / (x1 - x2)
    else:
        slope = None

    s_x, s_y = x1, y1
    same = False
    while not same:
        if s_x == x2 and s_y == y2:
            same = True
            break

        place_ink(int(s_x), int(s_y))
        if slope !=None:
            if s_x > x2:
                s_x -= 1
                s_y -= slope
            elif s_x < x2:
                s_x += 1
                s_y += slope

            else:
                same = True
        else:
            if s_y != y2:
                if s_y<y2:
                    s_y+=1
                else:
                    s_y-=1
            else:
                same = True
times = 0
time = s_time
#Main game loop
point_1 = (0,0)
point_2 = (0,0)
while playing:
    #Gets a random image to use
    ran_image = random.choice(classes)

    #Makes a new grid
    grid = []
    for x in range(1600):
        col = []
        for y in range(1200):
            col.append((255, 255, 255))
        grid.append(col)

    #Drawing loop
    if score == 0:
        time = s_time
    while running:
        #Event loop
        for e in pygame.event.get():
            #Detects if pygame is closed to make everything close
            if e.type == pygame.QUIT:
                running = False
                playing = False
            #Sees if space is pressed and ends it early
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    # Stop drawing and proceed to inference.
                    running = False
        #Sees if the left mouse is down and draws
        if pygame.mouse.get_pressed() == (1, 0, 0):
            m_x, m_y = pygame.mouse.get_pos()
            point_1 = (m_x,m_y)
            draw_points(point_1,point_2)
            place_ink(m_x, m_y)
            point_2 = point_1
        else:
            times = 0
        if time <= 0:
            running = False
        time -= c.get_time()/1000
        #renders the ink and text
        draw_ink()
        font.render_to(w,(0,0), f"Time left: {int(time)}")
        fx,fy = find_mid(f"Draw: {ran_image}")
        font.render_to(w,(fx,0),f"Draw: {ran_image}")
        font.render_to(w,(1000,0),f"Press space to end early       Score: {score}")
        pygame.display.flip()
        #ticks the clock
        c.tick(60)

    # Save the drawn canvas and run the model on the saved image.
    #Fills the screen and renders fonts
    w.fill((171, 170, 91))
    fx,fy = find_mid("Calculating, don't click, it wont take long")
    font.render_to(w,(500,500),"Calculating, don't click, it wont take long")
    #Unrotates the image
    grid = un_rotate(grid)
    #Turns image into np array
    grid = np.array(grid).astype(np.uint8)
    pygame.display.flip()
    #saves teh array as a jpg
    img_save(grid, "training/classification/data/doodle/game/doodle.jpg", 'Q2', show=True)
    #The varibles that are for running the ai
    net = "models/doodle"
    dataset = "data/doodle"
    name = "doodle"
    #If pygame is not quited then we run the ai
    if playing:
        result = subprocess.run(
            ["imagenet.py",
             f"--model={net}/resnet18.onnx",
             f"--labels={dataset}/labels.txt",
             "--input_blob=input_0",
             "--output_blob=output_0",
             f"{dataset}/game/{name}.jpg",
             "output.jpg"],
            cwd="/home/adam/jetson-inference/python/training/classification",
            capture_output=True,
            text=True
        )
        #Seaches the output for the thing the ai thought what the user made
        output_match = re.search(r"^.*imagenet:.*\((.*)\)$", result.stdout, re.MULTILINE)
        #If it outputs something do everything else, if not just do nothing
        if output_match:
            #The thing that the user drew
            image = output_match.group(1)
            print(image)
        running = True
        inter = True
        #End drawing loop
        if ran_image == image:
            font.render_to(w,(fx,fy+50),f"You drew it correct you get +1 score")
        else:
            font.render_to(w,(fx,fy+50),f"You drew it wrong you're score is set to 0")
        while inter:
            #Reset the screen
            w.fill((171, 170, 91))
            #Event loop
            for e in pygame.event.get():
                #sees if user quit
                if e.type == pygame.QUIT:
                    inter = False
                    running = False
                    playing = False
                #Sees if player pressed space then run the game
                elif e.type == pygame.KEYDOWN:
        
                    if e.key == pygame.K_SPACE:
                        inter = False
                        break
            #renders the fonts
            fx,fy = find_mid(f"You got: {image}   Press space to move on.")
            font.render_to(w,(fx,fy),f"You got: {image}   Press space to move on.")
            #If the random image is same a normal then score +1 if not then score is reset to 0
            if ran_image == image:
                font.render_to(w,(fx,fy+50),f"You drew it correct you get +1 score")
                time = s_time//2
            else:
                font.render_to(w,(fx,fy+50),f"You drew it wrong you're score is set to 0")
                time = 60
            pygame.display.flip()
            c.tick(30)
    #Ticks main loop
    c.tick(60)