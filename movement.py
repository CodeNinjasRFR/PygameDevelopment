# importing necessary libraries and starting pygame
import pygame, sys, random
from pygame.locals import *
pygame.init()
 
# Colours RGB Values
BACKGROUND = (255, 255, 255)
CHARACTER = (255, 30, 70)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
 
# Initialize the window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')
 
# The main function that controls the game
def main():
    looping = True
    characterX = 375
    characterY = 275
    characterWidth = 50
    characterHeight = 50
    
    # Dictionary to keep track of the state of each key
    keys = {
        K_RIGHT: False,
        K_LEFT: False,
        K_UP: False,
        K_DOWN: False,
        K_a: False,
        K_d: False,
        K_w: False,
        K_s: False
    }

    while looping:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            # Check for key presses and releases
            if event.type == KEYDOWN:
                
                # if a movement key is pressed update True
                if event.key in keys:
                    keys[event.key] = True
                
                # when spacebar pressed go to random spot
                elif event.key == K_SPACE:
                    characterX = random.randint(0, WINDOW_WIDTH - characterWidth) # python random function to set position
                    characterY = random.randint(0, WINDOW_HEIGHT - characterHeight)

            elif event.type == KEYUP:
                
                # if a movement key is unpressed update False
                if event.key in keys:
                    keys[event.key] = False
        

        # Update character position based on key states
        if keys[K_RIGHT] or keys[K_d]:
            characterX += 3
        if keys[K_LEFT] or keys[K_a]:
            characterX -= 3
        if keys[K_UP] or keys[K_w]:
            characterY -= 3
        if keys[K_DOWN] or keys[K_s]:
            characterY += 3

        # Create character rectangle
        character = pygame.Rect(characterX, characterY, characterWidth, characterHeight)

        # Rendering
        WINDOW.fill(BACKGROUND)
        pygame.draw.rect(WINDOW, CHARACTER, character)
        pygame.display.update()
        
        fpsClock.tick(FPS)


 
main()


# Challenges:
# 1. Change how fast the player moves
# 2. Make it so that when you press 'r' the player respawns at the center of the screen
# 3. Make the player's color change when you press a certain button