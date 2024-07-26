# importing necessary libraries and starting pygame
import pygame, sys, random
from pygame.locals import *
pygame.init()
 
# Colours RGB Values
BACKGROUND = (255, 255, 255)
 
# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Character info
RED = (255, 0, 0)
GREEN= (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE= (255, 165, 0)
PURPLE= (128, 0, 128)
YELLOW= (255, 255, 0)
# Initialize the window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')
 
# main code for game
def main () :
    looping = True

    while looping :
        for event in pygame.event.get() :
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
    
        # Processing 
        rectangle1 = pygame.Rect(10, 30, 50, 50) # x, y, width, height
        rectangle2 = pygame.Rect(100,30,50,50)
        # Render elements of the game
        WINDOW.fill(BACKGROUND)
        pygame.draw.rect(WINDOW, RED, rectangle1) #surface, color, rectangle dimensions
        pygame.draw.rect(WINDOW, BLUE, rectangle2,2) #<- optional arg thickness works for all shapes
        
        pygame.draw.circle(WINDOW, GREEN, (200, 100), 30) #surface, color, center (x,y), radius <- optional args(... topRight, topleft, bottomRight, bottomLeft) True/False
    
        pygame.draw.line(WINDOW, PURPLE, (300, 200), (400, 200), 3) #surface,color,(startX,startY),(endX,endY),thickness
    
        #accessing data ingame example:
        print(rectangle1.x)

        pygame.display.update()
        fpsClock.tick(FPS)
main()

# Challenges:
# 1. Draw an orange circle at x 500 y 300 with radius 25
# 2. Draw a yellow circle centered in the middle of the game with radius 50