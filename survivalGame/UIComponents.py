# helpers.py

import pygame
import sys
import time
from pygame.locals import *

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    pygame.draw.rect(surface, (0, 0, 0), rect, width=2, border_radius=radius)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def death_screen(WINDOW, font, waves_survived_index, brokenScore, new_high_score, background_image, player_image, projectile_image):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                play_again_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, instructions_box.bottom - 60, 200, 50)
                if play_again_button.collidepoint(mouse_pos):
                    return

        WINDOW.blit(background_image, (0, 0))
        box_width = 800
        box_height = 400
        box_x = WINDOW_WIDTH // 2 - box_width // 2
        box_y = WINDOW_HEIGHT // 2 - box_height // 2
        instructions_box = pygame.Rect(box_x, box_y, box_width, box_height)
        
        draw_rounded_rect(WINDOW, (240, 235, 153, 150), instructions_box, radius=20)
        draw_text("Game Over", font, (0, 0, 0), WINDOW, WINDOW_WIDTH // 2, instructions_box.top + 40)
        wave_text = f"Waves Survived: {waves_survived_index}"
        draw_text(wave_text, font, (0, 0, 0), WINDOW, WINDOW_WIDTH // 2, instructions_box.top + 100)
        
        player_sprite_rect = pygame.Rect(WINDOW_WIDTH // 2 - 80, instructions_box.bottom - 150, 75, 75)
        projectile_rect = pygame.Rect(WINDOW_WIDTH // 2, instructions_box.bottom - 125, 75, 75)
        scaled_projectile_image = pygame.transform.scale(projectile_image, (40, 40))

        WINDOW.blit(player_image, player_sprite_rect)
        WINDOW.blit(scaled_projectile_image, projectile_rect)
        
        high_score_text = "NEW HIGH SCORE!" if new_high_score else f"High Score: {brokenScore}"
        draw_text(high_score_text, font, (0, 0, 0), WINDOW, WINDOW_WIDTH // 2, instructions_box.top + 160)
        
        play_again_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, instructions_box.bottom - 60, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(WINDOW, (145, 143, 115) if play_again_button.collidepoint(mouse_pos) else (194, 191, 153), play_again_button)
        draw_text("Play Again", font, (0, 0, 0), WINDOW, WINDOW_WIDTH // 2, instructions_box.bottom - 35)
        
        pygame.display.update()

def splash_screen(WINDOW, font, background_image):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                start_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50, 200, 50)
                if start_button.collidepoint(mouse_pos):
                    return

        WINDOW.blit(background_image, (0, 0))
        box_width = 800
        box_height = 400
        box_x = WINDOW_WIDTH // 2 - box_width // 2
        box_y = WINDOW_HEIGHT // 2 - box_height // 2
        instructions_box = pygame.Rect(box_x, box_y, box_width, box_height)
        draw_rounded_rect(WINDOW, (240, 235, 153, 150), instructions_box, radius=20)
        draw_text("Waves of enemies will appear, don't let them touch you.", font, (0, 0, 0), WINDOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100)
        draw_text("Space to shoot, arrows to aim, and wasd to move.", font, (0, 0, 0), WINDOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        
        start_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(WINDOW, (145, 143, 115) if start_button.collidepoint(mouse_pos) else (194, 191, 153), start_button)
        draw_text("Start", font, (0, 0, 0), WINDOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 75)
        
        pygame.display.update()

def draw_wave_caption(surface, text, font, color, center_x, center_y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    surface.blit(text_surface, text_rect)

def draw_wave_label(window, font, wave_index, color=(0, 0, 0)):
    wave_text = f"Wave: {wave_index + 1}"
    draw_text(wave_text, font, color, window, 50, 25)

def draw_health_label(window, font, health, color=(0, 0, 0)):
    health_text = f"Health: {health}"
    draw_text(health_text, font, color, window, 70, 55)
def draw_boss_health_bar(screen, boss):
    if boss is None:
        return

    # Health bar dimensions
    bar_width = 300
    bar_height = 30
    border_thickness = 2

    # Bar position (centered at the top of the screen)
    x = (WINDOW_WIDTH - bar_width) // 2
    y = 10  # Top margin

    # Health bar background
    pygame.draw.rect(screen, (50, 50, 50), (x - border_thickness, y - border_thickness, bar_width + 2 * border_thickness, bar_height + 2 * border_thickness))  # Border
    pygame.draw.rect(screen, (200, 200, 200), (x, y, bar_width, bar_height))  # Background

    # Health bar fill
    health_percentage = max(0, boss.health / 100)  # Assuming boss's max health is 100
    health_color = (255, 0, 0)  # Red color for health
    pygame.draw.rect(screen, health_color, (x, y, bar_width * health_percentage, bar_height))

    # Draw the caption
    font = pygame.font.Font(None, 24)  # Adjust font size as needed
    caption = font.render('Boss Health', True, (0, 0, 0))  # Black color
    screen.blit(caption, (x + bar_width // 2 - caption.get_width() // 2, y + bar_height + 5))  # Position below the bar
