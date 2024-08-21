import pygame, sys, random
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# free MP3 sounds online at pixabay.com then go to sound effects download to sounds folder
explode = pygame.mixer.Sound('./explosion.mp3')
flight = pygame.mixer.Sound('./flight.mp3')
music = pygame.mixer.music.load('./background.mp3')
# Colours RGB Values
BACKGROUND = (255, 192, 203)  # pink

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1550
WINDOW_HEIGHT = 800
ACCELERATION = 1

# Initialize the window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Dodge the Tick heads!')


# find free PNG images online and download to sprites folder
MORTIS_IMAGE= pygame.image.load('./mortissprite.png')
scaled_mortis_image = pygame.transform.scale(MORTIS_IMAGE,(100,100))

TICK_HEAD = pygame.image.load('./Tick_head.png')
scaled_tick_head = pygame.transform.scale(TICK_HEAD,(50,50))

def show_splash_screen(score):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:  # Press SPACE to exit splash screen
                    main()

        # Render splash screen
        WINDOW.fill(BACKGROUND)
        font = pygame.font.Font(None, 74)
        text = font.render('Game Over - Score: ' + str(score), True, (0,0,0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        WINDOW.blit(text, text_rect)

        font = pygame.font.Font(None, 36)
        instruction_text = font.render('Press SPACE to restart', True, (0,0,0))
        instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        WINDOW.blit(instruction_text, instruction_rect)

        pygame.display.update()
        fpsClock.tick(FPS)

# The main function that controls the game
def main():
    pygame.mixer.music.play(-1)
    font = pygame.font.Font(None, 36)

    looping = True
    game_over = False
    score=0
    # Initialize Mortis position and velocity
    characterX = 100
    characterY = 275
    velocityY = -15

    player_rect = pygame.Rect(characterX,characterY,100,100)

    enemyX1=WINDOW_WIDTH+400
    enemyY1= random.randint(0, WINDOW_HEIGHT - 50)
    enemy1_rect = pygame.Rect(enemyX1,enemyY1,50,50)

    enemyX2=WINDOW_WIDTH
    enemyY2= random.randint(0, WINDOW_HEIGHT - 50)
    enemy2_rect = pygame.Rect(enemyX2,enemyY2,50,50)

    enemyX3=WINDOW_WIDTH+800
    enemyY3= random.randint(0, WINDOW_HEIGHT - 50)
    enemy3_rect = pygame.Rect(enemyX3,enemyY3,50,50)



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
                    pygame.mixer.Sound.play(flight)
        
        # Processing
        velocityY += ACCELERATION
        characterY += velocityY

        if characterY > WINDOW_HEIGHT - 100:
            characterY = WINDOW_HEIGHT - 100
        if characterY<10:
            characterY = 10

        player_rect.topleft=(characterX,characterY)
        # Update Enemy position
        enemyX1-=10
        enemyX2-=10
        enemyX3-=10
        if enemyX1<0:
            enemyX1=WINDOW_WIDTH
            enemyY1=random.randint(0,WINDOW_HEIGHT-50)
            score+=1

        enemy1_rect.topleft=(enemyX1,enemyY1)

        if enemyX2<0:
            enemyX2=WINDOW_WIDTH
            enemyY2=random.randint(0,WINDOW_HEIGHT-50)
            score+=1

        enemy2_rect.topleft=(enemyX2,enemyY2)

        if enemyX3<0:
            enemyX3=WINDOW_WIDTH
            enemyY3=random.randint(0,WINDOW_HEIGHT-50)
            score+=1

        enemy3_rect.topleft=(enemyX3,enemyY3)
        
        if player_rect.colliderect(enemy1_rect) or player_rect.colliderect(enemy2_rect) or player_rect.colliderect(enemy3_rect):
            game_over = True
            pygame.mixer.Sound.play(explode)
    
        # Render elements of the game
        WINDOW.fill(BACKGROUND)
        WINDOW.blit(scaled_mortis_image, (characterX, characterY))
        WINDOW.blit(scaled_tick_head,(enemyX1,enemyY1))
        WINDOW.blit(scaled_tick_head,(enemyX2,enemyY2)) # add this
        WINDOW.blit(scaled_tick_head,(enemyX3,enemyY3)) # add this

        score_text = font.render('Score: ' + str(score), True, (0,0,0))
        score_rect = score_text.get_rect()
        score_rect.topleft = (WINDOW_WIDTH-150,10)
        WINDOW.blit(score_text, score_rect)

        pygame.display.update()
        fpsClock.tick(FPS)
    show_splash_screen(score)

main()
