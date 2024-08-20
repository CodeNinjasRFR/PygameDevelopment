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
BULL_SPEED = 5  # Speed at which the Bull moves left

# Initialize the window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')

# Load and scale the Mortis and Bull images
MORTIS_IMAGE = pygame.image.load('./mortissprite.png')
scaled_mortis_image = pygame.transform.scale(MORTIS_IMAGE, (100, 100))

TICK_HEAD = pygame.image.load('./Tick_head.png')  # Replace with the actual Bull sprite path
scaled_tick_image = pygame.transform.scale(TICK_HEAD, (50, 50))
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
    tickX1 = WINDOW_WIDTH+200
    tickX2 = WINDOW_WIDTH
    tickY1 = random.randint(0, WINDOW_HEIGHT - 50)  # Random Y position within the window height
    tickY2 = random.randint(0, WINDOW_HEIGHT - 50)  # Random Y position within the window height
    tick_velocityX = -BULL_SPEED

    player_rect = pygame.Rect(characterX, characterY, 100, 100)
    tick_rect1 = pygame.Rect(tickX1, tickY1, 50, 50)
    tick_rect2 = pygame.Rect(tickX2, tickY2, 50, 50)

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
        player_rect.topleft = (characterX, characterY)
        # Update Enemy position
        tickX1 += tick_velocityX
        if tickX1 < -50:  # If the Bull goes off the screen on the left
            tickX1 = WINDOW_WIDTH
            tickY1 = random.randint(0, WINDOW_HEIGHT - 50)  # Reset Bull to a new random Y position
            score+=1
        tick_rect1.topleft = (tickX1, tickY1)
        tickX2+=tick_velocityX
        if tickX2 <-50:
            tickX2=WINDOW_WIDTH
            tickY2=random.randint(0,WINDOW_HEIGHT-50)
            score+=1
        tick_rect2.topleft = (tickX2, tickY2)

        if player_rect.colliderect(tick_rect1) or player_rect.colliderect(tick_rect2):
            game_over = True
        # Render elements of the game
        WINDOW.fill(BACKGROUND)
        WINDOW.blit(scaled_mortis_image, (characterX, characterY))
        WINDOW.blit(scaled_tick_image, (tickX1, tickY1))
        WINDOW.blit(scaled_tick_image, (tickX2, tickY2))


        pygame.display.update()
        fpsClock.tick(FPS)
    show_splash_screen(score)

main()
