import pygame, sys, random, time
from pygame.locals import *
from UIComponents import death_screen, splash_screen, draw_wave_caption, draw_wave_label, draw_health_label
from classes import Player, Enemy
pygame.init()
pygame.mixer.init()

# Colours RGB Values
BACKGROUND = (240, 235, 153,150)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (194, 191, 153)
BUTTON_HOVER_COLOR = (145, 143, 115)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
game_state = 'splash'

# Text setup
font = pygame.font.SysFont(None, 36)

# Initialize the window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Survive!')

# Loading assets
background_image = pygame.image.load('./sprites/background.png')
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

player_image = pygame.image.load('./sprites/player.png')
player_image = pygame.transform.scale(player_image, (75, 75))

enemy_image = pygame.image.load('./sprites/enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (50, 50))


projectile_image = pygame.image.load('./sprites/projectile.png')
projectile_image = pygame.transform.scale(projectile_image, (25, 25))

heart_image = pygame.image.load('./sprites/heart.png')
heart_image = pygame.transform.scale(heart_image, (50, 50))

bolt_image = pygame.image.load('./sprites/bolt.png')
bolt_image = pygame.transform.scale(bolt_image, (50, 50))

# Loading sounds
music = pygame.mixer.music.load('./sounds/background.mp3')
throw = pygame.mixer.Sound('./sounds/throw.mp3')
enemy_death = pygame.mixer.Sound('./sounds/enemyDeath.mp3')
wave_clear = pygame.mixer.Sound('./sounds/waveClear.mp3')
player_damaged = pygame.mixer.Sound('./sounds/playerDamaged.mp3')
powerup = pygame.mixer.Sound('./sounds/powerup.mp3')

# functions for handling BG music logic
def start_music():
    pygame.mixer.music.play(-1)
def stop_music():
    pygame.mixer.music.stop()

def update_game_state(new_state):
    global game_state
    game_state = new_state

    if game_state == 'playing':
        start_music()
    else:
        stop_music()


#<---------------------------- NINJA ASSIGNMENTS HERE !!! -------------------------------------->


"""TODO:: CREATE THE POWERUP CLASS """


"""TODO: IMPLEMENT SPAWN ENEMY ON EDGE FUNCTION"""
def spawn_enemy_on_edge():


    return [300,200]

"""TODO: IMPLEMENT WAVE SPAWNING"""
def spawn_wave(number_of_enemies):
    x, y = spawn_enemy_on_edge() 
    enemy = Enemy(x, y, 100, 2,enemy_image) 
    all_sprites.add(enemy)
    enemies.add(enemy)

"""TODO: INITIALIZE WAVE SIZES AND NUMBER"""
WAVES = [1]


#<----------------------------------------------------------------------------------------------->




"""DO NOT EDIT GAME_LOOP!!!"""
def game_loop():
    global all_sprites, enemies, projectiles, high_score, powerups

    # instructions splash screen
    splash_screen(WINDOW,font,background_image) 
    update_game_state('playing') # begin BG music

    high_score = 0 # local high score
    while True:

        # Initialize game variables
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        projectiles = pygame.sprite.Group()
        powerups = pygame.sprite.Group()  # Group to manage power-ups

        # Initialize player in the middle
        player = Player(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,player_image,all_sprites,projectiles,projectile_image)
        all_sprites.add(player)

        # Initialize wave variables
        current_wave_index = 0
        enemies_to_spawn = WAVES[current_wave_index] if WAVES else 0
        wave_spawned = False
        game_active = True

        # Initialize timer variables
        last_wave_clear_time = pygame.time.get_ticks()
        delay_before_next_wave = 2000  # 2 seconds delay
        delay_in_progress = False
        while game_active:
            for event in pygame.event.get():
                # close game if window closed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Processing - most logic handled within classes
            player.update()

            # update each enemy 
            for enemy in enemies:
                enemy.update(player.rect.center)

            # update each projectile
            for projectile in projectiles:
                projectile.update()

            # Check for collision between projectiles and enemies - if so, kill enemy
            for projectile in projectiles:
                hits = pygame.sprite.spritecollide(projectile, enemies, True)
                if hits:
                    pygame.mixer.Sound.play(enemy_death)
                    projectile.kill()

            # Check for collision between player and enemies - if so, damage player
            hits = pygame.sprite.spritecollide(player, enemies, True)  # Remove enemy when hit with True parameter
            if hits:
                pygame.mixer.Sound.play(player_damaged)

                if player.take_damage(25):  # Damage amount; you can adjust this value

                    update_game_state('death')
                    game_active = False

                    # Check if the player has beaten the high score
                    if current_wave_index+1>high_score:
                        death_screen(WINDOW,font,current_wave_index + 1, high_score, True,background_image,player_image,projectile_image)# Show death screen with high score ui
                        high_score = current_wave_index + 1
                    else:
                        death_screen(WINDOW,font,current_wave_index + 1, high_score, False,background_image,player_image,projectile_image)  # Show death screen without high score ui
            # Check for collision between player and power-ups, or between enemies and power-ups
            for powerup in powerups:
                if pygame.sprite.collide_rect(player, powerup):
                    powerup.apply(player) # Apply power-up to player
                else:
                    hits = pygame.sprite.spritecollide(powerup, enemies,False)  # Remove enemy when hit set to False
                    if hits:
                        powerup.kill() # Remove power-up when enemy consumes it

            # Check if all enemies from the current wave are defeated
            if not enemies:

                # if a wave was currently active
                if wave_spawned:
                    # celebrate
                    pygame.mixer.Sound.play(wave_clear)

                    # Logic for 2 sec Delay before starting the next wave
                    delay_in_progress = True
                    last_wave_clear_time = pygame.time.get_ticks()
                    wave_spawned = False
                    current_wave_index += 1

                    # Check if all waves are completed
                    if current_wave_index < len(WAVES):
                        enemies_to_spawn = WAVES[current_wave_index]
                    else:
                        # All waves completed
                        print("All waves completed!")
                        pygame.quit()
                        sys.exit()

            # Handle delay before spawning the next wave
            if delay_in_progress:
                current_time = pygame.time.get_ticks()
                if (current_time - last_wave_clear_time) >= delay_before_next_wave:
                    delay_in_progress = False
                    wave_spawned = True
                    if enemies_to_spawn > 0:
                        spawn_wave(enemies_to_spawn)
                        enemies_to_spawn = 0

            # Spawn new enemies if needed (initial wave)
            if not wave_spawned and not delay_in_progress and enemies_to_spawn > 0:
                spawn_wave(enemies_to_spawn)
                enemies_to_spawn = 0
                wave_spawned = True

            # Render elements of the game
            WINDOW.blit(background_image, (0, 0))
            all_sprites.draw(WINDOW)
            draw_wave_label(WINDOW, font, current_wave_index)
            draw_health_label(WINDOW, font, player.health) 

            # show wave x cleared when it is done
            if delay_in_progress:
                draw_wave_caption(WINDOW, "Wave " + str(current_wave_index) + " cleared!", font, TEXT_COLOR, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

            pygame.display.update()
            fpsClock.tick(FPS)

game_loop()