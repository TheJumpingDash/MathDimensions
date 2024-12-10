import pygame
import math
from pygame.locals import *
import numpy as np
###########################SCREEN INITIALIZATION###########################
size = width, height = ((800, 800))
pygame.init()
running = True
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Disc de Pointcaré')
clock = pygame.time.Clock()
screen.fill ((0, 0, 0))
############################CREATION OF VARIABLES#########################
playerPosition = ((600), (600))
newPlayerPosition = ((600), (600))
playerRadius = 5
point1 = (0, 0)
point2 = (0, 0)
point3 = (0, 0)
point4 = (0, 0)
center = (0, 0)
radius = 20
hyperVelocity = 2
shouldMove= False

##############################MATH##########################
def euclidDist(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def normalise(a):
    if isinstance(a, (tuple, list)):
        return [normalise(n) for n in a]
    else:
        return (a-(width/2))/(width/2)

def deNormalise(a):
    if isinstance(a, (tuple, list)):
        return [deNormalise(n) for n in a]
    else:
        return a * (width/2) + width/2

def castIntoInt(a):
    a = [int(x) for x in a]
    return a 

def intersec2Circles(rad1, center1, rad2, center2):
    distance = euclidDist(center1, center2)
    pDistance = (rad1**2-rad2**2+distance**2)/(2*distance) #distance from the center of the first circle to the midpoint of the line that connects the two intersection points 
    p = (
        (center1[0] + pDistance*(center2[0]-center1[0])/distance), 
        (center1[1] + pDistance*(center2[1]-center1[1])/distance)
    )
    pToIntersec = math.sqrt(rad1**2-pDistance**2)#distance from the midpoint to the intersection points
    Intersec1 = ((p[0] + pToIntersec*(center2[1]-center1[1])/distance),(p[1] - pToIntersec*(center2[0]-center1[0])/distance))
    Intersec2 = ((p[0] - pToIntersec*(center2[1]-center1[1])/distance),(p[1] + pToIntersec*(center2[0]-center1[0])/distance))
    
    return Intersec1, Intersec2

def intersecCircleLine(rad, center, point1, point2):

    #Obtain line equation quocients
    a = point2[1] - point1[1]
    b = point2[0] - point1[0]
    c = -a*point1[0]+b*point1[1]
    F = a/b
    G = c/b

    #Obtain circle equation quocients
    A =-2*center[0]
    B = -2*center[1]
    C = center[0]**2+center[1]**2-rad**2

    #Combine both equations
    H = 1+F**2
    I = 2*F*G  + A + B*F
    J = B*G + C + G**2

    #Second degree equation
    result = [[0, 0], [0, 0]]
    result[0] [0] = (-I + math.sqrt(I**2 - 4*H*J))/(2*H)
    result[1] [0] = (-I - math.sqrt(I**2 - 4*H*J))/(2*H)

    #Finally, solve for x to obtain the y values
    for i in result:
        i [1] = F* i [0] + G  
    return result

def hiperbolicDistance(idealPoints, a, b): 
    if (euclidDist(a, idealPoints[0]) < euclidDist(b, idealPoints[0])): 
        #arranges the points so that (p is always the closest to a) and (q is closest to b)
        p = idealPoints[0]
        q = idealPoints[1]
    else:
        p = idealPoints[1]
        q = idealPoints[0]
    return np.log((euclidDist(a, q)*euclidDist(p,b))/(euclidDist(a, p)*euclidDist(q, b)))

def findParabola(p1, p2):#receives normalised points

    multiplierx = (p1[1]*((p2[0]**2)+(p2[1]**2)+1)-p2[1]*((p1[0]**2)+(p1[1]**2)+1))/(p1[0]*p2[1]-p2[0]*p1[1])
    multipliery = (p2[0]*((p1[0]**2)+(p1[1]**2)+1)-p1[0]*((p2[0]**2)+(p2[1]**2)+1))/(p1[0]*p2[1]-p2[0]*p1[1])
    return find_circle_center_radius(multiplierx, multipliery)


def find_circle_center_radius(A, B):
    # Coefficients of the equation x^2 + y^2 + Ax + By + 1 = 0
    # Complete the square for x terms
    h = -A / 2
    k = -B / 2
    
    # Calculate the constant term to move to the right side
    r_squared = (A / 2) ** 2 + (B / 2) ** 2 - 1
    
    # Calculate the radius
    r = math.sqrt(r_squared)
    return (h, k), r

def makeAStep(pointList, a, mousePosition, circleOrLineInfo, isCircle):
    #"a" is the player position, pointList is p and q, we need to calculate b
    stepLength = 1/10
    if hiperbolicDistance(pointList, a, mousePosition) < stepLength:
        finalPoint = mousePosition #teleports to position if the step is close enogh
    else:
        intersects = [] 
        filteredIntersects = [] 
        for i in (0,1): #Has to loop through two possible circles, as the p and q points can be shuffled 
            if i == 0:
                p = pointList[0]
                q = pointList[1]
            else:
                q = pointList[0]
                p = pointList[1]
 
            N = (math.exp(stepLength)*euclidDist(a, p)/euclidDist(a, q))**2
            A=(N-1)
            B=(-2*N*q[0]+2*p[0])
            D=(-2*N*q[1]+2*p[1])
            E=(N*q[0]**2+N*q[1]**2-p[0]**2-p[1]**2)
            center = ((-B/(2*A)), (-D/(2*A)))
            radius= math.sqrt((B/(2*A))**2+(D/(2*A))**2-E/A)
            
            if isCircle:
                radOfBigCircle = circleOrLineInfo[0] 
                centerOfBigCircle = circleOrLineInfo[1] 
                intersects.append(intersec2Circles(radius, center, radOfBigCircle, centerOfBigCircle))
            else:
                intersects.append(intersecCircleLine(radius, center, pointList[0], pointList[1]))  
        filteredIntersects = [a for n in intersects for a in n if (math.sqrt(a[0]**2+a[1]**2) < 1)] #removes points not in the unit disk.

        try:        
            if hiperbolicDistance(pointList, filteredIntersects[0], mousePosition) < hiperbolicDistance(pointList, filteredIntersects[1], mousePosition):
                finalPoint = filteredIntersects[0] #finally aquired the final point, by selecting the one closest to the mouse hiperbolic-wise.
            else:
                finalPoint = filteredIntersects[1]
        except IndexError:
            finalPoint = filteredIntersects[0]
    
    return finalPoint
   
def drawLine(pointa, pointb): 
    if ((pointa != (0, 0)) and (pointb != (0, 0))):  #This is so that it starts after two points are put down.
        try:  
            center, radius = findParabola(normalise(pointa), normalise(pointb))
            pygame.draw.circle(screen, (0, 0, 0), castIntoInt(((center[0]*(width/2)+(width/2)), (center[1]*(width/2)+(width/2)))), int(radius*(width/2)), 1) 
        except ZeroDivisionError: #ZeroDivisionError = it is a straight line
            pygame.draw.line(screen, (0, 255, 0), pointa, pointb, 2)

    pygame.draw.circle(screen, (255, 127, 0), castIntoInt(pointa), 3)
    pygame.draw.circle(screen, (19, 144, 247), castIntoInt(pointb), 3)

################################MAIN LOOP##################################
while running :

    #############################INPUTS##############################
    posx= pygame.mouse.get_pos()[0]
    posy= pygame.mouse.get_pos()[1]
    for event in pygame.event.get():

        if event.type == QUIT:
            running = False

        if event.type == MOUSEBUTTONDOWN:
            if (math.sqrt(( normalise(posx))**2 + (normalise(posy))**2) < 1):
                if (event.button ==1):
                    point1 = (posx, posy)
                elif (event.button==3):
                    point2 = (posx, posy)

        if event.type==KEYDOWN:
            if (math.sqrt(( normalise(posx))**2 + (normalise(posy))**2) < 1):
                if(event.key == K_a):
                    point3 = (posx, posy)
                elif (event.key == K_s):
                    point4 = (posx, posy)

    ################################SCREEN UPDATES AND FUNCTION CALLING############################
    screen.fill((0, 0, 0))  # Clear the screen
    pygame.draw.circle(screen, (255, 255, 255), ((width/2), (width/2)), (width/2))
    pygame.draw.circle(screen, (0, 0, 0), ((width/2), (width/2)), 2)

    drawLine(point1, point2)
    drawLine(point3, point4)   

    if pygame.mouse.get_pressed()[1]: #MOVEMENT OF THE PLAYER HERE

        normMousePosition = normalise((posx, posy))
        if math.sqrt(normMousePosition[0]**2+normMousePosition[1]**2) < 1:
            normPlayerPosition = normalise(playerPosition) 
            try:
                normCenterPlayer, normRadiusPlayer = findParabola(normPlayerPosition, normMousePosition)
                IdealPointListPlayer = intersec2Circles(1, (0, 0), normRadiusPlayer, normCenterPlayer)
                normPlayerPosition= makeAStep(IdealPointListPlayer, normPlayerPosition, normMousePosition, (normRadiusPlayer, normCenterPlayer), True)
            except ZeroDivisionError:
                try:
                    IdealPointListPlayer = intersecCircleLine(1, (0, 0), normPlayerPosition, normMousePosition)
                    normPlayerPosition= makeAStep(IdealPointListPlayer, normPlayerPosition ,normMousePosition, [0, 0], False)
                except ZeroDivisionError:
                    pass #error prevention
        
        newPlayerPosition = [int(a) for a in deNormalise(normPlayerPosition)]

        if euclidDist(playerPosition, newPlayerPosition) > 0.01:
            euclidStepLength = euclidDist(playerPosition, newPlayerPosition)
            hiperStepLength = hiperbolicDistance(IdealPointListPlayer, normalise(playerPosition), normalise(newPlayerPosition))
            if euclidStepLength > 1:
                radius = max(0.2 * euclidStepLength / hiperStepLength, 1)

            playerPosition = newPlayerPosition    
            
    pygame.draw.circle(screen, (155,38,182), newPlayerPosition, radius)
    pygame.display.update()

    clock.tick(30)
 