import pygame
import sys
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from game.character import Character
from game.inventory import Inventory
from game.combat_interface import CombatInterface
from game.enemy import Enemy
from game.combat_and_enemy import EnemyInterface

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Idle RPG")

# Charger le fond d'écran
background_image = pygame.image.load(os.path.join("assets", "background.png")).convert()

# Instances des classes
character = Character(screen)
inventory = Inventory(screen)
default_enemy = Enemy("Ennemi Débutant", health=60, level=1)
combat_interface = CombatInterface(screen, character, default_enemy)

# Assurez-vous que `enemy_groups` est correctement défini
enemy_groups = []  # Exemple de liste d'ennemis, à modifier selon votre logique
enemy_interface = EnemyInterface(screen, enemy_groups)

# Variables de contrôle
running = True
current_interface = "home"
character_selected = False  # Par défaut, aucun personnage n'est sélectionné

# Définir la couleur des boutons
BUTTON_COLOR = (100, 100, 100)  # Une couleur grise pour les boutons

# Création des boutons
buttons = {
    "character": pygame.Rect(350, 200, 300, 50),
    "inventory": pygame.Rect(350, 300, 300, 50),
    "combat": pygame.Rect(350, 400, 300, 50),
    "quit": pygame.Rect(350, 500, 300, 50)
}

# Fonction pour gérer les événements de la page d'accueil
def handle_home_page_events():
    global running, current_interface
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos  # Capturer les coordonnées de la souris
            if buttons["character"].collidepoint(mouse_x, mouse_y):
                current_interface = "character"
            elif buttons["inventory"].collidepoint(mouse_x, mouse_y) and character_selected:
                current_interface = "inventory"
            elif buttons["combat"].collidepoint(mouse_x, mouse_y) and character_selected:
                current_interface = "enemy_groups"  # Aller à l'interface des groupes d'ennemis
            elif buttons["quit"].collidepoint(mouse_x, mouse_y):
                running = False

# Fonction pour afficher la page d'accueil
def display_home_page():
    screen.blit(background_image, (0, 0))
    font = pygame.font.SysFont("arial", 30)
    for key, rect in buttons.items():
        pygame.draw.rect(screen, BUTTON_COLOR, rect, border_radius=15)
        text = font.render(key.capitalize(), True, WHITE)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
    pygame.display.flip()

# Fonction pour afficher l'interface de sélection de personnage
def display_character_selection():
    screen.blit(background_image, (0, 0))
    character.display_selection()
    pygame.display.flip()

# Fonction pour gérer les événements de sélection de personnage
def handle_character_selection_events():
    global character_selected, current_interface
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if character.handle_click(mouse_x, mouse_y):
                character_selected = True
                current_interface = "home"

# Fonction pour gérer l'affichage de l'inventaire
def display_inventory():
    screen.blit(background_image, (0, 0))
    inventory.display()
    pygame.display.flip()

# Fonction pour gérer les événements de l'inventaire
def handle_inventory_events():
    global current_interface
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            current_interface = "home"

# Fonction pour gérer les événements de l'interface de combat
def handle_combat_events():
    global current_interface
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Vous pouvez ajouter ici des événements spécifiques pour le combat
            current_interface = "home"  # Retourne à l'accueil si nécessaire

# Fonction pour afficher l'interface de combat avec les ennemis
def display_enemy_interface():
    screen.blit(background_image, (0, 0))  # Afficher le fond
    enemy_interface.display()  # Afficher l'interface de groupe d'ennemis
    pygame.display.flip()

# Boucle principale
while running:
    if current_interface == "home":
        display_home_page()
        handle_home_page_events()
    elif current_interface == "character":
        display_character_selection()
        handle_character_selection_events()
    elif current_interface == "inventory":
        display_inventory()
        handle_inventory_events()
    elif current_interface == "enemy_groups":
        display_enemy_interface()
        handle_home_page_events()
    elif current_interface == "combat":
        combat_interface.display_combat_interface()
        handle_combat_events()

pygame.quit()
sys.exit()
