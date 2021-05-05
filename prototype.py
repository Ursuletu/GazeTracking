import pygame as game
import pygame.math as math
from pygame.time import Clock
import random as r


import cv2
import numpy as np
from mss import mss
from PIL import ImageGrab, Image, ImageTk
from tkinter import *

from gaze_tracking import GazeTracking

game.init()

game.display.set_caption("Gazetracking Example")
screen = game.display.set_mode([1280, 1600])

time = 0
gameon = True
bgcolor = game.color.Color("#ffffff")
black = game.color.Color("black")
clock = Clock()

item = game.image.load("focus.png")
items = []
SPAWNENEMY = 1
CLOCK = 1

textToRead = game.image.load("textToRead.png")

game.time.set_timer(SPAWNENEMY, 800)
game.time.set_timer(CLOCK, 1000)

font=game.font.Font(None,20)
timetext=font.render("Time: 0", 0, black)

# Select a random initial position vector.
posn = math.Vector2(1280/2 - 300 , 800/2)

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while gameon:
    screen.fill(bgcolor)

    _, frame = webcam.read()
    gaze.refresh(frame)
    frame = gaze.annotated_frame()

    # Coordinates extracted here as tuple (Left, Right)
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    # Coordinates to be extracted to these variables
    xR = 0
    yR = 0
    xL = 0
    yL = 0

    if left_pupil is not None:
        xL = left_pupil[0]
        yL = left_pupil[1]
        print('x lefteye:' + str(xL))
        print('y lefteye:' + str(yL))

    
    if right_pupil is not None:
        xR = right_pupil[0]
        yR = right_pupil[1]
        print('x righteye:' + str(xR))
        print('y righteye:' + str(yR))
   
    # Create a random speed vector.
    speed = 2
    dx = 1+1
    dy = 1
    vector = math.Vector2(dx, dy)

    # Each item is a [position, speed vector].
    items.append([posn, vector])

    event = game.event.poll()

    if event.type == game.QUIT:
        gameon = False;

    for it in items:
        # Update positions.
        it[0] += it[1]  # Update position using speed vector.

    w, h = game.display.get_surface().get_size()

    screen.blit(textToRead, (0, 0))
 
    screen.blit(item, (150, (yR + yL)/1.5 - 300))

    clock.tick(60)
    game.display.flip()
