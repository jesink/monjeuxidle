
import pygame
import os
import json
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from game.inventory import Inventory  # Assurez-vous d'importer Inventory

class Character:
    def __init__(self, screen):
        self.screen = screen
        self.selected_character = None
        self.character_rects = []
        self.ok_button_rect = None
        self.inventory = []

        # Emplacements d'équipement pour Arme, Armure, et Bijou
        self.equipment_slots = {
            "Arme": None,
            "Armure": None,
            "Bijou": None
        }

        # Initialiser l'interface d'inventaire
        self.inventory_interface = Inventory(screen, self)

        self.load_character_data()

    def load_character_data(self):
        if os.path.exists("character_data.json"):
            with open("character_data.json", "r") as file:
                data = json.load(file)
                self.selected_character = data.get("character", None)
                self.inventory = data.get("inventory", [])
                self.equipment_slots = data.get("equipment_slots", self.equipment_slots)
        else:
            self.selected_character = {
                "type": None,
                "name": "Inconnu",
                "health": 100,
                "max_health": 100,
                "exp": 0,
                "max_exp": 100,
                "level": 1,
                "attack": 10,
                "defense": 5
            }
            self.inventory = []

    def save_character_data(self):
        with open("character_data.json", "w") as file:
            json.dump({
                "character": self.selected_character,
                "inventory": self.inventory,
                "equipment_slots": self.equipment_slots
            }, file)

    def add_loot_to_inventory(self, loot):
        self.inventory.append(loot)
        self.save_character_data()
        self.inventory_interface.update_inventory_display()
