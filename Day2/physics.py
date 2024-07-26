# importing necessary libraries and starting pygame
import pygame, sys, random
from pygame.locals import *
pygame.init()
 
# Colours RGB Values
BACKGROUND = (255, 255, 255)
PLAYER = (255, 0, 0)
# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
ACCELERATION = 1
# Initialize the window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')
 

# The main function that controls the game
def main () :
    looping = True
    
    characterX=375
    characterY=275
    velocityY=-10
    velocityX=10
    while looping :
      # Get inputs (arrow keys, spacebar, etc.)
      for event in pygame.event.get() :
        # Quit the game if the user closes the window
        if event.type == QUIT :
          pygame.quit()
          sys.exit()
        
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                velocityY=-20
    
      # Processing
      # This section will be built out later
      velocityY+=ACCELERATION
      characterY+=velocityY
      
      characterX+=velocityX
      characterX= characterX%WINDOW_WIDTH

      rectangle1 = pygame.Rect(characterX, characterY, 50, 50) # x, y, width, height

      # Render elements of the game
      WINDOW.fill(BACKGROUND)
      pygame.draw.rect(WINDOW, PLAYER, rectangle1)

      pygame.display.update()
      fpsClock.tick(FPS)
 
main()


# Challenges:
# 1. Change the background color
# 2. Change the size of the window
# 3. Change the title of the window