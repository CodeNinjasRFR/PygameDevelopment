import pygame, sys, random, time
from pygame.locals import *

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
WAVES = [10, 15, 20]

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

# Player class is the character the user controls
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = player_image
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.facing_direction = [1, 0]  # Default direction (facing right)
        self.projectile = None  # Track the current projectile
        self.health = 100  # Player starts with 100 health
        self.speed = 5  # Default speed
        self.boost_end_time = 0  # Time when the boost ends

    def update(self):
        keys = pygame.key.get_pressed()
        direction = [0, 0]
        arrows = [0, 0, 0, 0]

        # Handle directional movement
        if keys[K_a]:
            self.image = pygame.transform.flip(self.original_image, True, False)
            direction[0] -= 1
        if keys[K_d]:
            direction[0] += 1
            self.image = self.original_image
        if keys[K_w]:
            direction[1] -= 1
        if keys[K_s]:
            direction[1] += 1

        # Handle arrow directions
        if keys[K_LEFT]:
            arrows[0] = 1
        if keys[K_RIGHT]:
            arrows[1] = 1
        if keys[K_UP]:
            arrows[2] = 2
        if keys[K_DOWN]:
            arrows[3] = 1

        # Normalize direction vector to allow diagonal movement
        if direction != [0, 0]:
            length = (direction[0]**2 + direction[1]**2)**0.5
            direction = [direction[0] / length, direction[1] / length]
            # Update the facing direction based on movement
            self.facing_direction = direction

        # Calculate new position
        new_x = self.rect.x + direction[0] * self.speed
        new_y = self.rect.y + direction[1] * self.speed

        # Check boundaries to prevent going out of bounds
        new_x = max(0, min(new_x, WINDOW_WIDTH - self.rect.width))
        new_y = max(0, min(new_y, WINDOW_HEIGHT - self.rect.height))

        # Update player position
        self.rect.x = new_x
        self.rect.y = new_y

        # Check if space is pressed to fire a projectile
        if keys[K_SPACE]:
            # only one projectile at a time
            if self.projectile is None or not self.projectile.alive():
                arrowDirection = [0, 0]
                if arrows[0]:
                    arrowDirection[0] -= 1
                if arrows[1]:
                    arrowDirection[0] += 1
                if arrows[2]:
                    arrowDirection[1] -= 1
                if arrows[3]:
                    arrowDirection[1] += 1
                # if no direction is specified shoot where the player is facing
                if arrowDirection[0] == 0 and arrowDirection[1] == 0:
                    arrowDirection = self.facing_direction

                # instantiate projectile
                self.projectile = Projectile(self.rect.centerx, self.rect.centery, arrowDirection)
                pygame.mixer.Sound.play(throw)
                all_sprites.add(self.projectile)
                projectiles.add(self.projectile)

        # Check if the speed boost should be ended
        if time.time() >= self.boost_end_time and self.boost_end_time > 0:
            self.speed = 5  # Reset to original speed
            self.boost_end_time = 0  # Clear boost end time

    # logic to reduce health and return a boolean if player is dead or not
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            return True 
        return False

# Enemy class is the spider that chases the user
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health, speed):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = health
        self.speed = speed

    def update(self, player_pos):
        # calculate normalized vector in direction of enemy to player vector, so enemies go straight towards the player
        direction = pygame.Vector2(player_pos[0] - self.rect.centerx, player_pos[1] - self.rect.centery)
        distance = direction.length()

        # cannot normalize zero length vector. 
        # this condition should never be true, since if the spider has no distance between the player they are touching
        if distance != 0:
            direction.normalize_ip()

        # update position
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

# projectile class is the ball that is shot by the user
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = projectile_image
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 10

    def update(self):
        # update position
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Remove the projectile if it goes out of bounds
        if (self.rect.right < 0 or self.rect.left > WINDOW_WIDTH or 
            self.rect.bottom < 0 or self.rect.top > WINDOW_HEIGHT):
            self.kill()

# Powerups spawn once per wave. It is either a health or speed power-up
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

