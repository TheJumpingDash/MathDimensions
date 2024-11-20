#LP DISTANCE PROGRAM. CONTROLS: LEFT CLICK TO MOVE THE CIRCLE, SCROL TO CHANGE LP DISTANCE.
import pygame
import math
import pygame.freetype 
from pygame.locals import *

#create the screen
size = width, height = ((800, 800))
pygame.init()
textFont = pygame.freetype.SysFont("arial", 24)
running = True
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Lp distance demo')
clock = pygame.time.Clock()
screen.fill ((0, 0, 0))

#variable definition
angleIncrement = 3000
Xplayer = 0
Yplayer = 0
spinningAngle = 0
scrollWheelSensitivity = 0.1
stepLength = 10
p= 2

def angleBetweenPoints(u, v):
    cordsToZero = ((v[0]- u[0]), (v[1]- u[1]))
    angle = math.atan2(cordsToZero[1], cordsToZero[0])
    return angle

def findPointInLp(angle, lpDistance):
    cos = math.cos(angle)
    sin = math.sin(angle)

    LpDistToCircle = (abs(cos)**p + abs(sin)**p)**(1/p)
    euclidFinalLineLength = (lpDistance/LpDistToCircle)
    finalCords = (Xplayer +(cos*euclidFinalLineLength), Yplayer + (sin*euclidFinalLineLength))
    finalCords=finalCords
    return finalCords

#mainloop:
while running:
    mousex= pygame.mouse.get_pos()[0]
    mousey= pygame.mouse.get_pos()[1]
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            if event.y == -1:
                if p >= 1+round(scrollWheelSensitivity, 3):
                    p= round(p-scrollWheelSensitivity, 3)
            if event.y == 1:
                    p= round(p+scrollWheelSensitivity, 3)
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        anglePlayer = angleBetweenPoints((Xplayer, Yplayer),(mousex, mousey))
        Xplayer, Yplayer = findPointInLp (anglePlayer, stepLength)
    
    spinningAngle = 0
    while (spinningAngle <= (2*math.pi)):
        circleCords = findPointInLp(spinningAngle, 100)
        spinningAngle += 2*math.pi/(angleIncrement)
        pygame.draw.circle(screen, (155,38,182), circleCords, 1)

    textFont.render_to(screen, (width/2-25, height/4), f"p = {p}", (255, 255, 255))
    pygame.display.update()
    screen.fill((0, 0, 0))
    clock.tick(30) 