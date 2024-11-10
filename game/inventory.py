import pygame
import os
import json

class Inventory:
    def __init__(self, screen, character):
        self.screen = screen
        self.character = character

        # Charger l'image de fond
        self.background_image = pygame.image.load(os.path.join("assets", "background.png")).convert()

        # Emplacements d'équipement pour Arme, Armure, et Bijou
        self.equipment_slots = {
            "Arme": None,
            "Armure": None,
            "Bijou": None
        }

        # Taille des slots d'inventaire
        self.slot_size = 160
        self.spacing = 30

        # Bouton "Retour" en haut à droite
        self.return_button_rect = pygame.Rect(screen.get_width() - 170, 20, 150, 50)

        # Charger les données sauvegardées
        self.load_equipment_data()

        # Initialisation des objets d'inventaire avec des statistiques
        self.inventory_slots = self.character.inventory + [None] * (12 - len(self.character.inventory))
        self.inventory_slot_rects = []

        # Initialisation de l'état du menu d'options
        self.show_options_menu = False  # Correction : Ajouter cet attribut
        self.item_selected = None

    def update_inventory_slots(self):
        """Synchronise l'affichage avec l'inventaire du personnage."""
        self.inventory_slots = self.character.inventory + [None] * (12 - len(self.character.inventory))
        self.display()  # Rafraîchir l'affichage pour montrer les changements

    def display(self):
        """Affiche l'interface de l'inventaire à l'écran."""
        self.screen.blit(self.background_image, (0, 0))
        screen_width, screen_height = self.screen.get_size()
        font = pygame.font.SysFont(None, 30)

        # Afficher les emplacements d'équipement
        start_y_equipment = 50
        start_x_equipment = (screen_width - (3 * self.slot_size + 2 * self.spacing)) // 2

        for i, (slot_name, item) in enumerate(self.equipment_slots.items()):
            slot_rect = pygame.Rect(start_x_equipment + i * (self.slot_size + self.spacing), start_y_equipment, self.slot_size, self.slot_size)
            pygame.draw.rect(self.screen, (50, 50, 50), slot_rect, border_radius=10)
            text_surface = font.render(slot_name, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(slot_rect.centerx, slot_rect.top - 10))
            self.screen.blit(text_surface, text_rect)

            if item:
                item_text = font.render(item["name"], True, (255, 255, 255))
                item_text_rect = item_text.get_rect(center=slot_rect.center)
                self.screen.blit(item_text, item_text_rect)

        # Afficher les slots d'inventaire
        start_y_inventory = start_y_equipment + self.slot_size + 80
        start_x_inventory = (screen_width - (6 * self.slot_size + 5 * self.spacing)) // 2
        self.inventory_slot_rects = []

        for i in range(12):
            row = i // 6
            col = i % 6
            slot_rect = pygame.Rect(
                start_x_inventory + col * (self.slot_size + self.spacing),
                start_y_inventory + row * (self.slot_size + self.spacing),
                self.slot_size,
                self.slot_size
            )
            pygame.draw.rect(self.screen, (70, 70, 70), slot_rect, border_radius=10)
            self.inventory_slot_rects.append(slot_rect)

            if self.inventory_slots[i]:
                item_name = self.inventory_slots[i]["name"] if isinstance(self.inventory_slots[i], dict) else self.inventory_slots[i]
                item_text = font.render(item_name, True, (255, 255, 255))
                item_text_rect = item_text.get_rect(center=slot_rect.center)
                self.screen.blit(item_text, item_text_rect)

        # Bouton "Retour"
        pygame.draw.rect(self.screen, (100, 100, 100), self.return_button_rect, border_radius=10)
        return_text = font.render("Retour", True, (255, 255, 255))
        return_text_rect = return_text.get_rect(center=self.return_button_rect.center)
        self.screen.blit(return_text, return_text_rect)

        # Afficher le menu d'options si nécessaire
        if self.show_options_menu:
            self.draw_options_menu()

        pygame.display.flip()

    def save_equipment_data(self):
        """Sauvegarde les emplacements d'équipement et l'inventaire dans un fichier JSON."""
        data = {
            "equipment_slots": self.equipment_slots,
            "inventory": self.character.inventory
        }
        with open("equipment_data.json", "w") as file:
            json.dump(data, file, default=str)

    def load_equipment_data(self):
        """Charge les emplacements d'équipement et l'inventaire depuis un fichier JSON."""
        if os.path.exists("equipment_data.json"):
            with open("equipment_data.json", "r") as file:
                data = json.load(file)
                self.equipment_slots = data.get("equipment_slots", self.equipment_slots)
                self.character.inventory = data.get("inventory", self.character.inventory)
        self.update_inventory_slots()

    def handle_click(self, mouse_pos, button):
        """Gère les clics de souris dans l'interface d'inventaire."""
        if self.show_options_menu:
            # Gérer les options du menu
            pass
        for i, slot_rect in enumerate(self.inventory_slot_rects):
            if slot_rect.collidepoint(mouse_pos):
                if self.inventory_slots[i]:
                    self.item_selected = self.inventory_slots[i]
                    self.show_options_menu = True
                    return None
        if self.return_button_rect.collidepoint(mouse_pos):
            return "retour"
        return None
