import pygame, sys, random
from pygame.locals import *

pygame.init()

# Colours RGB Values
BACKGROUND = (255, 192, 203)  # pink

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
ACCELERATION = 0.75

# Initialize the window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')


# The main function that controls the game
def main():
    looping = True
    
    # Initialize Mortis position and velocity
    characterX = 375
    characterY = 275
    velocityY = -15
    velocityX = 10

    # Initialize Bull position and velocity
    

    while looping:
        # Get inputs (arrow keys, spacebar, etc.)
        for event in pygame.event.get():
            # Quit the game if the user closes the window
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    velocityY = -20
        
        # Processing
        if characterY > WINDOW_HEIGHT - 100:
            characterY = WINDOW_HEIGHT - 100

        # Update Bull position
        

        # Render elements of the game
        WINDOW.fill(BACKGROUND)

        pygame.display.update()
        fpsClock.tick(FPS)

main()
