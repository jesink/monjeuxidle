
class Enemy:
    def __init__(self, name, level, health):
        self.name = name
        self.level = level
        self.health = health
        self.max_health = health  # Définir max_health comme la santé initiale

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

# Fonction pour créer un groupe d'ennemis
def create_enemy_group(base_name, start_level, count):
    return [Enemy(f"{base_name} Niveau {i}", i, 50 + 10 * i) for i in range(start_level, start_level + count)]

# Exemple de groupes d'ennemis
enemy_groups = {
    "Ennemi Débutant": create_enemy_group("Ennemi Débutant", 1, 10),
    "Ennemi Intermédiaire": create_enemy_group("Ennemi Intermédiaire", 11, 10),
    "Ennemi Avancé": create_enemy_group("Ennemi Avancé", 21, 10),
    "Ennemi Expert": create_enemy_group("Ennemi Expert", 31, 10),
    "Ennemi Maître": create_enemy_group("Ennemi Maître", 41, 10),
    "Ennemi Légendaire": create_enemy_group("Ennemi Légendaire", 51, 10),
    "Ennemi Ultime": create_enemy_group("Ennemi Ultime", 61, 10),
    "Ennemi Cauchemar": create_enemy_group("Ennemi Cauchemar", 71, 10),
    "Ennemi Apocalyptique": create_enemy_group("Ennemi Apocalyptique", 81, 10),
    "Ennemi Divin": create_enemy_group("Ennemi Divin", 91, 10)
}
