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


def show_splash_screen(score):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:  # Press SPACE to exit splash screen
                    return

        # Render splash screen
        WINDOW.fill(BACKGROUND)
        font = pygame.font.Font(None, 74)
        text = font.render('Game Over - Score: ' + str(score), True, (0,0,0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        WINDOW.blit(text, text_rect)

        font = pygame.font.Font(None, 36)
        instruction_text = font.render('Press SPACE to exit', True, (0,0,0))
        instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        WINDOW.blit(instruction_text, instruction_rect)

        pygame.display.update()
        fpsClock.tick(FPS)

# The main function that controls the game
def main():
    looping = True
    game_over = False
    score=0
    # Initialize Mortis position and velocity
    characterX = 100
    characterY = 275
    velocityY = -15

    # Initialize Bull position and velocity
  



    while not game_over:
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
        velocityY += ACCELERATION
        characterY += velocityY

        if characterY > WINDOW_HEIGHT - 100:
            characterY = WINDOW_HEIGHT - 100
        # Update Enemy position
        

       
        # Render elements of the game
        WINDOW.fill(BACKGROUND)


        pygame.display.update()
        fpsClock.tick(FPS)
    show_splash_screen(score)

main()
