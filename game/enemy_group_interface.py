import pygame
import os
from settings import *
from game.enemy_list_debutant_interface import EnemyListDebutantInterface
from game.enemy_list_facile_interface import EnemyListFacileInterface
from game.enemy_list_modere_interface import EnemyListModereInterface
from game.enemy_list_intermediaire_interface import EnemyListIntermediaireInterface
from game.enemy_list_avance_interface import EnemyListAvanceInterface
from game.enemy_list_difficile_interface import EnemyListDifficileInterface
from game.enemy_list_tres_difficile_interface import EnemyListTresDifficileInterface
from game.enemy_list_expert_interface import EnemyListExpertInterface
from game.enemy_list_maitre_interface import EnemyListMaitreInterface
from game.enemy_list_legendaire_interface import EnemyListLegendaireInterface
from game.combat_interface import CombatInterface

class EnemyGroupInterface:
    def __init__(self, screen, character):
        self.screen = screen
        self.character = character
        self.background_image = pygame.image.load(os.path.join("assets", "background.png")).convert()

        # Instances des interfaces de liste d'ennemis
        self.enemy_list_debutant_interface = EnemyListDebutantInterface(screen, character, CombatInterface)
        self.enemy_list_facile_interface = EnemyListFacileInterface(screen, character, CombatInterface)
        self.enemy_list_modere_interface = EnemyListModereInterface(screen, character, CombatInterface)
        self.enemy_list_intermediaire_interface = EnemyListIntermediaireInterface(screen, character, CombatInterface)
        self.enemy_list_avance_interface = EnemyListAvanceInterface(screen, character, CombatInterface)
        self.enemy_list_difficile_interface = EnemyListDifficileInterface(screen, character, CombatInterface)
        self.enemy_list_tres_difficile_interface = EnemyListTresDifficileInterface(screen, character, CombatInterface)
        self.enemy_list_expert_interface = EnemyListExpertInterface(screen, character, CombatInterface)
        self.enemy_list_maitre_interface = EnemyListMaitreInterface(screen, character, CombatInterface)
        self.enemy_list_legendaire_interface = EnemyListLegendaireInterface(screen, character, CombatInterface)

        # Bouton "Retour"
        self.return_button_rect = pygame.Rect(self.screen.get_width() - 350, 20, 300, 50)

        # Noms des groupes d'ennemis
        self.enemy_group_names = [
            "Débutant", "Facile", "Modéré", "Intermédiaire", "Avancé",
            "Difficile", "Très Difficile", "Expert", "Maître", "Légendaire"
        ]

    def display(self):
        running = True
        should_return_to_main_menu = False  # Variable de contrôle pour signaler le retour

        while running:
            self.screen.blit(self.background_image, (0, 0))

            # Paramètres pour les cadres
            slot_width, slot_height = 400, 50
            x_start = (self.screen.get_width() - slot_width) // 2
            y_start = 100
            y_offset = 70

            font = pygame.font.SysFont("arial", 30)

            # Dessiner les cadres et les textes pour chaque groupe d'ennemis
            for index, name in enumerate(self.enemy_group_names):
                rect_x = x_start
                rect_y = y_start + index * y_offset
                group_rect = pygame.Rect(rect_x, rect_y, slot_width, slot_height)
                pygame.draw.rect(self.screen, (100, 100, 100), group_rect, border_radius=15)

                text = font.render(name, True, (255, 255, 255))
                text_rect = text.get_rect(center=(rect_x + slot_width // 2, rect_y + slot_height // 2))
                self.screen.blit(text, text_rect)

                # Vérifier si un bouton est cliqué
                if pygame.mouse.get_pressed()[0] and group_rect.collidepoint(pygame.mouse.get_pos()):
                    if index == 0:
                        self.enemy_list_debutant_interface.display()
                    elif index == 1:
                        self.enemy_list_facile_interface.display()
                    elif index == 2:
                        self.enemy_list_modere_interface.display()
                    elif index == 3:
                        self.enemy_list_intermediaire_interface.display()
                    elif index == 4:
                        self.enemy_list_avance_interface.display()
                    elif index == 5:
                        self.enemy_list_difficile_interface.display()
                    elif index == 6:
                        self.enemy_list_tres_difficile_interface.display()
                    elif index == 7:
                        self.enemy_list_expert_interface.display()
                    elif index == 8:
                        self.enemy_list_maitre_interface.display()
                    elif index == 9:
                        self.enemy_list_legendaire_interface.display()

            # Dessiner le bouton "Retour"
            pygame.draw.rect(self.screen, (100, 100, 100), self.return_button_rect, border_radius=15)
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
                    if self.return_button_rect.collidepoint(mouse_x, mouse_y):
                        print("Bouton Retour cliqué")
                        should_return_to_main_menu = True  # Signaler le retour
                        running = False

            if should_return_to_main_menu:
                break  # Sortir de la boucle principale

            # Ajouter un délai pour éviter de surcharger le CPU
            pygame.time.delay(10)

        return should_return_to_main_menu
