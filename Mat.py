import pygame
from pygame.locals import *
import sys
import math

import serial
import re
# Define the COM port and baud rate
com_port = 'COM4'
baud_rate = 9600

# Initialize Pygame

ser = serial.Serial(com_port, baud_rate)
print(f"Reading from {com_port} at {baud_rate} baud...")
pygame.init()
xp,yp=0,0
# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (0, 0, 0)
CUBE_COLOR = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Cube")

# Define the vertices of the cube
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

# Define the edges that connect the vertices
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
]

# Initialize rotation angles
angle_x = 0
angle_y = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Clear the screen
    screen.fill(BG_COLOR)

    # Rotate the cube around the X and Y axes
    rotated_vertices = []
    for vertex in vertices:
        x, y, z = vertex

        # Rotate around X-axis
        new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
        new_z = y * math.sin(angle_x) + z * math.cos(angle_x)

        # Rotate around Y-axis
        new_x = x * math.cos(angle_y) + z * math.sin(angle_y)

        rotated_vertices.append([new_x, new_y, new_z])

    # Draw the edges
    for edge in edges:
        start = rotated_vertices[edge[0]]
        end = rotated_vertices[edge[1]]
        pygame.draw.line(screen, CUBE_COLOR, (start[0] * 100 + WIDTH // 2, start[1] * 100 + HEIGHT // 2),
                         (end[0] * 100 + WIDTH // 2, end[1] * 100 + HEIGHT // 2), 2)

    pygame.display.flip()
    data = ser.readline().decode().strip()
    datax=list(map(int,data.split()))
    xpos,ypos=datax[0],datax[1]
    if abs(xp-xpos)>=5:
        if xpos-xp>=0:
            angle_x+=0.05
        elif xpos-xp<=0:
            angle_x-=0.05
        xp=xpos
        print("X is changing")
    if abs(yp-ypos)>=5:
        if ypos-yp>=0:
            angle_y-=0.05
        elif ypos-yp<=0:
            angle_y+=0.05
        yp=ypos
        print("Y is changing")
    print(xpos,ypos)
    # Update rotation angles

    # Limit the frame rate
    pygame.time.delay(10)

# Quit Pygame
pygame.quit()
sys.exit()
