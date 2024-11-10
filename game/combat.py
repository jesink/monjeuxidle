
import pygame
import os
from settings import *

class Combat:
    def __init__(self, screen):
        self.screen = screen
        difficulty_names = [
            "Débutant", "Facile", "Modéré", "Intermédiaire", "Avancé",
            "Difficile", "Très Difficile", "Expert", "Maître", "Légendaire"
        ]
        self.enemy_groups = [
            {"name": difficulty_names[i], "levels": [f"Ennemi Niveau {j+1}" for j in range(10)]}
            for i in range(10)
        ]  # 10 groupes avec 10 niveaux d'ennemis chacun, nommés par difficulté sans le mot "Groupe"

        # Charger le fond d'écran
        self.background_image = pygame.image.load(os.path.join("assets", "background.png")).convert()

    def draw_rounded_rect(self, surface, color, rect, corner_radius):
        """Dessine un rectangle avec des coins arrondis (ici, couleur transparente)."""
        if corner_radius > min(rect[2], rect[3]) // 2:
            corner_radius = min(rect[2], rect[3]) // 2
        s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)  # Surface avec transparence
        pygame.draw.rect(s, color, (0, 0, rect[2], rect[3]), border_radius=corner_radius)
        surface.blit(s, rect[:2])

    def display_combat_menu(self):
        running = True
        while running:
            # Afficher le fond d'écran
            self.screen.blit(self.background_image, (0, 0))

            # Calculer les positions pour lister les groupes d'ennemis
            slot_width, slot_height = 300, 50
            x_start = (1280 - slot_width) // 2
            y_start = 100
            y_offset = 60

            font = pygame.font.SysFont("arial", 24)

            for index, group in enumerate(self.enemy_groups):
                rect_x = x_start
                rect_y = y_start + index * y_offset
                self.draw_rounded_rect(self.screen, (50, 50, 50, 200), (rect_x, rect_y, slot_width, slot_height), 10)

                # Afficher le nom du groupe sans le mot "Groupe"
                text = font.render(group["name"], True, (173, 216, 230))  # Bleu clair
                text_rect = text.get_rect(center=(rect_x + slot_width // 2, rect_y + slot_height // 2))
                self.screen.blit(text, text_rect)

            # Rafraîchir l'affichage
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    for index, group in enumerate(self.enemy_groups):
                        rect_x = x_start
                        rect_y = y_start + index * y_offset
                        if rect_x <= mouse_x <= rect_x + slot_width and rect_y <= mouse_y <= rect_y + slot_height:
                            print(f"{group['name']} sélectionné")
                            # Logique pour afficher les niveaux des ennemis du groupe sélectionné
