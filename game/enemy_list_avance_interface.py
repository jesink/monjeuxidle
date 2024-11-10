import pygame
import os
from settings import *

class EnemyListAvanceInterface:
    def __init__(self, screen, character, combat_interface_class):
        self.screen = screen
        self.character = character
        self.combat_interface_class = combat_interface_class
        self.background_image = pygame.image.load(os.path.join("assets", "background.png")).convert()

        # Créez une liste d'ennemis avec des statistiques adaptées (par exemple, pour les niveaux 40 à 50)
        self.enemies = [
            {"level": level, "stats": self.generate_stats(level)}
            for level in range(40, 51)
        ]

        # Créez un bouton "Retour" en haut à droite
        self.return_button_rect = pygame.Rect(
            self.screen.get_width() - 350, 20, 300, 50
        )

    def generate_stats(self, level):
        """Génère des statistiques adaptées au niveau de l'ennemi."""
        return {
            "HP": 50 + level * 10,
            "Attack": 5 + level * 2,
            "Defense": 3 + level
        }

    def draw_rounded_rect(self, surface, color, rect, corner_radius):
        """Dessine un rectangle avec des coins arrondis."""
        if corner_radius > min(rect[2], rect[3]) // 2:
            corner_radius = min(rect[2], rect[3]) // 2
        s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        pygame.draw.rect(s, color, (0, 0, rect[2], rect[3]), border_radius=corner_radius)
        surface.blit(s, rect[:2])

    def display(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))

            # Paramètres pour les cadres
            slot_width, slot_height = 400, 50
            x_start = (self.screen.get_width() - slot_width) // 2
            y_start = 100  # Ajustement pour positionner les cadres plus bas
            y_offset = 70

            font = pygame.font.SysFont("arial", 24)

            # Dessiner les cadres et les textes pour chaque ennemi
            for index, enemy in enumerate(self.enemies):
                rect_x = x_start
                rect_y = y_start + index * y_offset
                self.draw_rounded_rect(self.screen, (100, 100, 100), (rect_x, rect_y, slot_width, slot_height), 15)

                stats_text = (f"Level: {enemy['level']} - "
                              f"HP: {enemy['stats']['HP']} - "
                              f"ATK: {enemy['stats']['Attack']} - "
                              f"DEF: {enemy['stats']['Defense']}")
                text = font.render(stats_text, True, (255, 255, 255))
                text_rect = text.get_rect(center=(rect_x + slot_width // 2, rect_y + slot_height // 2))
                self.screen.blit(text, text_rect)

            # Dessiner le bouton "Retour"
            self.draw_rounded_rect(self.screen, (100, 100, 100), self.return_button_rect, 15)
            return_text = font.render("Retour", True, (255, 255, 255))
            return_text_rect = return_text.get_rect(center=self.return_button_rect.center)
            self.screen.blit(return_text, return_text_rect)

            pygame.display.flip()

            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # Vérifier si le bouton "Retour" a été cliqué
                    if self.return_button_rect.collidepoint(mouse_x, mouse_y):
                        running = False  # Quitter l'interface pour revenir à EnemyGroupInterface

            pygame.time.delay(10)
