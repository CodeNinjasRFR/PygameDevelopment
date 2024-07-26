import pygame, sys, random
from pygame.locals import *
pygame.init()


def main():

    # Colours RGB Values
    BACKGROUND = (255, 255, 255)
    PLAYER = (255, 30, 70)
    COLLECTABLE = (255, 192, 203)
    TEXT_COLOR = (0, 0, 0)  

    # Game Setup
    FPS = 60
    fpsClock = pygame.time.Clock()
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600

    # Initialize the window
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Collect the cubes!')
    
    # Set up font
    font = pygame.font.Font(None, 36)  # None uses the default font, 36 is the font size

    # setup score at 0
    score = 0

    # Set up character to start in middle (800/2 - playerWidth/2)
    characterX = 375
    characterY = 275
    characterWidth = 50
    characterHeight = 50

    # Set up collectable with random position
    collectableX = random.randint(0, 800)
    collectableY = random.randint(0, 600)
    collectableWidth = 25
    collectableHeight = 25

    # The initial velocity of the character is moving right
    velocityX = 5
    velocityY = 0

    # Timer for game
    start_time = pygame.time.get_ticks()
    timer_duration = 30000  # 5000 milliseconds = 5 seconds

    # setup game loop
    looping = True

    while looping:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Check for key presses and releases
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    velocityX = 5
                    velocityY = 0
                elif event.key == K_LEFT:
                    velocityX = -5
                    velocityY = 0
                elif event.key == K_UP:
                    velocityX = 0
                    velocityY = -5
                elif event.key == K_DOWN:
                    velocityX = 0
                    velocityY = 5
                elif event.key == K_r:
                    # Reset player position to the center of the screen
                    characterX = WINDOW_WIDTH // 2
                    characterY = WINDOW_HEIGHT // 2
                elif event.key == K_c:
                    # Change the player's color (toggle between two colors for simplicity)
                    PLAYER = (0, 255, 0) if PLAYER == (255, 30, 70) else (255, 30, 70)

        # Process updated position
        characterX += velocityX 
        characterY += velocityY
        
        # By taking the remainder of the position/length, the block will loop back to the other side
        characterX = characterX % WINDOW_WIDTH
        characterY = characterY % WINDOW_HEIGHT

        # Create character and collectable rectangles
        character = pygame.Rect(characterX, characterY, characterWidth, characterHeight)
        collectable = pygame.Rect(collectableX, collectableY, collectableWidth, collectableHeight)

        # Check if the player collected the collectable
        if character.colliderect(collectable):
            score += 1
            collectableX = random.randint(0, 800)
            collectableY = random.randint(0, 600)

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        # Check if the timer has elapsed
        if elapsed_time > timer_duration:
            print("Timer expired!")
            print(score)            
            pygame.quit()
            sys.exit()

        # Rendering
        WINDOW.fill(BACKGROUND)
        pygame.draw.rect(WINDOW, PLAYER, character)
        pygame.draw.rect(WINDOW, COLLECTABLE, collectable)

        # Render and display the score
        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        score_rect = score_text.get_rect()
        score_rect.topright = (WINDOW_WIDTH - 10, 10)  # Position in the top-right corner with a 10-pixel margin
        WINDOW.blit(score_text, score_rect)

        timer_text = font.render(f"Time left: {30-(elapsed_time//1000)}", True, TEXT_COLOR)
        timer_rect = timer_text.get_rect()
        timer_rect.topright = (150, 10)  # Position in the top-right corner with a 10-pixel margin
        WINDOW.blit(timer_text, timer_rect)

        pygame.display.update()
        
        fpsClock.tick(FPS)

main()
