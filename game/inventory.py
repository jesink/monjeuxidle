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
        self.return_button_rect = pygame.Rect(self.screen.get_width() - 170, 20, 150, 50)

        # Charger les données sauvegardées
        self.load_equipment_data()

        # Initialisation des objets d'inventaire avec des statistiques
        self.inventory_slots = self.character.inventory + [None] * (12 - len(self.character.inventory))

        # Liste des rectangles pour chaque slot d'inventaire
        self.inventory_slot_rects = []

        # Initialisation de l'état du menu d'options
        self.show_options_menu = False
        self.item_selected = None

    def load_equipment_data(self):
        """Charge les emplacements d'équipement et l'inventaire depuis un fichier JSON."""
        if os.path.exists("equipment_data.json"):
            with open("equipment_data.json", "r") as file:
                data = json.load(file)
                self.equipment_slots = data.get("equipment_slots", self.equipment_slots)
                self.character.inventory = data.get("inventory", self.character.inventory)
        self.update_inventory_slots()

    def update_inventory_slots(self):
        """Met à jour les slots d'inventaire avec les objets actuels de l'inventaire du personnage."""
        self.inventory_slots = self.character.inventory + [None] * (12 - len(self.character.inventory))
        self.display()  # Rafraîchir l'affichage pour montrer les changements

    def display(self):
        """Affiche l'interface de l'inventaire à l'écran."""
        self.screen.blit(self.background_image, (0, 0))

        screen_width, screen_height = self.screen.get_size()
        font = pygame.font.SysFont(None, 30)
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

        pygame.draw.rect(self.screen, (100, 100, 100), self.return_button_rect, border_radius=10)
        return_text = font.render("Retour", True, (255, 255, 255))
        return_text_rect = return_text.get_rect(center=self.return_button_rect.center)
        self.screen.blit(return_text, return_text_rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, slot_rect in enumerate(self.inventory_slot_rects):
            if slot_rect.collidepoint(mouse_x, mouse_y) and self.inventory_slots[i]:
                self.show_tooltip(self.inventory_slots[i], mouse_x, mouse_y)

        if self.show_options_menu:
            self.draw_options_menu()

        pygame.display.flip()

    def show_tooltip(self, item, x, y):
        """Affiche une infobulle avec les statistiques de l'objet."""
        font = pygame.font.SysFont(None, 24)
        tooltip_width = 200
        tooltip_height = 100
        tooltip_rect = pygame.Rect(x, y, tooltip_width, tooltip_height)
        pygame.draw.rect(self.screen, (0, 0, 0), tooltip_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), tooltip_rect, 2)
        name_text = font.render(item["name"], True, (255, 255, 255))
        self.screen.blit(name_text, (x + 10, y + 10))
        stats_text = f"Attaque: {item['stats'].get('attack', 0)}  Défense: {item['stats'].get('defense', 0)}"
        stats_surface = font.render(stats_text, True, (255, 255, 255))
        self.screen.blit(stats_surface, (x + 10, y + 40))

    def draw_options_menu(self):
        """Dessine un menu d'options pour équiper, supprimer ou annuler."""
        font = pygame.font.SysFont(None, 30)
        menu_width = 400
        menu_height = 250
        screen_width, screen_height = self.screen.get_size()
        menu_rect = pygame.Rect((screen_width - menu_width) // 2, (screen_height - menu_height) // 2, menu_width, menu_height)
        pygame.draw.rect(self.screen, (0, 0, 0), menu_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), menu_rect, 2)
        message = f"Que faire avec {self.item_selected['name']} ?"
        message_surface = font.render(message, True, (255, 255, 255))
        self.screen.blit(message_surface, (menu_rect.x + 20, menu_rect.y + 20))
        equip_button = pygame.Rect(menu_rect.x + 30, menu_rect.y + 150, 100, 50)
        delete_button = pygame.Rect(menu_rect.x + 150, menu_rect.y + 150, 100, 50)
        cancel_button = pygame.Rect(menu_rect.x + 270, menu_rect.y + 150, 100, 50)
        pygame.draw.rect(self.screen, (100, 100, 100), equip_button)
        pygame.draw.rect(self.screen, (100, 100, 100), delete_button)
        pygame.draw.rect(self.screen, (100, 100, 100), cancel_button)
        equip_text = font.render("Équiper", True, (255, 255, 255))
        delete_text = font.render("Supprimer", True, (255, 255, 255))
        cancel_text = font.render("Annuler", True, (255, 255, 255))
        self.screen.blit(equip_text, (equip_button.x + 10, equip_button.y + 10))
        self.screen.blit(delete_text, (delete_button.x + 10, delete_button.y + 10))
        self.screen.blit(cancel_text, (cancel_button.x + 10, cancel_button.y + 10))
        self.equip_button = equip_button
        self.delete_button = delete_button
        self.cancel_button = cancel_button

    def handle_click(self, mouse_pos, button):
        """Gère les clics de souris dans l'interface d'inventaire."""
        if self.show_options_menu:
            if self.equip_button.collidepoint(mouse_pos):
                self.equip_item(self.item_selected)
                self.show_options_menu = False
                self.item_selected = None
            elif self.delete_button.collidepoint(mouse_pos):
                self.character.inventory.remove(self.item_selected)
                self.update_inventory_slots()
                self.show_options_menu = False
                self.item_selected = None
                self.save_equipment_data()
            elif self.cancel_button.collidepoint(mouse_pos):
                self.show_options_menu = False
                self.item_selected = None
            self.display()
            return None
        for i, slot_rect in enumerate(self.inventory_slot_rects):
            if slot_rect.collidepoint(mouse_pos):
                if self.inventory_slots[i]:
                    self.item_selected = self.inventory_slots[i]
                    self.show_options_menu = True
                    self.display()
                    return None
        if self.return_button_rect.collidepoint(mouse_pos):
            print("Bouton Retour cliqué")
            return "retour"
        return None

    def equip_item(self, item):
        """Équipe un objet dans le slot approprié."""
        if item["type"] == "Arme":
            self.equipment_slots["Arme"] = item
        elif item["type"] == "Armure":
            self.equipment_slots["Armure"] = item
        elif item["type"] == "Bijou":
            self.equipment_slots["Bijou"] = item
        if item in self.character.inventory:
            self.character.inventory.remove(item)
            self.character.inventory.append(None)
        self.update_inventory_slots()
        print(f"{item['name']} équipé !")
        self.save_equipment_data()
