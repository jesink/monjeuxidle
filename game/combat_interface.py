import pygame
import sys
import os
import random
import json
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from game.character import Character

class CombatInterface:
    def __init__(self, screen, character, enemy, enemy_group_interface):
        self.screen = screen
        self.character = character
        self.selected_enemy = enemy
        self.enemy_group_interface = enemy_group_interface
        self.background_image = pygame.image.load(os.path.join("assets", "background.png")).convert()
        self.character_frame = pygame.Rect(50, 100, 300, 400)
        self.enemy_frame = pygame.Rect(screen.get_width() - 350, 100, 300, 400)
        self.chat_frame = pygame.Rect(50, screen.get_height() - 200, screen.get_width() - 100, 150)
        self.return_button_rect = pygame.Rect(20, 20, 100, 50)
        self.combat_log = []
        self.combat_running = True
        self.combat_effects = []
        if 'max_health' not in self.selected_enemy['stats']:
            self.selected_enemy['stats']['max_health'] = self.selected_enemy['stats']['HP']

    def restore_character_health(self):
        """Restaure la santé maximale du personnage après le combat."""
        if self.character.selected_character:
            self.character.selected_character['health'] = self.character.selected_character['max_health']

    def restore_enemy_health(self):
        """Restaure la santé maximale de l'ennemi après le combat."""
        if self.selected_enemy:
            self.selected_enemy['stats']['HP'] = self.selected_enemy['stats']['max_health']

    def add_combat_event(self, event_text):
        """Ajoute un événement au journal de combat."""
        self.combat_log.append(event_text)
        if len(self.combat_log) > 5:  # Limite à 5 messages pour éviter de remplir le cadre
            self.combat_log.pop(0)

    def add_combat_effect(self, x, y, color):
        """Ajoute un effet de combat (par exemple, une explosion ou un flash) à la position donnée."""
        self.combat_effects.append({"x": x, "y": y, "color": color, "lifetime": 30})

    def update_combat_effects(self):
        """Met à jour les effets de combat en diminuant leur durée de vie."""
        for effect in self.combat_effects:
            effect["lifetime"] -= 1
        self.combat_effects = [effect for effect in self.combat_effects if effect["lifetime"] > 0]

    def draw_combat_effects(self):
        """Dessine les effets de combat à l'écran."""
        for effect in self.combat_effects:
            alpha = max(0, min(255, effect["lifetime"] * 8))  # Dégradé de transparence
            surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*effect["color"], alpha), (25, 25), 25)
            self.screen.blit(surface, (effect["x"] - 25, effect["y"] - 25))

    def gain_experience(self, exp_gained):
        """Gagne de l'expérience et monte de niveau si le seuil est atteint."""
        self.character.gain_experience(exp_gained)

    def generate_loot(self):
        """Génère un objet de loot avec des statistiques basées sur le type de personnage sélectionné."""
        loot_type = self.character.selected_character["type"]
        loot_category = random.choice(["Arme", "Armure", "Bijou"])
        loot_stats = self.get_loot_stats(loot_category)
        loot_item = {
            "name": f"{loot_category} de {loot_type}",
            "type": loot_category,
            "stats": loot_stats
        }
        # Ajouter le loot à l'inventaire du personnage
        self.character.add_loot_to_inventory(loot_item)
        self.character.save_character_data()

        # Mettre à jour les emplacements de l'inventaire
        if hasattr(self.character, "inventory_interface"):
            self.character.inventory_interface.update_inventory_slots()

        self.add_combat_event(f"Loot obtenu: {loot_item['name']}")
        self.character.save_character_data()

    def get_loot_stats(self, category):
        """Génère des statistiques pour le loot basé sur la catégorie."""
        if category == "Arme":
            return {"attack": random.randint(5, 15)}
        elif category == "Armure":
            return {"defense": random.randint(3, 10)}
        elif category == "Bijou":
            return {"health": random.randint(10, 30)}
        return {}

    def process_combat_round(self):
        """Effectue une seule manche de combat."""
        damage_to_enemy = random.randint(5, 15)
        damage_to_character = random.randint(3, 10)
        exp_gained = 20

        self.selected_enemy['stats']['HP'] = max(0, self.selected_enemy['stats']['HP'] - damage_to_enemy)
        self.character.selected_character['health'] = max(0, self.character.selected_character['health'] - damage_to_character)

        self.add_combat_event(f"Dégâts infligés: {damage_to_enemy}")
        self.add_combat_event(f"Dégâts reçus: {damage_to_character}")

        self.add_combat_effect(self.character_frame.x + 150, self.character_frame.y + 200, (255, 0, 0))
        self.add_combat_effect(self.enemy_frame.x + 150, self.enemy_frame.y + 200, (0, 0, 255))

        if self.selected_enemy['stats']['HP'] <= 0:
            self.combat_running = False
            self.add_combat_event("L'ennemi est vaincu !")
            self.add_combat_event(f"EXP gagnée: {exp_gained}")
            self.gain_experience(exp_gained)
            self.generate_loot()
            self.restore_character_health()
            self.restore_enemy_health()  # Restaurer la santé de l'ennemi
        elif self.character.selected_character['health'] <= 0:
            self.combat_running = False
            self.add_combat_event("Vous avez été vaincu !")
            self.restore_character_health()
            self.restore_enemy_health()  # Restaurer la santé de l'ennemi

    def display(self):
        running = True

        while running:
            self.screen.blit(self.background_image, (0, 0))

            pygame.draw.rect(self.screen, (100, 100, 100), self.character_frame, border_radius=15)
            pygame.draw.rect(self.screen, (100, 100, 100), self.enemy_frame, border_radius=15)
            pygame.draw.rect(self.screen, (50, 50, 50), self.chat_frame, border_radius=10)

            font = pygame.font.SysFont("arial", 20)
            if self.character.selected_character:
                name = self.character.selected_character.get('name', 'Inconnu')
                health = self.character.selected_character.get('health', 0)
                level = self.character.selected_character.get('level', 1)
                attack = self.character.selected_character.get('attack', 10)
                defense = self.character.selected_character.get('defense', 5)
                exp = self.character.selected_character.get('exp', 0)
                max_exp = self.character.selected_character.get('max_exp', 100)
                character_text = font.render(f"Personnage: {name}", True, WHITE)
                self.screen.blit(character_text, (self.character_frame.x + 20, self.character_frame.y + 20))
                health_text = font.render(f"HP: {health}", True, WHITE)
                self.screen.blit(health_text, (self.character_frame.x + 20, self.character_frame.y + 50))
                level_text = font.render(f"Niveau: {level}", True, WHITE)
                self.screen.blit(level_text, (self.character_frame.x + 20, self.character_frame.y + 80))
                attack_text = font.render(f"Attaque: {attack}", True, WHITE)
                self.screen.blit(attack_text, (self.character_frame.x + 20, self.character_frame.y + 110))
                defense_text = font.render(f"Défense: {defense}", True, WHITE)
                self.screen.blit(defense_text, (self.character_frame.x + 20, self.character_frame.y + 140))
                exp_text = font.render(f"EXP: {exp}/{max_exp}", True, WHITE)
                self.screen.blit(exp_text, (self.character_frame.x + 20, self.character_frame.y + 170))
            else:
                character_text = font.render("Personnage: Aucun", True, WHITE)
                self.screen.blit(character_text, (self.character_frame.x + 20, self.character_frame.y + 20))

            enemy_text = font.render(f"Ennemi: Niveau {self.selected_enemy['level']}", True, WHITE)
            self.screen.blit(enemy_text, (self.enemy_frame.x + 20, self.enemy_frame.y + 20))
            enemy_hp_text = font.render(f"HP: {self.selected_enemy['stats']['HP']}", True, WHITE)
            self.screen.blit(enemy_hp_text, (self.enemy_frame.x + 20, self.enemy_frame.y + 50))

            y_offset = 20
            for event in self.combat_log:
                chat_text = font.render(event, True, WHITE)
                self.screen.blit(chat_text, (self.chat_frame.x + 10, self.chat_frame.y + y_offset))
                y_offset += 20

            self.update_combat_effects()
            self.draw_combat_effects()

            pygame.draw.rect(self.screen, (100, 100, 100), self.return_button_rect, border_radius=10)
            return_text = font.render("Retour", True, WHITE)
            self.screen.blit(return_text, (30, 30))

            if self.combat_running:
                self.process_combat_round()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if self.return_button_rect.collidepoint(mouse_x, mouse_y):
                        self.enemy_group_interface.display()
                        running = False

            pygame.time.delay(1000)
