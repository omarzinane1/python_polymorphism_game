import random

class Obstacle:
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
        pass  # Polymorphisme

    def delete(self):
        self.canvas.delete(self.id)

class Cactus(Obstacle):
    def __init__(self, canvas, x, y, image):
        super().__init__(canvas, x, y, image, damage=10)

    def affect_player(self, player):
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
        # Bouge légèrement de gauche à droite
        dx = random.randint(-2,2)
        self.canvas.move(self.id, dx, 0)
        if self.coords()[0] < 1000:
            self.canvas.after(50, self.animate)
