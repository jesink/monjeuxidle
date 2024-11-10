import pygame
import sys
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from game.character import Character
from game.inventory import Inventory
from game.enemy_group_interface import EnemyGroupInterface

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Idle RPG")

# Charger le fond d'écran
background_image = pygame.image.load(os.path.join("assets", "background.png")).convert()

# Instances des classes
character = Character(screen)  # Créez l'objet Character
inventory = Inventory(screen, character)  # Passez l'objet Character en argument
enemy_group_interface = EnemyGroupInterface(screen, character)

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
            mouse_x, mouse_y = event.pos
            if buttons["character"].collidepoint(mouse_x, mouse_y):
                current_interface = "character"
            elif buttons["inventory"].collidepoint(mouse_x, mouse_y) and character_selected:
                current_interface = "inventory"
            elif buttons["combat"].collidepoint(mouse_x, mouse_y) and character_selected:
                current_interface = "enemy_group"
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
            mouse_x, mouse_y = event.pos
            # Vérifiez si le clic est sur le bouton "Retour"
            if inventory.return_button_rect.collidepoint(mouse_x, mouse_y):
                current_interface = "home"
            else:
                # Gérer les autres clics pour interagir avec l'inventaire
                inventory.handle_click((mouse_x, mouse_y), event.button)

# Fonction pour afficher l'interface EnemyGroupInterface
def display_enemy_group_interface():
    should_return = enemy_group_interface.display()
    if should_return:  # Si le retour est demandé
        global current_interface
        current_interface = "home"

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
    elif current_interface == "enemy_group":
        display_enemy_group_interface()

pygame.quit()
sys.exit()
