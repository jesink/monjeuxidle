import pygame
import os
from settings import *

class Battle:
    def __init__(self, screen, player_character):
        self.screen = screen
        self.player_character = player_character

    def display_combat(self, selected_enemy):
        # Affichage du combat
        self.screen.fill((0, 0, 0))  # Remplir l'écran en noir
        player_surface = pygame.font.SysFont("arial", 40).render(f"{self.player_character['image']} (HP: {self.player_character['hp']})", True, (255, 255, 255))
        enemy_surface = pygame.font.SysFont("arial", 40).render(f"{selected_enemy['name']} (HP: {selected_enemy['stats']['HP']})", True, (255, 255, 255))

        self.screen.blit(player_surface, (100, 100))
        self.screen.blit(enemy_surface, (500, 100))
        pygame.display.flip()