# draw rectangle for death screen UI
def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    pygame.draw.rect(surface, (0,0,0), rect, width=2, border_radius=radius)
# draw text for death screen UI
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
# UI for death screen
def death_screen(waves_survived_index, brokenScore, new_high_score):
    while True:
        # process inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # if the play again button is clicked then exit the death screen and restart the game
                if play_again_button.collidepoint(mouse_pos):
                    update_game_state('playing') # resume BG music

                    return

        # Fill the screen with the background image
        WINDOW.blit(background_image, (0, 0))
        
        # Draw instructions box with rounded corners and border
        box_width = 800
        box_height = 400
        box_x = WINDOW_WIDTH // 2 - box_width // 2
        box_y = WINDOW_HEIGHT // 2 - box_height // 2
        instructions_box = pygame.Rect(box_x, box_y, box_width, box_height)
        
        # Draw the background color of the box
        draw_rounded_rect(WINDOW, BACKGROUND, instructions_box, radius=20)
        
        # Draw game over text
        draw_text("Game Over", font, TEXT_COLOR, WINDOW, WINDOW_WIDTH // 2, instructions_box.top + 40)
        
        # Draw waves survived text
        wave_text = f"Waves Survived: {waves_survived_index}"
        draw_text(wave_text, font, TEXT_COLOR, WINDOW, WINDOW_WIDTH // 2, instructions_box.top + 100)
        
        # Draw the player sprite and projectile sprite side by side
        player_sprite_rect = pygame.Rect(WINDOW_WIDTH // 2 - 80, instructions_box.bottom - 150, 75, 75)
        projectile_rect = pygame.Rect(WINDOW_WIDTH // 2, instructions_box.bottom - 125, 75, 75)
        scaled_projectile_image = pygame.transform.scale(projectile_image, (40,40))

        WINDOW.blit(player_image, player_sprite_rect)
        WINDOW.blit(scaled_projectile_image, projectile_rect)
        
        # Draw new high score text if applicable
        if new_high_score:
            high_score_text = "NEW HIGH SCORE!"
        else:
            high_score_text = "High Score: " + str(brokenScore)
        draw_text(high_score_text, font, TEXT_COLOR, WINDOW, WINDOW_WIDTH // 2, instructions_box.top + 160)
        
        # Draw Play Again button
        play_again_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, instructions_box.bottom - 60, 200, 50)

        # hover logic to darken button
        mouse_pos = pygame.mouse.get_pos()
        if play_again_button.collidepoint(mouse_pos):
            pygame.draw.rect(WINDOW, BUTTON_HOVER_COLOR, play_again_button)
        else:
            pygame.draw.rect(WINDOW, BUTTON_COLOR, play_again_button)
        
        draw_text("Play Again", font, TEXT_COLOR, WINDOW, WINDOW_WIDTH // 2, instructions_box.bottom - 35)
        
        pygame.display.update()
        fpsClock.tick(FPS)

# instructions splash screen called once at start of python file 
def splash_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # if the user clicks the start button close the splash screen
                if start_button.collidepoint(mouse_pos):
                    return  

        # Fill the screen with the background image and text border
        WINDOW.blit(background_image, (0, 0))
        box_width = 800
        box_height = 400
        box_x = WINDOW_WIDTH // 2 - box_width // 2
        box_y = WINDOW_HEIGHT // 2 - box_height // 2
        instructions_box = pygame.Rect(box_x, box_y, box_width, box_height)
        draw_rounded_rect(WINDOW, BACKGROUND, instructions_box, radius=20)

        # Draw instructions
        draw_text("Waves of enemies will appear, don't let them touch you.", font, TEXT_COLOR, WINDOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100)
        draw_text("Space to shoot, arrows to aim, and wasd to move.", font, TEXT_COLOR, WINDOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        
        # Draw Start button
        start_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50, 200, 50)
        mouse_pos = pygame.mouse.get_pos()

        # start button hover logic
        if start_button.collidepoint(mouse_pos):
            pygame.draw.rect(WINDOW, BUTTON_HOVER_COLOR, start_button)
        else:
            pygame.draw.rect(WINDOW, BUTTON_COLOR, start_button)
        
        draw_text("Start", font, TEXT_COLOR, WINDOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 75)
        
        pygame.display.update()
        fpsClock.tick(FPS)

# Every time a wave is cleared we show a text to the user with this function
def draw_wave_caption(surface, text, font, color, center_x, center_y):
    """Draw wave text centered at a given position."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    surface.blit(text_surface, text_rect)

# Function to draw wave label in the top left of the screen
def draw_wave_label(window, font, wave_index, color=(0, 0, 0)):
    """Draws the wave label at the top-left corner of the screen."""
    wave_text = f"Wave: {wave_index + 1}"
    draw_text(wave_text, font, color, window, 50, 25)  # Adjust x and y for desired position

# Function to draw health label in the top left of the screen right under wave label

def draw_health_label(window, font, health, color=(0, 0, 0)):
    """Draws the health label just underneath the wave label."""
    health_text = f"Health: {health}"
    draw_text(health_text, font, color, window, 70, 55)  # Adjust x and y for desired position

# Function to spawn enemies at the edge
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

# Function to spawn a wave of enemies
def spawn_wave(number_of_enemies):
    # loop through number of enemies and spawn them at random locations
    for _ in range(number_of_enemies):
        x, y = spawn_enemy_on_edge() # calculate random spawn location
        enemy = Enemy(x, y, 100, 2) # instantiate enemy
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    # one powerup per wave chosen randomly here. 50/50 health or speed
    if random.randint(1,2)==1:
        powerup = PowerUp(random.randint(0, WINDOW_WIDTH - 50), random.randint(0, WINDOW_HEIGHT - 50), 'health', heart_image)
    else:
        powerup=PowerUp(random.randint(0, WINDOW_WIDTH - 50), random.randint(0, WINDOW_HEIGHT - 50), 'speed',bolt_image)
    powerups.add(powerup)
    all_sprites.add(powerup)

# Main Game loop
def game_loop():
    global all_sprites, enemies, projectiles, high_score, powerups

    splash_screen() # Show the instruction screen one time at the start
    update_game_state('playing') # begin BG music

    high_score = 0 # local high score
    while True:

        # Initialize game variables
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        projectiles = pygame.sprite.Group()
        powerups = pygame.sprite.Group()  # Group to manage power-ups

        # Initialize player in the middle
        player = Player(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
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
                        death_screen(current_wave_index + 1, high_score, True)# Show death screen with high score ui
                        high_score = current_wave_index + 1
                    else:
                        death_screen(current_wave_index + 1, high_score, False)  # Show death screen without high score ui
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