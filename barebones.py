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
 
# Initialize the window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')
 
# The main function that controls the game
def main () :
    looping = True
  
    # The main game loop. Essentially runs until the game stops or we say so
    # Standard steps for a game loop in professional games:
    # 1. Get inputs (arrow keys, spacebar, etc.)
    # 2. Process changes (move enemies, lower health, lower timers, etc.)
    # 3. Show changes (draw the new changes on the screen)

    while looping :
      # Get inputs (arrow keys, spacebar, etc.)
      for event in pygame.event.get() :
        # Quit the game if the user closes the window
        if event.type == QUIT :
          pygame.quit()
          sys.exit()
    
      # Processing
      # This section will be built out later
 
      # Render elements of the game
      WINDOW.fill(BACKGROUND)
      pygame.display.update()
      fpsClock.tick(FPS)
 
main()


# Challenges:
# 1. Change the background color
# 2. Change the size of the window
# 3. Change the title of the window