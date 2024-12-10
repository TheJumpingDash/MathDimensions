#FRACTAL DIMENSIONS MEASURER. CONTROLS: 
#LEFT AND RIGTH MOVEMENT: LEFT AND RIGTH ARROWS
#SMALL STEPS LEFT AND RIGTH: “A” AND “D”
#SHORTENING AND PROLONGING THE LAST LINE: H AND D
#PLACING THE LINE: SPACE
import sys
import math
import pygame
from pygame.locals import *


# Initializes the screen
size = width, height = (3000, 2000)
pygame.init()
running = True
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
screen.fill((0, 0, 0))


#Initial conditions
location = 'capDeCreus'
inmutable_line_length = 100
line_length = inmutable_line_length
line_angle = 0


# Loads the image, in this example I have three images ready.
if location=='barcelona':
    mapImage = pygame.image.load("map1.5.png") #Here goes the name of the image file: Must be in the same folder as the code.
    circle_center = [1080, 1206]
elif location=='capDeCreus':
    mapImage = pygame.image.load("map1.7.png")
    circle_center = [1309, 1119]
else:
    mapImage = pygame.image.load("mapkoch.png")
    circle_center = [1165, 786]
mapImage_loc = mapImage.get_rect()
mapImage_loc.center = width/2, height/2


#variable declaration
circleCenterMove = False
l_arrowdown = False
r_arrowdown = False
lineArray = []
lastLine=False


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE: #allows exit
                running = False
            if event.key == K_LEFT: #move the line left and rigth.
                l_arrowdown = True
            if event.key == K_RIGHT:
                r_arrowdown = True
            if event.key == K_a: #There are two different line controls to make the measuring process easier.
                line_angle -= 0.03
            if event.key == K_d:
                line_angle += 0.03
            if event.key == K_h:
                line_length -=3 #changes the line length for the last step.
                lastLine=True   #(after the last step, the total length is displayed in the console)
            if event.key == K_g:
                line_length +=3
            if event.key == K_SPACE: #pressing space settles the line down.
                circleCenterMove = True
            elif event.key != K_SPACE:
                circleCenterMove = False
        elif event.type == KEYUP:
            if event.key== K_LEFT:
                l_arrowdown = False
            if event.key== K_RIGHT:
                r_arrowdown = False
   
    if l_arrowdown == True:
        line_angle -= 0.05
    if r_arrowdown == True:
        line_angle += 0.05


    screen.fill((0, 0, 0))   # Clears the screeen
    screen.blit(mapImage, mapImage_loc)


    # Calculates the line endpoint using trigonometry
    line_endpoint_x = int(circle_center[0] + line_length * math.cos(line_angle))
    line_endpoint_y = int(circle_center[1] + line_length * math.sin(line_angle))


    line_color = (255, 0, 0)


    #All lines are stored in the lineArray to be displayed.
    if circleCenterMove == True:
        lineArray.append(((circle_center[0], circle_center[1]),(line_endpoint_x, line_endpoint_y)))
        print(lineArray)
        if lastLine==True:
            print(len(lineArray)-1 + line_length/inmutable_line_length)
            sys.exit() #automatically quits after the last line (the one that has been shortened) is placed.


    counter = 0
    for i in lineArray: #draws the lines
        pygame.draw.line(screen, line_color, (lineArray[counter] [0] [0], lineArray[counter] [0] [1]),(lineArray[counter] [1] [0], lineArray[counter] [1] [1]), 2)  
        counter +=1


    if circleCenterMove == True: #calculates where the next line should go if one is placed.
        circle_center[0] = line_endpoint_x
        circle_center[1] = line_endpoint_y
        line_endpoint_x = int(circle_center[0] + line_length * math.cos(line_angle))
        line_endpoint_y = int(circle_center[1] + line_length * math.sin(line_angle))
        circleCenterMove = False


    # Draws the line that pivots.
    pygame.draw.line(screen, line_color, circle_center, (line_endpoint_x, line_endpoint_y), 2)
    pygame.display.update()
    clock.tick(30)
