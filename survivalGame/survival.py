import pygame, sys, random
from pygame.locals import *

pygame.init()

# Colours RGB Values
BACKGROUND = (255, 255, 255)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

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

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = player_image
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.facing_direction = [1, 0]  # Default direction (facing right)
        self.projectile = None  # Track the current projectile
        self.health=100

    def update(self):
        keys = pygame.key.get_pressed()
        direction = [0, 0]

        if keys[K_LEFT]:
            self.image = pygame.transform.flip(self.original_image, True, False)
            direction[0] = -1
        elif keys[K_RIGHT]:
            direction[0] = 1
            self.image = self.original_image

        if keys[K_UP]:
            direction[1] = -1
        if keys[K_DOWN]:
            direction[1] = 1

        # Normalize direction vector to allow diagonal movement
        if direction != [0, 0]:
            length = (direction[0]**2 + direction[1]**2)**0.5
            direction = [direction[0] / length, direction[1] / length]
            # Update the facing direction based on movement
            self.facing_direction = direction

        # Move player
        self.rect.x += direction[0] * 5
        self.rect.y += direction[1] * 5

        # Check if space is pressed to fire a projectile
        if keys[K_SPACE]:
            if self.projectile is None or not self.projectile.alive():
                # Create a new projectile and add it to the game
                self.projectile = Projectile(self.rect.centerx, self.rect.centery, self.facing_direction)
                all_sprites.add(self.projectile)
                projectiles.add(self.projectile)
# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health, speed):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = health
        self.speed = speed

    def update(self, player_pos):
        direction = pygame.Vector2(player_pos[0] - self.rect.centerx, player_pos[1] - self.rect.centery)
        distance = direction.length()

        if distance != 0:
            direction.normalize_ip()

        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = projectile_image
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 10

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Remove the projectile if it goes out of bounds
        if (self.rect.right < 0 or self.rect.left > WINDOW_WIDTH or 
            self.rect.bottom < 0 or self.rect.top > WINDOW_HEIGHT):
            self.kill()

# Function to spawn enemies at the edge
def spawn_enemy_on_edge():
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
    for _ in range(number_of_enemies):
        x, y = spawn_enemy_on_edge()
        enemy = Enemy(x, y, 100, 2)
        all_sprites.add(enemy)
        enemies.add(enemy)

# Main function
def main():
    global all_sprites, enemies, projectiles
    looping = True

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()

    # Create player
    player = Player(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    all_sprites.add(player)

    # Waves configuration
    waves = [10, 15, 20]
    current_wave_index = 0
    enemies_to_spawn = waves[current_wave_index] if waves else 0
    wave_spawned = False

    while looping:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Processing
        player.update()
        for enemy in enemies:
            enemy.update(player.rect.center)
        for projectile in projectiles:
            projectile.update()

        # Check for collision between projectiles and enemies
        for projectile in projectiles:
            hits = pygame.sprite.spritecollide(projectile, enemies, True)
            if hits:
                projectile.kill()

        # Check for collision between player and enemies
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            pygame.quit()
            sys.exit()

        # Check if all enemies from the current wave are defeated
        if not enemies:
            if wave_spawned:
                current_wave_index += 1
                if current_wave_index < len(waves):
                    enemies_to_spawn = waves[current_wave_index]
                    wave_spawned = False
                else:
                    print("All waves completed!")
                    pygame.quit()
                    sys.exit()
            else:
                wave_spawned = True

        # Spawn new enemies if needed
        if wave_spawned and enemies_to_spawn > 0:
            spawn_wave(enemies_to_spawn)
            enemies_to_spawn = 0

        # Render elements of the game
        WINDOW.blit(background_image, (0, 0))
        all_sprites.draw(WINDOW)

        pygame.display.update()
        fpsClock.tick(FPS)

main()
