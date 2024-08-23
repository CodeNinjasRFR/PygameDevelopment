import pygame, time
from pygame.locals import *
from pygame.math import Vector2

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

pygame.mixer.init()


throw = pygame.mixer.Sound('./sounds/throw.mp3')
enemy_death = pygame.mixer.Sound('./sounds/enemyDeath.mp3')
player_damaged = pygame.mixer.Sound('./sounds/playerDamaged.mp3')
powerup = pygame.mixer.Sound('./sounds/powerup.mp3')

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, player_image, all_sprites, projectiles, projectile_image):
        super().__init__()
        self.original_image = player_image
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.facing_direction = [1, 0]  # Default direction (facing right)
        self.projectile = None  # Track the current projectile
        self.health = 100  # Player starts with 100 health
        self.speed = 5  # Default speed
        self.boost_end_time = 0  # Time when the boost ends
        self.all_sprites = all_sprites  # pointer to all_sprites defined in survival.py
        self.projectiles = projectiles  # pointer to projectiles defined in survival.py
        self.projectile_image = projectile_image
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
                self.projectile = Projectile(self.rect.centerx, self.rect.centery, arrowDirection,self.projectile_image)
                pygame.mixer.Sound.play(throw)
                self.all_sprites.add(self.projectile)
                self.projectiles.add(self.projectile)

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
    def __init__(self, x, y, health, speed,enemy_image):
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
    def __init__(self, x, y, direction, projectile_image):
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
