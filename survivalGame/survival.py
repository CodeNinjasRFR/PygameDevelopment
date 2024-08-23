import pygame, sys, random, time
from pygame.locals import *
from UIComponents import death_screen, splash_screen, draw_wave_caption, draw_wave_label, draw_health_label, draw_boss_health_bar
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
BOSS_HEALTH=100
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

boss_image = pygame.image.load('./sprites/boss.png')
boss_image = pygame.transform.scale(boss_image, (100, 100))
# Loading sounds
music = pygame.mixer.music.load('./sounds/background.mp3')
throw = pygame.mixer.Sound('./sounds/throw.mp3')
enemy_death = pygame.mixer.Sound('./sounds/enemyDeath.mp3')
wave_clear = pygame.mixer.Sound('./sounds/waveClear.mp3')
player_damaged = pygame.mixer.Sound('./sounds/playerDamaged.mp3')
powerup = pygame.mixer.Sound('./sounds/powerup.mp3')
boss_spawn = pygame.mixer.Sound('./sounds/bossSpawn.mp3')

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

"""TODO:: CREATE THE BOSS CLASS """
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image, health):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.health = health

    def update(self, player_pos):
        # Example: Simple movement towards the player (could be more complex)
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        distance = max(1, (dx**2 + dy**2) ** 0.5)
        self.rect.x += self.speed * dx / distance
        self.rect.y += self.speed * dy / distance

    def take_damage(self, amount):
        global boss
        self.health -= amount
        print(self.health)
        if self.health <= 0:
            self.kill()
            boss=None

    def check_collision_with_player(self, player):
        if pygame.sprite.collide_rect(self, player):
            return True
        return False
    def teleport(self, player):
        # Move the boss to a random position away from the player
        new_x = player.rect.centerx + random.randint(100, 200) * random.choice([-1, 1])
        new_y = player.rect.centery + random.randint(100, 200) * random.choice([-1, 1])
        self.rect.topleft = (new_x, new_y)


"""TODO:: CREATE THE POWERUP CLASS """

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, type, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = type  # Type of power-up (e.g., "health", "speed")
    
    # Powerups have no update logic since they only behave when collided
    def update(self):
        pass

    # Apply the power-up to the player based on type
    def apply(self, player):
        if self.type == "health":
            player.health = min(player.health + 25, 100)  # Restore health, max 100
        elif self.type == "speed":
            player.speed *= 2  # Temporarily increase player speed
            player.boost_end_time = time.time() + 15  # Set boost duration to 15 seconds

        # Remove the power-up after applying it
        pygame.mixer.Sound.play(powerup)
        self.kill()

"""TODO: IMPLEMENT SPAWN ENEMY ON EDGE FUNCTION"""

def spawn_enemy_on_edge():
    # randomly choose side to spawn the enemy, then randomize spawn location on that side
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    if edge == 'top':
        x = random.randint(0, WINDOW_WIDTH - 50)
        y = -50
    elif edge == 'bottom':
        x = random.randint(0, WINDOW_WIDTH - 50)
        y = WINDOW_HEIGHT
    elif edge == 'left':
        x = -50
        y = random.randint(0, WINDOW_HEIGHT - 50)
    elif edge == 'right':
        x = WINDOW_WIDTH
        y = random.randint(0, WINDOW_HEIGHT - 50)

    return x, y

"""TODO: IMPLEMENT WAVE SPAWNING"""
def spawn_wave(number_of_enemies,current_wave):
    global boss
    # loop through number of enemies and spawn them at random locations
    for _ in range(number_of_enemies):
        x, y = spawn_enemy_on_edge() # calculate random spawn location
        enemy = Enemy(x, y, 100, 2,enemy_image) # instantiate enemy
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    # one powerup per wave chosen randomly here. 50/50 health or speed
    if random.randint(1,2)==1:
        powerup = PowerUp(random.randint(0, WINDOW_WIDTH - 50), random.randint(0, WINDOW_HEIGHT - 50), 'health', heart_image)
    else:
        powerup=PowerUp(random.randint(0, WINDOW_WIDTH - 50), random.randint(0, WINDOW_HEIGHT - 50), 'speed',bolt_image)
    powerups.add(powerup)
    all_sprites.add(powerup)
    if (current_wave+1) % 3==0:
        x, y = spawn_enemy_on_edge()
        boss = Boss(x, y, 4,boss_image,BOSS_HEALTH)
        pygame.mixer.Sound.play(boss_spawn)
        all_sprites.add(boss)

"""TODO: INITIALIZE WAVE SIZES AND NUMBER"""
WAVES = [10,15,20,30,40,50]


#<----------------------------------------------------------------------------------------------->

# Main Game loop
def game_loop():
    global all_sprites, enemies, projectiles, high_score, powerups, boss

    splash_screen(WINDOW,font,background_image) # Show the instruction screen one time at the start
    update_game_state('playing') # begin BG music

    high_score = 0 # local high score
    boss=None
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

            if boss:
                boss.update(player.rect.center)

            # Check for collision between projectiles and enemies - if so, kill enemy
            for projectile in projectiles:
                hits = pygame.sprite.spritecollide(projectile, enemies, True)
                if hits:
                    pygame.mixer.Sound.play(enemy_death)
                    projectile.kill()
            if boss:
                for projectile in projectiles:
                    if pygame.sprite.collide_rect(projectile, boss):
                        pygame.mixer.Sound.play(enemy_death)
                        boss.take_damage(BOSS_HEALTH/4)  # Boss loses 1/4 of its health
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

            if boss and boss.check_collision_with_player(player):
                pygame.mixer.Sound.play(player_damaged)
                if player.take_damage(50):  # Player loses 1/2 of its health
                    update_game_state('death')
                    game_active = False

                    # Check if the player has beaten the high score
                    if current_wave_index + 1 > high_score:
                        death_screen(current_wave_index + 1, high_score, True, background_image, player_image, projectile_image)  # Show death screen with high score ui
                        high_score = current_wave_index + 1
                    else:
                        death_screen(current_wave_index + 1, high_score, False, background_image, player_image, projectile_image)  # Show death screen without high score ui
                boss.teleport(player)

            # Check if all enemies from the current wave are defeated
            if not enemies and not (boss and boss.alive()):

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
                        spawn_wave(enemies_to_spawn,current_wave_index)
                        enemies_to_spawn = 0

            # Spawn new enemies if needed (initial wave)
            if not wave_spawned and not delay_in_progress and enemies_to_spawn > 0:
                spawn_wave(enemies_to_spawn,current_wave_index)
                enemies_to_spawn = 0
                wave_spawned = True

            # Render elements of the game
            WINDOW.blit(background_image, (0, 0))
            all_sprites.draw(WINDOW)
            draw_wave_label(WINDOW, font, current_wave_index)
            draw_health_label(WINDOW, font, player.health) 

            draw_boss_health_bar(WINDOW, boss)


            # show wave x cleared when it is done
            if delay_in_progress:
                draw_wave_caption(WINDOW, "Wave " + str(current_wave_index) + " cleared!", font, TEXT_COLOR, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

            pygame.display.update()
            fpsClock.tick(FPS)

game_loop()