import random

class Obstacle:
    def __init__(self, canvas, x, y, image, damage=10):
        self.canvas = canvas
        self.id = canvas.create_image(x, y, image=image)
        self.x = x
        self.y = y
        self.damage = damage

    def move(self, speed=7):
        """Déplace l’obstacle horizontalement."""
        self.canvas.move(self.id, speed, 0)

    def coords(self):
        """Retourne les coordonnées actuelles de l’obstacle."""
        return self.canvas.coords(self.id)

    def affect_player(self, player):
        """Méthode polymorphe : effet sur le joueur (à redéfinir dans les sous-classes)."""
        pass

    def delete(self):
        """Supprime l’obstacle du canvas."""
        self.canvas.delete(self.id)


class Cactus(Obstacle):
    def __init__(self, canvas, x, y, image):
        super().__init__(canvas, x, y, image, damage=10)

    def affect_player(self, player):
        """Inflige des dégâts au joueur s’il n’est pas invincible."""
        if not player.invincible:
            player.health -= self.damage


class Rock(Obstacle):
    def __init__(self, canvas, x, y, image):
        super().__init__(canvas, x, y, image, damage=5)

    def affect_player(self, player):
        if not player.invincible:
            player.health -= self.damage


class Flying(Obstacle):
    def __init__(self, canvas, x, y, image):
        super().__init__(canvas, x, y, image, damage=5)

    def affect_player(self, player):
        if not player.invincible:
            player.health -= self.damage


class Special(Obstacle):
    def __init__(self, canvas, x, y, image):
        super().__init__(canvas, x, y, image, damage=50)

    def affect_player(self, player):
        if not player.invincible:
            player.health -= self.damage

    def animate(self):
        """Animation spéciale : bouge légèrement de gauche à droite de façon aléatoire."""
        dx = random.randint(-2, 2)
        self.canvas.move(self.id, dx, 0)
        if self.coords()[0] < 1000:  # Continue l’animation tant que l’obstacle est visible
            self.canvas.after(50, self.animate)
