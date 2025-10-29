import random
from interfaces import IDrawable, IMovable

class Obstacle(IDrawable, IMovable):
    def __init__(self, canvas, x, y, image, damage=10):
        self.canvas = canvas
        self.id = canvas.create_image(x, y, image=image)
        self.x = x
        self.y = y
        self.damage = damage

    def move(self, speed=7):
        self.canvas.move(self.id, speed, 0)

    def coords(self):
        return self.canvas.coords(self.id)

    def affect_player(self, player):
        pass

    def delete(self):
        self.canvas.delete(self.id)

# --- Sous-classes ---
class Cactus(Obstacle):
    def affect_player(self, player):
        if not player.invincible:
            player.health -= self.damage

class Rock(Obstacle):
    def affect_player(self, player):
        if not player.invincible:
            player.health -= self.damage

class Flying(Obstacle):
    def affect_player(self, player):
        if not player.invincible:
            player.health -= self.damage

class Special(Obstacle):
    def affect_player(self, player):
        if not player.invincible:
            player.health -= self.damage

    def animate(self):
        dx = random.randint(-2, 2)
        self.canvas.move(self.id, dx, 0)
        if self.coords()[0] < 1000:
            self.canvas.after(50, self.animate)
